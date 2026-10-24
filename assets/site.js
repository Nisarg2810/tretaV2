/* TRETĀ Derma, site behaviour */
(function () {
  "use strict";
  var WA = "918511799700";
  var TEL = "+918511799700";
  var ADDR = "402, 4th Floor, Sigma Esquire, Above Domino's, Opp. Kankaria, Maninagar, Ahmedabad 380008";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm5.8 14.13c-.24.68-1.42 1.32-1.95 1.36-.5.05-.97.24-3.27-.68-2.77-1.09-4.52-3.92-4.66-4.1-.13-.18-1.12-1.49-1.12-2.84 0-1.35.71-2.01.96-2.29.25-.27.55-.34.73-.34l.52.01c.17.01.39-.06.61.47.24.55.79 1.9.86 2.04.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.27.14.43.11.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.33Z"/></svg>';

  function waLink(text) { return "https://wa.me/" + WA + "?text=" + encodeURIComponent(text); }
  function openWA(text) { window.open(waLink(text), "_blank", "noopener"); }
  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }

  /* clinic time, always India Standard Time */
  function ist() {
    var p = {};
    new Intl.DateTimeFormat("en-GB", { timeZone: "Asia/Kolkata", year: "numeric", month: "numeric", day: "numeric", hour: "numeric", minute: "numeric", hour12: false, weekday: "short" })
      .formatToParts(new Date()).forEach(function (x) { p[x.type] = x.value; });
    var dows = { Sun: 0, Mon: 1, Tue: 2, Wed: 3, Thu: 4, Fri: 5, Sat: 6 };
    return { y: +p.year, m: +p.month, d: +p.day, h: +p.hour % 24, min: +p.minute, dow: dows[p.weekday] };
  }
  function sessions(dow) {
    if (dow === 0) return [];
    if (dow === 6) return [[600, 780]];
    return [[600, 780], [1020, 1200]];
  }
  function openState() {
    var n = ist(), t = n.h * 60 + n.min, s = sessions(n.dow), i;
    for (i = 0; i < s.length; i++) if (t >= s[i][0] && t < s[i][1]) return { open: true, until: s[i][1] };
    for (i = 0; i < s.length; i++) if (t < s[i][0]) return { open: false, next: "today at " + fmtMin(s[i][0]) };
    var d = (n.dow + 1) % 7; if (d === 0) d = 1;
    return { open: false, next: (d === (n.dow + 1) % 7 ? "tomorrow" : "Monday") + " at 10 am" };
  }
  function fmtMin(m) {
    var h = Math.floor(m / 60), mm = m % 60, ap = h >= 12 ? "pm" : "am", hh = h % 12 || 12;
    return hh + (mm ? ":" + (mm < 10 ? "0" : "") + mm : "") + " " + ap;
  }
  function statusText() {
    var s = openState();
    return s.open ? "Open now, until " + fmtMin(s.until) : "Closed now, opens " + s.next;
  }
  $$("[data-status]").forEach(function (el) {
    var s = openState();
    el.innerHTML = '<i class="dot' + (s.open ? " on" : "") + '"></i>' + statusText();
  });
  $$(".hours tr[data-dow]").forEach(function (tr) {
    if (tr.getAttribute("data-dow").split(",").indexOf(String(ist().dow)) > -1) tr.classList.add("today");
  });

  /* header */
  var hdr = $(".hdr");
  function onScroll() { if (hdr) hdr.classList.toggle("scrolled", window.scrollY > 20); }
  window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
  var burger = $(".burger"), mnav = $(".mnav");
  if (burger && mnav) {
    burger.addEventListener("click", function () {
      var o = mnav.classList.toggle("open");
      burger.setAttribute("aria-expanded", o);
      if (hdr) { if (o && hdr.classList.contains("over")) { hdr.classList.remove("over"); hdr._over = true; } else if (!o && hdr._over) hdr.classList.add("over"); }
      document.body.style.overflow = o ? "hidden" : "";
    });
    $$("a", mnav).forEach(function (a) { a.addEventListener("click", function () { mnav.classList.remove("open"); document.body.style.overflow = ""; if (hdr && hdr._over) hdr.classList.add("over"); }); });
  }
  $$(".dd > button").forEach(function (b) {
    b.addEventListener("click", function () { var o = b.parentNode.classList.toggle("open"); b.setAttribute("aria-expanded", o); });
  });
  document.addEventListener("click", function (e) { $$(".dd.open").forEach(function (d) { if (!d.contains(e.target)) d.classList.remove("open"); }); });

  /* reveal */
  $$(".split").forEach(function (el) {
    var html = el.innerHTML.split(/(<[^>]+>)/).map(function (part) {
      if (part.charAt(0) === "<") return part;
      return part.replace(/(\S+)/g, '<span class="w"><span>$1</span></span>');
    }).join("");
    el.innerHTML = html;
    $$(".w > span", el).forEach(function (s, i) { s.style.transitionDelay = (i * 0.05) + "s"; });
  });
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { rootMargin: "0px 0px -8% 0px" });
    $$(".rv,.split").forEach(function (el) { io.observe(el); });
  } else { $$(".rv,.split").forEach(function (el) { el.classList.add("in"); }); }
  setTimeout(function () { $$(".hero-full .rv,.hero-full .split,.phero .rv,.phero .split").forEach(function (el) { el.classList.add("in"); }); }, 60);
  if (location.hash === "#shot") $$(".rv,.split").forEach(function (el) { el.classList.add("in"); });

  /* before / after */
  $$(".ba").forEach(function (ba) {
    var r = $("input", ba);
    if (!r) return;
    var set = function () { ba.style.setProperty("--p", r.value + "%"); };
    r.addEventListener("input", set); set();
  });
  var heroBa = $(".hero .ba input");
  if (heroBa && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    var t0 = null, touched = false;
    heroBa.addEventListener("pointerdown", function () { touched = true; });
    heroBa.addEventListener("input", function () { touched = true; });
    var sweep = function (ts) {
      if (touched) return;
      if (!t0) t0 = ts;
      var k = (ts - t0) / 1000;
      if (k > 4.2) { heroBa.value = 50; heroBa.dispatchEvent(new Event("input")); touched = false; return; }
      heroBa.value = 50 + Math.sin(k * 1.5) * 32 * Math.max(0, 1 - k / 4.2);
      heroBa.closest(".ba").style.setProperty("--p", heroBa.value + "%");
      requestAnimationFrame(sweep);
    };
    setTimeout(function () { requestAnimationFrame(sweep); }, 900);
  }

  /* results filter */
  $$(".filters").forEach(function (f) {
    var grid = $(f.getAttribute("data-for"));
    $$("button", f).forEach(function (b) {
      b.addEventListener("click", function () {
        $$("button", f).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        var c = b.getAttribute("data-cat");
        $$(".res", grid).forEach(function (r) { r.classList.toggle("hide", c !== "all" && r.getAttribute("data-cat") !== c); });
      });
    });
  });

  /* concern finder tabs */
  $$(".finder").forEach(function (fd) {
    var tabs = $$(".tab", fd);
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () {
        tabs.forEach(function (x) { x.setAttribute("aria-selected", x === t); x.tabIndex = x === t ? 0 : -1; });
        $$(".panel", fd).forEach(function (p) { p.classList.toggle("on", p.id === t.getAttribute("aria-controls")); });
      });
      t.addEventListener("keydown", function (e) {
        var k = e.key === "ArrowDown" || e.key === "ArrowRight" ? 1 : e.key === "ArrowUp" || e.key === "ArrowLeft" ? -1 : 0;
        if (k) { e.preventDefault(); var n = tabs[(i + k + tabs.length) % tabs.length]; n.focus(); n.click(); }
      });
    });
  });

  /* hair transplant growth timeline, drawn in code */
  var tl = $(".tl");
  if (tl) {
    var svg = $(".scalp svg", tl), range = $(".tl-range", tl), stages = JSON.parse(tl.getAttribute("data-stages"));
    var N = 46, lines = [], ns = "http://www.w3.org/2000/svg", i;
    for (i = 0; i < N; i++) {
      var x = 20 + i * (360 / (N - 1)), l = document.createElementNS(ns, "line");
      var tt = (x - 10) / 380, base = 238 - 152 * tt * (1 - tt);
      l.setAttribute("x1", x); l.setAttribute("y1", base); l.setAttribute("x2", x); l.setAttribute("y2", base);
      l.setAttribute("stroke-width", 2.6);
      l._b = base; l._x = x; l._r = 0.75 + ((i * 37) % 11) / 40; l._lean = ((i * 53) % 7) - 3;
      svg.appendChild(l); lines.push(l);
    }
    var paint = function (k) {
      var st = stages[k];
      $(".tl-stage", tl).textContent = st.t;
      $(".tl-copy", tl).textContent = st.d;
      $$(".tl-ticks button", tl).forEach(function (b, j) { b.classList.toggle("on", j === k); });
      lines.forEach(function (l, j) {
        var keep = st.keep >= 1 || ((j * 7) % 10) / 10 < st.keep;
        var len = keep ? st.len * l._r : 2;
        l.setAttribute("x2", l._x + l._lean * st.len / 60);
        l.setAttribute("y2", l._b - len);
        l.style.opacity = keep ? 1 : 0.25;
      });
    };
    range.addEventListener("input", function () { paint(+range.value); });
    $$(".tl-ticks button", tl).forEach(function (b, j) { b.addEventListener("click", function () { range.value = j; paint(j); }); });
    paint(0);
  }

  /* booking */
  var CONCERNS = [
    ["Hair transplant", "FUE and DHI", "transplant"], ["Hair fall or thinning", "PRP, GFC, alopecia", "prp"],
    ["Acne or acne scars", "Active acne, marks, pits", "acne"], ["Pigmentation or melasma", "Dark spots, uneven tone", "glow"],
    ["Anti-ageing or Hydrafacial", "Fine lines, dullness", "face"], ["Laser treatment", "Hair reduction, tattoo, toning", "laser"],
    ["Skin condition", "Eczema, psoriasis, vitiligo", "derm"], ["Mole, cyst or skin tag", "Minor skin surgery", "tattoo"]
  ];
  var MODES = [["In-clinic consultation", "Meet the doctor in Maninagar", "derm"], ["Video consultation", "On WhatsApp video, from home", "face"], ["Scalp analysis for transplant", "Graft estimate and hairline plan", "transplant"], ["Follow-up visit", "For existing patients", "peel"]];
  var DOCTORS = [["First available", "Quickest slot"], ["Dr. Sohini Soneji Shah", "Skin and anti-ageing"], ["Dr. Malhar Shah", "Hair and transplant"]];
  var ICONS = window.TRETA_ICONS || {};
  var MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"], DOW = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

  function days14() {
    var n = ist(), out = [];
    for (var k = 0; k < 15; k++) {
      var dt = new Date(Date.UTC(n.y, n.m - 1, n.d + k));
      out.push({ y: dt.getUTCFullYear(), m: dt.getUTCMonth(), d: dt.getUTCDate(), dow: dt.getUTCDay(), today: k === 0 });
    }
    return out;
  }
  function slotsFor(day) {
    var n = ist(), now = n.h * 60 + n.min, out = [];
    sessions(day.dow).forEach(function (s) {
      for (var t = s[0]; t <= s[1] - 30; t += 30) out.push({ t: t, off: day.today && t <= now + 30, eve: t >= 1020 });
    });
    return out;
  }
  function dayLabel(d) { return DOW[d.dow] + ", " + d.d + " " + MON[d.m]; }

  function Booking(root, preset, inDialog) {
    var st = { step: 0, concern: preset || "", mode: "", doctor: "First available", day: null, slot: null, name: "", phone: "", note: "" };
    var STEPS = 4;
    function opt(label, sub, ic, sel) {
      return '<button type="button" class="opt" aria-pressed="' + sel + '" data-v="' + label + '">' + (ic ? '<span class="ic">' + (ICONS[ic] || "") + "</span>" : "") + "<span>" + label + "<small>" + sub + "</small></span></button>";
    }
    function body() {
      if (st.step === 0) {
        return '<p class="bk-q">What brings you in?</p><div class="opts" data-k="concern">' + CONCERNS.map(function (c) { return opt(c[0], c[1], c[2], st.concern === c[0]); }).join("") + "</div>";
      }
      if (st.step === 1) {
        return '<p class="bk-q">How would you like to meet?</p><div class="opts" data-k="mode">' + MODES.map(function (c) { return opt(c[0], c[1], c[2], st.mode === c[0]); }).join("") +
          '</div><p class="bk-q" style="margin-top:24px">Doctor</p><div class="opts" data-k="doctor">' + DOCTORS.map(function (c) { return opt(c[0], c[1], "", st.doctor === c[0]); }).join("") + "</div>";
      }
      if (st.step === 2) {
        var ds = days14();
        var h = '<p class="bk-q">Pick a day</p><div class="days">' + ds.map(function (d, i) {
          var none = !slotsFor(d).some(function (s) { return !s.off; });
          var sel = st.day && st.day.d === d.d && st.day.m === d.m;
          return '<button type="button" class="day" data-i="' + i + '" aria-pressed="' + !!sel + '"' + (none ? " disabled" : "") + ' aria-label="' + dayLabel(d) + (none ? ", unavailable" : "") + '"><small>' + (d.today ? "Today" : DOW[d.dow]) + "</small><b>" + d.d + "</b><small>" + MON[d.m] + "</small></button>";
        }).join("") + "</div>";
        if (st.day) {
          var sl = slotsFor(st.day), am = sl.filter(function (s) { return !s.eve; }), pm = sl.filter(function (s) { return s.eve; });
          var row = function (arr) { return '<div class="slots">' + arr.map(function (s) { return '<button type="button" class="slot" data-t="' + s.t + '" aria-pressed="' + (st.slot === s.t) + '"' + (s.off ? " disabled" : "") + ">" + fmtMin(s.t) + "</button>"; }).join("") + "</div>"; };
          h += '<p class="bk-q">Pick a time <span style="text-transform:none;letter-spacing:0;font-weight:600">(India time)</span></p>';
          if (am.length) h += '<div class="slot-grp">Morning</div>' + row(am);
          if (pm.length) h += '<div class="slot-grp">Evening</div>' + row(pm);
        } else h += '<p class="muted small">Open Monday to Saturday. Sundays closed. Saturdays are mornings only.</p>';
        return h;
      }
      if (st.step === 3) {
        return '<div class="fields"><div class="field"><label for="bk-n">Your name</label><input id="bk-n" autocomplete="name" value="' + esc(st.name) + '" required></div>' +
          '<div class="field"><label for="bk-p">Phone or WhatsApp number</label><input id="bk-p" type="tel" inputmode="tel" autocomplete="tel" value="' + esc(st.phone) + '" placeholder="+91" required></div></div>' +
          '<div class="field"><label for="bk-o">Anything the doctor should know? (optional)</label><textarea id="bk-o" rows="2">' + esc(st.note) + "</textarea></div>" +
          '<div class="summary"><div><span>Concern</span><b>' + st.concern + "</b></div><div><span>Visit</span><b>" + st.mode + "</b></div><div><span>Doctor</span><b>" + st.doctor + "</b></div><div><span>When</span><b>" + dayLabel(st.day) + ", " + fmtMin(st.slot) + "</b></div></div>" +
          '<div class="bk-err" role="alert"></div>';
      }
      return '<div class="bk-done"><div class="ok"><svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12.5l4.5 4.5L19 7"/></svg></div><h3>Almost done, ' + esc(st.name.split(" ")[0]) + '.</h3><p class="muted">Send the WhatsApp message that just opened. The clinic team will confirm your slot for <b style="color:var(--ink)">' + dayLabel(st.day) + ", " + fmtMin(st.slot) + '</b> in reply.</p><div class="row"><button type="button" class="btn btn-wa" data-act="resend">' + WA_SVG + ' Open WhatsApp again</button><button type="button" class="btn btn-line" data-act="ics">Add to calendar</button><a class="btn btn-line" target="_blank" rel="noopener" href="https://www.google.com/maps/dir/?api=1&destination=' + encodeURIComponent("Treta Derma Skin and Hair Institute, Sigma Esquire, Maninagar, Ahmedabad") + '">Directions</a></div></div>';
    }
    function esc(s) { return String(s || "").replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
    function msg() {
      return "Hello TRETĀ Derma, I would like to book a consultation.\n\nConcern: " + st.concern + "\nVisit: " + st.mode + "\nDoctor: " + st.doctor + "\nPreferred slot: " + dayLabel(st.day) + ", " + fmtMin(st.slot) + "\nName: " + st.name + "\nPhone: " + st.phone + (st.note ? "\nNote: " + st.note : "") + "\n\nPlease confirm. Thank you.";
    }
    function ok() {
      if (st.step === 0) return !!st.concern;
      if (st.step === 1) return !!st.mode;
      if (st.step === 2) return st.day && st.slot !== null;
      return true;
    }
    function render() {
      var done = st.step >= STEPS;
      root.innerHTML = '<div class="bk"><div class="bk-top"><div><span class="eyebrow">' + (done ? "Request ready" : "Step " + (st.step + 1) + " of " + STEPS) + '</span><h2 style="margin-top:10px">' + (done ? "Thank you." : ["Book a consultation", "Choose your visit", "Choose a time", "Your details"][st.step]) + "</h2></div>" +
        (inDialog ? '<button type="button" class="bk-close" data-act="close" aria-label="Close booking"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' : "") +
        '</div><div class="bk-prog">' + [0, 1, 2, 3].map(function (i) { return "<i" + (i <= st.step ? ' class="on"' : "") + "></i>"; }).join("") + '</div><div class="bk-body">' + body() + "</div>" +
        (done ? "" : '<div class="bk-foot"><button type="button" class="tlink" data-act="back" ' + (st.step ? "" : 'style="visibility:hidden"') + '>Back</button><div style="display:flex;gap:10px;flex-wrap:wrap"><a class="btn btn-line" href="tel:' + TEL + '">Call instead</a>' +
          (st.step < 3 ? '<button type="button" class="btn btn-ink" data-act="next"' + (ok() ? "" : " disabled style=\"opacity:.4\"") + '>Continue <span class="arrow">→</span></button>' : '<button type="button" class="btn btn-wa" data-act="send">' + WA_SVG + " Confirm on WhatsApp</button>") + "</div></div>") + "</div>";
      if (st.step === 2 && st.day) { var sel = $(".day[aria-pressed=true]", root); if (sel && sel.scrollIntoView) sel.parentNode.scrollLeft = sel.offsetLeft - 20; }
    }
    root.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      var grp = b.parentNode.getAttribute && b.parentNode.getAttribute("data-k");
      if (b.classList.contains("opt") && grp) { st[grp] = b.getAttribute("data-v"); render(); return; }
      if (b.classList.contains("day")) { st.day = days14()[+b.getAttribute("data-i")]; st.slot = null; render(); return; }
      if (b.classList.contains("slot")) { st.slot = +b.getAttribute("data-t"); render(); return; }
      var a = b.getAttribute("data-act");
      if (a === "next" && ok()) { st.step++; render(); }
      if (a === "back") { st.step = Math.max(0, st.step - 1); render(); }
      if (a === "close") { var d = root.closest("dialog"); if (d) d.close(); }
      if (a === "resend") openWA(msg());
      if (a === "ics") ics();
      if (a === "send") {
        st.name = $("#bk-n", root).value.trim(); st.phone = $("#bk-p", root).value.trim(); st.note = $("#bk-o", root).value.trim();
        if (st.name.length < 2) return err("Please add your name.");
        if (st.phone.replace(/\D/g, "").length < 10) return err("Please add a phone number with at least 10 digits.");
        openWA(msg()); st.step = STEPS; render();
      }
    });
    root.addEventListener("input", function (e) {
      if (e.target.id === "bk-n") st.name = e.target.value;
      if (e.target.id === "bk-p") st.phone = e.target.value;
      if (e.target.id === "bk-o") st.note = e.target.value;
    });
    function err(t) { var el = $(".bk-err", root); if (el) el.textContent = t; }
    function ics() {
      var mins = st.slot - 330, dt = new Date(Date.UTC(st.day.y, st.day.m, st.day.d, 0, mins));
      var f = function (x) { return x.toISOString().replace(/[-:]/g, "").replace(/\.\d+/, ""); };
      var end = new Date(dt.getTime() + 30 * 60000);
      var body = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//TRETA Derma//Booking//EN", "BEGIN:VEVENT", "UID:" + Date.now() + "@tretaderma", "DTSTAMP:" + f(new Date()), "DTSTART:" + f(dt), "DTEND:" + f(end),
        "SUMMARY:TRETĀ Derma, " + st.mode, "LOCATION:" + ADDR.replace(/,/g, "\\,"), "DESCRIPTION:" + st.concern + " with " + st.doctor + ". Awaiting confirmation on WhatsApp. Call +91 85117 99700.", "END:VEVENT", "END:VCALENDAR"].join("\r\n");
      var a = document.createElement("a");
      a.href = URL.createObjectURL(new Blob([body], { type: "text/calendar" })); a.download = "treta-derma-appointment.ics";
      document.body.appendChild(a); a.click(); a.remove();
    }
    this.reset = function (p) { st.step = 0; st.concern = p || st.concern; render(); };
    render();
  }

  var dlg = $("#book-dialog"), dlgBooking = null;
  $$(".booking-inline").forEach(function (el) { new Booking(el, el.getAttribute("data-preset") || "", false); });
  document.addEventListener("click", function (e) {
    var t = e.target.closest("[data-book]"); if (!t || !dlg) return;
    e.preventDefault();
    var p = t.getAttribute("data-book");
    if (!dlgBooking) dlgBooking = new Booking($(".book-shell", dlg), p, true); else dlgBooking.reset(p);
    if (dlg.showModal) dlg.showModal(); else dlg.setAttribute("open", "");
    closeChat();
  });
  if (dlg) dlg.addEventListener("click", function (e) { if (e.target === dlg || e.target.classList.contains("book-shell")) dlg.close(); });

  /* WhatsApp live chat */
  var fab = document.createElement("button");
  fab.className = "wa-fab"; fab.setAttribute("aria-label", "Chat with TRETĀ Derma on WhatsApp"); fab.setAttribute("aria-expanded", "false");
  fab.innerHTML = WA_SVG + '<span class="badge" aria-hidden="true">1</span>';
  var nudge = document.createElement("div"); nudge.className = "wa-nudge"; nudge.textContent = "Questions about a treatment? Chat with the clinic team.";
  var panel = document.createElement("div"); panel.className = "wa-panel"; panel.setAttribute("role", "dialog"); panel.setAttribute("aria-label", "WhatsApp chat with TRETĀ Derma");
  var os = openState();
  panel.innerHTML = '<div class="wa-hd"><span class="av">TRETĀ</span><div><b>TRETĀ Derma</b><small><i class="' + (os.open ? "" : "off") + '"></i>' + (os.open ? "Online, usually replies in minutes" : "Away, replies from " + os.next.replace("today at ", "")) + '</small></div><button class="x" type="button" aria-label="Close chat"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 6l12 12M18 6L6 18"/></svg></button></div>' +
    '<div class="wa-body" aria-live="polite"></div><form class="wa-in"><label class="sr" for="wa-text">Type a message</label><input id="wa-text" placeholder="Type a message" autocomplete="off"><button type="submit" aria-label="Send on WhatsApp"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M3.4 20.4 21 12 3.4 3.6 3.3 10l12.6 2-12.6 2z"/></svg></button></form><div class="wa-foot">Messages continue in WhatsApp with the clinic team</div>';
  document.body.appendChild(nudge); document.body.appendChild(panel); document.body.appendChild(fab);
  var chatBody = $(".wa-body", panel), started = false;
  function now() { var n = ist(); return (n.h % 12 || 12) + ":" + (n.min < 10 ? "0" : "") + n.min + (n.h >= 12 ? " pm" : " am"); }
  function bubble(html, who) {
    var m = document.createElement("div"); m.className = "msg " + who; m.innerHTML = html + "<time>" + now() + "</time>";
    chatBody.appendChild(m); chatBody.scrollTop = chatBody.scrollHeight; return m;
  }
  function botSay(html, after) {
    var t = document.createElement("div"); t.className = "msg bot typing"; t.innerHTML = "<i></i><i></i><i></i>";
    chatBody.appendChild(t); chatBody.scrollTop = chatBody.scrollHeight;
    setTimeout(function () { t.remove(); var m = bubble(html, "bot"); if (after) after(m); }, 700 + Math.min(html.length * 6, 900));
  }
  var REPLIES = {
    "Book a consultation": null,
    "Hair transplant": ["Our FUE transplants are done by Dr. Malhar Shah in a single day under local anaesthesia. A scalp analysis decides your graft count and hairline.", "Hi, I would like to know about hair transplant and book a scalp analysis."],
    "Acne or scars": ["We treat active acne with medicines and peels, and pitted scars with microneedling and fractional CO₂ laser, planned over a few sessions.", "Hi, I would like help with acne or acne scars."],
    "Pigmentation": ["Melasma and dark spots respond to a mix of medicines, peels and pigment lasers. Your doctor builds the plan after a skin check.", "Hi, I would like help with pigmentation or melasma."],
    "Hair fall": ["Hair fall is first diagnosed, then treated with medicines, PRP or GFC. Patchy loss (alopecia areata) responds well to targeted therapy.", "Hi, I am facing hair fall and would like a consultation."],
    "Timings and location": ["We are at 402, Sigma Esquire, above Domino's, opposite Kankaria, Maninagar. Open Mon to Fri 10 am to 1 pm and 5 to 8 pm, Saturday 10 am to 1 pm.", "Hi, I would like directions to the clinic."]
  };
  function chips() {
    var c = document.createElement("div"); c.className = "chips";
    c.innerHTML = Object.keys(REPLIES).map(function (k) { return '<button type="button">' + k + "</button>"; }).join("");
    chatBody.appendChild(c); chatBody.scrollTop = chatBody.scrollHeight;
  }
  function go(text) { return '<a class="wa-go" target="_blank" rel="noopener" href="' + waLink(text) + '">' + WA_SVG + " Continue on WhatsApp</a>"; }
  chatBody.addEventListener("click", function (e) {
    var b = e.target.closest(".chips button"); if (!b) return;
    var k = b.textContent; b.parentNode.remove(); bubble(k, "me");
    if (k === "Book a consultation") {
      botSay("Lovely. Pick a concern, a doctor and a time in our booking form. It takes under a minute.", function (m) {
        var x = document.createElement("button"); x.className = "wa-go"; x.setAttribute("data-book", ""); x.style.border = "0"; x.textContent = "Open booking";
        m.insertBefore(x, $("time", m)); setTimeout(chips, 400);
      });
      return;
    }
    var r = REPLIES[k];
    botSay(r[0] + "<br>" + go(r[1]), function () { setTimeout(chips, 500); });
  });
  $("form", panel).addEventListener("submit", function (e) {
    e.preventDefault();
    var inp = $("#wa-text", panel), v = inp.value.trim(); if (!v) return;
    bubble(esc(v), "me"); inp.value = "";
    botSay("Thanks. Opening WhatsApp so a team member can reply to you personally.", function () { setTimeout(function () { openWA(v); }, 600); });
  });
  function esc(s) { return s.replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function openChat() {
    panel.classList.add("open"); fab.setAttribute("aria-expanded", "true"); nudge.classList.remove("on");
    var bd = $(".badge", fab); if (bd) bd.remove();
    store("wa-seen", "1");
    if (!started) {
      started = true;
      botSay("Hello and welcome to TRETĀ Derma 👋", function () {
        botSay("I can answer quick questions or help you book with Dr. Sohini or Dr. Malhar. What would you like help with?", chips);
      });
    }
    setTimeout(function () { $("#wa-text", panel).focus({ preventScroll: true }); }, 400);
  }
  function closeChat() { panel.classList.remove("open"); fab.setAttribute("aria-expanded", "false"); }
  fab.addEventListener("click", function () { panel.classList.contains("open") ? closeChat() : openChat(); });
  $(".x", panel).addEventListener("click", closeChat);
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeChat(); });
  $$("[data-chat]").forEach(function (b) { b.addEventListener("click", function (e) { e.preventDefault(); openChat(); }); });
  if (!store("wa-seen")) setTimeout(function () { if (!panel.classList.contains("open")) { nudge.classList.add("on"); setTimeout(function () { nudge.classList.remove("on"); }, 7000); } }, 9000);
  nudge.addEventListener("click", openChat);
})();
