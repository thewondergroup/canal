/* CANAL — menus, drawn from a Google Sheet (published as CSV) or data/menu.csv.
   Sheet columns: menu | section | item | description | price | tag   (tag: v, ve, gf — optional) */
(function () {
  var root = document.querySelector('[data-menus]');
  var previews = document.querySelectorAll('[data-menu-preview]');
  if (!root && !previews.length) return;
  var C = window.CANAL || {};

  function parseCSV(text) {
    var rows = [], row = [], cell = '', q = false;
    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (q) {
        if (ch === '"') { if (text[i + 1] === '"') { cell += '"'; i++; } else q = false; }
        else cell += ch;
      } else if (ch === '"') q = true;
      else if (ch === ',') { row.push(cell); cell = ''; }
      else if (ch === '\n' || ch === '\r') { if (ch === '\r' && text[i + 1] === '\n') i++; row.push(cell); rows.push(row); row = []; cell = ''; }
      else cell += ch;
    }
    if (cell || row.length) { row.push(cell); rows.push(row); }
    var head = (rows.shift() || []).map(function (h) { return h.trim().toLowerCase(); });
    return rows.filter(function (r) { return r.join('').trim(); }).map(function (r) {
      var o = {}; head.forEach(function (h, i) { o[h] = (r[i] || '').trim(); }); return o;
    });
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }
  function price(p) { if (!p) return ''; return p.split('/').map(function (x) { x = x.trim(); return /^\d/.test(x) ? x : x; }).join(' / '); }

  function render(items) {
    var menus = {}, order = [];
    items.forEach(function (it) {
      var m = (it.menu || 'food').toLowerCase();
      if (!menus[m]) { menus[m] = {}; menus[m]._order = []; order.push(m); }
      var s = it.section || '';
      if (!menus[m][s]) { menus[m][s] = []; menus[m]._order.push(s); }
      menus[m][s].push(it);
    });
    var tabs = root.querySelector('.menu-tabs'), body = root.querySelector('.menu-body');
    tabs.innerHTML = order.map(function (m, i) {
      return '<button role="tab" aria-selected="' + (i === 0) + '" data-m="' + esc(m) + '">' + esc(m.charAt(0).toUpperCase() + m.slice(1)) + '</button>';
    }).join('');
    body.innerHTML = order.map(function (m, i) {
      var secs = menus[m]._order.map(function (s) {
        return '<div class="menu-sec rv in"><h3>' + esc(s) + '</h3><ul>' + menus[m][s].map(function (it) {
          var tag = it.tag ? '<span class="mtag">' + esc(it.tag) + '</span>' : '';
          return '<li><div><span class="mi">' + esc(it.item) + tag + '</span>' + (it.description ? '<span class="md">' + esc(it.description) + '</span>' : '') +
            '</div><span class="mp">' + esc(price(it.price)) + '</span></li>';
        }).join('') + '</ul></div>';
      }).join('');
      return '<div class="menu-panel" data-m="' + esc(m) + '"' + (i ? ' hidden' : '') + '>' + secs + '</div>';
    }).join('');
    tabs.querySelectorAll('button').forEach(function (b) {
      b.addEventListener('click', function () {
        tabs.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-selected', x === b); });
        body.querySelectorAll('.menu-panel').forEach(function (p) { p.hidden = p.getAttribute('data-m') !== b.getAttribute('data-m'); });
      });
    });
    var hash = (location.hash || '').slice(1);
    var t = tabs.querySelector('[data-m="' + hash + '"]'); if (t) t.click();
    root.classList.add('loaded');
  }

  function preview(items) {
    previews.forEach(function (el) {
      var menu = el.getAttribute('data-menu') || 'food';
      var secs = (el.getAttribute('data-sections') || '').split(',').map(function (x) { return x.trim(); }).filter(Boolean);
      var per = +(el.getAttribute('data-per') || 3);
      var html = secs.map(function (s) {
        var rows = items.filter(function (it) { return (it.menu || 'food').toLowerCase() === menu && it.section === s; }).slice(0, per);
        if (!rows.length) return '';
        return '<div class="menu-sec"><h3>' + esc(s) + '</h3><ul>' + rows.map(function (it) {
          return '<li><div><span class="mi">' + esc(it.item) + '</span>' + (it.description ? '<span class="md">' + esc(it.description) + '</span>' : '') +
            '</div><span class="mp">' + esc(price(it.price)) + '</span></li>';
        }).join('') + '</ul></div>';
      }).join('');
      el.innerHTML = html;
    });
  }

  function load(url) { return fetch(url, { cache: 'no-store' }).then(function (r) { if (!r.ok) throw 0; return r.text(); }); }
  var local = (root && root.getAttribute('data-menus')) || 'data/menu.csv';
  (C.menuSheetCsv ? load(C.menuSheetCsv).catch(function () { return load(local); }) : load(local))
    .then(function (t) { var items = parseCSV(t); if (root) render(items); if (previews.length) preview(items); })
    .catch(function () { if (root) root.querySelector('.menu-body').innerHTML = '<p class="body">Menus are loading slowly — see the PDFs below.</p>'; });
})();
