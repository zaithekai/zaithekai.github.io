/* Behaviour for the portfolio: certification pills, and nothing else.
   Page routing is Jekyll's job. The site is light-only, and the entrance and
   scroll-reveal animations were removed, so no observer runs here any more. */
(function () {
  "use strict";

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

})();
