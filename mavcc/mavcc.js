/* ==========================================================================
   MAVCC behaviours — mobile drawer, accordion, ticker pause, GHL form modal,
   newsletter submit, scroll reveal.

   PASTE TARGET: GHL → Settings → Tracking Code → Footer, wrapped in <script>.
   No dependencies. Safe to load twice. Never throws if a block is absent.
   ========================================================================== */
(function () {
  'use strict';

  var root = document.querySelector('.mavcc');
  if (!root || root.dataset.mavccReady === '1') return;
  root.dataset.mavccReady = '1';
  root.classList.add('js');

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ---------------------------------------------------------------- focus */
  var FOCUSABLE = 'a[href],button:not([disabled]),input:not([disabled]),' +
                  'select:not([disabled]),textarea:not([disabled]),iframe,[tabindex]:not([tabindex="-1"])';

  function trap(container, e) {
    var items = Array.prototype.filter.call(
      container.querySelectorAll(FOCUSABLE),
      function (el) { return el.offsetParent !== null || el.tagName === 'IFRAME'; }
    );
    if (!items.length) return;
    var first = items[0], last = items[items.length - 1];
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  }

  function lockScroll(on) {
    document.documentElement.style.overflow = on ? 'hidden' : '';
  }

  /* -------------------------------------------------------- mobile drawer */
  var drawer = root.querySelector('[data-drawer]');
  var drawerReturn = null;

  function setDrawer(open) {
    if (!drawer) return;
    drawer.dataset.open = open ? 'true' : 'false';
    drawer.setAttribute('aria-hidden', open ? 'false' : 'true');
    lockScroll(open);
    Array.prototype.forEach.call(root.querySelectorAll('[data-drawer-open]'), function (b) {
      b.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    if (open) {
      drawerReturn = document.activeElement;
      var f = drawer.querySelector(FOCUSABLE);
      if (f) f.focus();
    } else if (drawerReturn) {
      drawerReturn.focus();
      drawerReturn = null;
    }
  }

  root.addEventListener('click', function (e) {
    if (e.target.closest('[data-drawer-open]')) { e.preventDefault(); setDrawer(true); }
    if (e.target.closest('[data-drawer-close]')) { e.preventDefault(); setDrawer(false); }
  });
  if (drawer) {
    drawer.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') setDrawer(false);
      if (e.key === 'Tab' && drawer.dataset.open === 'true') trap(drawer, e);
    });
    Array.prototype.forEach.call(drawer.querySelectorAll('nav a'), function (a) {
      a.addEventListener('click', function () { setDrawer(false); });
    });
  }

  /* ------------------------------------------------------------ accordion */
  Array.prototype.forEach.call(root.querySelectorAll('[data-acc-btn]'), function (btn) {
    btn.addEventListener('click', function () {
      var panel = document.getElementById(btn.getAttribute('aria-controls'));
      if (!panel) return;
      var open = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', open ? 'false' : 'true');
      panel.dataset.open = open ? 'false' : 'true';
    });
  });

  /* --------------------------------------------------------------- ticker */
  Array.prototype.forEach.call(root.querySelectorAll('[data-ticker]'), function (ticker) {
    var btn = ticker.querySelector('[data-ticker-pause]');
    if (!btn) return;
    var label = btn.querySelector('[data-ticker-label]');

    // Reduced motion: the CSS already stopped it — reflect that in the control.
    if (reduced) {
      ticker.dataset.paused = 'true';
      btn.setAttribute('aria-pressed', 'true');
      if (label) label.textContent = 'Motion off';
      btn.disabled = true;
      btn.style.opacity = '.6';
      btn.style.cursor = 'default';
      return;
    }
    btn.addEventListener('click', function () {
      var paused = ticker.dataset.paused === 'true';
      ticker.dataset.paused = paused ? 'false' : 'true';
      btn.setAttribute('aria-pressed', paused ? 'false' : 'true');
      if (label) label.textContent = paused ? 'Pause' : 'Play';
    });
  });

  /* ------------------------------------------- GHL form modal (lazy iframe) */
  var modal = root.querySelector('[data-modal]');
  var modalReturn = null;

  function openModal(src, title) {
    if (!modal) return;
    var frame = modal.querySelector('[data-modal-frame]');
    var heading = modal.querySelector('[data-modal-title]');
    if (heading && title) heading.textContent = title;
    // Load only on open — keeps the embed off the critical path.
    if (frame && frame.getAttribute('src') !== src) frame.setAttribute('src', src);
    modalReturn = document.activeElement;
    modal.dataset.open = 'true';
    modal.setAttribute('aria-hidden', 'false');
    lockScroll(true);
    var close = modal.querySelector('[data-modal-close]');
    if (close) close.focus();
  }

  function closeModal() {
    if (!modal) return;
    modal.dataset.open = 'false';
    modal.setAttribute('aria-hidden', 'true');
    lockScroll(false);
    if (modalReturn) { modalReturn.focus(); modalReturn = null; }
  }

  root.addEventListener('click', function (e) {
    var opener = e.target.closest('[data-form-modal]');
    if (opener) {
      e.preventDefault();
      openModal(opener.getAttribute('data-form-modal'), opener.getAttribute('data-form-title') || 'Form');
    }
    if (e.target.closest('[data-modal-close]')) { e.preventDefault(); closeModal(); }
  });
  if (modal) {
    modal.addEventListener('click', function (e) { if (e.target === modal) closeModal(); });
    modal.addEventListener('keydown', function (e) {
      if (e.key === 'Escape') closeModal();
      if (e.key === 'Tab' && modal.dataset.open === 'true') trap(modal, e);
    });
  }

  /* ----------------------------------------------------------- newsletter */
  Array.prototype.forEach.call(root.querySelectorAll('[data-news]'), function (form) {
    var input = form.querySelector('input[type="email"]');
    var err = form.querySelector('[data-news-error]');
    var ok = form.querySelector('[data-news-ok]');
    if (!input) return;

    form.addEventListener('submit', function (e) {
      var value = input.value.trim();
      var valid = /^[^@\s]+@[^@\s.]+\.[^@\s]{2,}$/.test(value);
      if (!valid) {
        e.preventDefault();
        input.setAttribute('aria-invalid', 'true');
        if (err) {
          err.textContent = value
            ? 'That address is missing an @ or a domain — check it and try again.'
            : 'Enter your email address to subscribe.';
          err.hidden = false;
        }
        input.focus();
        return;
      }
      input.setAttribute('aria-invalid', 'false');
      if (err) err.hidden = true;
      if (ok) { ok.hidden = false; }
      // The action attribute carries the real GHL endpoint; let it submit.
    });

    input.addEventListener('input', function () {
      if (input.getAttribute('aria-invalid') === 'true' && input.value.trim()) {
        input.setAttribute('aria-invalid', 'false');
        if (err) err.hidden = true;
      }
    });
  });

  /* --------------------------------------------------------------- reveal */
  var targets = root.querySelectorAll('[data-reveal]');
  if (!targets.length) return;

  if (reduced || !('IntersectionObserver' in window)) {
    Array.prototype.forEach.call(targets, function (el) { el.dataset.shown = 'true'; });
    return;
  }
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.dataset.shown = 'true';
        io.unobserve(entry.target);
      }
    });
  }, { rootMargin: '0px 0px -12% 0px', threshold: 0.05 });

  Array.prototype.forEach.call(targets, function (el) { io.observe(el); });
})();
