/* Behaviour for the portfolio: hash routing, theme toggle, scroll reveal. */
(function () {
  "use strict";

  var PAGES = ["index", "work", "project", "notes", "post", "contact"];
  var NAV_OF = { index: "index", work: "work", project: "work", notes: "notes", post: "notes", contact: "contact" };

  /* ---- theme ------------------------------------------------------------- */

  function currentTheme() {
    return document.documentElement.getAttribute("data-theme") === "dark" ? "dark" : "light";
  }

  function applyTheme(t) {
    document.documentElement.setAttribute("data-theme", t);
    var label = document.querySelector("[data-theme-label]");
    if (label) label.textContent = t === "dark" ? "Light" : "Dark";
    document.querySelectorAll("[data-theme-icon]").forEach(function (el) {
      el.hidden = el.getAttribute("data-theme-icon") !== (t === "dark" ? "dark" : "light");
    });
  }

  function toggleTheme() {
    var t = currentTheme() === "dark" ? "light" : "dark";
    try { localStorage.setItem("az-theme", t); } catch (e) {}
    applyTheme(t);
    reveal();
  }

  /* ---- scroll reveal ----------------------------------------------------- */

  var observer = null;
  var SELECTOR = "[data-reveal]:not(.is-in),[data-stagger]:not(.is-in)";

  function reveal() {
    var nodes = document.querySelectorAll(SELECTOR);
    if (!("IntersectionObserver" in window)) {
      nodes.forEach(function (el) { el.classList.add("is-in"); });
      return;
    }
    if (!observer) {
      observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (!e.isIntersecting) return;
          var el = e.target;
          observer.unobserve(el);
          requestAnimationFrame(function () {
            requestAnimationFrame(function () { el.classList.add("is-in"); });
          });
        });
      }, { rootMargin: "0px 0px -6% 0px", threshold: 0.06 });
    }
    nodes.forEach(function (el) {
      // A hidden page has zero size and never intersects; observe it once shown.
      if (el.closest("[data-page][hidden]")) return;
      observer.observe(el);
    });
  }

  /* ---- routing ----------------------------------------------------------- */

  function pageFromHash() {
    var h = (location.hash || "").replace(/^#/, "");
    return PAGES.indexOf(h) === -1 ? "index" : h;
  }

  function show(page) {
    document.querySelectorAll("[data-page]").forEach(function (el) {
      el.hidden = el.getAttribute("data-page") !== page;
    });
    var active = NAV_OF[page];
    document.querySelectorAll("[data-nav]").forEach(function (el) {
      el.classList.toggle("is-active", el.getAttribute("data-nav") === active);
    });
    requestAnimationFrame(reveal);
  }

  function route(scroll) {
    show(pageFromHash());
    if (scroll) window.scrollTo(0, 0);
  }

  /* ---- wiring ------------------------------------------------------------ */

  document.addEventListener("click", function (e) {
    var toggle = e.target.closest("[data-theme-toggle]");
    if (toggle) { toggleTheme(); return; }

    var placeholder = e.target.closest("[data-placeholder]");
    if (placeholder) { e.preventDefault(); return; }

    var link = e.target.closest('a[href^="#"]');
    if (!link) return;
    var page = link.getAttribute("href").slice(1);
    if (PAGES.indexOf(page) === -1) return;
    e.preventDefault();
    if (pageFromHash() === page) {
      window.scrollTo(0, 0);
    } else {
      location.hash = page;
    }
  });

  window.addEventListener("hashchange", function () { route(true); });

  applyTheme(currentTheme());
  route(false);
})();
