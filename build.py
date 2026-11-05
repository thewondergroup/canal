#!/usr/bin/env python3
"""Builds the Canal static site. Media is local (img/, video/, pdf/).
If a site photo hasn't been added yet, a stand-in from the photos we do have is used,
so the build always previews properly. Re-run after adding media."""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
CDN = "https://cdn.prod.website-files.com/67e6bf22004be258360f5e1b/"

BOOK = "https://www.sevenrooms.com/explore/canalrestaurant/reservations/create/search/"
ENQ = "https://hamrestaurants.tripleseat.com/party_request/43999"
GIFT = "https://canalrestaurant.giftpro.co.uk/"
INSTA = "https://www.instagram.com/canal.canal.canal/"
MAPS = "https://maps.google.com/?q=Canal+Restaurant+11b+Woodfield+Road+London+W9+2BA"

PDF_CDN = {
    "food": "6aeb6f21a556361f654105da_Canal%20Menu%2004.11.pdf",
    "wine": "6aad6137d8c88da69738c892_Canal%20Wine%20List%2016.09.2026.pdf",
    "bouillabaisse": "69c29b1b239aa25f83ca2978_Boullibaisse%20Menu.pdf",
    "group": "6ae60e11dd229cd3f45bf1ac_Events%20Sample%20Set%20Menu.pdf",
    "festive": "6ada08e1ca433ed46792d45f_Canal%20Festive%20Menu%202026.pdf",
    "xmasday": "6ada09470bd0525dde5a31bc_Canal%20Christmas%20Day%20Lunch%202026.pdf",
    "xmasveg": "6adb2ad1e17b9f611a338a5b_Canal-Christmas-Day-Vegetarian-Menu-2026.pdf",
    "brochure": "6ad898a9bf59357c47fdd13f_Canal-Xmas-Event-Brochure.pdf",
}
PDF_LOCAL = {"food": "food-menu.pdf", "wine": "wine-list.pdf", "bouillabaisse": "bouillabaisse.pdf",
             "group": "group-set-menu.pdf", "festive": "festive-menu-2026.pdf", "xmasday": "christmas-day-2026.pdf",
             "xmasveg": "christmas-day-veg-2026.pdf", "brochure": "xmas-event-brochure.pdf"}


def pdf(k):
    loc = "pdf/" + PDF_LOCAL[k]
    return loc if os.path.exists(os.path.join(OUT, loc)) else CDN + PDF_CDN[k]


# Stand-ins, in order of preference, for photos still to come from the current site
POOL = ["summer-spread.jpg", "xmas-1.jpg", "xmas-5.jpg", "xmas-6.jpg", "xmas-3.jpg", "xmas-2.jpg",
        "xmas-4.jpg", "xmas-7.jpg", "xmas-8.jpg"]
_used = {}


def img(name):
    """img/<name> if present, else a stand-in (stable per name)."""
    if os.path.exists(os.path.join(OUT, "img", name)):
        return "img/" + name
    if name not in _used:
        _used[name] = POOL[len(_used) % len(POOL)]
    return "img/" + _used[name]


def has(path):
    return os.path.exists(os.path.join(OUT, path))


ARR = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M2 8h11M9 4l4 4-4 4"/></svg>'
NAV = [("menus.html", "Menus"), ("festive.html", "Christmas"), ("groups.html", "Groups & events"), ("find-us.html", "Find us")]


def ph(name, alt, cls="", cap=""):
    c = f'<span class="cap">{cap}</span>' if cap else ""
    return f'<div class="ph {cls}"><img src="{img(name)}" alt="{alt}" loading="lazy">{c}</div>'


def reel(name, alt):
    return (f'<div class="ph r916"><video data-inview autoplay muted loop playsinline preload="metadata" poster="video/{name}-poster.jpg" '
            f'aria-label="{alt}"><source src="video/{name}.mp4" type="video/mp4"></video></div>')


def head(title, desc, slug, solid=False):
    og = img("og.jpg")
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="https://www.canalrestaurant.com/{slug}">
<meta property="og:type" content="website"><meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}"><meta property="og:image" content="https://www.canalrestaurant.com/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#F8B830">
<link rel="icon" href="img/logo-caramel.png">
<link rel="preload" href="fonts/GeigyLLSub-Medium.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="css/style.css?v=27">
<script type="application/ld+json">
{{"@context":"https://schema.org","@type":"Restaurant","name":"Canal","url":"https://www.canalrestaurant.com/",
"telephone":"+442081766073","email":"hello@canalrestaurant.com","servesCuisine":"Modern European","priceRange":"££",
"address":{{"@type":"PostalAddress","streetAddress":"11b Woodfield Road","addressLocality":"London","postalCode":"W9 2BA","addressCountry":"GB"}},
"openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],"opens":"12:00","closes":"22:00"}},
{{"@type":"OpeningHoursSpecification","dayOfWeek":"Sunday","opens":"12:00","closes":"20:30"}}],
"acceptsReservations":"{BOOK}","sameAs":["{INSTA}"]}}
</script>
</head>
<body{' class="solid-header"' if solid else ''}>
"""


def header(cur):
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == cur else ""}>{t}</a>' for h, t in NAV)
    mnav = "".join(f'<a class="big" href="{h}">{t}</a>' for h, t in NAV)
    return f"""<header class="header">
  <nav class="nav" aria-label="Main">{nav}</nav>
  <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span><span></span></button>
  <a class="logo" href="index.html" aria-label="Canal — home"></a>
  <div class="header-right">
    <a class="small" href="{GIFT}" target="_blank" rel="noopener">Gift vouchers</a>
    <a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book</a>
  </div>
</header>
<div class="menu">
  <a class="big" href="index.html">Home</a>{mnav}<a class="big" href="faq.html">FAQs</a>
  <div class="menu-foot">
    <a class="btn" href="{BOOK}" target="_blank" rel="noopener" style="align-self:flex-start">Book a table</a>
    <a href="{GIFT}" target="_blank" rel="noopener">Gift vouchers</a>
    <span>11b Woodfield Road, W9 2BA · 020 8176 6073</span>
  </div>
</div>
"""


FOOT = f"""<footer class="footer">
  <div class="wrap">
    <img class="big-logo" src="img/logo-white.png" alt="Canal">
    <span class="spaced">Westbourne Park</span>
    <div class="fgrid">
      <div><h4>Find us</h4><ul><li>Canal, Mason &amp; Fifth</li><li>11b Woodfield Road</li><li>Westbourne Park, London W9 2BA</li><li><a href="{MAPS}" target="_blank" rel="noopener">Directions →</a></li></ul></div>
      <div><h4>Open</h4><ul><li>Mon – Sat · 12pm – 10pm</li><li>Sunday · 12pm – 8.30pm</li><li>Bar &amp; terrace all day</li></ul></div>
      <div><h4>Say hello</h4><ul><li><a href="mailto:hello@canalrestaurant.com">hello@canalrestaurant.com</a></li><li><a href="tel:+442081766073">020 8176 6073</a></li><li><a href="{INSTA}" target="_blank" rel="noopener">@canal.canal.canal</a></li><li>Press: <a href="mailto:canal@crabcommunications.com">canal@crabcommunications.com</a></li></ul></div>
      <div><h4>More</h4><ul><li><a href="{BOOK}" target="_blank" rel="noopener">Book a table</a></li><li><a href="{GIFT}" target="_blank" rel="noopener">Gift vouchers</a></li><li><a href="groups.html">Private hire</a></li><li><a href="faq.html">FAQs &amp; terms</a></li><li><a href="mailto:careers@canalrestaurant.com">Careers</a></li></ul></div>
    </div>
    <div class="fbottom"><span>© Canal 2026</span><span>Splish, splash.</span></div>
  </div>
</footer>
<script src="js/config.js?v=7"></script>
<script src="js/site.js?v=9"></script>
<script src="js/live.js?v=7"></script>
<script src="js/ripple.js?v=7"></script>
<script src="js/menus.js?v=7"></script>
</body>
</html>
"""


def signup(bg="blush"):
    return f"""<section class="sec s {bg}">
  <div class="wrap grid2">
    <div class="rv"><span class="tag">Newsletter</span><h2 class="h2">News from the bargemen</h2></div>
    <div class="rv">
      <p class="body" style="margin-bottom:18px">New menus, supper clubs, summer parties and first dibs on Christmas. Not too often, promise.</p>
      <form class="signup"><label class="sr" for="em">Email</label><input id="em" type="email" placeholder="Your email" required><button class="btn" type="submit">Subscribe</button></form>
      <p class="msg" aria-live="polite"></p>
    </div>
  </div>
</section>
"""


def signoff(line="See you canal&#8209;side."):
    return f"""<section class="signoff">
  <h2 class="rv">{line}</h2>
  <div class="btns rv"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book a table {ARR}</a><a class="btn line" href="{GIFT}" target="_blank" rel="noopener">Gift vouchers</a></div>
</section>
"""


TICK_ITEMS = ["Splish, splash", "Always sunny canal-side", "Modern European", "South-facing terrace",
              "Dogs welcome", "Christmas Day lunch", "Bouillabaisse by the water"]
TICKER = '<div class="ticker" aria-hidden="true"><div class="t">' + \
    "".join(f"<span>{t}<i></i></span>" for t in TICK_ITEMS * 2) + "</div></div>"


def write(name, html):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(html)
    print("wrote", name)


def hero_media():
    if has("video/hero.mp4"):
        poster = "video/hero-poster.jpg" if has("video/hero-poster.jpg") else img("hero.jpg")
        return f'<video autoplay muted loop playsinline poster="{poster}"><source src="video/hero.mp4" type="video/mp4"></video>'
    return f'<img src="{img("hero.jpg")}" alt="A table of dishes at Canal">'


# ===================================================================== HOME
def vid(name, alt, cls="", loop=True):
    return (f'<div class="vid {cls}"><video data-inview autoplay muted {"loop " if loop else ""}playsinline preload="metadata" poster="video/{name}.jpg" '
            f'aria-label="{alt}"><source src="video/{name}.mp4" type="video/mp4"></video></div>')


def arch(name, alt, cap):
    return f'<figure class="small arch"><div class="ph"><img src="img/{name}" alt="{alt}" loading="lazy"></div></figure>'


h = head("Canal | Waterside Restaurant & Terrace, Westbourne Park",
         "Canal is a modern European restaurant on the Grand Union Canal at Westbourne Park, with a sun-soaked south-facing terrace, seasonal menus and cocktails by the water.", "")
h += header("index.html")
h += f"""
<section class="hero split">
  <div class="media">
    <video autoplay muted loop playsinline poster="video/v-wall-pasta.jpg" aria-label="A plate of pasta on the canal wall, the water moving behind"><source src="video/v-wall-pasta.mp4" type="video/mp4"></video>
    <video autoplay muted loop playsinline poster="video/v-terrace-man.jpg" aria-label="Lunch on the terrace beside the canal, seen from above"><source src="video/v-terrace-man.mp4" type="video/mp4"></video>
    <video class="m-only" autoplay muted loop playsinline poster="video/v-terrace-table.jpg" aria-label="A group at lunch on the terrace, seen from above"><source src="video/v-terrace-table.mp4" type="video/mp4"></video>
  </div>
  <div class="center">
    <img src="img/logo-white.png" alt="Canal">
    <span class="spaced">Westbourne Park</span>
  </div>
  <div class="foot">
    <div>
      <div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book a table {ARR}</a><a class="btn line" href="menus.html">Our menus</a></div>
    </div>
    <div class="live" data-live aria-live="polite"><span class="live-item">Mon – Sat 12 – 10pm</span><span class="live-item">Sun 12 – 8.30pm</span></div>
  </div>
</section>

<section class="intro-sec">
  <div class="wrap intro-grid">
    <div><p class="splish rv">Splish, splash</p>
    <p class="statement rv">A modern European restaurant on the water’s edge of the Grand Union Canal. Whatever the time of year, it’s <em>always sunny canal-side.</em></p></div>
    <div class="rv"><p class="body" style="margin-bottom:22px">A dining room and bar inside Mason &amp; Fifth, opening onto a south-facing terrace. Long lunches, a spritz after work, dinner as the water goes quiet.</p>
      <div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book a table {ARR}</a></div></div>
  </div>
</section>

<!-- Lunch / dinner / festive -->
<section class="sec s">
  <div class="wrap services swipe">
    <a class="rv" href="menus.html">{ph('plates-overhead-a.jpg', 'Lunch plates on the table at Canal')}<div class="row"><h3>Lunch</h3><span>From 12, every day</span></div><p>Plates for the table and a terrace in the sun.</p></a>
    <a class="rv" href="menus.html">{ph('table-schnitzel.jpg', 'Dinner at Canal with a glass of wine')}<div class="row"><h3>Dinner</h3><span>Until 10, Sun 8.30</span></div><p>Seasonal, modern European, mostly for sharing.</p></a>
    <a class="rv" href="menus.html#drinks">{ph('cocktails.jpg', 'Cocktails on the bar at Canal')}<div class="row"><h3>The bar &amp; terrace</h3><span>Walk in, all day</span></div><p>No booking needed for drinks. Cocktails, wine by the glass and snacks.</p></a>
  </div>
</section>

<!-- Menus -->
<section class="menu-reveal" data-reveal>
  <div class="wrap">
    <div class="top rv"><span>Sample menus</span><span>Changes through the week</span></div>
    <a class="mr-row rv" href="menus.html" data-img="img/wall-crudo.jpg"><span class="w">Food</span><span class="m">Lunch &amp; dinner, mostly for sharing</span><img class="thumb" src="img/wall-crudo.jpg" alt="">{ARR}</a>
    <a class="mr-row rv" href="menus.html#drinks" data-img="img/cocktails.jpg"><span class="w">Drinks</span><span class="m">Cocktails, beer &amp; wine by the glass</span><img class="thumb" src="img/cocktails.jpg" alt="">{ARR}</a>
    <a class="mr-row rv" href="festive.html" data-img="img/festive2.jpg"><span class="w">Christmas</span><span class="m">Festive sharing menu &amp; Christmas Day</span><img class="thumb" src="img/festive2.jpg" alt="">{ARR}</a>
  </div>
  <div class="mr-float" aria-hidden="true"><img alt=""></div>
</section>

<!-- What's on now -->
<section class="sec">
  <div class="wrap feat">
    <div class="txt rv">
      <span class="tag" style="color:var(--caramel)">Now booking</span>
      <h2>Christmas at Canal</h2>
      <p class="lead">Long lunches and parties by the water, through the festive season and on the day itself.</p>
      <ul class="facts">
        <li><span>Festive sharing menu</span><span>£68 pp</span></li>
        <li><span>Christmas Day lunch</span><span>£100 pp</span></li>
        <li><span>Book online</span><span>Up to 30</span></li>
        <li><span>Parties &amp; exclusive hire</span><span>Up to 150</span></li>
      </ul>
      <div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book</a><a class="btn line" href="festive.html">Christmas menus</a><a class="btn line" href="{ENQ}" target="_blank" rel="noopener">Party enquiries</a></div>
    </div>
    <div class="media rv">
      <div class="ph big"><img src="img/xmas-5.jpg" alt="Christmas Day lunch at Canal, roast duck in the middle of the table" loading="lazy"></div>
      {arch('archive-barge.jpg', 'Archive photograph of a woman with a mug on a working barge', 'Winter on the Grand Union.')}
    </div>
  </div>
</section>

<!-- Bouillabaisse -->
<section class="sec">
  <div class="wrap">
    <div class="ph rv" style="aspect-ratio:21/9"><img src="img/bouillabaisse.jpg" alt="Bouillabaisse served at the table" loading="lazy"></div>
    <div class="wide-txt rv">
      <h2>Bouillabaisse by the water</h2>
      <div><p class="lead">Inspired by Marseille, served in courses for the table. £75 per person, for groups of 6 or more.</p>
        <div class="btns"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Enquire</a><a class="btn line" href="menus.html#bouillabaisse">View menu</a></div></div>
    </div>
  </div>
</section>

<!-- Groups -->
<section class="sec">
  <div class="wrap feat flip">
    <div class="txt rv">
      <span class="tag">Groups &amp; private hire</span>
      <h2>Bring everyone</h2>
      <p class="lead">Big tables, part hire or the whole place, with a sharing menu built for a crowd.</p>
      <ul class="facts">
        <li><span>Group bookings</span><span>8 or more</span></li>
        <li><span>Exclusive hire, seated</span><span>Up to 70</span></li>
        <li><span>Exclusive hire, standing</span><span>Up to 120</span></li>
      </ul>
      <div class="btns"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Enquire</a><a class="btn line" href="groups.html">Groups &amp; events</a></div>
    </div>
    <div class="media rv">
      <div class="ph big land"><img src="img/spread-spring.jpg" alt="A long table of sharing plates" loading="lazy"></div>
      {arch('archive-fishermen.jpg', 'Archive photograph of three fishermen sitting together on deck', 'Table for a crowd.')}
    </div>
  </div>
</section>

<!-- Staff -->
<section class="sec s booked-band">
  <div class="wrap">
    <div class="booked rv"><h2>Have you booked yet?</h2><div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book a table {ARR}</a></div></div>
    <div class="team swipe rv">
      {vid('v-team-1', 'A member of the Canal team at lunch')}
      {vid('v-team-2', 'A member of the Canal team at lunch')}
      {vid('v-team-3', 'A member of the Canal team at lunch')}
      {vid('v-team-4', 'A member of the Canal team at lunch')}
    </div>
  </div>
</section>

<!-- Instagram -->
<section class="ig" aria-label="Canal on Instagram">
  <div class="wrap ig-head"><a href="{INSTA}" target="_blank" rel="noopener">@canal.canal.canal</a><span>Instagram</span></div>
  <div class="ig-track"><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/plate-logo.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/wall-crudo.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/mural.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/crudo.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/wall-toast.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/olives.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/schnitzel.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/archive-tub.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/wall-lemon.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/art-wall.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/crudo-plate.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/archive-swimmer.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/plate-logo.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/wall-crudo.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/mural.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/crudo.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/wall-toast.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/olives.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/schnitzel.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/archive-tub.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/wall-lemon.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/art-wall.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/crudo-plate.jpg" alt="" loading="lazy"></a><a href="{INSTA}" target="_blank" rel="noopener" tabindex="-1"><img src="img/archive-swimmer.jpg" alt="" loading="lazy"></a></div>
</section>

<!-- Find us -->
<section class="sec water">
  <div class="wrap feat">
    <div class="txt rv">
      <span class="tag">Find us</span>
      <p class="addr">Canal, Mason &amp; Fifth<br>11b Woodfield Road<br>Westbourne Park, W9 2BA</p>
      <ul class="hours"><li><span>Monday – Saturday</span><span>12pm – 10pm</span></li><li><span>Sunday</span><span>12pm – 8.30pm</span></li></ul>
      <p class="body" style="margin-top:22px">Two minutes from Westbourne Park station.<br>hello@canalrestaurant.com · 020 8176 6073</p>
      <div class="btns" style="margin-top:22px"><a class="btn white" href="{MAPS}" target="_blank" rel="noopener">Directions</a><a class="btn line" href="find-us.html">Getting here</a></div>
    </div>
    <div class="media rv">
      {vid('v-exterior', 'The Canal canopy over the terrace and the canal', 'big')}
    </div>
  </div>
</section>

{signup('')}
"""
h += FOOT
write("index.html", h)

# ===================================================================== SHARED (inner pages)
def page_hero(tag, title, media, split=False):
    return f"""<section class="phero{' split' if split else ''}">
  <div class="media">{media}</div>
  <div class="in"><span class="tag">{tag}</span><h1>{title}</h1></div>
</section>
"""


def hvid(name, alt, cls=""):
    return f'<video class="{cls}" autoplay muted loop playsinline poster="video/{name}.jpg" aria-label="{alt}"><source src="video/{name}.mp4" type="video/mp4"></video>'


def book_band(title="Have you booked yet?", label="Book a table", href=None, ext=True):
    href = href or BOOK
    t = ' target="_blank" rel="noopener"' if ext else ''
    return f"""<section class="sec s booked-band">
  <div class="wrap booked" style="margin-bottom:0"><h2 class="rv">{title}</h2><div class="btns rv"><a class="btn" href="{href}"{t}>{label} {ARR}</a></div></div>
</section>
"""


# ===================================================================== MENUS
m = head("Menus | Canal, Westbourne Park",
         "Canal's seasonal food menu and drinks list, plus bouillabaisse for groups of 6+ (£75pp). Modern European on the Grand Union Canal, Westbourne Park.", "menus")
m += header("menus.html")
m += f"""
<section class="phero short-hero">
  <div class="media"><img src="img/plates-overhead-b.jpg" alt="Plates on the table at Canal"></div>
  <div class="in"><span class="tag">Westbourne Park</span><h1>Our menus.</h1></div>
</section>

<section class="sec note-sec">
  <div class="wrap note-grid">
    <div id="menu" class="note-menu" data-menus="data/menu.csv">
      <p class="note-date">Sample menu</p>
      <div class="menu-tabs" role="tablist"></div>
      <div class="menu-body"></div>
      <p class="note-fine">v vegetarian // ve vegan<br>Discretionary 13.5% service // £1pp for unlimited filtered water<br>Please tell us about any allergies when you book.</p>
      <div class="btns" style="margin-top:28px"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book a table {ARR}</a></div>
    </div>
    <aside class="note-art" aria-hidden="true">
      <div class="ph a1"><img src="img/archive-fish.jpg" alt="" loading="lazy"></div>
      <div class="ph a2"><img src="img/archive-tub.jpg" alt="" loading="lazy"></div>
    </aside>
  </div>
</section>

<section class="sec note-sec bouill" id="bouillabaisse">
  <div class="wrap note-grid">
    <div class="note-menu">
      <h2 class="note-title">Bouillabaisse</h2>
      <ul class="note-lines">
        <li>Mussels escabeche</li><li>Fried olives, leek mayonnaise</li>
        <li class="gap">Bouillabaisse</li><li>Croutons, garlic, rouille &amp; gruyère</li>
        <li class="gap">Monkfish, gurnard, mussels &amp; clams</li>
        <li class="gap">Pink Fir potatoes</li><li>Greens</li>
        <li class="gap">Chocolate cremeux, olive oil &amp; sea salt</li>
      </ul>
      <p class="note-price">£75pp // groups of 6+</p>
      <div class="btns"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Enquire {ARR}</a></div>
    </div>
    <aside class="note-art single" aria-hidden="true">
      <div class="ph a1"><img src="img/archive-fishwife.jpg" alt="" loading="lazy"></div>
    </aside>
  </div>
</section>

<section class="sec s print-extras">
  <div class="print-wrap">
    <p class="dl">Download: <a href="{pdf('food')}" target="_blank" rel="noopener">Food</a> · <a href="{pdf('wine')}" target="_blank" rel="noopener">Wine list</a> · <a href="{pdf('group')}" target="_blank" rel="noopener">Group menu</a> · <a href="{pdf('bouillabaisse')}" target="_blank" rel="noopener">Bouillabaisse</a> · <a href="festive.html">Christmas</a></p>
  </div>
</section>
"""
m += book_band()
m += FOOT
write("menus.html", m)

# ===================================================================== FESTIVE
def xcard(media, big, label, line, cta_html, menu_html):
    return f"""<div class="xcard rv">
      <div class="xc-media">{media}<div class="xc-over"><span class="big-num">{big}</span><h3>{label}</h3></div></div>
      <p>{line}</p>
      <div class="btns">{cta_html}</div>
      <details class="see"><summary>See the menu</summary><div class="dishes one">{menu_html}</div></details>
    </div>"""


def choice(big, label, line, cta_html, menu_html):
    return f"""<div class="choice rv">
      <span class="big-num">{big}</span>
      <h3>{label}</h3>
      <p>{line}</p>
      <div class="btns">{cta_html}</div>
      <details class="see"><summary>See the menu</summary><div class="dishes one">{menu_html}</div></details>
    </div>"""


FEST_MENU = """<div><h4>For the table</h4><ul><li>Bread, brown butter</li><li>Todolí citrus &amp; radicchio salad</li><li>Shellfish cocktail</li><li>Hand-dived scallop, ’nduja butter, sea aster <small>+£15 each</small></li></ul>
<h4>One main for the table</h4><ul><li>Braised short rib, celeriac, roasted carrot, horseradish</li><li>Curried monkfish pie</li><li>Delica pumpkin risotto, chestnut &amp; Cashel Blue <small>v</small></li></ul>
<h4>Sides &amp; dessert</h4><ul><li>Fries · winter leaf salad</li><li>Brown butter cake, spiced poached pear, crème fraîche</li></ul></div>"""
XMAS_MENU = """<div><h4>To start</h4><ul><li>Forget de Brimont, Brut Terroir, Champagne</li><li>Soda bread &amp; brown butter</li><li>Smoked trout, crème fraîche, pickled fennel</li><li>Coombeshead Farm ham</li><li>Montgomery cheddar dumplings, Tunworth custard</li><li>Burrata, Todolí citrus, hazelnut, balsamic</li><li>Crudo, clementine, fennel</li></ul>
<h4>For the table</h4><ul><li>Roast duck, creamed Brussels sprouts, quince</li><li>Fried potato, duck fat, confit garlic</li><li>Steamed carrots, chervil butter</li></ul>
<h4>Dessert</h4><ul><li>Brown butter cake, spiced pear, crème fraîche</li></ul></div>"""
PARTY_MENU = """<div><h4>Sizes</h4><ul><li>Book online · up to 30</li><li>Seated · 50 – 70</li><li>Standing · up to 100</li><li>Standing, with the terrace · up to 150</li></ul>
<h4>Food</h4><ul><li>Seated parties: the festive sharing menu</li><li>Standing parties: bites and bowls</li></ul></div>"""

f = head("Christmas at Canal | Christmas Day Lunch & Festive Menu, Westbourne Park",
         "Christmas Day lunch (£100) and a £68 festive sharing menu at Canal on the Grand Union Canal. Christmas parties for up to 150 with the terrace.", "festive")
f += header("festive.html")
f += f"""
<section class="xmas-open">
  <div class="xo-vid"><video autoplay muted loop playsinline poster="video/xmas-edit-poster.jpg" aria-label="Christmas Day at Canal"><source src="video/xmas-edit.mp4" type="video/mp4"></video></div>
  <div class="xo-txt">
    <span class="tag" data-countdown>Christmas 2026</span>
    <h1>The best seat for Christmas is by the water.</h1>
    <p class="lead">Long lunches, roast duck for the table, and the whole place lit up for parties. A place to gather, a place to indulge.</p>
    <div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book Christmas {ARR}</a><a class="btn line" href="#choices">See the options</a></div>
  </div>
</section>

<section class="sec" id="choices">
  <div class="wrap">
    <div class="kicker rv"><h2>Three ways to do it</h2><p>Book up to 30 online. Bigger than that, talk to us.</p></div>
    <div class="xcards swipe">
      {xcard('<img src="img/festive2.jpg" alt="Curried monkfish pie, short rib, fries and winter leaves" loading="lazy">', '£68', 'Festive sharing menu',
             'Short rib or monkfish pie for the table, brown butter cake to finish. Lunch and dinner through December.',
             f'<a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book</a>', FEST_MENU)}
      {xcard('<img src="img/xmas-7.jpg" alt="Roast duck carved at the Christmas table" loading="lazy">', '£100', 'Christmas Day',
             'Champagne to start, plates to pass, roast duck in the middle. Nobody cooks, nobody washes up.',
             f'<a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book the 25th</a><a class="btn line" href="{pdf("xmasveg")}" target="_blank" rel="noopener">Vegetarian</a>', XMAS_MENU)}
      {xcard('<img src="img/bar.jpg" alt="The bar and dining room at Canal" loading="lazy">', '150', 'Parties for up to 150 guests',
             'Seated or standing, the whole place and the terrace, all lit up.',
             f'<a class="btn" href="{ENQ}" target="_blank" rel="noopener">Enquire</a><a class="btn line" href="{pdf("brochure")}" target="_blank" rel="noopener">Brochure</a>', PARTY_MENU)}
    </div>
  </div>
</section>

<section class="sec xstory">
  <div class="wrap">
    <div class="kicker rv"><h2>Christmas Day at Canal</h2><p>How the day goes.</p></div>

    <div class="xs-row rv">
      <div class="xs-txt"><span class="xs-n">Arrive</span><p class="xs-big">Come in off the towpath, and everything arrives at once.</p><p class="xs-small">A glass of Forget de Brimont Champagne, then soda bread and brown butter, smoked trout, Coombeshead Farm ham, Montgomery cheddar dumplings with Tunworth custard, and burrata with Todolí citrus. All for sharing.</p></div>
      <div class="xs-media">{vid('xmas-cheers-top', 'Glasses raised over Christmas lunch')}</div>
    </div>

    <div class="xs-row flip rv">
      <div class="xs-txt"><span class="xs-n">Stay a while</span><p class="xs-big">Roast duck at the table, then one more glass.</p><p class="xs-small">Duck with creamed sprouts and quince, potatoes fried in duck fat, brown butter cake to finish. There’s a full vegetarian menu too. Nobody cooks, nobody washes up.</p>
        <div class="btns" style="margin-top:22px"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book Christmas Day {ARR}</a></div></div>
      <div class="xs-media">{vid('xmas-gravy-top', 'Gravy poured over roast duck, then red wine on the table')}</div>
    </div>
  </div>
</section>

<section class="xmas-wide">
  <div class="vid"><video data-inview autoplay muted loop playsinline preload="metadata" poster="video/v-terrace-plates.jpg" aria-label="Plates arriving at a terrace table by the canal"><source src="video/v-terrace-plates.mp4" type="video/mp4"></video></div>
  <div class="xw-txt"><span class="tag">Christmas parties</span><p>The whole place, the water, the lights. Up to 70 seated or 150 standing with the terrace.</p><a class="btn white" href="{ENQ}" target="_blank" rel="noopener">Plan your party {ARR}</a></div>
</section>

<section class="sec s">
  <div class="wrap give rv">
    <div><span class="tag" style="color:var(--caramel)">Stuck for a present?</span><h2>Give Canal.</h2></div>
    <p class="lead">Digital gift vouchers for any amount, sent straight to their inbox.</p>
    <div class="btns"><a class="btn" href="{GIFT}" target="_blank" rel="noopener">Buy a gift voucher {ARR}</a></div>
  </div>
</section>
"""
f += book_band("Book Christmas")
f += FOOT
write("festive.html", f)

# ===================================================================== GROUPS
def fmt(img_html, num, label, line, guests):
    return f"""<a class="format rv" href="#enquire" data-guests="{guests}" data-occasion="{label}">
      {img_html}
      <div class="fmt-txt"><span class="big-num">{num}</span><h3>{label}</h3><p>{line}</p><span class="arrow">Enquire {ARR}</span></div>
    </a>"""


g = head("Groups, Private Hire & Events | Canal, Westbourne Park",
         "Private hire and group bookings at Canal on the Grand Union Canal: up to 70 seated or 120 standing, with a south-facing terrace.", "groups")
g += header("groups.html")
g += page_hero("Groups &amp; private hire", "Bring everyone.", hvid('v-terrace-drink', 'A guest raising a glass on the terrace'))
g += f"""
<section class="sec">
  <div class="wrap">
    <div class="kicker rv"><h2>Pick your format</h2><p>Up to 6 book online. For anything bigger, tell us the shape of it.</p></div>
    <div class="formats swipe">
      {fmt(ph('spread-spring.jpg', 'A long table of sharing plates'), '8+', 'A long table', 'A big table in the dining room or on the terrace, eating from the sharing set menu.', '8')}
      {fmt(ph('room-waiter.jpg', 'The dining room at Canal'), '70', 'Seated dinner', 'The whole dining room to yourselves — a long lunch or dinner, set up your way.', '40')}
      {fmt(ph('og.jpg', 'The terrace beside the canal'), '120', 'The whole place', 'Dining room, bar and terrace. Drinks, bites and bowls for a crowd.', '100')}
    </div>
  </div>
</section>

<section class="sec s occasions-sec">
  <div class="wrap">
    <span class="tag rv" style="color:var(--caramel)">What people book us for</span>
    <p class="occasions rv">Birthdays. Launches. Wedding lunches. Leaving drinks. Long Sundays. <em>Christmas parties.</em></p>
  </div>
</section>

<section class="sec s">
  <div class="wrap team swipe">
    {ph('chef-fish.jpg', 'A chef holding a whole fish over the canal')}
    {ph('logo-glass.jpg', 'The Canal logo on the glass by the bar')}
    {ph('wall-langoustine.jpg', 'Langoustines on the canal wall')}
    <div class="ph arch"><img src="img/archive-coracle.jpg" alt="Archive photograph of a man and two children in a small boat on the canal" loading="lazy"></div>
  </div>
</section>

<section class="sec" id="enquire">
  <div class="wrap grid2 top">
    <div class="rv">
      <span class="tag" style="color:var(--caramel)">Enquire</span>
      <h2 class="h2">Tell us what you’re planning.</h2>
      <p class="body">The quickest way is our events form — it goes straight to the team. Or fill this in and it opens an email to us.</p>
      <div class="btns" style="margin-top:22px"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Events form</a><a class="btn line" href="{pdf('group')}" target="_blank" rel="noopener">Group menu</a></div>
      <p class="body muted" style="margin-top:22px">hello@canalrestaurant.com · 020 8176 6073</p>
    </div>
    <form id="enquiry" class="form rv">
      <div class="field"><label for="f1">Name</label><input id="f1" name="name" required></div>
      <div class="field"><label for="f2">Email</label><input id="f2" name="email" type="email" required></div>
      <div class="field"><label for="f3">Phone</label><input id="f3" name="phone" type="tel"></div>
      <div class="field"><label for="f4">Guests</label><input id="f4" name="guests" type="number" min="8"></div>
      <div class="field"><label for="f5">Date</label><input id="f5" name="date" type="date"></div>
      <div class="field"><label for="f6">Occasion</label><select id="f6" name="type"><option>A long table</option><option>Seated dinner</option><option>The whole place</option><option>Birthday / celebration</option><option>Corporate</option><option>Launch / brand event</option><option>Wedding</option><option>Bouillabaisse</option><option>Christmas party</option><option>Other</option></select></div>
      <div class="field full"><label for="f7">Anything else</label><textarea id="f7" name="message"></textarea></div>
      <button class="btn" type="submit">Send enquiry</button>
      <p class="msg full" aria-live="polite"></p>
    </form>
  </div>
</section>
"""
g += book_band("Planning something?", "Enquire", "#enquire", ext=False)
g += FOOT
write("groups.html", g)

# ===================================================================== FIND US
fu = head("Find Us | Canal, 11b Woodfield Road, Westbourne Park W9",
          "Canal is at Mason & Fifth, 11b Woodfield Road, London W9 2BA, on the Grand Union Canal — two minutes from Westbourne Park station. Opening hours and directions.", "find-us")
fu += header("find-us.html")
fu += page_hero("Find us", "On the water at Westbourne Park.", '<img src="img/og.jpg" alt="A table on the terrace beside the canal">')
fu += f"""
<section class="sec water">
  <div class="wrap grid2">
    <div class="rv">
      <p class="addr">Canal, Mason &amp; Fifth<br>11b Woodfield Road<br>Westbourne Park, London W9 2BA</p>
      <ul class="hours"><li><span>Monday – Saturday</span><span>12pm – 10pm</span></li><li><span>Sunday</span><span>12pm – 8.30pm</span></li></ul>
      <div class="live on-light" data-live style="margin-top:18px"></div>
      <p class="body" style="margin-top:18px">hello@canalrestaurant.com · 020 8176 6073</p>
      <div class="btns" style="margin-top:22px"><a class="btn white" href="{MAPS}" target="_blank" rel="noopener">Open in Maps</a><a class="btn line" href="{BOOK}" target="_blank" rel="noopener">Book a table</a></div>
    </div>
    <div class="map rv"><iframe title="Map of Canal, 11b Woodfield Road, W9 2BA" loading="lazy" src="https://www.google.com/maps?q=11b+Woodfield+Road,+London+W9+2BA&output=embed"></iframe></div>
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="kicker rv"><h2>Getting here</h2><p>Two minutes from Westbourne Park station.</p></div>
    <div class="info rv">
      <div><h3>Tube</h3><p>Westbourne Park (Circle, Hammersmith &amp; City) is two minutes away. Royal Oak and Ladbroke Grove about ten.</p></div>
      <div><h3>Towpath</h3><p>Walk or cycle along the canal from Little Venice or Ladbroke Grove.</p></div>
      <div><h3>Just for a drink</h3><p>The bar and terrace are open all day. No booking needed.</p></div>
      <div><h3>Step-free</h3><p>Restaurant and terrace are step-free with accessible facilities. Just let us know what would help.</p></div>
      <div><h3>Dogs</h3><p>Welcome inside and out. Paws on the floor.</p></div>
      <div><h3>Little ones</h3><p>Very welcome. Children’s menu on request and high chairs if you mention them when booking.</p></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap feat flip">
    <div class="txt rv">
      <span class="tag" style="color:var(--caramel)">The terrace</span>
      <h2>South-facing, right on the water</h2>
      <p class="lead">Terrace tables book online. Part heated and part covered, so it works well beyond summer.</p>
      <div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book the terrace</a></div>
    </div>
    <div class="media rv">
      <div class="ph big land"><img src="img/window-table.jpg" alt="A table by the window onto the terrace" loading="lazy"></div>
      {arch('archive-narrowboat.jpg', 'Archive photograph of a narrowboat on the canal', '')}
    </div>
  </div>
</section>
"""
fu += signup('')
fu += FOOT
write("find-us.html", fu)

# ===================================================================== FAQ
faqs = [
    ("Visiting", [
        ("Do I need to book?", "We recommend it, especially for dinner and weekends, but we always keep space for walk-ins."),
        ("Can I just come for a drink?", "Of course. The bar and waterside terrace are open for drinks without a booking, with snacks all day."),
        ("Do you have outdoor seating?", "Yes — a south-facing terrace overlooking the Grand Union Canal. Terrace tables can be booked online. It’s part heated and part covered."),
        ("Are children welcome?", "Very. There’s a children’s menu on request, and we can set up high chairs if you mention them when booking."),
        ("Can I bring my dog?", "Yes, inside and out. Paws on the floor."),
        ("Is Canal accessible?", "Yes. The restaurant and terrace are step-free with accessible facilities. Let us know anything that would help."),
    ]),
    ("Bookings", [
        ("Can I change or cancel?", "Yes, through the link in your confirmation email. Any trouble, email or call us."),
        ("Is there a cancellation policy?", "Card details secure bookings and we ask for 24 hours’ notice. No-shows and late cancellations are charged at £40 per person for dinner and £20 per person for lunch."),
        ("Can I book for a group?", "Up to 6 online, in the dining room or on the terrace. For 8 or more, private hire and events, send us an enquiry."),
        ("Do you host private events?", "Yes, from big tables to exclusive hire: up to 70 seated or 120 standing."),
    ]),
    ("Food & drink", [
        ("Do you cater for dietary requirements?", "Yes — vegetarian, vegan, gluten-free and allergy-friendly options. Mention them when booking or tell your server."),
        ("Is there a service charge?", "A discretionary 13.5% service charge is added."),
        ("Corkage?", "£50 per 750ml bottle of wine, £75 per 750ml of sparkling. Bringing a cake is £5 per head."),
        ("Do you take cash?", "We’re cashless. All major cards, Apple Pay and Google Pay."),
        ("Gift vouchers?", "Yes — digital vouchers for any amount from our gift voucher shop."),
    ]),
]
fq = ""
for grp, qs in faqs:
    fq += f'<div class="faq-group rv"><h3>{grp}</h3><div class="faq">' + \
        "".join(f'<details><summary>{q}</summary><div class="a"><p>{a}</p></div></details>' for q, a in qs) + "</div></div>"

q = head("FAQs & Terms | Canal, Westbourne Park",
         "Bookings, cancellations, dogs, children, accessibility, dietary requirements, corkage and gift vouchers at Canal, Westbourne Park.", "faq", solid=True)
q += header("faq.html")
q += f"""
<section class="phero flat"><div class="in wrap" style="padding-left:var(--g)"><span class="tag">FAQs &amp; terms</span><h1>Good to know.</h1></div></section>
<section class="sec">
  <div class="wrap grid2 top">
    <div>{fq}</div>
    <div class="rv" style="position:sticky;top:110px">{ph('logo-glass.jpg', 'The Canal logo on the glass', 'r45')}
      <p class="body muted" style="margin-top:18px">Anything else? hello@canalrestaurant.com · 020 8176 6073</p></div>
  </div>
</section>
<section class="sec" id="terms" style="border-top:1px solid var(--line)">
  <div class="wrap legal">
    <span class="tag">The small print</span>
    <h3 id="bookings">Bookings</h3>
    <p>Bookings are for dining. Outdoor tables are part heated and part covered and subject to the weather. Card details secure bookings; late cancellations and no-shows are charged as set out above.</p>
    <h3 id="privacy">Privacy</h3>
    <p>When you book or sign up we collect your name, email, phone number and, where given, address. We don’t store card details or share your data beyond the booking and events platforms that run the restaurant. Email hello@canalrestaurant.com to see, correct or delete your data; we may need to verify your identity. Anything shared publicly on social media may stay visible there. We’ll post any changes to this policy here.</p>
    <h3 id="complaints">Complaints</h3>
    <p>We’d always rather hear it on the day. Otherwise email hello@canalrestaurant.com or write to Quality Restaurants Limited, MCA, One Canada Square, 9th Floor, London E14 5AA. We aim to propose a course of action within one working week.</p>
  </div>
</section>
"""
q += book_band()
q += FOOT
write("faq.html", q)

print("stand-ins used:", _used)
