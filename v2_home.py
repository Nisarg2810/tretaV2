# V2 home page. Imported by build.py, which passes its globals in.
import json, html
E = html.escape

def home2(g):
    T, RESULTS, DOCTORS, FAQS, THEMES, ICONS = g["T"], g["RESULTS"], g["DOCTORS"], g["FAQS"], g["THEMES"], g["ICONS"]
    CAL_SVG, WA_SVG, WA, REVIEWS, PHOTO = g["CAL_SVG"], g["WA_SVG"], g["WA"], g["REVIEWS"], g["PHOTO"]
    ba, faq_html, visit_block = g["ba"], g["faq_html"], g["visit_block"]

    letters = "".join(f'<span class="l"><span>{c}</span></span>' for c in "TRETĀ")
    hero = f'''
<section class="hx" id="top" aria-label="Introduction">
 <div class="hx-stick">
  <p class="hx-tag hx-tl">Skin and Hair Institute</p><p class="hx-tag hx-tr">Maninagar, Ahmedabad</p>
  <div class="hx-word" aria-hidden="true">{letters}</div>
  <div class="hx-media"><div class="hx-word hx-in" aria-hidden="true">{letters}</div><picture><source media="(max-width:760px)" srcset="assets/photo/hero-m.jpg"><img src="assets/photo/hero.jpg" alt="Woman with healthy, glowing skin in warm sunlight" fetchpriority="high" width="2800" height="1867"></picture><span class="hx-shade"></span></div>
  <div class="hx-copy wrap">
   <span class="status hx-c" data-status></span>
   <h1 class="hx-h hx-c">Skin and hair,<br><em>chosen wisely.</em></h1>
   <p class="hx-p hx-c">Two MD dermatologists. Evidence based care for acne, pigmentation, hair loss and FUE hair transplant.</p>
   <div class="hx-ctas hx-c"><a class="btn btn-white mag" href="book.html" data-book="">{CAL_SVG} Book a consultation</a><a class="btn glass mag" href="https://wa.me/{WA}" data-chat="">{WA_SVG} Chat on WhatsApp</a></div>
  </div>
  <div class="hx-scroll" aria-hidden="true"><span></span>Scroll</div>
 </div>
</section>'''

    inl = lambda src, alt: f'<span class="inl"><img src="{src}" alt="{alt}" loading="lazy"></span>'
    mani = f'''
<section class="mani" aria-label="Our philosophy"><div class="wrap">
 <span class="eyebrow">Our philosophy</span>
 <p class="mani-t" data-words>We treat skin {inl("assets/photo/acne-s.jpg","Healthy skin close up")} and hair {inl("assets/photo/hair-s.jpg","Full, healthy hair")} the way medicine should. Diagnose first, explain clearly, and recommend only what you need. Two dermatologists {inl("assets/doctors/doctor-female.jpg","Dr. Sohini Soneji Shah")} one standard of care.</p>
 <div class="mani-foot"><div class="stats">
  <div><b data-count="5.0">5.0</b><span>Google rating</span></div><div><b data-count="101">101</b><span>Patient reviews</span></div>
  <div><b data-count="60">60+</b><span>Treatments</span></div><div><b data-count="13">13</b><span>Published results</span></div></div>
  <a class="tlink" href="doctors.html">Meet the doctors <span class="arrow">→</span></a></div>
</div></section>'''

    panels = [("01", "Skin", "Acne, pigmentation, eczema, vitiligo and every everyday concern, diagnosed properly.", "skin-disease-treatment", "acne"),
              ("02", "Anti-ageing", "Hydrafacial, fillers and skin tightening that look rested, never done.", "anti-ageing-hydrafacial", "hydrafacial"),
              ("03", "Lasers", "Hair reduction, tattoo removal and toning, set by a dermatologist for Indian skin.", "laser-treatment-ahmedabad", "laser"),
              ("04", "Hair", "From hair fall to FUE transplant, planned and performed by Dr. Malhar Shah.", "hair-transplant-ahmedabad", "hair")]
    ph = "".join(f'''<a class="hz-p" href="{u}.html"><span class="hz-img"><img src="assets/photo/{img}.jpg" alt="{t} treatments at TRETĀ Derma" loading="lazy"></span>
<span class="hz-meta"><span class="n">{n}</span><span class="go" aria-hidden="true">→</span></span><h3>{t}</h3><p>{d}</p></a>''' for n, t, d, u, img in panels)
    hz = f'''
<section class="hz" aria-label="Disciplines"><div class="hz-pin">
 <div class="hz-head wrap"><span class="eyebrow">Four disciplines</span><h2 class="h2 split">One roof. <em>Every concern.</em></h2></div>
 <div class="hz-track">{ph}<div class="hz-end"><p class="h3">Not sure where<br>you fit?</p><a class="btn btn-ink mag" href="https://wa.me/{WA}" data-chat="">{WA_SVG} Ask the clinic</a></div></div>
 <div class="hz-bar" aria-hidden="true"><i></i></div>
</div></section>'''

    rows = "".join(f'''<li><a href="{t["slug"]}.html" data-img="assets/photo/{PHOTO[t["slug"]][0]}-s.jpg"><span class="n">{i+1:02d}</span><span class="t">{t["nav"]}</span><span class="s">{t["short"]}</span><span class="go" aria-hidden="true">→</span></a></li>''' for i, t in enumerate(T))
    idx = f'''
<section class="idx" id="treatments" aria-label="Treatments"><div class="wrap">
 <div class="sec-hd"><div><span class="eyebrow">Treatment index</span><h2 class="h2 split">Every treatment,<br><em>one standard.</em></h2></div><p class="lead rv">Nine specialities and more than sixty treatments. Hover to preview, tap to read how we treat it.</p></div>
 <ul class="idx-list">{rows}</ul>
 <p style="margin-top:36px"><a class="tlink" href="treatments.html">See the full menu <span class="arrow">→</span></a></p>
</div><div class="idx-float" aria-hidden="true"><img alt="" src="assets/photo/hair-s.jpg"></div></section>'''

    data = [dict(slug=r[0], t=r[1], cat=r[2], tag=r[3], d=r[4]) for r in RESULTS]
    items = "".join(f'''<li data-cat="{r[2]}"><button type="button" data-i="{i}" aria-pressed="{str(i==0).lower()}"><img src="assets/ba/{r[0]}-after.jpg?v=4" alt="" loading="lazy"><span><b>{E(r[1])}</b><small>{E(r[3])}</small></span><span class="k">{i+1:02d}</span></button></li>''' for i, r in enumerate(RESULTS))
    ev = f'''
<section class="ev ink" id="results" aria-label="Results" data-results='{E(json.dumps(data))}'><div class="wrap">
 <div class="sec-hd"><div><span class="eyebrow">The evidence</span><h2 class="h2 split">Real patients.<br><em>Real results.</em></h2></div><p class="lead rv">Every photo is our own patient, unretouched and shared with consent. Drag across any image to compare.</p></div>
 <div class="ev-grid">
  <div class="ev-stage rv">{ba(RESULTS[0][0], cls="ev-ba")}
   <div class="ev-cap"><span class="ev-k">01 / {len(RESULTS):02d}</span><div><span class="chip">{E(RESULTS[0][3])}</span><h3>{E(RESULTS[0][1])}</h3><p>{E(RESULTS[0][4])}</p></div></div></div>
  <div class="ev-side rv d1"><div class="filters ev-f" role="group" aria-label="Filter results">{"".join(f'<button type="button" data-cat="{c}" aria-pressed="{str(c=="all").lower()}">{n}</button>' for c, n in [("all","All"),("hair","Hair"),("skin","Skin"),("procedure","Procedures")])}</div>
   <ul class="ev-list">{items}</ul><a class="btn btn-paper mag" href="results.html" style="margin-top:22px">Open the full gallery <span class="arrow">→</span></a></div>
 </div></div></section>'''

    stages = [dict(t="Day 1", m=0, d="Grafts are placed in one sitting under local anaesthesia. You go home the same evening.", len=6, keep=1),
              dict(t="Weeks 2 to 6", m=1, d="Transplanted hairs shed. This is normal and expected, the roots stay safely in place.", len=3, keep=.35),
              dict(t="Month 3", m=3, d="New, fine hair starts to grow through, slowly at first.", len=22, keep=.7),
              dict(t="Month 6", m=6, d="Clear, visible improvement. Most people see the change in the mirror now.", len=52, keep=.95),
              dict(t="Months 9 to 12", m=12, d="The final result. Hair thickens and matures, and keeps growing for life.", len=80, keep=1)]
    ticks = "".join(f'<span>{s["t"]}</span>' for s in stages)
    jr = f'''
<section class="jr ink" aria-label="Hair transplant timeline"><div class="jr-pin"><div class="wrap jr-grid" data-stages='{E(json.dumps(stages))}'>
 <div><span class="eyebrow">The hair transplant journey</span><h2 class="h2" style="margin:16px 0 0">Twelve months,<br><em>one hairline.</em></h2>
  <p class="jr-stage" aria-live="polite">Day 1</p><p class="lead jr-copy">{stages[0]["d"]}</p>
  <div class="jr-prog"><i></i></div><div class="jr-ticks">{ticks}</div>
  <p style="margin-top:34px"><a class="btn btn-paper mag" href="hair-transplant-ahmedabad.html">Hair transplant at TRETĀ <span class="arrow">→</span></a></p></div>
 <div class="jr-card" aria-hidden="true"><svg viewBox="0 0 400 260"><path class="ground" d="M10 236 Q200 160 390 236 L390 260 L10 260Z"/></svg><span class="jr-cap">Illustration of graft growth</span></div>
</div></div></section>'''

    docs = "".join(f'''<article class="dr{" dr-b" if i else ""}"><a class="dr-ph" href="doctors.html"><img src="assets/doctors/{d["img"]}.jpg" alt="{d["name"]}, dermatologist at TRETĀ Derma" loading="lazy" data-par></a>
<div class="dr-bd"><span class="cred">{d["cred"]}</span><h3>{d["name"].rsplit(" ", 1)[0]} <em>{d["name"].rsplit(" ", 1)[1]}</em></h3><p class="role">{d["role"]}</p><p>{d["bio"]}</p><a class="tlink" href="book.html" data-book="{d["book"]}">Book with {d["name"].split()[1]} <span class="arrow">→</span></a></div></article>''' for i, d in enumerate(DOCTORS))
    drs = f'''
<section class="drs" id="doctors" aria-label="Doctors"><div class="wrap">
 <div class="sec-hd"><div><span class="eyebrow">Your doctors</span><h2 class="h2 split">Two specialists.<br><em>Every single visit.</em></h2></div><p class="lead rv">You are always seen by an MD dermatologist. Never a technician, never a sales desk.</p></div>
 <div class="drs-grid">{docs}</div></div></section>'''

    steps = [("Reach out", "Book online in a minute or message us on WhatsApp. A photo helps us prepare."),
             ("Consult", "Your dermatologist examines your skin or scalp and finds the real cause."),
             ("Plan", "A written plan with sessions, timelines and what to expect at every step."),
             ("Follow up", "Progress photos at each visit, and a team that is one message away.")]
    proc = f'''
<section class="proc paper" aria-label="Your first visit"><div class="wrap proc-grid">
 <div class="proc-l"><span class="eyebrow">Your first visit</span><h2 class="h2 split" style="margin-top:16px">Unhurried,<br><em>from hello.</em></h2><div class="proc-ph"><img src="assets/photo/glow-s.jpg" alt="Calm treatment room" loading="lazy" data-par></div></div>
 <ol class="proc-r">{"".join(f'<li class="rv"><span class="n">0{i+1}</span><h3>{h}</h3><p>{p}</p></li>' for i, (h, p) in enumerate(steps))}</ol>
</div></section>'''

    q = "".join(f'<figure><span class="stars" aria-label="5 stars">★★★★★</span><blockquote>“{a}”</blockquote><figcaption>{b}</figcaption></figure>' for a, b in THEMES)
    rev = f'''
<section class="rvw" id="reviews" aria-label="Reviews"><div class="wrap rvw-top"><div><span class="eyebrow">Loved by patients</span><p class="rvw-score"><span data-count="5.0">5.0</span></p></div>
 <div><span class="stars" style="font-size:22px">★★★★★</span><p class="lead" style="margin:12px 0 22px">Rated 5.0 from 101 reviews on Google. Read every one, unfiltered.</p><a class="btn btn-line mag" href="{REVIEWS}" target="_blank" rel="noopener">Read reviews on Google <span class="arrow">↗</span></a></div></div>
 <div class="rvw-mq"><div class="rvw-track">{q}{q}</div></div></section>'''

    qs = FAQS["ht"][:5] + FAQS["hair"][:1] + FAQS["acne"][:1] + FAQS["pig"][:1]
    faq = f'''
<section class="sec faq2" id="faq" aria-label="Questions"><div class="wrap faq2-grid"><div class="faq2-l"><span class="eyebrow">Good questions</span><h2 class="h2 split" style="margin-top:16px">Straight answers,<br><em>from our doctors.</em></h2><p class="lead rv" style="margin-top:22px">Still curious? Ask us on WhatsApp. A real person from the clinic replies.</p></div>{faq_html(qs)}</div></section>'''

    end = f'''
<section class="fin ink" aria-label="Book"><div class="wrap"><span class="eyebrow">Be wise. Choose right.</span>
 <h2 class="fin-h split">Your skin and hair,<br><em>in expert hands.</em></h2>
 <div class="fin-row"><a class="btn btn-white mag" href="book.html" data-book="">{CAL_SVG} Book a consultation</a><a class="btn glass mag" href="https://wa.me/{WA}" data-chat="">{WA_SVG} Chat on WhatsApp</a></div></div></section>'''

    return hero + mani + hz + idx + ev + jr + drs + proc + rev + faq + visit_block() + end, qs
