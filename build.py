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
    return (f'<div class="ph r916"><video data-inview muted loop playsinline preload="none" poster="video/{name}-poster.jpg" '
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
<link rel="stylesheet" href="css/style.css">
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
<script src="js/config.js"></script>
<script src="js/site.js"></script>
<script src="js/live.js"></script>
<script src="js/ripple.js"></script>
<script src="js/menus.js"></script>
</body>
</html>
"""


def signup(bg="blush"):
    return f"""<section class="sec s {bg}">
  <div class="wrap grid2">
    <div class="rv"><span class="tag">Newsletter</span><h2 class="h2">Never miss a thing canal-side.</h2></div>
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
h = head("Canal | Waterside Restaurant & Terrace, Westbourne Park",
         "Canal is a modern European restaurant on the Grand Union Canal at Westbourne Park, with a sun-soaked south-facing terrace, seasonal menus and cocktails by the water.", "")
h += header("index.html")
h += f"""
<section class="hero">
  <div class="media ripple" data-ripple data-water="0.17,0.6" data-keep='[[0.43,0.32,0.545,0.63],[0.815,0.26,0.92,0.52],[0.03,0.44,0.405,0.66],[0.5,0.455,1.0,0.66]]'><img src="img/terrace.jpg" alt="A table set on the terrace beside the Grand Union Canal, a red narrowboat reflected in the water"></div>
  <div class="center">
    <img src="img/logo-white.png" alt="Canal">
    <span class="spaced">Westbourne Park</span>
  </div>
  <div class="foot">
    <div>
      <p style="margin-bottom:18px">A waterside restaurant led by the seasons.</p>
      <div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book a table {ARR}</a><a class="btn line" href="menus.html">Our menus</a></div>
    </div>
    <div class="live" data-live aria-live="polite"><span class="live-item">Mon – Sat 12 – 10pm</span><span class="live-item">Sun 12 – 8.30pm</span></div>
  </div>
</section>
{TICKER}

<section class="intro-sec">
  <div class="wrap intro-grid">
    <p class="statement rv">A modern European restaurant on the water’s edge of the Grand Union Canal. Whatever the time of year, it’s <em>always sunny canal-side.</em></p>
    <p class="body rv">A dining room and bar inside Mason &amp; Fifth, opening onto a south-facing terrace. Long lunches, a spritz after work, dinner as the water goes quiet. Walk in for drinks; book for food.</p>
  </div>
</section>

<section class="wide rv">
  {ph('og.jpg', 'A table on the terrace beside the Grand Union Canal')}
  <div class="caption"><span>The terrace</span><span>Grand Union Canal, W9</span></div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="three offset">
      <figure class="rv">{ph('spread.jpg', 'Sharing plates at lunch')}<figcaption><span>Lunch</span><span>From 12</span></figcaption></figure>
      <figure class="rv">{ph('cocktails.jpg', 'Cocktails at the bar')}<figcaption><span>The bar &amp; terrace</span><span>All afternoon</span></figcaption></figure>
      <figure class="rv">{ph('group.jpg', 'A full table at dinner')}<figcaption><span>Dinner</span><span>Until 10</span></figcaption></figure>
    </div>
  </div>
</section>

<section class="sec butter">
  <div class="wrap">
    <div class="grid2" style="margin-bottom:56px;align-items:end">
      <div class="rv"><span class="tag">What’s on</span><h2 class="h2">This season.</h2></div>
      <p class="body rv">Christmas by the water, a proper Marseille bouillabaisse, and room for the whole gang.</p>
    </div>
    <div class="whatson">
      <a class="rv" href="festive.html">{ph('festive2.jpg', 'Curried monkfish pie and short rib from the festive menu')}<span class="label">Booking now</span><h3>Christmas at Canal</h3><p>A £68 festive sharing menu, Christmas Day lunch, and parties for up to 150.</p></a>
      <a class="rv" href="menus.html#bouillabaisse">{ph('bouillabaisse.jpg', 'Bouillabaisse at Canal')}<span class="label">For the table</span><h3>Bouillabaisse</h3><p>Inspired by Marseille, served in courses. Enquire to reserve.</p></a>
      <a class="rv" href="groups.html">{ph('interior.jpg', 'The bar and wine wall at Canal')}<span class="label">Groups &amp; events</span><h3>Private hire</h3><p>Tables of 8 and up, or the whole place — 70 seated, 120 standing.</p></a>
    </div>
  </div>
</section>

<section class="sec ink-bg">
  <div class="wrap">
    <div class="grid2" style="margin-bottom:44px;align-items:end">
      <div class="rv"><span class="tag" style="color:var(--mustard)">Christmas Day 2026</span><h2 class="h2">Roast duck, passed plates, a glass of Champagne.</h2></div>
      <div class="rv"><p class="body muted" style="margin-bottom:22px">Christmas Day lunch at Canal: £100 a head, everything to share, the canal outside.</p>
        <div class="btns"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book Christmas Day</a><a class="btn line" href="festive.html#christmas-day">See the menu</a></div></div>
    </div>
    <div class="reels rv">
      {reel('xmas-edit', 'Christmas Day at Canal')}
      {ph('xmas-2.jpg', 'Christmas starters at Canal', 'r916')}
      {reel('xmas-duck', 'Roast duck carved at the table')}
      {ph('xmas-8.jpg', 'Carving the duck at the table', 'r916')}
    </div>
  </div>
</section>

<section class="sec water">
  <div class="wrap grid2">
    <div class="rv">
      <span class="tag">Find us</span>
      <p class="addr">Canal, Mason &amp; Fifth<br>11b Woodfield Road<br>Westbourne Park, W9 2BA</p>
      <ul class="hours"><li><span>Monday – Saturday</span><span>12pm – 10pm</span></li><li><span>Sunday</span><span>12pm – 8.30pm</span></li></ul>
      <p class="body" style="margin-top:22px">Two minutes from Westbourne Park station. Dogs welcome.</p>
      <div class="btns" style="margin-top:22px"><a class="btn white" href="{MAPS}" target="_blank" rel="noopener">Directions</a><a class="btn line" href="find-us.html">Getting here</a></div>
    </div>
    <div class="rv">{ph('art-wall.jpg', 'The dining room at Canal', 'r45')}</div>
  </div>
</section>

{signup('')}
{signoff()}
"""
h += FOOT
write("index.html", h)

# ===================================================================== MENUS
m = head("Menus | Canal, Westbourne Park",
         "Canal's seasonal food menu, wine and cocktail list (with A Bar with Shapes for a Name), bouillabaisse and group menus. Modern European on the Grand Union Canal.", "menus")
m += header("menus.html")
m += f"""
<section class="phero">
  <div class="media"><img src="{img('hero-poster.jpg')}" alt="Dishes on the table at Canal"></div>
  <div class="in"><span class="tag">Our menus</span><h1>Led by the seasons.</h1></div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap">
    <div class="grid2 top" style="margin-bottom:60px">
      <p class="statement rv" style="font-size:clamp(26px,3vw,44px)">Seasonal produce at its very best — crudo and shellfish when it’s warm, braises and pies when it isn’t. <em>Most things arrive for the table.</em></p>
      <p class="body muted rv">Menus change through the week, so these are the latest versions. Vegetarian, vegan and gluten-free options are always on. Tell us about allergies when you book. A discretionary 13.5% service charge is added.</p>
    </div>
    <div id="menu" class="menu-card rv" data-menus="data/menu.csv">
      <img class="card-logo" src="img/logo-ink.png" alt="Canal">
      <span class="card-sub spaced">Westbourne Park</span>
      <div class="menu-tabs" role="tablist"></div>
      <div class="menu-body"></div>
      <p class="fine" style="margin-top:8px">v vegetarian · ve vegan. Our menus change often — this is today’s. Discretionary 13.5% service; £1 per person for unlimited filtered water.</p>
    </div>
  </div>
</section>

<section class="sec s butter">
  <div class="wrap">
    <span class="tag rv">Take them with you</span>
    <div class="menus rv">
      <a class="mrow" href="{pdf('food')}" target="_blank" rel="noopener"><h3>Food menu</h3><p>Snacks, raw &amp; cured, plates for the table, desserts.</p><span class="arrow">View PDF</span></a>
      <a class="mrow" href="{pdf('wine')}" target="_blank" rel="noopener"><h3>Full wine list</h3><p>Every bottle, from Beaujolais to Margaux.</p><span class="arrow">View PDF</span></a>
      <a class="mrow" href="{pdf('bouillabaisse')}" target="_blank" rel="noopener"><h3>Bouillabaisse</h3><p>Marseille, by way of W9. For the table, booked ahead.</p><span class="arrow">View PDF</span></a>
      <a class="mrow" href="{pdf('group')}" target="_blank" rel="noopener"><h3>Group set menu</h3><p>Sharing menu for parties of 8 or more.</p><span class="arrow">View PDF</span></a>
      <a class="mrow" href="festive.html"><h3>Christmas</h3><p>£68 festive sharing menu and £100 Christmas Day lunch.</p><span class="arrow">See menus</span></a>
    </div>
  </div>
</section>

<div class="wave"></div>

<section class="sec butter" id="bouillabaisse">
  <div class="wrap grid2">
    <div class="rv">{ph('bouillabaisse.jpg', 'Bouillabaisse served at Canal', 'r45')}</div>
    <div class="rv">
      <span class="tag">Bouillabaisse by the water</span>
      <h2 class="h2">Southern France, Westbourne Park.</h2>
      <p class="body">Inspired by Marseille: a saffron broth, the day’s fish, rouille and toasted bread, served in courses and made for a long afternoon.</p>
      <p class="body">Prepared for the table and booked in advance — enquire and we’ll confirm your date.</p>
      <div class="btns" style="margin-top:26px"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Enquire now</a><a class="btn line" href="{pdf('bouillabaisse')}" target="_blank" rel="noopener">The menu</a></div>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap grid2 rev">
    <div class="rv">{ph('cocktails.jpg', 'Cocktails at the bar at Canal', 'r45')}</div>
    <div class="rv">
      <span class="tag" style="color:var(--caramel)">Drinks</span>
      <h2 class="h2">Just here for a spritz? Perfect.</h2>
      <p class="body">The bar and terrace don’t need a booking. Our drinks list is made with A Bar with Shapes for a Name — a dynamic balance of the classics and the progressive — plus wine by the glass and snacks all day.</p>
      <a class="arrow" style="margin-top:22px" href="{pdf('wine')}" target="_blank" rel="noopener">Drinks list {ARR}</a>
    </div>
  </div>
</section>
{signoff("Hungry yet?")}
"""
m += FOOT
write("menus.html", m)

# ===================================================================== FESTIVE
f = head("Christmas at Canal | Christmas Day Lunch & Festive Menu, Westbourne Park",
         "Christmas Day lunch (£100) and a £68 festive sharing menu at Canal on the Grand Union Canal. Christmas parties for up to 150 with the terrace.", "festive")
f += header("festive.html")
f += f"""
<section class="phero">
  <div class="media"><img src="img/xmas-5.jpg" alt="Christmas Day lunch table at Canal with roast duck"></div>
  <div class="in"><span class="tag">Christmas 2026</span><h1>Christmas at Canal.</h1>
    <div class="btns" style="margin-top:26px"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book a table</a><a class="btn line" href="{ENQ}" target="_blank" rel="noopener">Party enquiries</a></div></div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap grid2">
    <p class="statement rv">A place to gather, a place to indulge. Celebrate the festive season <em>by the water.</em></p>
    <p class="body muted rv">A sharing menu for tables of any size, a long Christmas Day lunch, and the whole place — terrace included — for parties. Up to 30 can book the festive menu straight in.</p>
  </div>
</section>

<section class="sec s ink-bg">
  <div class="wrap"><div class="reels rv">
    {ph('xmas-3.jpg', 'Roast duck with sides', 'r916')}
    {reel('xmas-cheers', 'Glasses raised at Christmas lunch')}
    {ph('xmas-4.jpg', 'The Christmas table from above', 'r916')}
    {reel('xmas-plates', 'Plates passed around the table')}
  </div></div>
</section>

<section class="sec butter" id="festive-menu">
  <div class="wrap grid2 top">
    <div class="rv">
      <span class="tag">Festive menu</span>
      <h2 class="h2">The sharing menu.</h2>
      <p class="price">£68<small>per person</small></p>
      <p class="body muted">For the whole table, with one main chosen in advance. Lunch and dinner through the festive season.</p>
      <div class="btns" style="margin-top:22px"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book (up to 30)</a><a class="btn line" href="{pdf('festive')}" target="_blank" rel="noopener">PDF</a></div>
      <div style="margin-top:36px">{ph('festive2.jpg', 'Curried monkfish pie, short rib, fries and winter leaves', 'r45')}</div>
    </div>
    <div class="dishes rv">
      <div>
        <h4>For the table</h4>
        <ul><li>Bread, brown butter</li><li>Todolí citrus &amp; radicchio salad</li><li>Shellfish cocktail</li><li>Hand-dived scallop, ’nduja butter, sea aster <small>+£15 each</small></li></ul>
        <h4>Sides</h4><ul><li>Fries</li><li>Winter leaf salad</li></ul>
      </div>
      <div>
        <h4>One main for the table</h4>
        <ul><li>Braised short rib, celeriac, roasted carrot, horseradish</li><li>Curried monkfish pie</li><li>Delica pumpkin risotto, chestnut &amp; Cashel Blue <small>v</small></li></ul>
        <h4>Dessert</h4><ul><li>Brown butter cake, spiced poached pear, crème fraîche</li></ul>
        <p class="fine">Discretionary 13.5% service. Please tell us about allergies.</p>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="christmas-day">
  <div class="wrap grid2 top">
    <div class="rv">
      <span class="tag" style="color:var(--caramel)">25 December</span>
      <h2 class="h2">Christmas Day lunch.</h2>
      <p class="price">£100<small>per person</small></p>
      <p class="body muted">Champagne to start, a table full of things to pass, and roast duck in the middle of it all. A full vegetarian menu too.</p>
      <div class="btns" style="margin-top:22px"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book Christmas Day</a><a class="btn line" href="{pdf('xmasday')}" target="_blank" rel="noopener">Menu</a><a class="btn line" href="{pdf('xmasveg')}" target="_blank" rel="noopener">Vegetarian</a></div>
      <div style="margin-top:36px">{ph('xmas-7.jpg', 'Roast duck being carved at the table', 'r45')}</div>
    </div>
    <div class="dishes rv">
      <div>
        <h4>To start</h4>
        <ul><li>Forget de Brimont, Brut Terroir, Champagne</li><li>Soda bread &amp; brown butter</li><li>Smoked trout, crème fraîche, pickled fennel</li><li>Coombeshead Farm ham</li><li>Montgomery cheddar dumplings, Tunworth custard</li><li>Burrata, Todolí citrus, hazelnut, balsamic</li><li>Crudo, clementine, fennel</li></ul>
      </div>
      <div>
        <h4>For the table</h4>
        <ul><li>Roast duck, creamed Brussels sprouts, quince</li><li>Fried potato, duck fat, confit garlic</li><li>Steamed carrots, chervil butter</li></ul>
        <h4>Dessert</h4><ul><li>Brown butter cake, spiced pear, crème fraîche</li></ul>
        <h4>Vegetarian</h4>
        <ul><li>Smoked beetroot, crème fraîche, pickled fennel</li><li>Winter tomato &amp; fennel salad, buckwheat</li><li>Roast celeriac, confit mushrooms, quince</li></ul>
        <p class="fine">Discretionary 13.5% service.</p>
      </div>
    </div>
  </div>
</section>

<div class="wave"></div>

<section class="sec blush" id="parties">
  <div class="wrap">
    <div class="grid2" style="margin-bottom:40px;align-items:end">
      <div class="rv"><span class="tag">Christmas parties</span><h2 class="h2">The whole place, the water, the lights.</h2></div>
      <p class="body rv">Seated parties eat the festive sharing menu. Standing parties get a rolling run of bites and bowls, plus the bar. The brochure has the detail.</p>
    </div>
    <div class="stats rv">
      <div><b>30</b><span>Book straight in</span></div>
      <div><b>50–70</b><span>Seated</span></div>
      <div><b>100</b><span>Standing</span></div>
      <div><b>150</b><span>With the terrace</span></div>
    </div>
    <div class="btns rv" style="margin-top:32px"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Enquire about a party</a><a class="btn line" href="{pdf('brochure')}" target="_blank" rel="noopener">Event brochure</a></div>
  </div>
</section>

<section class="sec s"><div class="wrap"><div class="gallery rv">
  {ph('xmas-1.jpg','Christmas lunch spread at Canal')}{ph('xmas-2.jpg','Christmas starters')}{ph('xmas-6.jpg','Roast duck, carrots and chard')}{ph('xmas-8.jpg','Carving the duck')}
</div></div></section>
{signoff("Merry Christmas, canal&#8209;side.")}
"""
f += FOOT
write("festive.html", f)

# ===================================================================== GROUPS
g = head("Groups, Private Hire & Events | Canal, Westbourne Park",
         "Private hire and group bookings at Canal on the Grand Union Canal: up to 70 seated or 120 standing, with a south-facing terrace.", "groups")
g += header("groups.html")
g += f"""
<section class="phero">
  <div class="media"><img src="{img('group.jpg')}" alt="Friends sharing a long table at Canal"></div>
  <div class="in"><span class="tag">Groups &amp; events</span><h1>Having a big party?</h1></div>
</section>
{TICKER}
<section class="sec">
  <div class="wrap grid2">
    <div class="rv">
      <p class="statement" style="margin-bottom:28px">A space just for you — <em>and everyone you like.</em></p>
      <p class="body">For tables over 8, private hire, events and catering. Dining room, bar and a south-facing terrace on the water, with room for up to 120 standing or 70 seated. Birthdays, brand dinners, launches, summer parties, a wedding lunch with the canal behind you.</p>
      <div class="btns" style="margin-top:26px"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Get in touch</a><a class="btn line" href="{pdf('group')}" target="_blank" rel="noopener">Group menu</a></div>
    </div>
    <div class="rv">{ph('spread.jpg', 'A table spread for a group at Canal', 'r45')}</div>
  </div>
</section>

<section class="sec blush">
  <div class="wrap">
    <span class="tag rv">How it works</span>
    <div class="info rv" style="margin:10px 0 48px">
      <div><h3>Big tables</h3><p>Up to 6 book online. From 8, send an enquiry and eat from the sharing set menu, chosen ahead so everyone eats together.</p></div>
      <div><h3>Part hire</h3><p>A stretch of the dining room or the terrace for 20–40, with Canal carrying on around you.</p></div>
      <div><h3>Exclusive hire</h3><p>The whole place: 70 seated, 120 standing, more on the terrace in summer. Set menus, bites, bowls and a bar built for a crowd.</p></div>
    </div>
    <div class="stats rv">
      <div><b>8+</b><span>Group bookings</span></div>
      <div><b>70</b><span>Seated</span></div>
      <div><b>120</b><span>Standing</span></div>
      <div><b>S</b><span>South-facing terrace</span></div>
    </div>
  </div>
</section>

<section class="sec butter" id="enquire">
  <div class="wrap grid2 top">
    <div class="rv">
      <span class="tag">Enquire</span>
      <h2 class="h2">Tell us what you’re planning.</h2>
      <p class="body">The quickest way is our events form — it goes straight to the team. Or fill in the short form and it’ll open an email to us.</p>
      <div class="btns" style="margin-top:22px"><a class="btn" href="{ENQ}" target="_blank" rel="noopener">Events form</a></div>
      <p class="body muted" style="margin-top:22px">hello@canalrestaurant.com · 020 8176 6073</p>
    </div>
    <form id="enquiry" class="form rv">
      <div class="field"><label for="f1">Name</label><input id="f1" name="name" required></div>
      <div class="field"><label for="f2">Email</label><input id="f2" name="email" type="email" required></div>
      <div class="field"><label for="f3">Phone</label><input id="f3" name="phone" type="tel"></div>
      <div class="field"><label for="f4">Guests</label><input id="f4" name="guests" type="number" min="8"></div>
      <div class="field"><label for="f5">Date</label><input id="f5" name="date" type="date"></div>
      <div class="field"><label for="f6">Occasion</label><select id="f6" name="type"><option>Birthday / celebration</option><option>Corporate</option><option>Drinks reception</option><option>Launch / brand event</option><option>Wedding</option><option>Bouillabaisse</option><option>Christmas party</option><option>Other</option></select></div>
      <div class="field full"><label for="f7">Anything else</label><textarea id="f7" name="message"></textarea></div>
      <button class="btn" type="submit">Send enquiry</button>
      <p class="msg full" aria-live="polite"></p>
    </form>
  </div>
</section>

<section class="sec s"><div class="wrap"><div class="gallery rv">
  {ph('terrace.jpg','The terrace set for a group')}{ph('olives.jpg','Olives at the bar')}{ph('mural.jpg','Dining table beneath the mural')}{ph('crudo.jpg','Sea bream crudo')}
</div></div></section>
{signoff("Let’s throw a party.")}
"""
g += FOOT
write("groups.html", g)

# ===================================================================== FIND US
fu = head("Find Us | Canal, 11b Woodfield Road, Westbourne Park W9",
          "Canal is at Mason & Fifth, 11b Woodfield Road, London W9 2BA, on the Grand Union Canal — two minutes from Westbourne Park station. Opening hours and directions.", "find-us")
fu += header("find-us.html")
fu += f"""
<section class="phero">
  <div class="media"><img src="{img('og.jpg')}" alt="Canal beside the Grand Union Canal"></div>
  <div class="in"><span class="tag">Find us</span><h1>On the water at Westbourne Park.</h1></div>
</section>
<section class="sec water">
  <div class="wrap grid2">
    <div class="rv">
      <p class="addr">Canal, Mason &amp; Fifth<br>11b Woodfield Road<br>Westbourne Park, London W9 2BA</p>
      <ul class="hours"><li><span>Monday – Saturday</span><span>12pm – 10pm</span></li><li><span>Sunday</span><span>12pm – 8.30pm</span></li></ul>
      <div class="live on-light" data-live style="margin-top:20px"></div>
      <p class="body" style="margin-top:18px">hello@canalrestaurant.com · 020 8176 6073</p>
      <div class="btns" style="margin-top:22px"><a class="btn white" href="{MAPS}" target="_blank" rel="noopener">Open in Maps</a><a class="btn line" href="{BOOK}" target="_blank" rel="noopener">Book a table</a></div>
    </div>
    <div class="map rv"><iframe title="Map of Canal, 11b Woodfield Road, W9 2BA" loading="lazy" src="https://www.google.com/maps?q=11b+Woodfield+Road,+London+W9+2BA&output=embed"></iframe></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <h2 class="h2 rv" style="margin-bottom:10px">Getting here.</h2>
    <p class="body muted rv" style="margin-bottom:44px">Two minutes from Westbourne Park station.</p>
    <div class="info rv">
      <div><h3>Tube</h3><p>Westbourne Park (Circle, Hammersmith &amp; City) is two minutes away. Royal Oak and Ladbroke Grove about ten.</p></div>
      <div><h3>Just for a drink</h3><p>The bar and terrace are open all day. No booking needed.</p></div>
      <div><h3>Towpath</h3><p>Walk or cycle along the canal from Little Venice (15 minutes) or Ladbroke Grove.</p></div>
      <div><h3>Step-free</h3><p>Restaurant and terrace are step-free with accessible facilities. Just let us know what would help.</p></div>
      <div><h3>Dogs</h3><p>Welcome inside and out. Paws on the floor.</p></div>
      <div><h3>Little ones</h3><p>Very welcome. Children’s menu on request and high chairs if you mention them when booking.</p></div>
    </div>
  </div>
</section>
<div class="wave"></div>
<section class="sec butter">
  <div class="wrap grid2 rev">
    <div class="rv">{ph('terrace.jpg', 'The south-facing terrace at Canal', 'r32')}</div>
    <div class="rv"><span class="tag">The terrace</span><h2 class="h2">South-facing. Right on the water.</h2>
      <p class="body">Terrace tables book online. Part heated and part covered, so it works well beyond summer. Drinks and snacks all day, no booking needed.</p>
      <div class="btns" style="margin-top:22px"><a class="btn" href="{BOOK}" target="_blank" rel="noopener">Book the terrace</a></div></div>
  </div>
</section>
{signup('blush')}
"""
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
<div class="wave"></div>
<section class="sec">
  <div class="wrap grid2 top">
    <div>{fq}</div>
    <div class="rv" style="position:sticky;top:110px">{ph('mural.jpg', 'The dining room at Canal', 'r45')}
      <p class="body muted" style="margin-top:18px">Anything else? hello@canalrestaurant.com · 020 8176 6073</p></div>
  </div>
</section>
<section class="sec butter" id="terms">
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
q += FOOT
write("faq.html", q)

print("stand-ins used:", _used)
