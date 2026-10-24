/* TRETĀ Derma V2: motion, smooth scroll, cursor, scroll stories */
(function () {
  "use strict";
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };
  var root = document.documentElement;
  var fine = window.matchMedia("(hover:hover) and (pointer:fine)").matches;
  function store(k, v) { try { if (v === undefined) return sessionStorage.getItem(k); if (v === null) sessionStorage.removeItem(k); else sessionStorage.setItem(k, v); } catch (e) { return null; } }

  /* evidence viewer and index work without GSAP */
  evidence();
  if (!window.gsap || !window.ScrollTrigger || !root.classList.contains("m")) { root.classList.remove("m"); return; }
  var gsap = window.gsap, ST = window.ScrollTrigger;
  gsap.registerPlugin(ST);

  /* smooth scroll */
  var lenis = null;
  if (window.Lenis) {
    lenis = new window.Lenis({ duration: 1.15, smoothWheel: true, prevent: function (n) { return !!(n.closest && n.closest("dialog,.wa-panel,.ev-list,.days,.mnav")); } });
    lenis.on("scroll", ST.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    window.lenis = lenis;
    var dlg = $("#book-dialog");
    if (dlg) {
      new MutationObserver(function () { dlg.open ? lenis.stop() : lenis.start(); }).observe(dlg, { attributes: true, attributeFilter: ["open"] });
    }
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a[href*='#']"); if (!a) return;
    var url = new URL(a.href, location.href);
    if (url.pathname !== location.pathname || !url.hash || url.hash === "#") return;
    var t = document.getElementById(url.hash.slice(1)); if (!t) return;
    e.preventDefault();
    if (lenis) lenis.scrollTo(t, { offset: -70, duration: 1.6 }); else t.scrollIntoView({ behavior: "smooth" });
  });

  /* header hides on the way down */
  var hdr = $(".hdr"), lastY = 0;
  ST.create({ start: 0, end: "max", onUpdate: function (s) {
    var y = s.scroll();
    if (hdr) hdr.classList.toggle("hide", y > 300 && y > lastY && !$(".mnav.open"));
    lastY = y;
  } });

  /* page transitions */
  var curtain = $(".curtain");
  if (root.classList.contains("navin") && curtain) {
    gsap.fromTo(curtain, { yPercent: 0 }, { yPercent: -100, duration: .9, ease: "expo.inOut", delay: .05, onComplete: function () { root.classList.remove("navin"); gsap.set(curtain, { clearProps: "all" }); } });
    store("nav", null);
  }
  document.addEventListener("click", function (e) {
    var a = e.target.closest("a"); if (!a || e.defaultPrevented) return;
    if (a.target || a.hasAttribute("download") || a.hasAttribute("data-book") || a.hasAttribute("data-chat") || e.metaKey || e.ctrlKey || e.shiftKey) return;
    var url = new URL(a.href, location.href);
    if (url.origin !== location.origin || url.pathname === location.pathname || !/(\.html|\/)$/.test(url.pathname)) return;
    e.preventDefault(); store("nav", "1");
    curtain.classList.add("in");
    setTimeout(function () { location.href = url.href; }, 700);
  });
  window.addEventListener("pageshow", function (e) { if (e.persisted && curtain) curtain.classList.remove("in"); });

  /* preloader then hero intro */
  var pre = $(".pre"), showPre = pre && getComputedStyle(pre).display !== "none";
  function heroIntro() {
    var hx = $(".hx"); if (!hx) return;
    var tl = gsap.timeline();
    tl.from(".hx-word .l > span", { yPercent: 115, duration: 1.4, stagger: .07, ease: "expo.out" }, 0)
      .from(".hx-media", { opacity: 0, duration: 1.4, ease: "power2.out" }, .15).from(".hx-media picture", { scale: 1.25, duration: 2.2, ease: "expo.out" }, .15)
      .from(".hx-tag,.hx-scroll", { opacity: 0, y: 12, duration: 1, stagger: .1, ease: "power3.out" }, .5);
  }
  if (showPre) {
    store("pre", "1");
    var n = { v: 0 }, num = $(".pre-n");
    if (lenis) lenis.stop();
    gsap.timeline({ onComplete: function () { pre.remove(); if (lenis) lenis.start(); } })
      .to(".pre-word > span > span", { yPercent: 0, duration: 1, stagger: .06, ease: "expo.out" }, 0)
      .to(n, { v: 100, duration: 1.5, ease: "power2.inOut", onUpdate: function () { num.textContent = Math.round(n.v); } }, 0)
      .to(".pre-bar", { scaleX: 1, duration: 1.5, ease: "power2.inOut" }, 0)
      .to(".pre-word > span > span", { yPercent: -115, duration: .8, stagger: .04, ease: "expo.in" }, 1.55)
      .to(pre, { yPercent: -100, duration: 1, ease: "expo.inOut" }, 2.05)
      .add(heroIntro, 2.35);
  } else heroIntro();

  /* hero scroll story */
  if ($(".hx")) {
    var small = window.matchMedia("(max-width: 760px)").matches;
    var clipFrom = small ? "inset(24% 14% 18% 14% round 999px 999px 24px 24px)" : "inset(22% 34% 14% 34% round 999px 999px 28px 28px)";
    gsap.set(".hx-media", { clipPath: clipFrom });
    gsap.timeline({ scrollTrigger: { trigger: ".hx", start: "top top", end: "bottom bottom", scrub: .8 } })
      .fromTo(".hx-media", { clipPath: clipFrom }, { clipPath: "inset(0% 0% 0% 0% round 0px 0px 0px 0px)", ease: "none", duration: 1 }, 0)
      .to(".hx-media img", { scale: 1, ease: "none", duration: 1 }, 0)
      .to(".hx-word .l", { yPercent: -40, opacity: 0, stagger: .05, duration: .45, ease: "power1.in" }, .08)
      .to(".hx-tag,.hx-scroll", { opacity: 0, duration: .2 }, 0)
      .to(".hx-shade", { opacity: 1, duration: .35 }, .6)
      .to(".hx-c", { opacity: 1, y: 0, stagger: .07, duration: .3, ease: "power2.out" }, .7);
  }

  /* manifesto: words light up as you read */
  var mt = $(".mani-t");
  if (mt) {
    var walk = function (node) {
      Array.prototype.slice.call(node.childNodes).forEach(function (c) {
        if (c.nodeType === 3) {
          var frag = document.createDocumentFragment();
          c.textContent.split(/(\s+)/).forEach(function (w) {
            if (!w) return;
            if (/^\s+$/.test(w)) frag.appendChild(document.createTextNode(w));
            else { var s = document.createElement("span"); s.className = "wd"; s.textContent = w; frag.appendChild(s); }
          });
          c.parentNode.replaceChild(frag, c);
        } else if (c.nodeType === 1 && !c.classList.contains("inl")) walk(c);
      });
    };
    walk(mt);
    gsap.set($$(".inl", mt), { opacity: .14 });
    gsap.to($$(".wd,.inl", mt), { opacity: 1, stagger: .1, ease: "none", scrollTrigger: { trigger: mt, start: "top 82%", end: "bottom 50%", scrub: true } });
    $$(".inl", mt).forEach(function (el) { gsap.from(el, { width: 0, duration: 1.2, ease: "expo.out", scrollTrigger: { trigger: el, start: "top 85%" } }); });
  }

  /* counters */
  $$("[data-count]").forEach(function (el) {
    var txt = el.textContent, end = parseFloat(el.getAttribute("data-count")), dec = (el.getAttribute("data-count").split(".")[1] || "").length, suf = txt.replace(/[\d.]/g, "");
    var o = { v: 0 };
    ST.create({ trigger: el, start: "top 90%", once: true, onEnter: function () {
      gsap.to(o, { v: end, duration: 1.8, ease: "power3.out", onUpdate: function () { el.textContent = o.v.toFixed(dec) + suf; } });
    } });
  });

  var mm = gsap.matchMedia();
  /* horizontal disciplines, desktop only */
  mm.add("(min-width: 761px)", function () {
    var track = $(".hz-track"); if (!track) return;
    var dist = function () { return Math.max(0, track.scrollWidth - window.innerWidth); };
    var tw = gsap.to(track, { x: function () { return -dist(); }, ease: "none", scrollTrigger: { trigger: ".hz", pin: ".hz-pin", start: "top top", end: function () { return "+=" + dist(); }, scrub: 1, invalidateOnRefresh: true } });
    gsap.to(".hz-bar i", { scaleX: 1, ease: "none", scrollTrigger: { trigger: ".hz", start: "top top", end: function () { return "+=" + dist(); }, scrub: true, invalidateOnRefresh: true } });
    $$(".hz-img img").forEach(function (img) {
      gsap.fromTo(img, { xPercent: -6 }, { xPercent: 6, ease: "none", scrollTrigger: { trigger: img.closest(".hz-p"), containerAnimation: tw, start: "left right", end: "right left", scrub: true } });
    });
  });

  /* hair growth journey */
  var jr = $(".jr-grid");
  if (jr) {
    var stages = JSON.parse(jr.getAttribute("data-stages")), svg = $("svg", jr), ns = "http://www.w3.org/2000/svg", lines = [], N = 52, i;
    for (i = 0; i < N; i++) {
      var x = 20 + i * (360 / (N - 1)), tt = (x - 10) / 380, base = 238 - 152 * tt * (1 - tt), l = document.createElementNS(ns, "line");
      l.setAttribute("x1", x); l.setAttribute("y1", base); l.setAttribute("x2", x); l.setAttribute("y2", base); l.setAttribute("stroke-width", 2.6);
      l._b = base; l._x = x; l._r = .75 + ((i * 37) % 11) / 40; l._lean = ((i * 53) % 7) - 3; l._k = ((i * 7) % 10) / 10;
      svg.appendChild(l); lines.push(l);
    }
    var cur = -1, ticks = $$(".jr-ticks span", jr), prog = $(".jr-prog i", jr);
    var paint = function (p) {
      var f = p * (stages.length - 1), a = Math.floor(f), b = Math.min(stages.length - 1, a + 1), k = f - a;
      var A = stages[a], Bs = stages[b], len = A.len + (Bs.len - A.len) * k, keep = A.keep + (Bs.keep - A.keep) * k;
      lines.forEach(function (ln) {
        var on = keep >= 1 || ln._k < keep, L = on ? len * ln._r : 2;
        ln.setAttribute("x2", ln._x + ln._lean * len / 60); ln.setAttribute("y2", ln._b - L); ln.style.opacity = on ? 1 : .25;
      });
      var r = Math.round(f);
      if (r !== cur) {
        cur = r; $(".jr-stage", jr).textContent = stages[r].t; $(".jr-copy", jr).textContent = stages[r].d;
        ticks.forEach(function (t, j) { t.classList.toggle("on", j === r); });
        gsap.fromTo([".jr-stage", ".jr-copy"], { opacity: .2, y: 10 }, { opacity: 1, y: 0, duration: .5, stagger: .05 });
      }
      if (prog) prog.style.transform = "scaleX(" + p + ")";
    };
    paint(0);
    mm.add("(min-width: 761px)", function () {
      ST.create({ trigger: ".jr", pin: ".jr-pin", start: "top top", end: "+=200%", scrub: true, onUpdate: function (s) { paint(s.progress); } });
    });
    mm.add("(max-width: 760px)", function () {
      ST.create({ trigger: ".jr-card", start: "top 80%", end: "bottom 25%", scrub: true, onUpdate: function (s) { paint(s.progress); } });
    });
  }

  /* parallax images */
  $$("[data-par]").forEach(function (img) {
    gsap.fromTo(img, { yPercent: -9 }, { yPercent: 0, ease: "none", scrollTrigger: { trigger: img.parentNode, start: "top bottom", end: "bottom top", scrub: true } });
  });

  /* inner page hero image */
  $$(".phero-img").forEach(function (box) {
    gsap.to(box, { clipPath: "inset(0% 0 0 0 round 24px)", duration: 1.5, ease: "expo.inOut", delay: .25 });
    gsap.to($("img", box), { scale: 1, duration: 2, ease: "expo.out", delay: .35 });
  });
  /* gallery cards rise in */
  $$(".pcard,.res").forEach(function (c) { c.classList.remove("rv"); gsap.from(c, { y: 60, opacity: 0, duration: 1.2, ease: "expo.out", scrollTrigger: { trigger: c, start: "top 92%" } }); });

  /* cursor */
  if (fine) {
    var cur = $(".cur"), xTo = gsap.quickTo(cur, "x", { duration: .35, ease: "power3" }), yTo = gsap.quickTo(cur, "y", { duration: .35, ease: "power3" });
    var span = $("span", cur);
    window.addEventListener("mousemove", function (e) {
      xTo(e.clientX); yTo(e.clientY);
      var t = e.target, lab = t.closest && (t.closest(".ba") ? "Drag" : t.closest(".hz-p,.pcard") ? "View" : t.closest(".dr-ph") ? "Meet" : "");
      cur.classList.toggle("label", !!lab); span.textContent = lab || "";
      cur.classList.toggle("link", !lab && !!(t.closest && t.closest("a,button,summary,input,label")));
      cur.classList.toggle("on-dark", !!(t.closest && t.closest(".ink,.ftr,.hx-media,.hx-copy,.mnav.open")));
    }, { passive: true });
    document.addEventListener("mouseleave", function () { gsap.to(cur, { opacity: 0, duration: .2 }); });
    document.addEventListener("mouseenter", function () { gsap.to(cur, { opacity: 1, duration: .2 }); });

    /* magnetic buttons */
    $$(".mag,.hdr .btn,.icon-btn").forEach(function (b) {
      var bx = gsap.quickTo(b, "x", { duration: .6, ease: "elastic.out(1,.4)" }), by = gsap.quickTo(b, "y", { duration: .6, ease: "elastic.out(1,.4)" });
      b.addEventListener("mousemove", function (e) { var r = b.getBoundingClientRect(); bx((e.clientX - r.left - r.width / 2) * .3); by((e.clientY - r.top - r.height / 2) * .35); });
      b.addEventListener("mouseleave", function () { bx(0); by(0); });
    });

    /* index hover preview */
    var fl = $(".idx-float"), list = $(".idx-list");
    if (fl && list) {
      var fx = gsap.quickTo(fl, "x", { duration: .6, ease: "power3" }), fy = gsap.quickTo(fl, "y", { duration: .6, ease: "power3" }), fimg = $("img", fl);
      list.addEventListener("mousemove", function (e) { fx(e.clientX + 30); fy(e.clientY - 165); });
      $$("a", list).forEach(function (a) {
        a.addEventListener("mouseenter", function () { var s = a.getAttribute("data-img"); if (fimg.getAttribute("src") !== s) fimg.src = s; fl.classList.add("on"); });
      });
      list.addEventListener("mouseleave", function () { fl.classList.remove("on"); });
    }
  }
  window.addEventListener("load", function () { ST.refresh(); });

  /* ---------- evidence viewer (no GSAP needed) ---------- */
  function evidence() {
    var ev = $(".ev"); if (!ev) return;
    var data = JSON.parse(ev.getAttribute("data-results")), stage = $(".ev-stage", ev), baEl = $(".ev-ba", stage);
    var imgs = $$("img", baEl), range = $("input", baEl);
    var show = function (i) {
      var r = data[i];
      $$(".ev-list button", ev).forEach(function (b) { b.setAttribute("aria-pressed", +b.getAttribute("data-i") === i); });
      stage.style.opacity = .35;
      setTimeout(function () {
        imgs[0].src = "assets/ba/" + r.slug + "-after.jpg?v=4"; imgs[0].alt = r.t + " after treatment at TRETĀ Derma";
        imgs[1].src = "assets/ba/" + r.slug + "-before.jpg?v=4"; imgs[1].alt = r.t + " before treatment";
        range.value = 50; baEl.style.setProperty("--p", "50%"); range.setAttribute("aria-label", "Compare before and after: " + r.t);
        $(".ev-k", stage).textContent = (i < 9 ? "0" : "") + (i + 1) + " / " + data.length;
        $(".ev-cap .chip", stage).textContent = r.tag; $(".ev-cap h3", stage).textContent = r.t; $(".ev-cap p", stage).textContent = r.d;
        var done = function () { stage.style.opacity = 1; };
        if (imgs[0].complete) done(); else imgs[0].onload = done;
      }, 220);
    };
    stage.style.transition = "opacity .35s";
    $(".ev-list", ev).addEventListener("click", function (e) { var b = e.target.closest("button"); if (b) show(+b.getAttribute("data-i")); });
    $$(".ev-f button", ev).forEach(function (b) {
      b.addEventListener("click", function () {
        var c = b.getAttribute("data-cat");
        $$(".ev-f button", ev).forEach(function (x) { x.setAttribute("aria-pressed", x === b); });
        var first = -1;
        $$(".ev-list li", ev).forEach(function (li, i) { var on = c === "all" || li.getAttribute("data-cat") === c; li.classList.toggle("hide", !on); if (on && first < 0) first = i; });
        if (first > -1) show(first);
      });
    });
  }
})();
