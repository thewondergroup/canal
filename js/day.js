/* CANAL — day & evening.
   The site switches to its evening look after sunset (set early in <head> so nothing flashes),
   the header toggle lets anyone flip it, and "A day at Canal" walks from lunch to last orders. */
(function () {
  var root = document.documentElement;

  // Toggle
  document.querySelectorAll('.mode').forEach(function (b) {
    b.addEventListener('click', function () {
      var next = root.getAttribute('data-mode') === 'evening' ? 'day' : 'evening';
      root.setAttribute('data-mode', next);
      try { sessionStorage.setItem('canal-mode', next); } catch (e) {}
      b.setAttribute('aria-label', next === 'evening' ? 'Switch to daytime' : 'Switch to evening');
    });
  });

  // A day at Canal
  var day = document.querySelector('.day');
  if (!day) return;
  var steps = [].slice.call(day.querySelectorAll('.step'));
  var imgs = [].slice.call(day.querySelectorAll('.day-plate img'));
  var clock = day.querySelector('.day-clock');
  function set(i) {
    day.setAttribute('data-step', i);
    steps.forEach(function (s, j) { s.classList.toggle('on', j === i); });
    imgs.forEach(function (im, j) { im.classList.toggle('on', j === i); });
    if (clock) clock.textContent = steps[i].getAttribute('data-time');
  }
  // live sunset time in the sunset step
  var sun = day.querySelector('[data-sunset]');
  if (sun && window.CANAL_SUNSET) {
    sun.setAttribute('data-time', window.CANAL_SUNSET.hhmm);
    var w = sun.querySelector('.when'); if (w) w.textContent = 'Sunset · ' + window.CANAL_SUNSET.label + ' today';
  }
  set(0);
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) set(steps.indexOf(e.target)); });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(function (s) { io.observe(s); });
  }
})();
