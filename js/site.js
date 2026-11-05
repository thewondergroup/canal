/* CANAL — site behaviour */
(function () {
  var header = document.querySelector('.header');
  var solidAlways = document.body.classList.contains('solid-header');
  function onScroll() {
    if (!header) return;
    header.classList.toggle('solid', solidAlways || window.scrollY > 60);
  }
  window.addEventListener('scroll', onScroll, { passive: true });
  onScroll();

  // Mobile menu
  var burger = document.querySelector('.burger');
  var menu = document.querySelector('.menu');
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('open');
      document.body.classList.toggle('locked', open);
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  // Reveal on scroll
  var els = document.querySelectorAll('.rv');
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    els.forEach(function (el) { io.observe(el); });
  } else { els.forEach(function (el) { el.classList.add('in'); }); }

  // Only play reels while they're on screen
  var vids = document.querySelectorAll('video[data-inview]');
  if ('IntersectionObserver' in window) {
    var vo = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { var p = e.target.play(); if (p && p.catch) p.catch(function () {}); }
        else e.target.pause();
      });
    }, { threshold: 0.25 });
    vids.forEach(function (v) { vo.observe(v); });
  }

  // Menus: today's date, and a photo that follows the cursor
  var today = document.querySelector('[data-today]');
  if (today) {
    try { today.textContent = 'Today’s menu · ' + new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', weekday: 'long', day: 'numeric', month: 'long' }).format(new Date()); } catch (e) {}
  }
  var rev = document.querySelector('[data-reveal]');
  if (rev && window.matchMedia && window.matchMedia('(hover:hover)').matches) {
    var fl = rev.querySelector('.mr-float'), fi = fl.querySelector('img'), tx = 0, ty = 0, cx = 0, cy = 0, raf = null;
    function tick() { cx += (tx - cx) * .18; cy += (ty - cy) * .18; fl.style.left = cx + 'px'; fl.style.top = cy + 'px';
      raf = Math.abs(tx - cx) + Math.abs(ty - cy) > .5 ? requestAnimationFrame(tick) : null; }
    rev.addEventListener('mousemove', function (e) { tx = e.clientX + 160; ty = e.clientY; if (!raf) raf = requestAnimationFrame(tick); });
    rev.querySelectorAll('.mr-row').forEach(function (r) {
      r.addEventListener('mouseenter', function (e) { fi.src = r.getAttribute('data-img'); if (!fl.classList.contains('on')) { cx = tx = e.clientX + 160; cy = ty = e.clientY; } fl.classList.add('on'); });
      r.addEventListener('mouseleave', function () { fl.classList.remove('on'); });
    });
  }

  // Christmas countdown
  var cd = document.querySelector('[data-countdown]');
  if (cd) {
    try {
      var p = new Intl.DateTimeFormat('en-GB', { timeZone: 'Europe/London', year: 'numeric', month: '2-digit', day: '2-digit' }).formatToParts(new Date());
      var o = {}; p.forEach(function (x) { o[x.type] = x.value; });
      var today = Date.UTC(+o.year, +o.month - 1, +o.day), xmas = Date.UTC(+o.year, 11, 25);
      var days = Math.round((xmas - today) / 864e5);
      if (days > 1) cd.textContent = 'Christmas Day is ' + days + ' days away';
      else if (days === 1) cd.textContent = 'Christmas Day is tomorrow';
      else if (days === 0) cd.textContent = 'Merry Christmas';
    } catch (e) {}
  }

  // Groups: a format card fills in the enquiry form
  document.querySelectorAll('.format[data-guests]').forEach(function (a) {
    a.addEventListener('click', function () {
      var g = document.getElementById('f4'), t = document.getElementById('f6');
      if (g) g.value = a.getAttribute('data-guests');
      if (t) t.value = a.getAttribute('data-occasion');
    });
  });

  // Newsletter (swap in the real list endpoint before launch)
  document.querySelectorAll('.signup').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var m = f.parentElement.querySelector('.msg');
      if (m) m.textContent = 'Splish, splash. You’re on the list.';
      f.reset();
    });
  });

  // Events enquiry -> email draft (Tripleseat link sits alongside)
  var enq = document.querySelector('#enquiry');
  if (enq) {
    enq.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(enq);
      var lines = ['Name: ' + d.get('name'), 'Email: ' + d.get('email'), 'Phone: ' + d.get('phone'),
        'Guests: ' + d.get('guests'), 'Date: ' + d.get('date'), 'Event: ' + d.get('type'), '', d.get('message') || ''];
      var m = enq.querySelector('.msg');
      if (m) m.textContent = 'Opening an email to hello@canalrestaurant.com…';
      window.location.href = 'mailto:hello@canalrestaurant.com?subject=' +
        encodeURIComponent('Event enquiry — ' + d.get('name')) + '&body=' + encodeURIComponent(lines.join('\n'));
    });
  }
})();
