"""
Redraws Cosmic Clock's artwork: Sulekha's avatar (docs/sulekha.svg), the app icon
(docs/icon.svg + PNGs) and the Android launcher layers.
Needs:  pip install resvg-py        Run from the repository root:  python tools/make_art.py
"""
import math, os, random
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")
random.seed(5)

# ── palette taken from her photo ──────────────────────────────────────────────
SKIN_HI, SKIN, SKIN_MID, SKIN_SH = "#F7D6BC", "#E8BC9C", "#D9A887", "#BF8A6E"
HAIR_HI, HAIR = "#4A4150", "#121016"
FRAME, ACCENT = "#17131C", "#E0388A"

stars = "".join(f'<circle class="tw" style="animation-delay:{random.uniform(0,4):.1f}s" cx="{random.uniform(40,400):.0f}" '
                f'cy="{random.uniform(40,400):.0f}" r="{random.choice([0.8,1,1.3,1.7]):.1f}" fill="#FFFFFF" opacity=".85"/>' for _ in range(38))
ticks = []
for i in range(12):
    a = math.radians(i * 30)
    r1, r2 = (178, 196) if i % 3 == 0 else (186, 196)
    ticks.append(f'<line x1="{220 + r1*math.sin(a):.1f}" y1="{220 - r1*math.cos(a):.1f}" x2="{220 + r2*math.sin(a):.1f}" '
                 f'y2="{220 - r2*math.cos(a):.1f}" stroke="#FFE27A" stroke-width="{4 if i % 3 == 0 else 2.4}" stroke-linecap="round"/>')

def stitches(cx, cy, r, n, col):   # crochet texture: rings of little loops
    out = []
    for k in range(n):
        a = 2 * math.pi * k / n
        out.append(f'<ellipse cx="{cx + r*math.cos(a):.1f}" cy="{cy + r*math.sin(a):.1f}" rx="2.1" ry="1.3" '
                   f'transform="rotate({math.degrees(a)+90:.0f} {cx + r*math.cos(a):.1f} {cy + r*math.sin(a):.1f})" fill="none" stroke="{col}" stroke-width=".8" opacity=".75"/>')
    return "".join(out)

rose = f'''
  <g filter="url(#soft)">
    <ellipse cx="208" cy="394" rx="22" ry="10" transform="rotate(-24 208 394)" fill="url(#leaf)"/>
    <ellipse cx="272" cy="394" rx="22" ry="10" transform="rotate(22 272 394)" fill="url(#leaf)"/>
    <path d="M192 400 Q206 392 220 394 M288 400 Q274 392 260 394" stroke="#3E8F2F" stroke-width="1.4" fill="none"/>
    <circle cx="240" cy="380" r="29" fill="url(#petal)"/>
    {stitches(240, 380, 25, 28, "#7B5BB8")}
    <circle cx="240" cy="378" r="20" fill="url(#petal2)"/>
    {stitches(240, 378, 16, 20, "#6F4FAE")}
    <path d="M227 378 C229 366 251 364 253 376 C255 388 237 392 233 382 C231 374 245 370 247 378" fill="none" stroke="#5E3F9E" stroke-width="2.4" stroke-linecap="round"/>
    <circle cx="240" cy="377" r="5.4" fill="#8D6CCB"/>
    <ellipse cx="232" cy="365" rx="7" ry="3.5" fill="#FFFFFF" opacity=".35"/>
  </g>'''

avatar = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440" role="img" aria-labelledby="t d">
<title id="t">Sulekha Gupta</title>
<desc id="d">Illustrated 3D-style avatar of Sulekha: round face, black hair centre-parted and tied back, wide black rectangular glasses with a magenta accent, gentle smile, pink checked shirt, holding a lavender crochet rose, inside a glowing cosmic clock.</desc>
<style>
.tw{{animation:tw 3.2s ease-in-out infinite}} @keyframes tw{{0%,100%{{opacity:.15}}50%{{opacity:1}}}}
.minute{{transform-origin:220px 220px;animation:spin 60s linear infinite}} .hour{{transform-origin:220px 220px;animation:spin 720s linear infinite}}
@keyframes spin{{to{{transform:rotate(360deg)}}}}
.orbit{{transform-origin:220px 220px;animation:spin 24s linear infinite}}
.eyes{{transform-box:fill-box;transform-origin:center;animation:blink 5s infinite}} @keyframes blink{{0%,93%,100%{{transform:scaleY(1)}}95.5%{{transform:scaleY(.12)}}}}
.head{{transform-origin:222px 280px;animation:tilt 6s ease-in-out infinite}} @keyframes tilt{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-2.2deg)}}}}
.rose{{transform-origin:240px 400px;animation:bob 3.6s ease-in-out infinite}} @keyframes bob{{0%,100%{{transform:translateY(0) rotate(0)}}50%{{transform:translateY(-4px) rotate(6deg)}}}}
.float{{animation:fl 6s ease-in-out infinite}} .float.b{{animation-duration:8s;animation-direction:reverse}}
@keyframes fl{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-9px)}}}}
.ring{{animation:hue 10s linear infinite}} @keyframes hue{{to{{filter:hue-rotate(360deg)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<defs>
  <radialGradient id="space" cx="50%" cy="42%" r="62%"><stop offset="0" stop-color="#5A1E9C"/><stop offset=".55" stop-color="#2A0C5C"/><stop offset="1" stop-color="#12052B"/></radialGradient>
  <radialGradient id="neb1" cx="25%" cy="30%" r="40%"><stop offset="0" stop-color="#FF4FD8" stop-opacity=".55"/><stop offset="1" stop-color="#FF4FD8" stop-opacity="0"/></radialGradient>
  <radialGradient id="neb2" cx="78%" cy="70%" r="45%"><stop offset="0" stop-color="#22E4FF" stop-opacity=".45"/><stop offset="1" stop-color="#22E4FF" stop-opacity="0"/></radialGradient>
  <linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF4FD8"/><stop offset=".35" stop-color="#8B5CFF"/><stop offset=".7" stop-color="#22E4FF"/><stop offset="1" stop-color="#B6FF3B"/></linearGradient>
  <radialGradient id="face" cx="40%" cy="34%" r="72%"><stop offset="0" stop-color="{SKIN_HI}"/><stop offset=".45" stop-color="{SKIN}"/><stop offset=".78" stop-color="{SKIN_MID}"/><stop offset="1" stop-color="#AE785E"/></radialGradient>
  <radialGradient id="ear" cx="40%" cy="40%" r="70%"><stop offset="0" stop-color="{SKIN}"/><stop offset="1" stop-color="{SKIN_SH}"/></radialGradient>
  <linearGradient id="neck" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#B98166"/><stop offset=".45" stop-color="{SKIN_MID}"/><stop offset="1" stop-color="{SKIN}"/></linearGradient>
  <linearGradient id="hair" x1="0" y1="0" x2=".8" y2="1"><stop offset="0" stop-color="{HAIR_HI}"/><stop offset=".45" stop-color="#211C26"/><stop offset="1" stop-color="{HAIR}"/></linearGradient>
  <radialGradient id="petal" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#E6D6FF"/><stop offset=".6" stop-color="#BFA4F0"/><stop offset="1" stop-color="#8F6CD6"/></radialGradient>
  <radialGradient id="petal2" cx="40%" cy="35%" r="70%"><stop offset="0" stop-color="#D9C6FF"/><stop offset="1" stop-color="#A383E2"/></radialGradient>
  <linearGradient id="leaf" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9BEA6A"/><stop offset="1" stop-color="#3E9B2E"/></linearGradient>
  <linearGradient id="hand" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{SKIN_HI}"/><stop offset="1" stop-color="{SKIN_MID}"/></linearGradient>
  <pattern id="plaid" width="26" height="26" patternUnits="userSpaceOnUse" patternTransform="rotate(-4)">
    <rect width="26" height="26" fill="#F7DCE6"/>
    <rect x="0" width="7" height="26" fill="#E08AAA" opacity=".55"/><rect y="0" width="26" height="7" fill="#E08AAA" opacity=".5"/>
    <rect x="13" width="3" height="26" fill="#9B97AA" opacity=".55"/><rect y="13" width="26" height="3" fill="#9B97AA" opacity=".5"/>
    <rect x="19" width="2" height="26" fill="#FFFFFF" opacity=".8"/><rect y="19" width="26" height="2" fill="#FFFFFF" opacity=".8"/>
    <rect x="9" width="1" height="26" fill="#B4527A" opacity=".6"/><rect y="9" width="26" height="1" fill="#B4527A" opacity=".6"/>
  </pattern>
  <radialGradient id="shirtshade" cx="50%" cy="20%" r="85%"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#5A2346" stop-opacity=".45"/></radialGradient>
  <linearGradient id="glare" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".55"/><stop offset=".5" stop-color="#FFFFFF" stop-opacity=".05"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".3"/></linearGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#1B0638" flood-opacity=".45"/></filter>
  <filter id="blur2" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="2.2"/></filter>
  <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="5"/></filter>
  <clipPath id="disc"><circle cx="220" cy="220" r="200"/></clipPath>
</defs>

<!-- cosmic clock -->
<circle cx="220" cy="220" r="214" fill="none" stroke="url(#rim)" stroke-width="12" opacity=".75" filter="url(#glow)" class="ring"/>
<circle cx="220" cy="220" r="206" fill="none" stroke="url(#rim)" stroke-width="6" class="ring"/>
<circle cx="220" cy="220" r="200" fill="url(#space)"/>
<g clip-path="url(#disc)">
  <circle cx="220" cy="220" r="200" fill="url(#neb1)"/><circle cx="220" cy="220" r="200" fill="url(#neb2)"/>
  {stars}
  {"".join(ticks)}
  <g class="hour"><line x1="220" y1="220" x2="152" y2="150" stroke="#FFE27A" stroke-width="7" stroke-linecap="round" opacity=".9"/></g>
  <g class="minute"><line x1="220" y1="220" x2="306" y2="120" stroke="#FFF3B0" stroke-width="4.5" stroke-linecap="round" opacity=".9"/></g>
  <circle cx="220" cy="220" r="7" fill="#FFE27A"/>

  <!-- shirt -->
  <g filter="url(#soft)">
    <path d="M96 440C98 368 128 318 176 300L204 284L222 302L240 284L268 300C316 318 346 368 348 440Z" fill="url(#plaid)"/>
    <path d="M96 440C98 368 128 318 176 300L204 284L222 302L240 284L268 300C316 318 346 368 348 440Z" fill="url(#shirtshade)"/>
    <path d="M204 282L180 298L194 322L219 303Z" fill="url(#plaid)" stroke="#C26C8E" stroke-width="1.2" stroke-linejoin="round"/>
    <path d="M240 282L264 298L250 322L225 303Z" fill="url(#plaid)" stroke="#C26C8E" stroke-width="1.2" stroke-linejoin="round"/>
    <path d="M222 303V440" stroke="#C97A98" stroke-width="2.2"/>
    <circle cx="222" cy="326" r="2.8" fill="#FBE7EF" stroke="#B5668A"/>
    <rect x="154" y="344" width="40" height="34" rx="5" fill="url(#plaid)" stroke="#C26C8E" stroke-width="1.2"/>
    <path d="M154 352H194" stroke="#C26C8E" stroke-width="1.2"/><circle cx="174" cy="356" r="2.4" fill="#FBE7EF" stroke="#B5668A"/>
  </g>
</g>

<!-- neck and head (round full face, hair centre-parted and pulled back) -->
<path d="M203 252L241 252L243 304L201 304Z" fill="url(#neck)"/>
<g class="head" filter="url(#soft)">
  <path d="M140 198C132 120 170 64 222 64C274 64 312 120 304 198C300 180 294 164 286 154L158 154C150 164 144 180 140 198Z" fill="url(#hair)"/>
  <ellipse cx="148" cy="198" rx="10" ry="14" fill="url(#ear)"/><ellipse cx="151" cy="199" rx="5" ry="9" fill="{SKIN_SH}" opacity=".55"/>
  <ellipse cx="296" cy="198" rx="10" ry="14" fill="url(#ear)"/><ellipse cx="293" cy="199" rx="5" ry="9" fill="{SKIN_SH}" opacity=".55"/>
  <path d="M150 184C150 132 182 100 222 100C262 100 294 132 294 184C294 234 268 268 222 272C176 268 150 234 150 184Z" fill="url(#face)"/>
  <path d="M158 210C164 244 186 264 222 268" fill="none" stroke="#FFF1E6" stroke-width="2.6" opacity=".3" stroke-linecap="round"/>
  <path d="M286 206C282 240 262 262 230 268" fill="none" stroke="#9E6A52" stroke-width="5" opacity=".18" stroke-linecap="round" filter="url(#blur2)"/>
  <ellipse cx="212" cy="136" rx="26" ry="11" fill="#FFFFFF" opacity=".13"/>
  <!-- hairline: high arch from the parting, swept back over the ears -->
  <path d="M157 188C156 150 174 126 200 116Q210 112.5 218 112.5Q228 112.5 238 116C266 126 288 150 287 188C294 150 292 98 256 78C246 70 234 66 222 66C208 66 196 70 186 78C150 98 150 150 157 188Z" fill="url(#hair)"/>
  <path d="M160 184C162 150 180 128 202 119Q212 115.5 218 115.5Q228 115.5 238 119C262 128 282 150 284 184" fill="none" stroke="#8E5E4A" stroke-width="5" opacity=".28" filter="url(#blur2)"/>
  <path d="M218 112C216 98 214 82 213 68" stroke="#8C7C84" stroke-width="1.8" opacity=".85" fill="none"/>
  <path d="M212 82C194 88 176 104 166 132M226 82C246 88 264 104 276 132M206 94C190 102 180 116 174 136M232 94C248 102 260 116 268 136" stroke="#5A4E5C" stroke-width="1.3" opacity=".7" fill="none"/>
  <path d="M180 84C200 72 244 71 266 88" stroke="#FFFFFF" stroke-width="4" opacity=".17" fill="none" stroke-linecap="round"/>
  <path d="M157 176C150 186 147 198 150 210M287 176C294 184 297 196 295 208M162 150C154 158 150 168 151 178" stroke="{HAIR}" stroke-width="1.3" fill="none" opacity=".8"/>
  <!-- cheeks, brows, eyes -->
  <ellipse cx="184" cy="228" rx="16" ry="9" fill="#F08E86" opacity=".3"/><ellipse cx="260" cy="228" rx="16" ry="9" fill="#F08E86" opacity=".3"/>
  <ellipse cx="180" cy="216" rx="11" ry="6" fill="#FFFFFF" opacity=".17"/><ellipse cx="264" cy="216" rx="10" ry="5" fill="#FFFFFF" opacity=".11"/>
  <ellipse cx="192" cy="207" rx="20" ry="4" fill="#A9735C" opacity=".2" filter="url(#blur2)"/><ellipse cx="252" cy="207" rx="20" ry="4" fill="#A9735C" opacity=".2" filter="url(#blur2)"/>
  <path d="M172 161Q192 154 212 159" stroke="#2B1D1C" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <path d="M232 159Q252 154 272 161" stroke="#2B1D1C" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <g class="eyes">
    <path d="M181 184Q194 172 208 184Q194 192 181 184Z" fill="#FFFFFF"/><path d="M236 184Q250 172 263 184Q250 192 236 184Z" fill="#FFFFFF"/>
    <circle cx="194.5" cy="183.5" r="6.3" fill="#3A2318"/><circle cx="249.5" cy="183.5" r="6.3" fill="#3A2318"/>
    <circle cx="194.5" cy="183.5" r="3" fill="#0E0806"/><circle cx="249.5" cy="183.5" r="3" fill="#0E0806"/>
    <circle cx="196.6" cy="181.4" r="1.7" fill="#FFFFFF"/><circle cx="251.6" cy="181.4" r="1.7" fill="#FFFFFF"/>
    <path d="M180 183.5Q194 171 209 183.5M235 183.5Q250 171 264 183.5" stroke="#2B1A16" stroke-width="2.2" fill="none" stroke-linecap="round"/>
  </g>
  <!-- wide rectangular glasses, heavier top rim, magenta hinge accent -->
  <path d="M168 174H153M276 174H291" stroke="{FRAME}" stroke-width="3.6" stroke-linecap="round"/>
  <rect x="167" y="168" width="49" height="33" rx="7" fill="url(#glare)" fill-opacity=".25" stroke="{FRAME}" stroke-width="3.6"/>
  <rect x="228" y="168" width="49" height="33" rx="7" fill="url(#glare)" fill-opacity=".25" stroke="{FRAME}" stroke-width="3.6"/>
  <path d="M168 170Q191 164 215 169M229 169Q253 164 276 170" stroke="{FRAME}" stroke-width="5.6" fill="none" stroke-linecap="round"/>
  <path d="M216 177Q222 172 228 177" stroke="{FRAME}" stroke-width="3.2" fill="none"/>
  <path d="M271 168L278 171M166 171L173 168" stroke="{ACCENT}" stroke-width="3.2" stroke-linecap="round"/>
  <path d="M174 196L188 172M235 196L249 172" stroke="#FFFFFF" stroke-width="2.6" opacity=".33" stroke-linecap="round"/>
  <!-- broad rounded nose -->
  <path d="M222 196C220 208 216 216 216 222" stroke="#B57A60" stroke-width="2" fill="none" opacity=".55" stroke-linecap="round"/>
  <ellipse cx="212" cy="225" rx="5" ry="4" fill="#B57A60" opacity=".18"/><ellipse cx="233" cy="225" rx="5" ry="4" fill="#B57A60" opacity=".22"/>
  <ellipse cx="222" cy="222" rx="10" ry="7" fill="#F6D2B6" opacity=".6"/>
  <path d="M208 224Q211 232 218 231Q222 233 226 231Q233 232 236 224" stroke="#A86E57" stroke-width="2.1" fill="none" stroke-linecap="round"/>
  <!-- gentle closed smile -->
  <path d="M203 246Q222 257 241 246" stroke="#9E4C57" stroke-width="3.2" fill="none" stroke-linecap="round"/>
  <path d="M208 248Q222 258 236 248Q222 253 208 248Z" fill="#D2827E" opacity=".75"/>
  <path d="M210 244Q222 247 234 244" stroke="#C67B78" stroke-width="1.4" fill="none" opacity=".5"/>
  <path d="M202 244Q200 246.5 202.5 249M242 244Q244 246.5 241.5 249" stroke="#B5675E" stroke-width="1.4" fill="none" opacity=".6"/>
</g>

<!-- cupped hands holding her crochet rose -->
<g class="rose">
  <g filter="url(#soft)">
    <path d="M182 410C186 396 212 392 240 394C268 392 294 396 298 410C286 422 256 426 240 424C224 426 194 422 182 410Z" fill="url(#hand)"/>
    <ellipse cx="190" cy="400" rx="7" ry="12" transform="rotate(-30 190 400)" fill="url(#hand)"/>
    <ellipse cx="290" cy="400" rx="7" ry="12" transform="rotate(30 290 400)" fill="url(#hand)"/>
    <path d="M206 416Q212 420 220 420M260 420Q268 420 274 416M240 400V422" stroke="{SKIN_SH}" stroke-width="1.3" fill="none" opacity=".6"/>
  </g>
  {rose}
</g>

<!-- floating friends: telomere chromosome, ringed planet on an orbit, DNA -->
<g transform="translate(58 70)"><g class="float">
  <path d="M-12 -18L12 18M12 -18L-12 18" stroke="#8B5CFF" stroke-width="11" stroke-linecap="round"/>
  <circle cx="-12" cy="-18" r="6" fill="#B6FF3B"/><circle cx="12" cy="18" r="6" fill="#B6FF3B"/><circle cx="12" cy="-18" r="6" fill="#B6FF3B"/><circle cx="-12" cy="18" r="6" fill="#B6FF3B"/>
</g></g>
<g class="orbit"><g transform="translate(388 150)">
  <circle r="14" fill="#FF9F43"/><ellipse rx="24" ry="6" fill="none" stroke="#FFE27A" stroke-width="3" transform="rotate(-18)"/><circle cx="-4" cy="-5" r="4" fill="#FFFFFF" opacity=".4"/>
</g></g>
<g transform="translate(46 360)"><g class="float b">
  <path d="M-14 -22C14 -11 -14 11 14 22M14 -22C-14 -11 14 11 -14 22" stroke="#22E4FF" stroke-width="4" fill="none" stroke-linecap="round"/>
  <path d="M-6 -14H6M-7 0H7M-6 14H6" stroke="#FF4FD8" stroke-width="3" stroke-linecap="round"/>
</g></g>
</svg>'''
open(os.path.join(OUT, "sulekha.svg"), "w").write(avatar)

# ── app icon: a glowing clock in a nebula, hands at ten past ten, a planet in orbit ──
TICKS = [(54 + 22*math.sin(math.radians(a)), 54 - 22*math.cos(math.radians(a)), 54 + 27*math.sin(math.radians(a)), 54 - 27*math.cos(math.radians(a))) for a in (0, 90, 180, 270)]
def icon_fg(s, mono=False):
    f = lambda v: f"{v*s:.2f}"
    gold = "#FFFFFF" if mono else "#FFE27A"
    o = [f'<circle cx="{f(54)}" cy="{f(54)}" r="{f(29)}" fill="none" stroke="#FFFFFF" stroke-width="{f(4.4)}"/>']
    o += [f'<line x1="{f(a)}" y1="{f(b)}" x2="{f(c)}" y2="{f(d)}" stroke="{gold}" stroke-width="{f(3.2)}" stroke-linecap="round"/>' for a, b, c, d in TICKS]
    o.append(f'<line x1="{f(54)}" y1="{f(54)}" x2="{f(41)}" y2="{f(42)}" stroke="{gold}" stroke-width="{f(5)}" stroke-linecap="round"/>')
    o.append(f'<line x1="{f(54)}" y1="{f(54)}" x2="{f(67)}" y2="{f(37)}" stroke="#FFFFFF" stroke-width="{f(3.6)}" stroke-linecap="round"/>')
    o.append(f'<circle cx="{f(54)}" cy="{f(54)}" r="{f(3.4)}" fill="{gold}"/>')
    o.append(f'<circle cx="{f(80)}" cy="{f(72)}" r="{f(6)}" fill="{"#FFFFFF" if mono else "#B6FF3B"}"/>')
    o.append(f'<path d="M{f(30)} {f(26)}l{f(1.6)} {f(4)} {f(4)} {f(1.6)} {f(-4)} {f(1.6)} {f(-1.6)} {f(4)} {f(-1.6)} {f(-4)} {f(-4)} {f(-1.6)} {f(4)} {f(-1.6)}z" fill="#FFFFFF"/>')
    return "".join(o)
BG = ('<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#7A2CF5"/>'
      '<stop offset=".55" stop-color="#E23CC9"/><stop offset="1" stop-color="#FF8A3D"/></linearGradient></defs>')
icon = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{BG}<rect width="512" height="512" rx="116" fill="url(#g)"/>{icon_fg(512/108)}</svg>'
mask = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{BG}<rect width="512" height="512" fill="url(#g)"/>{icon_fg(512/108)}</svg>'
open(os.path.join(OUT, "icon.svg"), "w").write(icon)

import resvg_py
def png(svg, size, path):
    open(path, "wb").write(bytes(resvg_py.svg_to_bytes(svg_string=svg, width=size, height=size)))
png(icon, 192, f"{OUT}/icon-192.png"); png(icon, 512, f"{OUT}/icon-512.png")
png(mask, 512, f"{OUT}/icon-maskable-512.png"); png(mask, 180, f"{OUT}/apple-touch-icon.png")
if os.environ.get("PREVIEW"):
    png(avatar, 880, os.environ["PREVIEW"])

def cpath(cx, cy, r):
    return f"M{cx-r:.2f},{cy:.2f}a{r:.2f},{r:.2f} 0 1,0 {2*r:.2f},0a{r:.2f},{r:.2f} 0 1,0 {-2*r:.2f},0"
def vector(mono):
    gold = "#FFFFFF" if mono else "#FFE27A"
    p = ['<?xml version="1.0" encoding="utf-8"?>',
         '<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">',
         f'  <path android:strokeColor="#FFFFFF" android:strokeWidth="4.4" android:fillColor="#00000000" android:pathData="{cpath(54, 54, 29)}"/>']
    for a, b, c, d in TICKS:
        p.append(f'  <path android:strokeColor="{gold}" android:strokeWidth="3.2" android:strokeLineCap="round" android:pathData="M{a:.2f},{b:.2f}L{c:.2f},{d:.2f}"/>')
    p.append(f'  <path android:strokeColor="{gold}" android:strokeWidth="5" android:strokeLineCap="round" android:pathData="M54,54L41,42"/>')
    p.append('  <path android:strokeColor="#FFFFFF" android:strokeWidth="3.6" android:strokeLineCap="round" android:pathData="M54,54L67,37"/>')
    p.append(f'  <path android:fillColor="{gold}" android:pathData="{cpath(54, 54, 3.4)}"/>')
    p.append(f'  <path android:fillColor="{"#FFFFFF" if mono else "#B6FF3B"}" android:pathData="{cpath(80, 72, 6)}"/>')
    p.append('  <path android:fillColor="#FFFFFF" android:pathData="M30,26l1.6,4 4,1.6 -4,1.6 -1.6,4 -1.6,-4 -4,-1.6 4,-1.6z"/>')
    p.append('</vector>')
    return "\n".join(p) + "\n"
res = os.path.join(ROOT, "android", "app", "src", "main", "res", "drawable")
os.makedirs(res, exist_ok=True)
open(os.path.join(res, "ic_launcher_foreground.xml"), "w").write(vector(False))
open(os.path.join(res, "ic_launcher_monochrome.xml"), "w").write(vector(True))
print("art written")
