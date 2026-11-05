"""Illustrated strip map of the Grand Union (Paddington Arm) around Canal."""

CANAL = "M-20,206 C120,176 220,236 360,206 S560,168 700,198 S930,236 1060,200 S1180,176 1240,190"
TOW = "M-20,170 C120,140 220,200 360,170 S560,132 700,162 S930,200 1060,164 S1180,140 1240,154"

MAP_SVG = f"""<svg class="canal-map" viewBox="0 0 1220 400" role="img" aria-labelledby="mapt mapd">
  <title id="mapt">Map: Canal on the Grand Union Canal</title>
  <desc id="mapd">Canal sits on the canal at Westbourne Park. Westbourne Park station is about 3 minutes' walk; Royal Oak about 10. Along the towpath, Ladbroke Grove is about 15 minutes west and Little Venice about 20 minutes east.</desc>
  <defs>
    <path id="canalpath" d="{CANAL}"/>
    <pattern id="ripples" width="46" height="14" patternUnits="userSpaceOnUse">
      <path d="M2 7c5-5 9-5 14 0s9 5 14 0" fill="none" stroke="#FAF7F0" stroke-opacity=".55" stroke-width="1.4" stroke-linecap="round"/>
    </pattern>
  </defs>

  <!-- land -->
  <rect width="1220" height="400" fill="#FFF3BD"/>
  <g fill="none" stroke="#A4601C" stroke-opacity=".18" stroke-width="1">
    <path d="M0 330 H1220 M0 92 H1220 M300 0 V400 M640 0 V400 M960 0 V400"/>
  </g>

  <!-- the canal -->
  <use href="#canalpath" fill="none" stroke="#6F9C9C" stroke-width="52" stroke-linecap="round"/>
  <use href="#canalpath" fill="none" stroke="url(#ripples)" stroke-width="40"/>
  <use href="#canalpath" class="flow" fill="none" stroke="#FAF7F0" stroke-opacity=".7" stroke-width="1.6" stroke-dasharray="2 22" stroke-linecap="round"/>
  <text font-size="13" letter-spacing="3" fill="#FAF7F0" opacity=".9"><textPath href="#canalpath" startOffset="62%" dy="4">GRAND UNION CANAL</textPath></text>

  <!-- towpath -->
  <path d="{TOW}" fill="none" stroke="#A4601C" stroke-width="2" stroke-dasharray="1 9" stroke-linecap="round"/>

  <!-- the boat -->
  <g class="boat">
    <g transform="translate(-26,-9)">
      <rect x="0" y="4" width="52" height="12" rx="3" fill="#C8372D"/>
      <rect x="10" y="0" width="30" height="7" rx="2" fill="#201B16"/>
      <rect x="13" y="2" width="5" height="3" fill="#FFF3BD"/><rect x="22" y="2" width="5" height="3" fill="#FFF3BD"/><rect x="31" y="2" width="5" height="3" fill="#FFF3BD"/>
    </g>
    <animateMotion dur="70s" repeatCount="indefinite" rotate="auto" keyPoints="0.08;0.92;0.08" keyTimes="0;0.5;1" calcMode="linear"><mpath href="#canalpath"/></animateMotion>
  </g>
  <!-- two ducks -->
  <g class="ducks" fill="#6B4A2B">
    <g transform="translate(560,196)"><ellipse rx="7" ry="4"/><circle cx="6" cy="-4" r="3"/></g>
    <g transform="translate(584,200)"><ellipse rx="7" ry="4"/><circle cx="6" cy="-4" r="3"/></g>
  </g>

  <!-- west: Ladbroke Grove -->
  <g transform="translate(70,188)">
    <circle r="7" fill="#201B16"/><circle r="3" fill="#FFF3BD"/>
    <text x="-12" y="-62" font-size="19" fill="#201B16">Ladbroke Grove</text>
    <text x="-12" y="-40" font-size="14" fill="#201B16" opacity=".7">≈15 min on the towpath</text>
  </g>

  <!-- east: Little Venice -->
  <g transform="translate(1150,186)">
    <circle r="7" fill="#201B16"/><circle r="3" fill="#FFF3BD"/>
    <text x="0" y="-60" text-anchor="end" font-size="19" fill="#201B16">Little Venice</text>
    <text x="0" y="-38" text-anchor="end" font-size="14" fill="#201B16" opacity=".7">≈20 min on the towpath</text>
  </g>

  <!-- stations (south of the canal) -->
  <g transform="translate(500,312)">
    <path d="M-14 -96 L0 -10" stroke="#201B16" stroke-width="1.5" stroke-dasharray="3 4"/>
    <rect x="-9" y="-9" width="18" height="18" rx="9" fill="#FAF7F0" stroke="#201B16" stroke-width="2.5"/>
    <text x="18" y="5" font-size="17" fill="#201B16">Westbourne Park station</text>
    <text x="18" y="27" font-size="14" fill="#201B16" opacity=".7">3 min walk</text>
  </g>
  <g transform="translate(860,322)">
    <rect x="-9" y="-9" width="18" height="18" rx="9" fill="#FAF7F0" stroke="#201B16" stroke-width="2.5"/>
    <text x="18" y="5" font-size="17" fill="#201B16">Royal Oak station</text>
    <text x="18" y="27" font-size="14" fill="#201B16" opacity=".7">≈10 min walk</text>
  </g>

  <!-- Canal -->
  <g transform="translate(424,176)">
    <path d="M0 0 C-22 -26 -30 -40 -30 -56 A30 30 0 0 1 30 -56 C30 -40 22 -26 0 0Z" fill="#A4601C"/>
    <circle cy="-56" r="12" fill="#FAF7F0"/>
    <image href="img/logo-caramel.png" x="52" y="-168" width="150" height="54"/>
    <text x="56" y="-96" font-size="15" fill="#201B16">11b Woodfield Road, W9 2BA</text>
    <text x="56" y="-75" font-size="14" fill="#201B16" opacity=".7">Arriving by boat? Tell us when you book.</text>
  </g>

  <text x="1200" y="388" text-anchor="end" font-size="11" fill="#201B16" opacity=".55"><tspan fill="#A4601C" font-size="16">···</tspan>  towpath  ·  not to scale  ·  walking times approximate</text>
</svg>"""
