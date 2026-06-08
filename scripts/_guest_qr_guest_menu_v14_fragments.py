"""Guest order screen — menu load + categories + scroll (v14)."""

ENSURE_GUEST_MENU_LOAD_OLD = """function ensureGuestRestaurantMenuLoaded() {
  try {
    if (typeof load === 'function') menuItems = load('menuItems', menuItems);
  } catch (e) {}
  if (!Array.isArray(menuItems) || !menuItems.length) {
    if (typeof defaultMenuItems !== 'undefined' && Array.isArray(defaultMenuItems) && defaultMenuItems.length) menuItems = defaultMenuItems.slice();
    else menuItems = [];
  }
  if (!Array.isArray(restaurantOrders)) restaurantOrders = [];
}"""

ENSURE_GUEST_MENU_LOAD_NEW = """function ensureGuestRestaurantMenuLoaded() {
  try {
    if (typeof load === 'function') menuItems = load('menuItems', menuItems);
  } catch (e) {}
  if (!Array.isArray(menuItems) || !menuItems.length) {
    if (typeof defaultMenuItems !== 'undefined' && Array.isArray(defaultMenuItems) && defaultMenuItems.length) {
      menuItems = defaultMenuItems.slice();
    } else if (typeof nisha1DefaultMenuItems === 'function') {
      menuItems = nisha1DefaultMenuItems();
    } else {
      menuItems = [];
    }
  }
  if (!Array.isArray(restaurantOrders)) restaurantOrders = [];
}
function guestRestMenuCategoryNorm(c) {
  return String(c == null ? '' : c).trim().toLowerCase();
}
function guestRestGetMenuCategories() {
  ensureGuestRestaurantMenuLoaded();
  var seen = {};
  var list = [];
  function addCat(c) {
    var n = guestRestMenuCategoryNorm(c);
    if (!n || seen[n]) return;
    seen[n] = true;
    list.push(String(c).trim());
  }
  if (typeof getMenuCategories === 'function') {
    getMenuCategories().forEach(addCat);
  }
  (menuItems || []).forEach(function(m) { if (m && m.category) addCat(m.category); });
  list.sort(function(a, b) { return a.localeCompare(b); });
  return list;
}
function guestRestMenuCategoryMatches(itemCat, filterCat) {
  if (!filterCat || filterCat === 'All') return true;
  return guestRestMenuCategoryNorm(itemCat) === guestRestMenuCategoryNorm(filterCat);
}"""

GUEST_REST_CATEGORIES_OLD = """  var categories = ['All'].concat(typeof getMenuCategories === 'function' ? getMenuCategories() : []);
  var searchQ = String(guestOrderMenuSearch || '').trim();
  var searchHtml = '<div class="guest-rest-search"><input type="search" class="form-control'"""

GUEST_REST_CATEGORIES_NEW = """  var categories = ['All'].concat(typeof guestRestGetMenuCategories === 'function' ? guestRestGetMenuCategories() : (typeof getMenuCategories === 'function' ? getMenuCategories() : []));
  var searchQ = String(guestOrderMenuSearch || '').trim();
  var searchHtml = '<div class="guest-rest-search"><input type="search" class="form-control'"""

GUEST_REST_FILTER_OLD = """  var filtered = (guestRestMenuFilter === 'All' ? menuItems : menuItems.filter(function(m) { return m && m.category === guestRestMenuFilter; })).filter(function(m) {
    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m)) && guestRestMenuMatchesSearch(m, searchQ);
  });"""

GUEST_REST_FILTER_NEW = """  var filtered = (guestRestMenuFilter === 'All' ? menuItems : menuItems.filter(function(m) { return m && guestRestMenuCategoryMatches(m.category, guestRestMenuFilter); })).filter(function(m) {
    return m && m.available !== false && (typeof rowDataVisible !== 'function' || rowDataVisible(m)) && guestRestMenuMatchesSearch(m, searchQ);
  });"""

GUEST_REST_CSS_SCROLL_OLD = """    .guest-rest-panel { background: var(--card-bg, #fff); border: 1px solid var(--border); border-radius: 12px; padding: 0.85rem; }"""

GUEST_REST_CSS_SCROLL_NEW = """    .guest-rest-panel { background: var(--card-bg, #fff); border: 1px solid var(--border); border-radius: 12px; padding: 0.85rem; min-width: 0; }
    .guest-rest-order-overlay .guest-rest-order-shell { max-width: 100%; width: 100%; }
    @media (min-width: 900px) { .guest-rest-order-overlay .guest-rest-order-shell { max-width: 1100px; margin: 0 auto; } }
    .guest-rest-layout .guest-rest-panel:first-child { max-height: min(72vh, calc(100dvh - 10rem)); overflow-y: auto; -webkit-overflow-scrolling: touch; }"""
