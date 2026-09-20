/* Behaviour for the portfolio: scroll reveal and certification pills.
   Page routing is Jekyll's job; this file is interactivity only. The site is
   light-only, so there is no theme handling here any more. */
(function () {
  "use strict";

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
    nodes.forEach(function (el) { observer.observe(el); });
  }

  /* ---- certification pills ----------------------------------------------- */

  var openCert = null;

  function certOf(el) {
    return el && el.closest ? el.closest(".cert") : null;
  }

  // The tray is absolutely positioned, so it can run off a narrow viewport;
  // measure it while it is laid out and flip it to right-aligned if so.
  function placeCert(cert) {
    var tray = cert.querySelector(".cert-tray");
    if (!tray) return;
    tray.classList.remove("is-flipped");
    if (tray.getBoundingClientRect().right > document.documentElement.clientWidth - 12) {
      tray.classList.add("is-flipped");
    }
  }

  function closeCert() {
    if (!openCert) return;
    var btn = openCert.querySelector(".cert-pill");
    if (btn) btn.setAttribute("aria-expanded", "false");
    openCert.classList.remove("is-open");
    openCert = null;
  }

  function showCert(cert) {
    if (openCert !== cert) closeCert();
    var btn = cert.querySelector(".cert-pill");
    if (btn) btn.setAttribute("aria-expanded", "true");
    cert.classList.add("is-open");
    openCert = cert;
    placeCert(cert);
  }

  // Hover is handled in CSS; JS only needs to keep the flip decision current.
  document.addEventListener("mouseover", function (e) {
    var cert = certOf(e.target);
    if (cert) placeCert(cert);
  });

  document.addEventListener("focusin", function (e) {
    var pill = e.target.closest ? e.target.closest(".cert-pill") : null;
    if (!pill) {
      if (openCert && !certOf(e.target)) closeCert();
      return;
    }
    // Only keyboard focus opens the tray; a pointer press is left to the
    // click handler below, which toggles.
    var keyboard = false;
    try { keyboard = pill.matches(":focus-visible"); } catch (err) {}
    if (keyboard) showCert(pill.parentNode);
  });

  document.addEventListener("keydown", function (e) {
    if (e.key !== "Escape" || !openCert) return;
    var btn = openCert.querySelector(".cert-pill");
    closeCert();
    if (btn) btn.focus();
  });

  window.addEventListener("resize", function () {
    if (openCert) placeCert(openCert);
  });

  /* ---- wiring ------------------------------------------------------------ */

  document.addEventListener("click", function (e) {
    var pill = e.target.closest(".cert-pill");
    if (pill) {
      var cert = pill.parentNode;
      if (openCert === cert) closeCert(); else showCert(cert);
      return;
    }
    if (openCert && !certOf(e.target)) closeCert();

    var placeholder = e.target.closest("[data-placeholder]");
    if (placeholder) { e.preventDefault(); return; }
  });

  reveal();
})();
