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
