/* CANAL — "canal-side right now": open/closed, sunset, terrace weather.
   Open/closed and sunset are worked out in the browser; weather comes from Open-Meteo (free, no key)
   and simply doesn't show if it can't be reached. */
(function () {
  var C = window.CANAL || {};
  var els = document.querySelectorAll('[data-live]');
  if (!els.length) return;

  var TZ = 'Europe/London';
  var DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];

  function londonParts(d) {
    var f = new Intl.DateTimeFormat('en-GB', { timeZone: TZ, weekday: 'short', year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', hour12: false });
    var p = {}; f.formatToParts(d).forEach(function (x) { p[x.type] = x.value; });
    var wd = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'].indexOf(p.weekday);
    return { wd: wd, mins: (+p.hour % 24) * 60 + (+p.minute), ymd: p.year + '-' + p.month + '-' + p.day };
  }
  function toMins(s) { var a = s.split(':'); return +a[0] * 60 + +a[1]; }
  function nice(s) { // "22:00" -> "10pm", "20:30" -> "8.30pm"
    var m = toMins(s), h = Math.floor(m / 60), mm = m % 60, ap = h >= 12 ? 'pm' : 'am';
    h = h % 12 || 12; return h + (mm ? '.' + String(mm).padStart(2, '0') : '') + ap;
  }

  function openState() {
    var now = londonParts(new Date());
    var hrs = C.hours || {}, closed = C.closedDates || [];
    var today = hrs[now.wd];
    if (today && closed.indexOf(now.ymd) < 0) {
      var o = toMins(today[0]), c = toMins(today[1]);
      if (now.mins >= o && now.mins < c) {
        var left = c - now.mins;
        return { open: true, text: left <= 45 ? 'Last orders soon · closes ' + nice(today[1]) : 'Open now · until ' + nice(today[1]) };
      }
      if (now.mins < o) return { open: false, text: 'Opens today at ' + nice(today[0]) };
    }
    for (var i = 1; i <= 7; i++) {
      var wd = (now.wd + i) % 7, h = hrs[wd];
      if (h) return { open: false, text: 'Closed now · opens ' + (i === 1 ? 'tomorrow' : DAYS[wd]) + ' ' + nice(h[0]) };
    }
    return { open: false, text: 'Closed' };
  }

  // Sunset (NOAA approximation) for today at the restaurant
  function sunset() {
    var lat = C.lat || 51.52, lng = C.lng || -0.2, d = new Date();
    var rad = Math.PI / 180;
    var start = Date.UTC(d.getUTCFullYear(), 0, 0);
    var n = Math.floor((Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()) - start) / 864e5);
    var g = 2 * Math.PI / 365 * (n - 1 + 0.5);
    var eq = 229.18 * (0.000075 + 0.001868 * Math.cos(g) - 0.032077 * Math.sin(g) - 0.014615 * Math.cos(2 * g) - 0.040849 * Math.sin(2 * g));
    var dec = 0.006918 - 0.399912 * Math.cos(g) + 0.070257 * Math.sin(g) - 0.006758 * Math.cos(2 * g) + 0.000907 * Math.sin(2 * g) - 0.002697 * Math.cos(3 * g) + 0.00148 * Math.sin(3 * g);
    var ha = Math.acos(Math.cos(90.833 * rad) / (Math.cos(lat * rad) * Math.cos(dec)) - Math.tan(lat * rad) * Math.tan(dec)) / rad;
    var utcMins = 720 - 4 * (lng - ha) - eq;
    var t = new Date(Date.UTC(d.getUTCFullYear(), d.getUTCMonth(), d.getUTCDate()) + utcMins * 6e4);
    var s = new Intl.DateTimeFormat('en-GB', { timeZone: TZ, hour: 'numeric', minute: '2-digit', hour12: true }).format(t);
    var past = t < d;
    return (past ? 'Sun set at ' : 'Sunset ') + s.replace(':', '.').replace(' ', '').toLowerCase();
  }

  var WX = [[0, 'clear skies', 'sunny'], [1, 'mostly clear', 'mostly sunny'], [2, 'some cloud', 'sunny spells'], [3, 'cloudy', 'cloudy'],
    [45, 'misty', 'misty'], [48, 'misty', 'misty'], [51, 'drizzle', 'drizzle'], [53, 'drizzle', 'drizzle'], [55, 'drizzle', 'drizzle'],
    [61, 'light rain', 'light rain'], [63, 'rain', 'rain'], [65, 'heavy rain', 'heavy rain'], [71, 'snow', 'snow'], [73, 'snow', 'snow'], [75, 'snow', 'snow'],
    [80, 'showers', 'showers'], [81, 'showers', 'showers'], [82, 'heavy showers', 'heavy showers'], [95, 'thunder', 'thunder']];
  function wxWord(code, day) {
    var best = WX[0]; WX.forEach(function (w) { if (code >= w[0]) best = w; });
    return day ? best[2] : best[1];
  }
  var weather = null;
  function getWeather() {
    if (!window.fetch) return;
    var u = 'https://api.open-meteo.com/v1/forecast?latitude=' + (C.lat || 51.52) + '&longitude=' + (C.lng || -0.2) +
      '&current=temperature_2m,weather_code,is_day&timezone=Europe%2FLondon';
    fetch(u).then(function (r) { return r.json(); }).then(function (j) {
      var c = j && j.current; if (!c) return;
      var t = Math.round(c.temperature_2m), code = c.weather_code, wet = code >= 51 && code < 95 || code >= 95;
      weather = 'Terrace ' + t + '° · ' + wxWord(code, c.is_day) + (wet ? ' — it’s covered &amp; heated' : '');
      render();
    }).catch(function () {});
  }

  function render() {
    var st = openState();
    var items = ['<span class="live-item"><i class="dot' + (st.open ? ' on' : '') + '"></i>' + st.text + '</span>',
      '<span class="live-item">' + sunset() + '</span>'];
    if (weather) items.push('<span class="live-item">' + weather + '</span>');
    els.forEach(function (el) { el.innerHTML = items.join(''); el.classList.add('ready'); });
  }

  render(); getWeather();
  setInterval(render, 60000);
  setInterval(getWeather, 15 * 60000);
})();
