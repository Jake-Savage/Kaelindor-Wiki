/* Client-side keyword search over the prebuilt search-index.json. No backend. */
(function () {
  "use strict";

  // Derive the site root from the stylesheet href (works at any nesting depth
  // and under a project subpath like GitHub Pages).
  var linkEl = document.querySelector('link[rel="stylesheet"]');
  var root = linkEl ? linkEl.getAttribute("href").replace(/static\/style\.css.*$/, "") : "";

  var docs = null;
  var ready = null;
  function load() {
    if (ready) return ready;
    ready = fetch(root + "search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { docs = d; return d; });
    return ready;
  }

  function tokenize(s) { return ((s || "").toLowerCase().match(/[a-z0-9']+/g)) || []; }

  function escapeHtml(s) {
    return (s || "").replace(/[&<>]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c];
    });
  }

  var TYPE_LABEL = {
    characters: "Character", locations: "Location", quests: "Quest",
    factions: "Faction", items: "Item", lore: "Lore", sessions: "Session"
  };

  function score(doc, terms) {
    var title = doc.title.toLowerCase();
    var summary = (doc.summary || "").toLowerCase();
    var tags = (doc.tags || []).join(" ").toLowerCase();
    var text = (doc.text || "").toLowerCase();
    var hay = title + "  " + tags + "  " + summary + "  " + text;
    // require every term to appear somewhere
    if (!terms.every(function (t) { return hay.indexOf(t) !== -1; })) return 0;
    var s = 0;
    terms.forEach(function (t) {
      if (title === t) s += 50;
      else if (title.indexOf(t) !== -1) s += 12;
      if (tags.indexOf(t) !== -1) s += 8;
      if (summary.indexOf(t) !== -1) s += 5;
      var idx = text.indexOf(t), c = 0;
      while (idx !== -1 && c < 10) { s += 1; idx = text.indexOf(t, idx + 1); c++; }
    });
    return s;
  }

  function search(q) {
    var terms = tokenize(q);
    if (!terms.length) return [];
    return docs
      .map(function (d) { return { doc: d, s: score(d, terms) }; })
      .filter(function (r) { return r.s > 0; })
      .sort(function (a, b) { return b.s - a.s; })
      .slice(0, 50);
  }

  function render(results, container) {
    if (!results.length) { container.innerHTML = '<p class="muted">No matches.</p>'; return; }
    var html = '<ul class="search-results">';
    results.forEach(function (r) {
      var d = r.doc;
      html += '<li><a href="' + root + d.url + '">' +
        '<span class="result-type result-' + d.type + '">' + (TYPE_LABEL[d.type] || d.type) + "</span> " +
        '<span class="result-title">' + escapeHtml(d.title) + "</span></a>" +
        '<p class="muted">' + escapeHtml(d.summary || "") + "</p></li>";
    });
    html += "</ul>";
    container.innerHTML = html;
  }

  // Wire up the dedicated search page if present.
  var input = document.getElementById("search-input");
  var resultsEl = document.getElementById("search-results");
  var statusEl = document.getElementById("search-status");
  if (input && resultsEl) {
    var q0 = new URLSearchParams(location.search).get("q") || "";
    var run = function () {
      var q = input.value.trim();
      if (!q) { resultsEl.innerHTML = ""; if (statusEl) statusEl.textContent = ""; return; }
      load().then(function () {
        var res = search(q);
        if (statusEl) {
          statusEl.textContent = res.length + " result" + (res.length === 1 ? "" : "s") + " for “" + q + "”";
        }
        render(res, resultsEl);
      });
    };
    input.addEventListener("input", run);
    if (q0) { input.value = q0; run(); }
  }
})();
