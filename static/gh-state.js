/*
 * Gaijin Hunter — client-side state module.
 *
 * Single source of truth in localStorage. Everything lives under one key so
 * export/import is one JSON blob. On first load we migrate from older shapes
 * (legacy per-list keys, and the v1 profile/tracker schema).
 *
 * window.GH provides:
 *   GH.getState()                       -> entire state object (cloned)
 *   GH.profile.get() / set(p) / isConfigured()
 *   GH.saved.list() / has(id) / toggle(id) / add(id) / remove(id)
 *   GH.hidden.list() / has(id) / add(id) / remove(id)
 *   GH.tracker.list() / get(id) / set(id, partial) / setStatus(id, s) / remove(id)
 *   GH.tracker.statuses / KANBAN / columnFor(status)
 *   GH.tracker.statusCounts() / overdueFollowUps() / appliedIds() / ids()
 *   GH.savedSearches.list() / add(name, qs) / remove(name)
 *   GH.export()                         -> JSON string of full state
 *   GH.import(json)                     -> bool success
 *   GH.computeMatch(job, profile?)      -> { score, label, band, why[], gaps[], breakdown[] }
 *   GH.matchLabel(score) / GH.matchBand(score)
 *   GH.applicationStrategy(job, match, profile?) -> string
 *   GH.refreshUi()                      -> repaint counts/badges/banners
 *
 * Application statuses (canonical, v2):
 *   "Saved", "Preparing", "Applied", "Recruiter screen",
 *   "First interview", "Final interview", "Offer",
 *   "Rejected", "Withdrawn", "Archived"
 */
(function () {
  "use strict";

  var STORAGE_KEY = "gaijin-hunter-state-v1";   // key unchanged (forward-compatible)
  var STATE_VERSION = 2;
  var LEGACY = {
    saved:   "japan-jobs-saved",
    applied: "japan-jobs-applied",
    hidden:  "japan-jobs-hidden",
  };

  // ---- application statuses --------------------------------------------------
  var STATUSES = [
    "Saved", "Preparing", "Applied", "Recruiter screen",
    "First interview", "Final interview", "Offer",
    "Rejected", "Withdrawn", "Archived",
  ];

  // Kanban grouping: column key -> statuses it contains.
  var KANBAN = [
    { key: "saved",        label: "Saved / Preparing", statuses: ["Saved", "Preparing"] },
    { key: "applied",      label: "Applied",            statuses: ["Applied"] },
    { key: "interviewing", label: "Interviewing",       statuses: ["Recruiter screen", "First interview", "Final interview"] },
    { key: "offer",        label: "Offer",              statuses: ["Offer"] },
    { key: "closed",       label: "Closed",             statuses: ["Rejected", "Withdrawn", "Archived"] },
  ];
  function columnFor(status) {
    for (var i = 0; i < KANBAN.length; i++) {
      if (KANBAN[i].statuses.indexOf(status) !== -1) return KANBAN[i].key;
    }
    return "saved";
  }
  // Statuses that count as "has applied or beyond" (for the /applied list + badge).
  var APPLIED_PLUS = ["Applied", "Recruiter screen", "First interview", "Final interview", "Offer"];

  // Map v1 statuses -> v2.
  var STATUS_MIGRATE = {
    "Phone Screen": "Recruiter screen",
    "Interview": "First interview",
  };

  // ---------- defaults --------------------------------------------------------
  function defaultProfile() {
    return {
      // Personal (optional — feeds resume builders)
      name: "",
      email: "",

      // Section 1 — Job target
      targetKeywords: "",          // free text, comma-ish
      targetRoleFamilies: [],      // multi-select
      preferredIndustries: "",     // free text
      minSalary: "",               // annual JPY
      employmentTerms: [],         // Full-time | Contract | Part-time | Internship
      preferredLocations: [],      // multi: Tokyo, Osaka, ... Remote Japan, Anywhere in Japan

      // Section 2 — Language & work eligibility
      japaneseLevel: "",           // None | Basic | Conversational | Business / Professional | Native / Fluent
      englishLevel: "",            // Conversational | Business / Professional | Native / Fluent
      visaNeed: "",                // "yes" | "no" | "unsure"
      applyingFrom: "",            // "outside" | "inside" | "flexible"
      openToRelocation: "",        // "yes" | "no" | "strong-offer"
      currentVisa: "",             // free text

      // Section 3 — Work preferences
      remotePreference: "",        // "remote-only" | "hybrid" | "onsite-ok" | "any"
      companyPreference: "",       // "gaishikei" | "jp-startup" | "large-jp" | "intl-startup" | "any"
      excludeTeaching: false,
      excludeJapaneseOnly: false,
      salaryListedOnly: false,
      highFitOnly: false,

      // Section 4 — Skills
      skills: "",                  // comma-separated
      yearsExperience: "",
      educationLevel: "",
      certifications: "",
      portfolioUrls: "",

      // Legacy fields retained for backward-compat reads (not surfaced in new form)
      visaStatus: "",              // "need" | "have" | "citizen"
      includeTeaching: true,
      openToAbroad: false,
      currentLocation: "",
    };
  }

  function defaultTrackerEntry() {
    return {
      status: "Saved",
      savedAt: "",
      appliedAt: "",
      followUpAt: "",
      recruiterName: "",
      recruiterEmail: "",
      salaryDiscussed: "",
      notes: "",
      docs: {
        englishResume: false,
        rirekisho: false,     // 履歴書
        shokumu: false,       // 職務経歴書
        coverLetter: false,
        portfolio: false,
      },
      sourceUrl: "",
      updatedAt: "",
    };
  }

  function defaultState() {
    return {
      version: STATE_VERSION,
      profile: defaultProfile(),
      saved: [],
      hidden: [],
      tracker: {},                 // jobId -> entry
      savedSearches: [],
    };
  }

  // ---------- normalisation / migration --------------------------------------
  function normalizeEntry(raw) {
    var base = defaultTrackerEntry();
    raw = raw || {};
    var e = Object.assign(base, raw);
    e.docs = Object.assign(base.docs, raw.docs || {});
    // migrate v1 status names
    if (STATUS_MIGRATE[e.status]) e.status = STATUS_MIGRATE[e.status];
    if (STATUSES.indexOf(e.status) === -1) e.status = "Saved";
    return e;
  }

  function normalizeProfile(raw) {
    var d = defaultProfile();
    raw = raw || {};
    var p = Object.assign(d, raw);
    // Backfill new canonical fields from legacy ones if the new ones are empty.
    if (!raw.visaNeed && raw.visaStatus) {
      p.visaNeed = raw.visaStatus === "need" ? "yes"
                 : (raw.visaStatus === "have" || raw.visaStatus === "citizen") ? "no" : "";
    }
    if (raw.excludeTeaching === undefined && raw.includeTeaching === false) {
      p.excludeTeaching = true;
    }
    if (!raw.applyingFrom && raw.openToAbroad) p.applyingFrom = "outside";
    // Normalise legacy remote value.
    if (p.remotePreference === "hybrid-ok") p.remotePreference = "hybrid";
    return p;
  }

  function load() {
    var raw;
    try { raw = localStorage.getItem(STORAGE_KEY); } catch (e) { return defaultState(); }
    if (!raw) return migrateLegacy();
    try {
      var s = JSON.parse(raw);
      var d = defaultState();
      Object.keys(d).forEach(function (k) { if (s[k] === undefined) s[k] = d[k]; });
      s.profile = normalizeProfile(s.profile);
      var t = {};
      Object.keys(s.tracker || {}).forEach(function (id) {
        t[String(id)] = normalizeEntry(s.tracker[id]);
      });
      s.tracker = t;
      s.version = STATE_VERSION;
      return s;
    } catch (e) {
      return defaultState();
    }
  }

  function persist(s) {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(s)); } catch (e) {}
  }

  function migrateLegacy() {
    var s = defaultState();
    function readArr(k) {
      try { return JSON.parse(localStorage.getItem(k) || "[]"); }
      catch (e) { return []; }
    }
    s.saved  = readArr(LEGACY.saved).slice();
    s.hidden = readArr(LEGACY.hidden).slice();
    var now = new Date().toISOString();
    readArr(LEGACY.applied).forEach(function (id) {
      s.tracker[String(id)] = normalizeEntry({
        status: "Applied", appliedAt: now, savedAt: now,
        notes: "(migrated from legacy applied list)", updatedAt: now,
      });
    });
    persist(s);
    return s;
  }

  // ---------- in-memory state with write-through -----------------------------
  var _state = load();

  function commit() { persist(_state); refreshUi(); }
  function getState() { return JSON.parse(JSON.stringify(_state)); }

  // ---------- profile ---------------------------------------------------------
  var profile = {
    get: function () { return JSON.parse(JSON.stringify(_state.profile)); },
    set: function (p) {
      _state.profile = normalizeProfile(Object.assign({}, _state.profile, p || {}));
      commit();
    },
    isConfigured: function () {
      var p = _state.profile;
      return !!(p.japaneseLevel
        || (p.targetRoleFamilies && p.targetRoleFamilies.length)
        || p.minSalary
        || (p.preferredLocations && p.preferredLocations.length)
        || p.targetKeywords || p.skills || p.visaNeed || p.remotePreference);
    },
  };

  // ---------- saved -----------------------------------------------------------
  var saved = {
    list: function () { return _state.saved.slice(); },
    has:  function (id) { return _state.saved.indexOf(parseInt(id, 10)) !== -1; },
    add:  function (id) {
      id = parseInt(id, 10);
      var changed = false;
      if (_state.saved.indexOf(id) === -1) { _state.saved.push(id); changed = true; }
      if (!_state.tracker[String(id)]) {
        var e = normalizeEntry({ status: "Saved" });
        e.savedAt = e.updatedAt = new Date().toISOString();
        _state.tracker[String(id)] = e;
        changed = true;
      }
      if (changed) commit();
    },
    remove: function (id) {
      id = parseInt(id, 10);
      var i = _state.saved.indexOf(id);
      var changed = false;
      if (i !== -1) { _state.saved.splice(i, 1); changed = true; }
      var t = _state.tracker[String(id)];
      if (t && t.status === "Saved") { delete _state.tracker[String(id)]; changed = true; }
      if (changed) commit();
    },
    toggle: function (id) {
      id = parseInt(id, 10);
      if (_state.saved.indexOf(id) === -1) { saved.add(id); return true; }
      saved.remove(id); return false;
    },
  };

  // ---------- hidden ----------------------------------------------------------
  var hidden = {
    list: function () { return _state.hidden.slice(); },
    has:  function (id) { return _state.hidden.indexOf(parseInt(id, 10)) !== -1; },
    add:  function (id) {
      id = parseInt(id, 10);
      if (_state.hidden.indexOf(id) === -1) { _state.hidden.push(id); commit(); }
    },
    remove: function (id) {
      id = parseInt(id, 10);
      var i = _state.hidden.indexOf(id);
      if (i !== -1) { _state.hidden.splice(i, 1); commit(); }
    },
  };

  // ---------- tracker ---------------------------------------------------------
  var tracker = {
    statuses: STATUSES.slice(),
    KANBAN: KANBAN.map(function (c) { return { key: c.key, label: c.label, statuses: c.statuses.slice() }; }),
    columnFor: columnFor,
    list: function () {
      return Object.keys(_state.tracker).map(function (id) {
        return Object.assign({ jobId: parseInt(id, 10) }, _state.tracker[id]);
      });
    },
    ids: function () { return Object.keys(_state.tracker).map(function (i) { return parseInt(i, 10); }); },
    appliedIds: function () {
      return Object.keys(_state.tracker)
        .filter(function (id) { return APPLIED_PLUS.indexOf(_state.tracker[id].status) !== -1; })
        .map(function (id) { return parseInt(id, 10); });
    },
    get: function (id) {
      var e = _state.tracker[String(parseInt(id, 10))];
      return e ? JSON.parse(JSON.stringify(e)) : null;
    },
    set: function (id, partial) {
      id = String(parseInt(id, 10));
      var current = _state.tracker[id] || defaultTrackerEntry();
      var next = Object.assign({}, current, partial || {});
      if (partial && partial.docs) next.docs = Object.assign({}, current.docs, partial.docs);
      if (!next.savedAt) next.savedAt = new Date().toISOString();
      var beyond = next.status && APPLIED_PLUS.indexOf(next.status) !== -1;
      if (beyond && !next.appliedAt) next.appliedAt = new Date().toISOString();
      next.updatedAt = new Date().toISOString();
      _state.tracker[id] = normalizeEntry(next);
      commit();
      return _state.tracker[id];
    },
    setStatus: function (id, status) { return tracker.set(id, { status: status }); },
    remove: function (id) {
      id = String(parseInt(id, 10));
      if (_state.tracker[id]) {
        delete _state.tracker[id];
        // keep saved list consistent if the job was only saved
        var si = _state.saved.indexOf(parseInt(id, 10));
        if (si !== -1) _state.saved.splice(si, 1);
        commit();
      }
    },
    statusCounts: function () {
      var counts = {}; STATUSES.forEach(function (s) { counts[s] = 0; });
      Object.keys(_state.tracker).forEach(function (id) {
        var s = _state.tracker[id].status || "Saved";
        counts[s] = (counts[s] || 0) + 1;
      });
      return counts;
    },
    overdueFollowUps: function () {
      var today = new Date(); today.setHours(23, 59, 59, 999);
      var out = [];
      Object.keys(_state.tracker).forEach(function (id) {
        var e = _state.tracker[id];
        if (!e.followUpAt) return;
        var d = new Date(e.followUpAt);
        if (!isNaN(d) && d <= today
            && e.status !== "Rejected" && e.status !== "Withdrawn"
            && e.status !== "Archived" && e.status !== "Offer") {
          out.push(Object.assign({ jobId: parseInt(id, 10) }, e));
        }
      });
      return out;
    },
  };

  // ---------- saved searches --------------------------------------------------
  var savedSearches = {
    list: function () { return _state.savedSearches.slice(); },
    add: function (name, querystring) {
      if (!name) return;
      _state.savedSearches = _state.savedSearches.filter(function (s) { return s.name !== name; });
      _state.savedSearches.unshift({
        name: name,
        querystring: String(querystring || "").replace(/^\?/, ""),
        createdAt: new Date().toISOString(),
      });
      commit();
    },
    remove: function (name) {
      _state.savedSearches = _state.savedSearches.filter(function (s) { return s.name !== name; });
      commit();
    },
  };

  // ---------- export / import -------------------------------------------------
  function exportJson() {
    return JSON.stringify({
      _exportedAt: new Date().toISOString(),
      _app: "gaijin-hunter",
      _version: STATE_VERSION,
      state: _state,
    }, null, 2);
  }
  function importJson(json) {
    try {
      var parsed = typeof json === "string" ? JSON.parse(json) : json;
      var s = parsed && parsed.state ? parsed.state : parsed;
      if (!s || typeof s !== "object") return false;
      var d = defaultState();
      Object.keys(d).forEach(function (k) { if (s[k] === undefined) s[k] = d[k]; });
      s.profile = normalizeProfile(s.profile);
      var t = {};
      Object.keys(s.tracker || {}).forEach(function (id) { t[String(id)] = normalizeEntry(s.tracker[id]); });
      s.tracker = t;
      s.version = STATE_VERSION;
      _state = s;
      commit();
      return true;
    } catch (e) { return false; }
  }

  // ===========================================================================
  // MATCH SCORING — transparent, weighted, profile-aware (0..100).
  // Separate from Foreigner Fit (which is the objective job-side score).
  // Weights: role 25, keywords/skills 20, JP 15, visa/abroad 15, salary 10,
  // location/remote 10, employment terms 5.
  // Unknown data -> partial credit (never a hard zero), per the spec.
  // ===========================================================================
  var JP_RANK = {
    "None": 0, "Not Required": 0,
    "Basic": 1, "Basic / Beginner": 1,
    "Conversational": 2,
    "Business": 3, "Business / Professional": 3,
    "Native": 4, "Native / Fluent": 4, "Fluent": 4,
  };

  function num(v) { var n = Number(v); return isNaN(n) ? 0 : n; }
  function toList(csv) {
    return String(csv || "").split(/[,\n;]+/).map(function (s) { return s.trim().toLowerCase(); }).filter(Boolean);
  }
  function jobText(job) {
    return [job.title, job.role_family, job.text, job.description, job.requirements, job.tags]
      .filter(Boolean).join(" ").toLowerCase();
  }

  // --- individual factors: each returns { earned, max, why?, gap? } ----------
  function fRole(job, p) {
    var max = 25;
    var fams = p.targetRoleFamilies || [];
    if (!fams.length) return { earned: max * 0.6, max: max };           // no info
    if (!job.role_family) return { earned: max * 0.6, max: max };       // unknown job side
    if (fams.indexOf(job.role_family) !== -1) {
      return { earned: max, max: max, why: "Role family matches " + job.role_family };
    }
    // soft keyword overlap with chosen families
    return { earned: max * 0.3, max: max, gap: "Different role family (" + job.role_family + ")" };
  }

  function fKeywords(job, p) {
    var max = 20;
    var terms = toList(p.targetKeywords).concat(toList(p.skills));
    // unique
    var seen = {}, uniq = [];
    terms.forEach(function (t) { if (t.length >= 2 && !seen[t]) { seen[t] = 1; uniq.push(t); } });
    if (!uniq.length) return { earned: max * 0.6, max: max };           // no info
    var text = jobText(job);
    if (!text) return { earned: max * 0.6, max: max };
    var hits = uniq.filter(function (t) { return text.indexOf(t) !== -1; });
    if (hits.length === 0) return { earned: max * 0.25, max: max, gap: "None of your keywords/skills appear in this posting" };
    var ratio = Math.min(1, hits.length / Math.min(4, uniq.length));
    var earned = max * (0.5 + 0.5 * ratio);                            // 50%..100%
    var shown = hits.slice(0, 4).join(", ");
    return { earned: earned, max: max, why: "Matches your keywords/skills: " + shown };
  }

  function fJapanese(job, p) {
    var max = 15;
    var ur = JP_RANK[p.japaneseLevel];
    var jr = JP_RANK[job.japanese_level];
    if (ur === undefined || jr === undefined) return { earned: max * 0.6, max: max };
    if (ur >= jr) return { earned: max, max: max, why: "Japanese level fits (needs " + job.japanese_level + ")" };
    var shortfall = jr - ur;
    var earned = shortfall === 1 ? max * 0.45 : max * 0.2;
    return { earned: earned, max: max, gap: "Japanese requirement (" + job.japanese_level + ") above your level" };
  }

  function fVisaAbroad(job, p) {
    var max = 15;                  // visa portion 10, apply-from-abroad portion 5
    var earned = 0, why = null, gap = null;
    // --- visa (10) ---
    var needs = p.visaNeed === "yes" || p.visaStatus === "need";
    var doesnt = p.visaNeed === "no" || p.visaStatus === "have" || p.visaStatus === "citizen";
    if (doesnt) {
      earned += 10;              // not a constraint
    } else if (needs) {
      if (job.visa_sponsorship_mentioned === 1) { earned += 10; why = "Visa sponsorship mentioned"; }
      else if (job.visa_sponsorship_mentioned === 0) { earned += 2; gap = "Visa sponsorship not confirmed"; }
      else { earned += 6; gap = "Visa sponsorship unclear"; }
    } else {
      earned += 6;               // unsure / unset
    }
    // --- apply from abroad (5) ---
    if (p.applyingFrom === "outside") {
      if (job.overseas_application_ok === 1) { earned += 5; why = (why ? why + "; " : "") + "Accepts applications from abroad"; }
      else if (job.overseas_application_ok === 0) { earned += 1; gap = (gap ? gap + "; " : "") + "May require you to already be in Japan"; }
      else { earned += 3; }
    } else {
      earned += 5;               // inside / flexible -> not a blocker
    }
    var out = { earned: earned, max: max };
    if (why) out.why = why;
    if (gap) out.gap = gap;
    return out;
  }

  function fSalary(job, p) {
    var max = 10;
    var floor = num(p.minSalary);
    if (!floor) return { earned: max * 0.6, max: max };                // no target set
    var jobMax = num(job.salary_max_annual_jpy) || num(job.salary_min_annual_jpy);
    if (!jobMax) return { earned: max * 0.6, max: max, gap: "Salary not listed" };
    if (jobMax >= floor) return { earned: max, max: max, why: "Salary meets your target (" + yen(jobMax) + ")" };
    if (jobMax >= floor * 0.85) return { earned: max * 0.6, max: max, gap: "Salary slightly below your target" };
    return { earned: max * 0.2, max: max, gap: "Salary below your target (" + yen(jobMax) + ")" };
  }

  function fLocationRemote(job, p) {
    var max = 10;                  // location 5, remote 5
    var earned = 0, why = null, gap = null;
    // --- location (5) ---
    var locs = (p.preferredLocations || []).map(function (s) { return String(s).toLowerCase(); });
    var anywhere = locs.indexOf("anywhere in japan") !== -1;
    if (!locs.length || anywhere) {
      earned += 5;
    } else {
      var jl = (job.location || job.prefecture || "").toLowerCase();
      var remoteWanted = locs.indexOf("remote japan") !== -1;
      if (!jl) { earned += 3; }
      else if (locs.some(function (l) { return l !== "remote japan" && l && jl.indexOf(l) !== -1; })) {
        earned += 5; why = "Location matches your preference";
      } else if (remoteWanted && job.remote_work_ok === 1) {
        earned += 5; why = "Remote role matches your preference";
      } else {
        earned += 1.5; gap = "Location not in your preferred list";
      }
    }
    // --- remote (5) ---
    var rp = p.remotePreference;
    if (!rp || rp === "any") {
      earned += 5;
    } else if (rp === "remote-only") {
      if (job.remote_work_ok === 1) { earned += 5; why = (why ? why + "; " : "") + "Remote matches your preference"; }
      else if (job.remote_work_ok === 0) { earned += 0.5; gap = (gap ? gap + "; " : "") + "On-site only — you wanted remote"; }
      else { earned += 2.5; }
    } else if (rp === "hybrid") {
      if (job.remote_work_ok === 1) { earned += 5; why = (why ? why + "; " : "") + "Offers remote/hybrid"; }
      else { earned += 3; }
    } else if (rp === "onsite-ok") {
      earned += 5;
    }
    var out = { earned: earned, max: max };
    if (why) out.why = why;
    if (gap) out.gap = gap;
    return out;
  }

  function fEmployment(job, p) {
    var max = 5;
    var terms = p.employmentTerms || [];
    if (!terms.length) return { earned: max * 0.6, max: max };
    var jt = String(job.employment_terms || job.work_type || "").toLowerCase();
    if (!jt) return { earned: max * 0.6, max: max };
    var match = terms.some(function (t) {
      t = t.toLowerCase();
      if (t === "full-time") return /full[\s-]?time|正社員|permanent/.test(jt);
      if (t === "contract") return /contract|契約|haken|dispatch/.test(jt);
      if (t === "part-time") return /part[\s-]?time|アルバイト|パート/.test(jt);
      if (t === "internship") return /intern/.test(jt);
      return jt.indexOf(t) !== -1;
    });
    if (match) return { earned: max, max: max, why: "Employment type matches" };
    return { earned: max * 0.3, max: max, gap: "Employment type differs from your preference" };
  }

  function yen(n) {
    n = num(n);
    if (n >= 1e6) return "¥" + (n / 1e6).toFixed(1).replace(/\.0$/, "") + "M";
    if (n >= 1e3) return "¥" + Math.round(n / 1e3) + "K";
    return "¥" + n;
  }

  var MATCH_BANDS = [
    { min: 90, band: "excellent", label: "Excellent match" },
    { min: 75, band: "strong",    label: "Strong match" },
    { min: 60, band: "possible",  label: "Possible match" },
    { min: 40, band: "weak",      label: "Weak match" },
    { min: 0,  band: "poor",      label: "Poor match" },
  ];
  function matchBand(score) {
    for (var i = 0; i < MATCH_BANDS.length; i++) if (score >= MATCH_BANDS[i].min) return MATCH_BANDS[i].band;
    return "poor";
  }
  function matchLabel(score) {
    for (var i = 0; i < MATCH_BANDS.length; i++) if (score >= MATCH_BANDS[i].min) return MATCH_BANDS[i].label;
    return "Poor match";
  }

  function computeMatch(job, profileOverride) {
    var p = profileOverride || _state.profile;
    var factors = [
      { name: "Role family",      r: fRole(job, p) },
      { name: "Keywords & skills", r: fKeywords(job, p) },
      { name: "Japanese level",   r: fJapanese(job, p) },
      { name: "Visa & eligibility", r: fVisaAbroad(job, p) },
      { name: "Salary",           r: fSalary(job, p) },
      { name: "Location & remote", r: fLocationRemote(job, p) },
      { name: "Employment terms", r: fEmployment(job, p) },
    ];
    var earned = 0, total = 0, why = [], gaps = [], breakdown = [];
    factors.forEach(function (f) {
      earned += f.r.earned; total += f.r.max;
      breakdown.push({ name: f.name, earned: Math.round(f.r.earned * 10) / 10, max: f.r.max });
      if (f.r.why) why.push(f.r.why);
      if (f.r.gap) gaps.push(f.r.gap);
    });
    var score = total > 0 ? Math.round((earned / total) * 100) : 0;
    score = Math.max(0, Math.min(100, score));
    return {
      score: score,
      band: matchBand(score),
      label: matchLabel(score),
      why: why,
      gaps: gaps,
      breakdown: breakdown,
    };
  }

  // Plain-language application strategy for the detail page.
  function applicationStrategy(job, match, profileOverride) {
    var p = profileOverride || _state.profile;
    var s = match.score;
    var parts = [];
    if (s >= 75) {
      parts.push("This role looks like a realistic, strong fit for your profile — worth a focused, tailored application.");
    } else if (s >= 60) {
      parts.push("This role is a plausible fit. Apply if it interests you, but lead with the parts of your background that line up most closely.");
    } else if (s >= 40) {
      parts.push("This is a stretch given your current profile. Only apply if you can make a clear case for the gaps below.");
    } else {
      parts.push("This role is far from your stated preferences. Consider it only if something specific draws you to it.");
    }
    // Tailored tips
    var tips = [];
    if (p.skills) tips.push("emphasise your " + toList(p.skills).slice(0, 3).join(", ") + " experience");
    if (p.englishLevel && /business|native|fluent/i.test(p.englishLevel)) tips.push("highlight English working-environment experience");
    if (p.openToRelocation === "yes" || p.applyingFrom === "outside") tips.push("state your willingness to relocate clearly");
    if (tips.length) parts.push("Emphasise: " + tips.join("; ") + ".");
    // Documents
    var docs = ["an English resume"];
    if (job.japanese_level && JP_RANK[job.japanese_level] >= 2) docs.unshift("a 職務経歴書 (shokumu keirekisho)");
    parts.push("Prepare " + docs.join(" and ") + " before applying.");
    // Gaps reminder
    if (match.gaps.length) parts.push("Address these gaps proactively: " + match.gaps.slice(0, 2).join("; ") + ".");
    return parts.join(" ");
  }

  // ---------- UI refresh helpers ---------------------------------------------
  function refreshUi() {
    var nSaved   = _state.saved.length;
    var nApplied = tracker.appliedIds().length;
    var nTracked = tracker.ids().length;
    var nOverdue = tracker.overdueFollowUps().length;

    setText("hdr-saved-count",   nSaved   > 0 ? "(" + nSaved + ")"   : "");
    setText("saved-count",       nSaved   > 0 ? "(" + nSaved + ")"   : "");
    setText("hdr-applied-count", nApplied > 0 ? "(" + nApplied + ")" : "");
    setText("applied-count",     nApplied > 0 ? "(" + nApplied + ")" : "");
    setText("tracker-count",     nTracked > 0 ? "(" + nTracked + ")" : "");
    setText("hdr-tracker-count", nOverdue > 0 ? "(" + nOverdue + ")" : "");

    // Header pill
    var due = document.getElementById("hdr-followup-badge");
    if (due) {
      if (nOverdue > 0) {
        due.textContent = "🔔 " + nOverdue + " follow-up" + (nOverdue === 1 ? "" : "s") + " due";
        due.style.display = "";
      } else { due.style.display = "none"; }
    }

    // Page-level follow-up banner(s): any element with class .gh-followup-banner
    var banners = document.querySelectorAll(".gh-followup-banner");
    banners.forEach(function (b) {
      if (nOverdue > 0) {
        var n = b.querySelector(".gh-followup-n");
        if (n) n.textContent = nOverdue;
        var txt = b.querySelector(".gh-followup-text");
        if (txt) txt.textContent = nOverdue + " application" + (nOverdue === 1 ? "" : "s") + " need follow-up";
        b.style.display = "flex";
      } else { b.style.display = "none"; }
    });

    // Let pages react (e.g. repaint match badges) without polling.
    try { document.dispatchEvent(new CustomEvent("gh:state", { detail: { saved: nSaved, applied: nApplied, tracked: nTracked, overdue: nOverdue } })); } catch (e) {}
  }
  function setText(id, txt) { var el = document.getElementById(id); if (el) el.textContent = txt; }

  // ---------- expose ----------------------------------------------------------
  window.GH = {
    STATUSES: STATUSES.slice(),
    KANBAN: KANBAN.map(function (c) { return { key: c.key, label: c.label, statuses: c.statuses.slice() }; }),
    MATCH_BANDS: MATCH_BANDS.slice(),
    getState: getState,
    profile: profile,
    saved: saved,
    hidden: hidden,
    tracker: tracker,
    savedSearches: savedSearches,
    export: exportJson,
    import: importJson,
    computeMatch: computeMatch,
    matchLabel: matchLabel,
    matchBand: matchBand,
    applicationStrategy: applicationStrategy,
    refreshUi: refreshUi,
    _reset: function () { _state = defaultState(); commit(); },
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", refreshUi);
  } else {
    refreshUi();
  }
})();
