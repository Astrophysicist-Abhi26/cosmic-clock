/* Cosmic Clock background: a fresh patch of sky on every visit.
   Twinkling stars, shooting comets and floating cartoon friends from Sulekha's world —
   telomere-capped chromosomes, DNA, mitochondria, senescent cells, ringed planets, rockets,
   astronauts, clocks and her crochet rose — plus fun facts from her newsletter. Motifs are
   weighted by the ranking profile's interests. Static when the reader prefers reduced motion. */
(function () {
  "use strict";
  const NS = "http://www.w3.org/2000/svg";
  const COLS = ["#ff4fd8", "#a77bff", "#22e4ff", "#b6ff3b", "#ffd23f", "#ff9f43"];
  const MOTIFS = {
    chromosome: (c) => `<path d="M-10-16L10 16M10-16L-10 16" stroke="${c}" stroke-width="8" stroke-linecap="round"/><circle cx="-10" cy="-16" r="4.5" fill="#ffd23f"/><circle cx="10" cy="16" r="4.5" fill="#ffd23f"/><circle cx="10" cy="-16" r="4.5" fill="#ffd23f"/><circle cx="-10" cy="16" r="4.5" fill="#ffd23f"/>`,
    dna: (c) => `<path d="M-10-24C12-12-12 12 10 24M10-24C-12-12 12 12-10 24" stroke="${c}" stroke-width="3" fill="none"/><path d="M-5-15H5M-6 0H6M-5 15H5" stroke="#fff" stroke-width="2" opacity=".7"/>`,
    mito: (c) => `<ellipse rx="22" ry="12" fill="none" stroke="${c}" stroke-width="3"/><path d="M-14 0q4-8 8 0t8 0 8 0" stroke="${c}" stroke-width="2" fill="none"/>`,
    cell: (c) => `<circle r="20" fill="${c}" opacity=".18" stroke="${c}" stroke-width="2.5"/><circle cx="4" cy="-3" r="7" fill="${c}" opacity=".7"/><circle cx="-9" cy="8" r="2.5" fill="#22e4ff"/><circle cx="10" cy="10" r="2" fill="#22e4ff"/>`,
    bacterium: (c) => `<rect x="-18" y="-8" width="36" height="16" rx="8" fill="${c}" opacity=".25" stroke="${c}" stroke-width="2.5"/><path d="M18 0q8-6 14 2" stroke="${c}" stroke-width="2" fill="none"/>`,
    planet: (c) => `<circle r="13" fill="${c}"/><ellipse rx="24" ry="6" fill="none" stroke="#ffd23f" stroke-width="2.5" transform="rotate(-20)"/><circle cx="-4" cy="-5" r="3.5" fill="#fff" opacity=".35"/>`,
    rocket: (c) => `<path d="M0-22C9-12 9 6 6 14H-6C-9 6-9-12 0-22Z" fill="#fff"/><circle cy="-6" r="4" fill="${c}"/><path d="M-6 8L-13 16-6 14M6 8L13 16 6 14" fill="${c}"/><path d="M-4 16L0 26 4 16Z" fill="#ff9f43"/>`,
    clock: (c) => `<circle r="18" fill="none" stroke="${c}" stroke-width="3"/><path d="M0 0V-11M0 0L8 5" stroke="#fff" stroke-width="2.5" stroke-linecap="round"/>`,
    rose: () => `<circle r="12" fill="#bfa4f0"/><path d="M-6 0c1-6 11-7 12-1s-8 8-10 3 6-6 7-1" stroke="#7b5bb8" stroke-width="2" fill="none"/><ellipse cx="-12" cy="9" rx="8" ry="4" fill="#6cc24a" transform="rotate(-25 -12 9)"/><ellipse cx="12" cy="9" rx="8" ry="4" fill="#6cc24a" transform="rotate(25 12 9)"/>`,
    astronaut: (c) => `<circle cy="-10" r="10" fill="#fff"/><rect x="-6" y="-14" width="12" height="7" rx="3" fill="${c}"/><rect x="-9" y="0" width="18" height="16" rx="6" fill="#fff"/><path d="M-9 4L-16 10M9 4L16 -2" stroke="#fff" stroke-width="5" stroke-linecap="round"/>`,
    star4: (c) => `<path d="M0-12L3-3 12 0 3 3 0 12-3 3-12 0-3-3Z" fill="${c}"/>`,
  };
  const FACTS = ["On the ISS the Sun rises 16 times a day", "Telomeres grew longer in space — then shrank back on Earth",
    "Microgravity: up to 1–2% bone loss a month", "Hot Jupiters keep their stars acting young",
    "Biological age can fall after pregnancy", "SA-β-gal turns senescent cells blue", "Ageing is a state of stress, not just a number"];
  let svg = null;
  const rnd = (a, b) => a + Math.random() * (b - a);
  function pick(weights) {
    const tot = weights.reduce((s, [, w]) => s + w, 0);
    let r = Math.random() * tot;
    for (const [k, w] of weights) { if ((r -= w) <= 0) return k; }
    return weights[0][0];
  }
  function render(opts) {
    const host = document.getElementById("bg");
    if (!host) return;
    const weight = (opts && opts.weight) || (() => 50);
    const still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const W = 1600, H = 1000;
    const mol = weight("molbio") || 30, mic = weight("micro") || 10;
    const choices = [["chromosome", 10 + mol / 6], ["dna", 8 + mol / 8], ["mito", 6 + mol / 10], ["cell", 8 + mol / 8], ["bacterium", 2 + mic / 8],
      ["planet", 12], ["rocket", 7], ["clock", 9], ["rose", 6], ["astronaut", 5], ["star4", 10]];
    let out = `<style>
      .tw{animation:tw 3s ease-in-out infinite}@keyframes tw{0%,100%{opacity:.15}50%{opacity:1}}
      .dr{animation:dr var(--d) ease-in-out infinite alternate}@keyframes dr{to{transform:translate(var(--x),var(--y)) rotate(var(--r))}}
      .cm{animation:cm var(--d) linear infinite}@keyframes cm{0%{transform:translate(0,0);opacity:0}5%{opacity:1}30%{transform:translate(-900px,520px);opacity:0}100%{opacity:0}}
      .ft{font:700 14px Nunito,system-ui,sans-serif;fill:currentColor;opacity:.3}
      ${still ? "*{animation:none!important}" : ""}</style>`;
    for (let i = 0; i < 110; i++) {
      out += `<circle class="tw" style="animation-delay:${rnd(0, 4).toFixed(1)}s" cx="${rnd(0, W).toFixed(0)}" cy="${rnd(0, H).toFixed(0)}" r="${rnd(.6, 2).toFixed(1)}" fill="${Math.random() < .8 ? "#fff" : COLS[i % 6]}"/>`;
    }
    for (let i = 0; i < 4; i++) {
      out += `<g class="cm" style="--d:${rnd(9, 16).toFixed(0)}s;animation-delay:${rnd(0, 12).toFixed(1)}s"><path d="M${rnd(900, 1600).toFixed(0)} ${rnd(-40, 300).toFixed(0)}l60 -34" stroke="#fff" stroke-width="2.5" stroke-linecap="round" opacity=".9"/></g>`;
    }
    for (let i = 0; i < 26; i++) {
      const m = pick(choices), c = COLS[(Math.random() * COLS.length) | 0];
      const x = rnd(30, W - 30), y = rnd(30, H - 30), s = rnd(.8, 1.8), r = rnd(-30, 30);
      out += `<g transform="translate(${x.toFixed(0)} ${y.toFixed(0)}) scale(${s.toFixed(2)})"><g class="dr" style="--d:${rnd(6, 14).toFixed(1)}s;--x:${rnd(-40, 40).toFixed(0)}px;--y:${rnd(-40, 40).toFixed(0)}px;--r:${r.toFixed(0)}deg">${MOTIFS[m](c)}</g></g>`;
    }
    const facts = FACTS.slice().sort(() => Math.random() - .5).slice(0, 3);
    facts.forEach((f, i) => {
      out += `<text class="ft" x="${rnd(60, W - 520).toFixed(0)}" y="${(260 + i * 270 + rnd(-40, 40)).toFixed(0)}">✦ ${f}</text>`;
    });
    if (!svg) { svg = document.createElementNS(NS, "svg"); svg.setAttribute("preserveAspectRatio", "xMidYMid slice"); host.appendChild(svg); }
    svg.setAttribute("viewBox", `0 0 ${W} ${H}`);
    svg.innerHTML = out;
    host.dataset.motifs = String(svg.querySelectorAll(".dr").length);
  }
  window.PPBackground = { render };
})();
