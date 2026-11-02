// Turns the five views into tabs. Without this script every view stays visible in
// page order and the header shows plain anchor links.
(function () {
  "use strict";

  var tablist = document.querySelector("[data-tablist]");
  var fallbackNav = document.querySelector("[data-fallback-nav]");
  var description = document.querySelector('meta[name="description"]');
  var tabs = Array.prototype.slice.call(document.querySelectorAll('[role="tab"]'));
  var panels = Array.prototype.slice.call(document.querySelectorAll("[data-view]"));
  if (!tablist || !fallbackNav || !tabs.length) return;

  function panelExists(id) {
    return panels.some(function (panel) { return panel.id === id; });
  }

  function viewFromHash() {
    var id = window.location.hash.slice(1);
    return panelExists(id) ? id : null;
  }

  function select(id) {
    tabs.forEach(function (tab) {
      var selected = tab.getAttribute("aria-controls") === id;
      tab.setAttribute("aria-selected", String(selected));
      tab.tabIndex = selected ? 0 : -1;
    });
    panels.forEach(function (panel) {
      var selected = panel.id === id;
      panel.hidden = !selected;
      if (selected) {
        document.title = panel.dataset.title;
        if (description) description.setAttribute("content", panel.dataset.description);
      }
    });
  }

  function tabFor(id) {
    return document.getElementById("tab-" + id);
  }

  // Keeps the URL shareable without letting the browser jump to the panel.
  function updateUrl(id, replace) {
    var url = "#" + id;
    if (window.location.hash === url) return;
    if (replace) history.replaceState(null, "", url);
    else history.pushState(null, "", url);
  }

  panels.forEach(function (panel) {
    panel.setAttribute("role", "tabpanel");
    panel.setAttribute("aria-labelledby", "tab-" + panel.id);
    panel.tabIndex = 0;
  });
  fallbackNav.remove();
  tablist.hidden = false;

  tablist.addEventListener("click", function (event) {
    var tab = event.target.closest('[role="tab"]');
    if (!tab) return;
    var id = tab.getAttribute("aria-controls");
    select(id);
    updateUrl(id, false);
  });

  // Arrow, Home and End move focus and show the view straight away; panels are static,
  // so there is no cost to selecting on focus. Enter and Space are native button clicks.
  tablist.addEventListener("keydown", function (event) {
    var index = tabs.indexOf(event.target);
    if (index === -1) return;
    var next;
    switch (event.key) {
      case "ArrowRight": next = (index + 1) % tabs.length; break;
      case "ArrowLeft": next = (index - 1 + tabs.length) % tabs.length; break;
      case "Home": next = 0; break;
      case "End": next = tabs.length - 1; break;
      default: return;
    }
    event.preventDefault();
    var id = tabs[next].getAttribute("aria-controls");
    select(id);
    updateUrl(id, true);
    tabs[next].focus();
  });

  // The header brand and the Home "Explore" buttons are links to a view.
  document.addEventListener("click", function (event) {
    var link = event.target.closest("[data-view-link]");
    if (!link) return;
    var id = link.getAttribute("data-view-link");
    if (!panelExists(id)) return;
    event.preventDefault();
    select(id);
    updateUrl(id, false);
    window.scrollTo(0, 0);
    tabFor(id).focus({ preventScroll: true });
  });

  // Back, forward and edited URLs. The skip link's #main is not a view, so it changes nothing.
  function syncFromUrl() {
    if (!window.location.hash) select("home");
    else if (viewFromHash()) select(viewFromHash());
  }
  window.addEventListener("popstate", syncFromUrl);
  window.addEventListener("hashchange", syncFromUrl);

  select(viewFromHash() || "home");

  // A deep link would otherwise load scrolled past the header and tabs.
  if (viewFromHash()) {
    window.addEventListener("load", function () { window.scrollTo(0, 0); });
  }
})();
