// Clicks through the whole site in a headless DOM and fails on any script error.
//   npm install jsdom@24
//   python scraper/scrape.py --offline --out /tmp/jobs.json
//   node tests/ui/ui_smoke.js /tmp/jobs.json
const fs = require("fs"), path = require("path");
const { JSDOM, VirtualConsole } = require("jsdom");
const DOCS = path.join(__dirname, "..", "..", "docs");
const data = JSON.parse(fs.readFileSync(process.argv[2] || path.join(DOCS, "jobs.json"), "utf8"));
const errors = [];
const vc = new VirtualConsole();
// jsdom has no navigation and no canvas drawing; the confetti simply skips itself there
vc.on("jsdomError", (e) => { if (!/Not implemented: (navigation|HTMLCanvasElement)/.test(e.message)) errors.push("jsdomError: " + e.message); });
vc.on("error", (e) => errors.push("console.error: " + e));
const html = fs.readFileSync(path.join(DOCS, "index.html"), "utf8").replace(/<script src="[^"]+"><\/script>/g, "");
const dom = new JSDOM(html, { url: "https://example.org/cosmic-clock/", runScripts: "outside-only", pretendToBeVisual: true, virtualConsole: vc });
const w = dom.window, d = w.document;
w.fetch = async () => ({ ok: true, json: async () => JSON.parse(JSON.stringify(data)) });
w.eval(fs.readFileSync(path.join(DOCS, "score.js"), "utf8"));
w.eval(fs.readFileSync(path.join(DOCS, "bg.js"), "utf8"));
w.eval(fs.readFileSync(path.join(DOCS, "app.js"), "utf8"));
const tick = () => new Promise((r) => setTimeout(r, 30));
const check = (cond, msg) => { if (!cond) { errors.push("FAIL: " + msg); } else console.log("  ok  " + msg); };
const cards = () => [...d.querySelectorAll("#list article.job")];
const job = (el) => data.jobs.find((j) => j.id === el.dataset.id);
const click = (el) => el.dispatchEvent(new w.MouseEvent("click", { bubbles: true }));
const change = (el) => el.dispatchEvent(new w.Event("change", { bubbles: true }));
const tab = async (t) => { click(d.querySelector(`.tabs [data-tab="${t}"]`)); await tick(); };
const reset = async () => { click(d.querySelector('#filters [data-act="reset"]')); await tick(); };
(async () => {
  await tick(); await tick();
  // ── PhD positions (default tab) ──
  const n0 = cards().length;
  check(n0 >= 3 && cards().every((c) => ["phd", "fellowship"].includes(job(c).kind)), `PhD tab shows only PhD positions and fellowships (${n0})`);
  check(/cellular senescence/.test(cards()[0].querySelector("h3").textContent), "top PhD is the senescence and matrix-ageing project");
  check(/Sample data/.test(d.querySelector("#status").textContent), "sample banner shown for offline data");
  check(d.querySelector("#profile").options.length === data.profiles.list.length, "profile picker lists all profiles");
  check(/Sulekha/.test(d.querySelector("#hello").textContent), "hero greets Sulekha");
  check(/The clock shows \d+ PhD positions? \(\d+ in Europe\), \d+ internships?/.test(d.querySelector("#today").textContent), "hero summarises PhDs, internships and jobs");
  check(d.querySelectorAll("#bg svg g").length > 20 && Number(d.querySelector("#bg").dataset.motifs) > 10, "cosmic background drawn with floating motifs");
  const ageDisc = d.querySelector('#discs [data-preset="ageing"]');
  check(!!ageDisc, "quick-search chips rendered");
  click(ageDisc); await tick();
  check(cards().length > 0 && w.location.search.includes("sub=") && ageDisc.getAttribute("aria-pressed") === "true", `ageing chip filters the list (${cards().length})`);
  await reset();
  check(cards().length === n0, "reset restores everything");
  const q = d.querySelector("#q"); q.value = "senescence"; q.dispatchEvent(new w.Event("input", { bubbles: true })); await new Promise((r) => setTimeout(r, 250));
  check(cards().length >= 1 && cards().every((c) => /senescen/i.test(c.textContent)), `search "senescence" (${cards().length})`);
  q.value = ""; q.dispatchEvent(new w.Event("input", { bubbles: true })); await new Promise((r) => setTimeout(r, 250));
  const chip = cards()[0].querySelector(".chip"); const sub = chip.dataset.sub; click(chip); await tick();
  check(cards().length > 0 && w.location.search.includes("sub=" + sub), `topic chip filters to ${sub} (${cards().length})`);
  await reset();
  check(/Ageing, senescence & longevity/.test(cards()[0].querySelector(".why").textContent), "score explanation lists the reasons");
  const first = cards()[0]; const id = first.dataset.id;
  click(first.querySelector('[data-act="track"]')); await tick();
  check(d.querySelector("#tcount").textContent === "1", "tracking updates the tab count (with confetti)");
  check(JSON.parse(w.localStorage.getItem("lh.tracker"))[id].status === "saved", "tracker saved in localStorage");
  const second = cards()[1]; const hid = second.dataset.id;
  click(second.querySelector('[data-act="hide"]')); await tick();
  check(!cards().some((c) => c.dataset.id === hid), "hidden position leaves the list");
  // ── Jobs after the MSc ──
  await tab("jobs");
  check(!d.querySelector("#view-positions").hidden && /Research-assistant/.test(d.querySelector("#listhead").textContent), "jobs tab reuses the list with its own heading");
  check(cards().length > 3 && cards().every((c) => ["technician", "scientist", "other"].includes(job(c).kind)), `jobs tab shows lab jobs only (${cards().length})`);
  const nophd = d.querySelector('#filters input[data-f="nophd"]'); nophd.checked = true; change(nophd); await tick();
  check(cards().length > 0 && cards().every((c) => !job(c).needs_phd), `"Hide jobs that need a PhD" works (${cards().length})`);
  nophd.checked = false; change(nophd); await tick();
  const sort = d.querySelector("#sort"); sort.value = "deadline"; change(sort); await tick();
  const dls = cards().map((c) => job(c).deadline).filter(Boolean);
  check(dls.join() === [...dls].sort().join(), "deadline sort is chronological");
  sort.value = "match"; change(sort); await tick();
  const sel = d.querySelector("#profile"); sel.value = "ai-labs"; change(sel); await tick();
  check(job(cards()[0]).sector === "ai-bio", `AI-for-biology profile puts an AI company first (${job(cards()[0]).title})`);
  sel.value = "sulekha"; change(sel); await tick();
  click(d.querySelector("#tune-btn")); await tick();
  const rank = () => cards().findIndex((c) => job(c).region === "india");
  const before = rank();
  const slider = d.querySelector('#tune input[data-tune="regions.india"]'); slider.value = "40"; slider.dispatchEvent(new w.Event("input", { bubbles: true })); await tick();
  check(before >= 0 && rank() === 0, `tuning India +40 lifts the first Indian job from #${before + 1} to #${rank() + 1}`);
  click(d.querySelector("#tune-reset")); await tick();
  // ── Internships: three columns ──
  await tab("internships");
  check(!d.querySelector("#view-internships").hidden && d.querySelectorAll("#internships .icol").length === 3, "internships tab shows three columns");
  check(/NCBS Bengaluru Summer Internship/.test(d.querySelector("#col-india").textContent), "Bengaluru internship sits in the India column");
  check(/Research Intern, Experimental Biology/.test(d.querySelector("#col-ai").textContent), "AI-company internship sits in its own column");
  check(/SRFP/.test(d.querySelector("#col-india").textContent) && /Enrolled students only/.test(d.querySelector("#col-india").textContent), "India schemes listed with the enrolment warning");
  check(/Charpak Lab/.test(d.querySelector("#col-abroad").textContent), "abroad schemes listed");
  click(d.querySelector('#col-india .mini [data-act="track"]')); await tick();
  check(d.querySelector("#tcount").textContent === "2", "tracking from an internship card works");
  click(d.querySelector('#internships [data-fid="srfp"]')); await tick();
  check(JSON.parse(w.localStorage.getItem("lh.tracker"))["f-srfp"] !== undefined, "tracking a scheme stores it");
  click(d.querySelector('#internships [data-goto="jobs"]')); await tick();
  check(!d.querySelector("#view-positions").hidden && w.location.search.includes("jobs") || /Research-assistant/.test(d.querySelector("#listhead").textContent), "the enrolment note links to Jobs after MSc");
  await tab("phd");
  click(d.querySelector('#discs [data-preset="blr"]')); await tick();
  check(!d.querySelector("#view-internships").hidden, "the Bengaluru chip opens the internships tab");
  // ── Programmes ──
  await tab("programmes");
  check(/IMPRS on the Biology of Ageing/.test(d.querySelector("#programmes").textContent) && /EMBL International PhD Programme/.test(d.querySelector("#programmes").textContent), "programmes tab lists PhD programmes");
  click(d.querySelector('#programmes [data-fid="embl"]')); await tick();
  check(JSON.parse(w.localStorage.getItem("lh.tracker"))["f-embl"].kind === "fellowship", "tracking a programme works");
  // ── Tracker, search, sources ──
  await tab("tracker");
  check(d.querySelectorAll("#board .tcard").length === 4 && !d.querySelector("#view-tracker").hidden, "tracker tab shows everything tracked");
  const st = d.querySelector('#board select[data-t="status"]'); st.value = "applied"; change(st); await tick();
  check([...d.querySelectorAll("#board .col")].some((c) => /Applied/.test(c.querySelector("h3").textContent) && c.querySelector(".tcard")), "status change moves the card to Applied");
  const form = d.querySelector("#add-form"); form.querySelector('[name="title"]').value = "LinkedIn post: summer intern, NCBS";
  form.querySelector('[name="deadline"]').value = "2027-02-01"; form.dispatchEvent(new w.Event("submit", { bubbles: true, cancelable: true })); await tick();
  check(d.querySelectorAll("#board .tcard").length === 5, "manual add works");
  await tab("search");
  const li = [...d.querySelectorAll("#search a.lcard")].find((a) => /LinkedIn Jobs/.test(a.textContent));
  check(li && /keywords=PhD%20position%20ageing/.test(li.href) && /location=Europe/.test(li.href), "LinkedIn saved search uses her profile");
  await tab("sources");
  check(d.querySelectorAll("#sources table.health tbody tr").length === data.health.length, "sources tab lists every source");
  let icsText = ""; w.URL.createObjectURL = (b) => { const r = new w.FileReader(); r.onload = () => (icsText = r.result); r.readAsText(b); return "blob:x"; }; w.URL.revokeObjectURL = () => {};
  await tab("tracker"); click(d.querySelector("#ics")); await new Promise((r) => setTimeout(r, 60));
  check(/BEGIN:VEVENT/.test(icsText) && /DTSTART;VALUE=DATE:20261130/.test(icsText), "calendar export contains the deadlines (SRFP 30 Nov)");
  console.log(errors.length ? "\nPROBLEMS:\n" + errors.join("\n") : "\nAll UI checks passed, no script errors.");
  process.exit(errors.length ? 1 : 0);
})();
