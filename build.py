#!/usr/bin/env python3
"""Builds the TRETĀ Derma site. Edit copy here, then run: python3 build.py"""
import json, os, html

ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = "https://nisarg2810.github.io/tretaV2/"
V = "1"  # cache buster for site.css / site.js
PHONE, PHONE_D, WA = "+918511799700", "+91 85117 99700", "918511799700"
IG, FB = "https://www.instagram.com/tretaderma/", "https://www.facebook.com/61562841763497"
GMAPS = "https://www.google.com/maps/search/?api=1&query=Treta+Derma+Skin+and+Hair+Institute+Sigma+Esquire+Maninagar+Ahmedabad"
REVIEWS = "https://www.google.com/search?q=treta+derma+skin+and+hair+institute"
E = html.escape

ICONS = {
  "acne": '<svg viewBox="0 0 24 24"><path d="M12 3c4.4 0 7.5 3.4 7.5 8.2 0 5-3.4 9.8-7.5 9.8s-7.5-4.8-7.5-9.8C4.5 6.4 7.6 3 12 3Z"/><circle cx="9" cy="11" r=".9"/><circle cx="14.5" cy="9.5" r=".9"/><circle cx="13.5" cy="14.5" r=".9"/><circle cx="9.5" cy="15.5" r=".6"/></svg>',
  "glow": '<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.2"/><path d="M12 2.5v2.2M12 19.3v2.2M2.5 12h2.2M19.3 12h2.2M5.3 5.3l1.6 1.6M17.1 17.1l1.6 1.6M5.3 18.7l1.6-1.6M17.1 6.9l1.6-1.6"/></svg>',
  "peel": '<svg viewBox="0 0 24 24"><path d="M12 3.2s5.8 6.3 5.8 10.2a5.8 5.8 0 0 1-11.6 0C6.2 9.5 12 3.2 12 3.2Z"/><path d="M9 14.5a3 3 0 0 0 3 3"/></svg>',
  "laser": '<svg viewBox="0 0 24 24"><rect x="3" y="9" width="9" height="6" rx="1.5"/><path d="M12 12h3"/><path d="M16.5 12h5M17.5 8.5l3.5-2M17.5 15.5l3.5 2"/></svg>',
  "face": '<svg viewBox="0 0 24 24"><path d="M12 3c4 0 7 3.1 7 7.6 0 3.2-1.2 6.2-3.4 8.2a5.3 5.3 0 0 1-7.2 0C6.2 16.8 5 13.8 5 10.6 5 6.1 8 3 12 3Z"/><path d="M9.2 10.5h.01M14.8 10.5h.01M9.8 14.8c1.3 1 3.1 1 4.4 0"/><path d="M19.5 4.5l1-1M20.5 7h1.2"/></svg>',
  "tattoo": '<svg viewBox="0 0 24 24"><path d="M4 20l6.5-6.5M10.5 13.5l7.8-7.8a1.8 1.8 0 0 0-2.5-2.5L8 11l2.5 2.5Z"/><path d="M14 5l5 5"/></svg>',
  "transplant": '<svg viewBox="0 0 24 24"><path d="M3 20.5h18"/><path d="M7 20.5c0-5 .8-9 2.5-13M11.5 20.5c0-6 .4-10.5 1.4-15M16 20.5c0-4.6 1-8.3 3-11.5"/><circle cx="9.5" cy="7.5" r=".9"/><circle cx="12.9" cy="5.5" r=".9"/><circle cx="19" cy="9" r=".9"/></svg>',
  "prp": '<svg viewBox="0 0 24 24"><path d="M14.5 3.5l6 6M17.5 6.5 8 16l-2.5.5.5-2.5 9.5-9.5M5.5 18.5 3 21"/><path d="M10.5 9.5l4 4"/></svg>',
  "derm": '<svg viewBox="0 0 24 24"><path d="M12 3 4.5 6v5.5c0 4.6 3.2 8.4 7.5 9.5 4.3-1.1 7.5-4.9 7.5-9.5V6L12 3Z"/><path d="M9 12h6M12 9v6"/></svg>',
}

# ------------------------------------------------------------------ results
RESULTS = [
  ("ht-hairline-1", "Hair transplant, hairline", "hair", "FUE, 6 months", "A receded hairline rebuilt graft by graft for a natural front."),
  ("ht-crown", "Hair transplant, crown", "hair", "FUE, 6 months", "An advanced bald crown restored to natural density."),
  ("acne-scars", "Acne scars", "skin", "Microneedling and CO₂", "Pitted scars resurfaced over a few planned sessions."),
  ("melasma", "Melasma and pigmentation", "skin", "Peels and laser", "Stubborn facial pigmentation lifted with medicine, peels and pigment lasers."),
  ("hair-loss", "Hair loss with GFC", "hair", "Growth factor concentrate", "Thinning areas re-densified with growth factor therapy."),
  ("acne", "Active acne", "skin", "Medicine and peels", "Inflamed acne cleared with oral and topical treatment plus peels."),
  ("ht-hairline-2", "Hair transplant, density", "hair", "FUE, 6 months", "A thinning frontal zone re-densified with careful angle planning."),
  ("alopecia", "Alopecia areata", "hair", "Intralesional therapy", "Patchy autoimmune hair loss regrown with targeted injections."),
  ("chemical-peel", "Chemical peel", "procedure", "Little to no downtime", "A controlled peel that calms acne, evens tone and renews skin."),
  ("ht-hairline-3", "Hair transplant, full front", "hair", "FUE, 6 months", "Complete frontal restoration with imported FUE instruments."),
  ("dpn", "Dermatosis papulosa nigra", "procedure", "Radiofrequency", "Small benign dark bumps removed precisely with radiofrequency."),
  ("warts", "Warts", "skin", "Immunotherapy", "Stubborn warts, often mistaken for corns, cleared with immunotherapy."),
  ("pityriasis-alba", "Pityriasis alba", "skin", "Gentle medical care", "Pale patches common in children, fully reversed with simple treatment."),
]
RES = {r[0]: r for r in RESULTS}

def ba(slug, label="", cls="", eager=False):
    r = RES[slug]
    ld = 'eager' if eager else 'lazy'
    return (f'<div class="ba {cls}"><img src="assets/ba/{slug}-after.jpg?v=4" alt="{E(r[1])} after treatment at TRETĀ Derma" loading="{ld}" decoding="async" width="900" height="1000">'
            f'<div class="b4"><img src="assets/ba/{slug}-before.jpg?v=4" alt="{E(r[1])} before treatment" loading="{ld}" decoding="async" width="900" height="1000"></div>'
            f'<span class="tag l">Before</span><span class="tag r">After</span><span class="handle"></span>'
            f'<input type="range" min="0" max="100" value="50" aria-label="Compare before and after: {E(r[1])}"></div>')

def res_card(slug, i=0):
    r = RES[slug]
    return (f'<article class="res rv d{i%3}" data-cat="{r[2]}">{ba(slug)}<span class="chip">{E(r[3])}</span>'
            f'<h3>{E(r[1])}</h3><p>{E(r[4])}</p></article>')

# ------------------------------------------------------------------ treatments
T = [
 dict(slug="hair-transplant-ahmedabad", nav="Hair transplant", icon="transplant", short="FUE and DHI, natural and lifelong",
  title="FUE Hair Transplant in Ahmedabad | TRETĀ Derma, Maninagar",
  desc="Natural FUE and DHI hair transplant in Maninagar, Ahmedabad by Dr. Malhar Shah, MD dermatologist and FIHTS hair transplant surgeon. One day procedure, lifelong results.",
  h1="Hair transplant, <em>done by a dermatologist.</em>",
  lead="Follicle by follicle restoration with FUE and DHI, planned and performed by Dr. Malhar Shah. Natural hairlines, safe donor harvesting and instruments imported from the USA and Turkey.",
  glance=[("Procedure time","5 to 9 hours, one day"),("Anaesthesia","Local, you stay awake"),("Back to desk work","2 to 3 days"),("Final result","9 to 12 months")],
  treats=["Receding hairline","Bald crown","Diffuse thinning","Beard and moustache","Eyebrow restoration","Repair of old transplants"],
  how=[("Scalp analysis","We check your donor area, hair loss pattern and calibre, then estimate grafts and draw your hairline with you."),
       ("Extraction","Healthy follicles are taken one by one from the DHT resistant donor zone, within safe limits."),
       ("Implantation","Each graft is placed at the right angle and direction so the result grows like your own hair."),
       ("Aftercare","Clear instructions, medicines and follow-ups. PRP or GFC sessions can support graft survival.")],
  body="A good transplant is mostly planning. The hairline has to suit your face and age, the donor area has to stay full, and your existing hair needs protecting too. That is why every case here starts with a doctor led scalp analysis, not a sales call.",
  results=["ht-hairline-1","ht-crown","ht-hairline-2","ht-hairline-3"], faq="ht"),
 dict(slug="hair-loss-treatment", nav="Hair fall, PRP and GFC", icon="prp", short="Diagnose the cause, then regrow",
  title="Hair Fall Treatment, PRP and GFC in Ahmedabad | TRETĀ Derma",
  desc="Hair fall, thinning and alopecia areata treatment in Maninagar, Ahmedabad. Trichologist led diagnosis with medicines, PRP, GFC and mesotherapy.",
  h1="Hair fall, <em>treated at the root.</em>",
  lead="Hair fall has many causes: genes, hormones, stress, nutrition, thyroid, autoimmunity. We find yours first, then treat it with medicine, PRP, GFC or mesotherapy.",
  glance=[("Visit length","30 to 45 minutes"),("PRP or GFC sessions","Usually 4 to 6, monthly"),("Downtime","None"),("Visible change","Around 3 to 4 months")],
  treats=["Male pattern baldness","Female hair thinning","Alopecia areata","Post illness hair shedding","Dandruff and scalp issues","Weak, thin hair"],
  how=[("Diagnosis","History, scalp examination and blood tests where needed, so we treat the cause and not just the symptom."),
       ("Medical plan","Evidence based medicines such as minoxidil, and finasteride for suitable men."),
       ("Regenerative care","PRP or Growth Factor Concentrate injections to strengthen follicles and thicken hair."),
       ("Review","Photos at every visit so you can see progress, and the plan adjusts as you improve.")],
  body="Most hair fall is treatable when it is caught early. Patchy loss from alopecia areata often regrows with targeted intralesional therapy, and thinning from pattern hair loss can be slowed and partly reversed.",
  results=["hair-loss","alopecia"], faq="hair"),
 dict(slug="acne-scar-treatment", nav="Acne and acne scars", icon="acne", short="Clear skin, smoother texture",
  title="Acne and Acne Scar Treatment in Ahmedabad | TRETĀ Derma",
  desc="Acne, acne marks and pitted acne scar treatment in Maninagar, Ahmedabad. Medicines, chemical peels, microneedling and fractional CO₂ laser by MD dermatologists.",
  h1="Acne and scars, <em>finally under control.</em>",
  lead="We calm active acne first, then repair what it left behind. Medicines and peels for breakouts, microneedling and fractional CO₂ laser for pitted scars.",
  glance=[("Active acne","Better in 6 to 8 weeks"),("Scar sessions","Usually 3 to 6"),("Gap between sessions","4 to 6 weeks"),("Downtime","0 to 5 days")],
  treats=["Active and cystic acne","Blackheads and whiteheads","Red and dark acne marks","Pitted and boxcar scars","Back and body acne","Hormonal acne"],
  how=[("Skin assessment","Acne grade, skin type and triggers such as hormones, products or diet."),
       ("Control breakouts","Oral and topical medicines with a simple routine you can actually follow."),
       ("Clear marks","Chemical peels lift leftover redness and pigmentation."),
       ("Resurface scars","Microneedling, subcision or fractional CO₂ laser to smooth texture over a few sessions.")],
  body="Scars only improve properly once acne is controlled, so the order matters. Your doctor plans both stages from the first visit, so you know what each session is for.",
  results=["acne","acne-scars"], faq="acne"),
 dict(slug="pigmentation-melasma-treatment", nav="Pigmentation and melasma", icon="glow", short="Even, luminous tone",
  title="Pigmentation and Melasma Treatment in Ahmedabad | TRETĀ Derma",
  desc="Melasma, dark spots, tanning and uneven skin tone treatment in Maninagar, Ahmedabad with medicines, chemical peels and pigment lasers, planned for Indian skin.",
  h1="Pigmentation, <em>lifted with care.</em>",
  lead="Melasma and dark spots need patience and the right sequence. We combine prescription creams, peels and pigment lasers, planned for Indian skin so the tone evens out without rebound.",
  glance=[("Plan length","3 to 6 months"),("Peel or laser sessions","Usually 4 to 8"),("Downtime","Little to none"),("Key habit","Daily sunscreen")],
  treats=["Melasma","Sun spots and tanning","Freckles","Post acne marks","Dark underarms and neck","Uneven skin tone"],
  how=[("Find the type","Pigment can sit shallow or deep. A careful exam decides which treatments will help."),
       ("Prescription base","Creams and sometimes oral medicine to slow pigment production."),
       ("Peels and lasers","Brightening peels and laser toning lift existing pigment, session by session."),
       ("Maintenance","Sun protection and a light routine to keep results, since melasma can return.")],
  body="Aggressive treatment can make Indian skin darker, not lighter. We go steady, review progress at every visit and adjust strength to your skin.",
  results=["melasma","chemical-peel"], faq="pig"),
 dict(slug="laser-treatment-ahmedabad", nav="Laser treatments", icon="laser", short="Hair reduction, tattoo, toning",
  title="Laser Hair Reduction and Laser Treatments in Ahmedabad | TRETĀ Derma",
  desc="Laser hair reduction, beard shaping, tattoo removal, laser toning and scar laser in Maninagar, Ahmedabad. Comfortable, safe settings for all Indian skin types.",
  h1="Lasers, <em>set for your skin.</em>",
  lead="Medical grade lasers for hair reduction, beard shaping, tattoo removal, pigment and scars, with settings chosen by a dermatologist for Indian skin.",
  glance=[("Hair reduction","6 to 8 sessions"),("Session gap","4 to 6 weeks"),("Discomfort","Mild, like a snap"),("Downtime","Usually none")],
  treats=["Laser hair reduction","Beard shaping","Tattoo removal","Laser toning","Pigment removal","Scar laser"],
  how=[("Patch test","A small test spot confirms the right energy for your skin and hair."),
       ("Session","Quick, comfortable passes with cooling. Most areas take 15 to 45 minutes."),
       ("Between visits","Gentle skin care and sun protection. No waxing between hair reduction sessions."),
       ("Top ups","Occasional maintenance sessions keep results long term.")],
  body="Lasers are only as safe as the person setting them. Every laser plan here is made by a dermatologist, which matters most for darker skin tones.",
  results=[], faq="laser"),
 dict(slug="anti-ageing-hydrafacial", nav="Anti-ageing and Hydrafacial", icon="face", short="Firm, fresh, rested skin",
  title="Anti-Ageing Treatments and Hydrafacial in Ahmedabad | TRETĀ Derma",
  desc="Hydrafacial, medifacial, skin tightening, anti-wrinkle treatment, fillers, Oxygeneo and non-surgical facelift in Maninagar, Ahmedabad by MD dermatologists.",
  h1="Anti-ageing, <em>quietly done.</em>",
  lead="Hydrafacial, anti-wrinkle treatment, fillers and skin tightening for results that look rested and natural, never overdone.",
  glance=[("Hydrafacial","About 45 minutes"),("Downtime","None for most"),("Results","Visible the same day"),("Best as","A monthly routine")],
  treats=["Hydrafacial and medifacial","Fine lines and wrinkles","Skin tightening","Fillers","Double chin reduction","Stretch marks"],
  how=[("Consult","We look at your skin quality, volume and lines, and agree on what you want to change."),
       ("Plan","A short list of treatments in the right order, from facials to injectables."),
       ("Treatment","Comfortable sessions with numbing where needed."),
       ("Maintain","Simple home care and periodic sessions to keep the glow.")],
  body="Good aesthetic work is invisible. People should notice that you look well, not that you had something done. That is the standard we hold every plan to.",
  results=[], faq="age"),
 dict(slug="chemical-peels", nav="Chemical peels", icon="peel", short="Renewal with little downtime",
  title="Chemical Peels in Ahmedabad for Acne, Tan and Pigmentation | TRETĀ Derma",
  desc="Medical chemical peels in Maninagar, Ahmedabad for acne, tanning, pigmentation and dull skin. Chosen by MD dermatologists, with little to no downtime.",
  h1="Chemical peels, <em>chosen by a doctor.</em>",
  lead="Controlled medical peels that calm acne, lift tan and pigmentation, and renew dull skin, usually with little or no downtime.",
  glance=[("Session time","20 to 30 minutes"),("Sessions","Usually 4 to 6"),("Session gap","2 to 4 weeks"),("Downtime","Little to none")],
  treats=["Active acne","Tanning","Pigmentation","Dull skin","Open pores","Fine lines"],
  how=[("Pick the peel","Salicylic, glycolic, lactic and combination peels each suit different skin and goals."),
       ("Prep","A short routine for a week or two before your first peel."),
       ("Peel","Applied and timed in clinic, then neutralised. Mild tingling is normal."),
       ("Recover","Light flaking for a few days at most. Sunscreen is essential.")],
  body="A peel is a medical procedure, not a facial. The right acid and strength depend on your skin, so we choose it at your consultation.",
  results=["chemical-peel","acne"], faq="peel"),
 dict(slug="skin-disease-treatment", nav="Skin conditions", icon="derm", short="Eczema, psoriasis, vitiligo, more",
  title="Dermatologist in Maninagar, Ahmedabad for Skin Diseases | TRETĀ Derma",
  desc="MD dermatologists in Maninagar, Ahmedabad for eczema, allergy, psoriasis, vitiligo, fungal infections, warts, pigmentary disorders and autoimmune skin disease.",
  h1="Skin conditions, <em>properly diagnosed.</em>",
  lead="From eczema and allergies to psoriasis, vitiligo and stubborn infections, our MD dermatologists diagnose carefully and treat with evidence based medicine.",
  glance=[("Consult","20 to 30 minutes"),("Doctors","Two MD dermatologists"),("Follow up","As your plan needs"),("For","Adults and children")],
  treats=["Eczema and allergy","Psoriasis","Vitiligo (white spots)","Fungal and skin infections","Warts, corns and skin tags","Autoimmune skin disease","Pityriasis alba","Sexually transmitted infections"],
  how=[("Listen and examine","A full history and skin exam, with tests only when they change the treatment."),
       ("Explain","What the condition is, what triggers it and what to realistically expect."),
       ("Treat","Medicines, procedures or phototherapy based plans, kept as simple as possible."),
       ("Follow up","Regular reviews, because chronic conditions need steady care.")],
  body="Many skin conditions look alike. Fungal infection can look like eczema, and warts are often mistaken for corns. A correct diagnosis is the treatment's first step.",
  results=["warts","pityriasis-alba"], faq="derm"),
 dict(slug="mole-cyst-skin-tag-removal", nav="Mole, cyst and tag removal", icon="tattoo", short="Minor skin surgery, same day",
  title="Mole, Cyst and Skin Tag Removal in Ahmedabad | TRETĀ Derma",
  desc="Same day mole removal, cyst removal, skin tag removal, DPN, ear lobe repair, nail surgery and vitiligo surgery in Maninagar, Ahmedabad.",
  h1="Moles, cysts and tags, <em>removed neatly.</em>",
  lead="Minor skin surgery done under local anaesthesia, with radiofrequency or surgical technique chosen for the smallest possible mark.",
  glance=[("Procedure","15 to 45 minutes"),("Anaesthesia","Local"),("Go home","Same day"),("Healing","About 1 to 2 weeks")],
  treats=["Mole removal","Cyst removal","Skin tag removal","Dermatosis papulosa nigra","Ear lobe repair","Nail surgery","Vitiligo surgery"],
  how=[("Check","The doctor examines the lesion and confirms it is safe and suitable to remove."),
       ("Numb","A small local anaesthetic injection, then you feel no pain."),
       ("Remove","Radiofrequency, excision or punch technique, depending on the lesion."),
       ("Heal","Simple dressing and aftercare. Stitches, if any, come out in about a week.")],
  body="Removal is quick, but technique decides the scar. We plan the cut along natural skin lines and send tissue for testing whenever there is any doubt.",
  results=["dpn"], faq="surg"),
]
TBY = {t["slug"]: t for t in T}
PHOTO = {"hair-transplant-ahmedabad": ("hair", "Man with full, natural hair"), "hair-loss-treatment": ("hairloss", "Healthy hair and scalp"),
 "acne-scar-treatment": ("acne", "Clear skin after facial care"), "pigmentation-melasma-treatment": ("pigment", "Even, luminous skin tone"),
 "laser-treatment-ahmedabad": ("laser", "Medical laser and skin device treatment"), "anti-ageing-hydrafacial": ("hydrafacial", "Hydrafacial treatment in progress"),
 "chemical-peels": ("peel", "Chemical peel being applied"), "skin-disease-treatment": ("derm", "Dermatologist applying topical treatment"),
 "mole-cyst-skin-tag-removal": ("procedure", "Minor skin procedure by a doctor")}
def photo(slug, size="-s", cls=""):
    f, alt = PHOTO[slug]
    return f'<img src="assets/photo/{f}{size}.jpg" alt="{alt}" loading="lazy" decoding="async"{cls}>'
def pcard(t, i, text):
    return f'<a class="pcard rv d{i%3}" href="{t["slug"]}.html"><span class="ph">{photo(t["slug"])}</span><h3>{t["nav"]} <span class="arrow">→</span></h3><p>{text}</p></a>'


FAQS = {
 "ht": [
  ("Is a hair transplant permanent?","Yes. Transplanted follicles come from the DHT resistant donor zone, so when the procedure is done correctly they keep growing for life."),
  ("Does it hurt?","It is done under local anaesthesia. You stay awake and comfortable, and can watch TV or rest. You feel mild discomfort only during the numbing injection, with some soreness for a day or two."),
  ("How long does it take?","Most transplants finish in one day. Around 2000 grafts take 5 to 6 hours. 3000 to 4000 grafts take roughly 7 to 9 hours, decided after a scalp analysis."),
  ("When will I see results?","Transplanted hair sheds in 2 to 6 weeks, which is normal. New growth starts around month 3, clear improvement shows by month 6, and the final result arrives at 9 to 12 months."),
  ("Who is a good candidate?","Adults above 23 with stable hair loss, a healthy donor area, good general health and realistic expectations. We usually advise against surgery before 23, since baldness may still be progressing."),
  ("Will the donor area look thin?","No. When extraction stays within safe limits and is done by an experienced dermatologist, the surrounding hair covers the donor zone naturally."),
  ("When can I go back to work and the gym?","Desk work in 2 to 3 days, physical work in 7 to 10 days. Light walking is fine after 3 to 4 days, but avoid sweating, swimming and heavy workouts for 2 to 3 weeks."),
  ("Will a transplant stop future hair loss?","It restores lost hair but does not stop thinning of your native hair. We protect existing density with medicines such as minoxidil, finasteride for suitable men, and often PRP or GFC."),
 ],
 "hair": [
  ("Is PRP or GFC better?","Both use growth factors from your own blood. GFC is a more concentrated, refined preparation. Your doctor will suggest one based on your hair loss and goals."),
  ("How many sessions will I need?","Most people need 4 to 6 sessions about a month apart, then occasional maintenance."),
  ("Can alopecia areata grow back?","Often, yes. Patchy alopecia areata usually responds well to intralesional injections and supportive treatment."),
  ("Do I need blood tests?","Sometimes. Thyroid, iron, vitamin D and hormone levels can all cause hair fall, so we test when your history suggests it."),
 ],
 "acne": [
  ("Can acne scars be removed completely?","Most scars can be improved a lot, often by 50 to 80 percent, though complete removal is rare. The right mix of treatments makes the biggest difference."),
  ("Is CO₂ laser safe for Indian skin?","Yes, when the settings and aftercare are chosen by a dermatologist. Expect a few days of redness and light scabbing."),
  ("Will acne come back after treatment?","Acne can flare with hormones or stress. A simple maintenance routine keeps most people clear."),
 ],
 "pig": [
  ("Can melasma be cured?","Melasma can be controlled very well, but it can return with sun or hormones. That is why maintenance and sunscreen matter."),
  ("Are skin lightening creams safe?","Some over the counter creams contain steroids that damage skin. Only use what your dermatologist prescribes."),
  ("How soon will I see a difference?","Most people see visible lightening in 6 to 8 weeks, with steady improvement after that."),
 ],
 "laser": [
  ("Is laser hair reduction permanent?","It gives long term reduction. Most people lose most of the treated hair, and a few top up sessions a year keep it that way."),
  ("Does laser work on dark skin?","Yes, with the right laser and settings. A patch test comes first."),
  ("Can any tattoo be removed?","Most tattoos fade a lot over several sessions. Black ink responds best, some colours need more sessions."),
 ],
 "age": [
  ("What does a Hydrafacial do?","It cleanses, gently exfoliates, extracts and hydrates in one session, for clean and glowing skin with no downtime."),
  ("Will fillers look fake?","Not when they are placed conservatively by a dermatologist. Our goal is a rested look, never an altered face."),
  ("When should I start anti-ageing care?","Sunscreen and a good routine from your twenties. Treatments can start whenever you notice changes that bother you."),
 ],
 "peel": [
  ("Will my skin peel a lot?","Most medical peels cause light flaking for 2 to 4 days at most. Many cause none at all."),
  ("Can I have a peel in summer?","Yes, with strict sun protection. Your doctor may choose a gentler peel."),
  ("Is a peel safe for sensitive skin?","Often yes, with a mild peel and proper prep. We decide after examining your skin."),
 ],
 "derm": [
  ("Do you treat children?","Yes. Many conditions such as eczema and pityriasis alba are common in children and respond well to gentle treatment."),
  ("Is vitiligo treatable?","Yes. Medicines, phototherapy and, for stable patches, vitiligo surgery can bring back colour."),
  ("Are my visits confidential?","Always, including for sexually transmitted infections."),
 ],
 "surg": [
  ("Will it leave a scar?","Most removals heal with a small, faint mark. We choose the technique that leaves the least."),
  ("Is mole removal safe?","Yes, after a doctor checks the mole. Any mole that looks unusual is sent for testing."),
  ("Can I go back to work the same day?","Usually yes. You just keep the area clean and dry as advised."),
 ],
}

FACILITIES = [
 ("Skin", "Medical dermatology", [("Eczema","skin-disease-treatment"),("Allergy","skin-disease-treatment"),("Acne","acne-scar-treatment"),("Melasma","pigmentation-melasma-treatment"),("Infections","skin-disease-treatment"),("Vitiligo","skin-disease-treatment"),("Autoimmune disorders","skin-disease-treatment"),("Psoriasis","skin-disease-treatment"),("Pigmentary disorders","pigmentation-melasma-treatment"),("Scars","acne-scar-treatment"),("Warts, tags and corns","skin-disease-treatment"),("Sexually transmitted disease","skin-disease-treatment")]),
 ("Anti-ageing", "Aesthetic care", [("Hydrafacial","anti-ageing-hydrafacial"),("Medifacial","anti-ageing-hydrafacial"),("Skin tightening","anti-ageing-hydrafacial"),("Anti-wrinkle treatment","anti-ageing-hydrafacial"),("Oxygeneo therapy","anti-ageing-hydrafacial"),("Non-surgical facelift","anti-ageing-hydrafacial"),("Vampire facelift","anti-ageing-hydrafacial"),("Hollywood facial","anti-ageing-hydrafacial"),("IV glutathione","anti-ageing-hydrafacial"),("Double chin reduction","anti-ageing-hydrafacial"),("Chemical peel","chemical-peels"),("Stretch marks","anti-ageing-hydrafacial"),("Fillers","anti-ageing-hydrafacial")]),
 ("Lasers", "Medical grade", [("Laser hair reduction","laser-treatment-ahmedabad"),("Beard shaping","laser-treatment-ahmedabad"),("Scar removal laser","acne-scar-treatment"),("Pigment removal","pigmentation-melasma-treatment"),("Tattoo removal","laser-treatment-ahmedabad"),("Laser toning","laser-treatment-ahmedabad")]),
 ("Hair", "Trichology and transplant", [("Baldness treatment","hair-loss-treatment"),("Hair fall treatment","hair-loss-treatment"),("PRP","hair-loss-treatment"),("Growth factor (GFC)","hair-loss-treatment"),("Hair transplant","hair-transplant-ahmedabad"),("Mesotherapy","hair-loss-treatment")]),
 ("Surgery", "Minor procedures", [("Mole removal","mole-cyst-skin-tag-removal"),("Cyst removal","mole-cyst-skin-tag-removal"),("Skin tag removal","mole-cyst-skin-tag-removal"),("Nail removal","mole-cyst-skin-tag-removal"),("Ear lobe repair","mole-cyst-skin-tag-removal"),("Vitiligo surgery","mole-cyst-skin-tag-removal")]),
]

DOCTORS = [
 dict(img="doctor-female", name="Dr. Sohini Soneji Shah", cred="MBBS, MD (Dermatology)", role="Dermatologist, trichologist and hair transplant surgeon",
      bio="Dr. Sohini brings medical precision and an aesthetic eye to every plan. She leads the institute's skin programmes, from acne and pigmentation to anti-ageing, with care designed around Indian skin.",
      book="Anti-ageing or Hydrafacial", schema_cred="MBBS, MD Dermatology"),
 dict(img="doctor-male", name="Dr. Malhar Shah", cred="MBBS, MD, FIHTS, PGDMLPE (Gold Medal)", role="Dermatologist, trichologist and hair transplant surgeon",
      bio="Trained at B.J. Medical College and VS Hospital, with a hair transplant fellowship under an American Board of Hair Restoration Surgery certified surgeon. He uses FUE instruments imported from the USA and Turkey for natural, dense, lifelong results.",
      book="Hair transplant", schema_cred="MBBS, MD, FIHTS, PGDMLPE"),
]

THEMES = [
 ("Patients describe Dr. Malhar as deeply knowledgeable, explaining every option clearly before starting.", "Mentioned often in Google reviews"),
 ("A clean, modern clinic. Hygiene and infrastructure come up again and again.", "Mentioned often in Google reviews"),
 ("Personal treatment plans with clear improvement in skin and hair.", "Mentioned often in Google reviews"),
]

HOURS_ROWS = '<table class="hours"><tbody><tr data-dow="1,2,3,4,5"><td>Monday to Friday</td><td>10 am to 1 pm, 5 to 8 pm</td></tr><tr data-dow="6"><td>Saturday</td><td>10 am to 1 pm</td></tr><tr data-dow="0"><td>Sunday</td><td>Closed</td></tr></tbody></table>'

# ------------------------------------------------------------------ schema
CLINIC = {
 "@type": ["MedicalClinic", "MedicalBusiness"], "@id": BASE + "#clinic",
 "name": "TRETĀ Derma Skin and Hair Institute", "alternateName": ["Treta Derma", "TRETA Derma"],
 "url": BASE, "logo": BASE + "assets/logo-badge.png", "image": BASE + "assets/og.jpg",
 "telephone": PHONE, "medicalSpecialty": "Dermatology", "priceRange": "₹₹",
 "slogan": "Be wise. Choose right.",
 "address": {"@type": "PostalAddress", "streetAddress": "402, 4th Floor, Sigma Esquire, Above Domino's, Opp. Kankaria", "addressLocality": "Maninagar, Ahmedabad", "addressRegion": "Gujarat", "postalCode": "380008", "addressCountry": "IN"},
 "hasMap": GMAPS, "areaServed": {"@type": "City", "name": "Ahmedabad"},
 "openingHoursSpecification": [
   {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "10:00", "closes": "13:00"},
   {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "17:00", "closes": "20:00"},
   {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "13:00"}],
 "aggregateRating": {"@type": "AggregateRating", "ratingValue": "5.0", "reviewCount": "101", "bestRating": "5"},
 "sameAs": [IG, FB],
 "availableService": [{"@type": "MedicalProcedure", "name": t["nav"], "url": BASE + t["slug"] + ".html"} for t in T],
}
def physician(d):
    return {"@type": "Physician", "name": d["name"], "medicalSpecialty": "Dermatology", "description": d["role"], "hasCredential": d["schema_cred"],
            "image": BASE + "assets/doctors/" + d["img"] + ".jpg", "worksFor": {"@id": BASE + "#clinic"}}

def ld(*objs):
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": list(objs)}, ensure_ascii=False) + "</script>"

def crumbs_ld(items):
    return {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": BASE + u} for i, (n, u) in enumerate(items)]}

def faq_ld(qs):
    return {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in qs]}

# ------------------------------------------------------------------ shell
WA_SVG = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12.04 2C6.58 2 2.13 6.45 2.13 11.91c0 1.75.46 3.45 1.32 4.95L2.05 22l5.25-1.38a9.9 9.9 0 0 0 4.74 1.21c5.46 0 9.91-4.45 9.91-9.91C21.95 6.45 17.5 2 12.04 2Zm5.8 14.13c-.24.68-1.42 1.32-1.95 1.36-.5.05-.97.24-3.27-.68-2.77-1.09-4.52-3.92-4.66-4.1-.13-.18-1.120-1.49-1.12-2.84 0-1.35.71-2.01.96-2.29.25-.27.55-.34.73-.34l.52.01c.17.01.39-.06.61.47.24.55.79 1.9.86 2.04.07.14.11.3.02.48-.09.18-.14.3-.27.46-.14.16-.29.36-.41.48-.14.14-.28.29-.12.56.16.27.71 1.17 1.52 1.9 1.05.93 1.93 1.22 2.2 1.36.27.14.43.11.59-.07.16-.18.68-.79.86-1.06.18-.27.36-.23.61-.14.25.09 1.59.75 1.86.89.27.14.45.2.52.32.07.11.07.66-.17 1.33Z"/></svg>'
PHONE_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2"/></svg>'
CAL_SVG = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/></svg>'
BRAND = '<a class="brand" href="./" aria-label="TRETĀ Derma home"><span class="mark" aria-hidden="true">T</span><span class="wm"><b>TRETĀ</b><span>Derma</span></span></a>'

def header(active):
    dd = "".join(f'<a href="{t["slug"]}.html"><span class="ic" aria-hidden="true">{ICONS[t["icon"]]}</span><span><b>{t["nav"]}</b><small>{t["short"]}</small></span></a>' for t in T)
    cur = lambda k: ' aria-current="page"' if k == active else ""
    sub = "".join(f'<a href="{t["slug"]}.html">{t["nav"]}</a>' for t in T)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="hdr"><div class="wrap">{BRAND}
<nav class="nav" aria-label="Main"><div class="dd"><button type="button" aria-expanded="false">Treatments</button><div class="dd-menu">{dd}</div></div>
<a href="hair-transplant-ahmedabad.html"{cur("ht")}>Hair transplant</a><a href="results.html"{cur("results")}>Results</a><a href="doctors.html"{cur("doctors")}>Doctors</a><a href="./#faq">FAQ</a><a href="./#visit">Visit</a></nav>
<div class="hdr-cta"><a class="icon-btn" href="tel:{PHONE}" aria-label="Call the clinic">{PHONE_SVG}</a><a class="btn btn-ink" href="book.html" data-book="">Book a visit <span class="arrow">→</span></a>
<button class="icon-btn burger" type="button" aria-label="Open menu" aria-expanded="false"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7"><path d="M4 8h16M4 16h16"/></svg></button></div></div></header>
<div class="mnav" aria-label="Mobile menu"><a href="./">Home</a><a href="treatments.html">Treatments</a><div class="sub">{sub}</div><a href="results.html">Results</a><a href="doctors.html">Doctors</a><a href="./#faq">FAQ</a><a href="./#visit">Visit us</a><a class="btn btn-ink" href="book.html">Book a visit</a></div>'''

def footer():
    tl = "".join(f'<li><a href="{t["slug"]}.html">{t["nav"]}</a></li>' for t in T[:7])
    return f'''<footer class="ftr"><div class="wrap"><div class="fgrid">
<div>{BRAND}<p class="tag">Be wise.<br>Choose right.</p><p>Skin and hair institute in Maninagar, Ahmedabad.<br>Two MD dermatologists. One standard of care.</p></div>
<div><h4>Treatments</h4><ul>{tl}<li><a href="treatments.html">All treatments</a></li></ul></div>
<div><h4>Clinic</h4><ul><li><a href="results.html">Before and after</a></li><li><a href="doctors.html">Our doctors</a></li><li><a href="book.html">Book a visit</a></li><li><a href="./#faq">FAQ</a></li><li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li><li><a href="{FB}" target="_blank" rel="noopener">Facebook</a></li></ul></div>
<div><h4>Visit</h4><ul><li>402, 4th Floor, Sigma Esquire,<br>Above Domino's, Opp. Kankaria,<br>Maninagar, Ahmedabad 380008</li><li><a href="tel:{PHONE}">{PHONE_D}</a></li><li>Mon to Fri, 10 to 1 and 5 to 8<br>Saturday, 10 to 1</li></ul></div></div>
<p class="areas">Patients visit us from Maninagar, Kankaria, Khokhra, Isanpur, Ghodasar, Vatva, Jashodanagar, Bhairavnath, Narol, CTM, Paldi, Satellite and across Ahmedabad.</p>
<div class="giant" aria-hidden="true">TRETĀ</div><div class="fbase"><span>© 2026 TRETĀ Derma Skin and Hair Institute. All rights reserved.</span><span>Information here is educational and does not replace an in-clinic consultation. Individual results vary.</span></div></div></footer>
<nav class="mbar" aria-label="Quick actions"><a href="tel:{PHONE}">{PHONE_SVG} Call</a><a href="#" data-chat="">{WA_SVG} Chat</a><button class="b" type="button" data-book="">{CAL_SVG} Book</button></nav>
<dialog class="book" id="book-dialog" aria-label="Book a consultation"><div class="book-shell"></div></dialog>'''

def page(fname, title, desc, body, active="", schema="", og_type="website"):
    preload = '<link rel="preload" as="image" href="assets/photo/hero.jpg" imagesrcset="assets/photo/hero-m.jpg 1200w, assets/photo/hero.jpg 2800w" imagesizes="100vw">' if fname == "index.html" else ""
    url = BASE + ("" if fname == "index.html" else fname)
    pre = '<div class="pre" aria-hidden="true"><div class="pre-word">' + ''.join(f'<span><span>{c}</span></span>' for c in 'TRETĀ') + '</div><div class="pre-foot"><span>Skin and Hair Institute</span><span class="pre-n">0</span></div><i class="pre-bar"></i></div>' if fname == "index.html" else ""
    icons_js = "window.TRETA_ICONS=" + json.dumps(ICONS) + ";"
    return f'''<!doctype html>
<html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{url}">
<meta name="robots" content="index,follow,max-image-preview:large"><meta name="theme-color" content="#F4F2EE">
<meta name="geo.region" content="IN-GJ"><meta name="geo.placename" content="Maninagar, Ahmedabad">
<meta property="og:type" content="{og_type}"><meta property="og:site_name" content="TRETĀ Derma"><meta property="og:locale" content="en_IN">
<meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}assets/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{BASE}assets/og.jpg">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="apple-touch-icon" href="assets/logo-badge.png">
<link rel="preconnect" href="https://api.fontshare.com"><link rel="preconnect" href="https://cdn.fontshare.com" crossorigin>{preload}
<link href="https://api.fontshare.com/v2/css?f[]=gambetta@300,301,400&f[]=general-sans@400,500,600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css?v={V}"><link rel="stylesheet" href="assets/v2.css?v={V}">
<script>(function(d){{var m=!matchMedia("(prefers-reduced-motion: reduce)").matches;try{{if(sessionStorage.getItem("pre"))d.classList.add("nopre");if(sessionStorage.getItem("nav"))d.classList.add("navin")}}catch(e){{}}if(m){{d.classList.add("m");setTimeout(function(){{if(!window.gsap)d.classList.remove("m")}},3500)}}}})(document.documentElement)</script>
{schema}
</head><body class="pg-{fname[:-5]}">
{pre}<div class="curtain" aria-hidden="true"></div><div class="cur" aria-hidden="true"><span></span></div>
{header(active)}
<main id="main">{body}</main>
{footer()}
<script>{icons_js}</script><script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script><script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script><script src="https://unpkg.com/lenis@1.1.13/dist/lenis.min.js" defer></script><script src="assets/site.js?v={V}" defer></script><script src="assets/v2.js?v={V}" defer></script>
</body></html>'''

def faq_html(qs):
    return '<div class="faq">' + "".join(f'<details class="rv"><summary>{E(q)}<i aria-hidden="true"></i></summary><div class="a"><p>{E(a)}</p></div></details>' for q, a in qs) + "</div>"

def cta_block(h="Your skin and hair,<br><em>in expert hands.</em>", p="Book a consultation in under a minute, or message the clinic team on WhatsApp. We reply during clinic hours.", preset=""):
    return f'''<section class="cta ink"><div class="wrap"><span class="eyebrow">Be wise. Choose right.</span><h2 class="display split" style="margin-top:22px">{h}</h2>
<p class="lead" style="margin-left:auto;margin-right:auto">{p}</p><div class="row"><a class="btn btn-paper" href="book.html" data-book="{E(preset)}">{CAL_SVG} Book a consultation</a><a class="btn btn-wa" href="https://wa.me/{WA}" data-chat="">{WA_SVG} Chat on WhatsApp</a></div></div></section>'''

def visit_block():
    return f'''<section class="sec" id="visit"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Visit</span><h2 class="h2 split">Opposite Kankaria,<br><em>in Maninagar.</em></h2></div>
<p class="lead rv">Fourth floor of Sigma Esquire, right above Domino's. Easy to find, with parking nearby. <span data-status class="status" style="margin-top:14px"></span></p></div>
<div class="visit"><div class="vcard rv"><dl style="margin:0">
<div class="vrow"><dt>Address</dt><dd>402, 4th Floor, Sigma Esquire,<br>Above Domino's, Opp. Kankaria,<br>Maninagar, Ahmedabad 380008<br><a class="tlink" href="{GMAPS}" target="_blank" rel="noopener">Get directions</a></dd></div>
<div class="vrow"><dt>Hours</dt><dd>{HOURS_ROWS}</dd></div>
<div class="vrow"><dt>Call</dt><dd><a class="tlink" href="tel:{PHONE}">{PHONE_D}</a></dd></div>
<div class="vrow"><dt>Follow</dt><dd><a class="tlink" href="{IG}" target="_blank" rel="noopener">Instagram</a> &nbsp; <a class="tlink" href="{FB}" target="_blank" rel="noopener">Facebook</a></dd></div></dl>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:22px"><a class="btn btn-ink" href="book.html" data-book="">Book a visit</a><a class="btn btn-line" href="https://wa.me/{WA}" data-chat="">{WA_SVG} WhatsApp</a></div></div>
<div class="map rv d1"><iframe title="Map to TRETĀ Derma in Maninagar, Ahmedabad" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=Treta%20Derma%20Skin%20and%20Hair%20Institute%20Sigma%20Esquire%20Maninagar%20Ahmedabad&output=embed"></iframe></div></div></div></section>'''

def doctors_block(full=False):
    cards = "".join(f'''<article class="doc rv d{i}"><div class="ph"><img src="assets/doctors/{d["img"]}.jpg" alt="{d["name"]}, dermatologist at TRETĀ Derma Ahmedabad" loading="lazy" width="800" height="1199"></div>
<div class="bd"><span class="cred">{d["cred"]}</span><h3>{d["name"]}</h3><span class="role">{d["role"]}</span><p>{d["bio"]}</p><a class="btn btn-ink" href="book.html" data-book="{d["book"]}">Book with {d["name"].split()[1]} <span class="arrow">→</span></a></div></article>''' for i, d in enumerate(DOCTORS))
    return f'<div class="docs">{cards}</div>'

def results_grid(slugs, gid="res-grid", filters=True):
    f = ""
    if filters:
        f = (f'<div class="filters rv" data-for="#{gid}" role="group" aria-label="Filter results">' +
             "".join(f'<button type="button" data-cat="{c}" aria-pressed="{str(c=="all").lower()}">{n}</button>' for c, n in [("all","All"),("hair","Hair"),("skin","Skin"),("procedure","Procedures")]) + "</div>")
    return f + f'<div class="grid-res" id="{gid}">' + "".join(res_card(s, i) for i, s in enumerate(slugs)) + "</div>"

# ------------------------------------------------------------------ home
def home():
    marq = "".join(f"<span>{w}</span>" for w in ["Acne", "Acne scars", "Melasma", "Hair transplant", "PRP and GFC", "Chemical peels", "Laser hair reduction", "Hydrafacial", "Alopecia", "Vitiligo", "Anti-ageing", "Tattoo removal"]) * 2
    disc = [("01","Skin","Acne, pigmentation, eczema, vitiligo and every everyday concern.","skin-disease-treatment","acne"),
            ("02","Anti-ageing","Hydrafacial, fillers and tightening that look natural.","anti-ageing-hydrafacial","hydrafacial"),
            ("03","Lasers","Hair reduction, tattoo removal, toning and scar lasers.","laser-treatment-ahmedabad","laser"),
            ("04","Hair transplant","FUE and DHI, planned and performed by a dermatologist.","hair-transplant-ahmedabad","hair")]
    disc_html = "".join(f'<a href="{u}.html" class="rv"><span class="n">{n}</span><span class="t">{t}</span><span class="d">{d}</span><span class="go" aria-hidden="true">→</span><span class="peek" aria-hidden="true"><img src="assets/photo/{img}-s.jpg" alt="" loading="lazy"></span></a>' for n, t, d, u, img in disc)
    tabs = "".join(f'<button type="button" class="tab" role="tab" id="tab-{i}" aria-controls="pn-{i}" aria-selected="{str(i==0).lower()}" tabindex="{0 if i==0 else -1}">{c}<span>{len(items)}</span></button>' for i, (c, s, items) in enumerate(FACILITIES))
    panels = "".join(f'<div class="panel{" on" if i==0 else ""}" id="pn-{i}" role="tabpanel" aria-labelledby="tab-{i}"><h3 class="h3">{s}</h3><div class="pills">' + "".join(f'<a class="pill" href="{u}.html">{n} <span class="arrow">→</span></a>' for n, u in items) + "</div></div>" for i, (c, s, items) in enumerate(FACILITIES))
    cards = "".join(pcard(t, i, t["short"] + ".") for i, t in enumerate(T))
    stages = [dict(t="Day 1", d="Grafts are placed in one sitting under local anaesthesia. You go home the same evening.", len=6, keep=1),
              dict(t="Weeks 2 to 6", d="Transplanted hairs shed. This is normal and expected, the roots stay safely in place.", len=3, keep=.35),
              dict(t="Month 3", d="New, fine hair starts to grow through, slowly at first.", len=22, keep=.7),
              dict(t="Month 6", d="Clear, visible improvement. Most people see the change in the mirror now.", len=52, keep=.95),
              dict(t="Months 9 to 12", d="The final result. Hair thickens and matures, and keeps growing for life.", len=80, keep=1)]
    ticks = "".join(f'<button type="button">{s["t"]}</button>' for s in stages)
    quotes = "".join(f'<figure class="quote rv d{i}" style="margin:0"><span class="stars" aria-label="5 stars">★★★★★</span><p>“{q}”</p><small>{s}</small></figure>' for i, (q, s) in enumerate(THEMES))
    body = f'''
<section class="hero-full"><picture><source media="(max-width:760px)" srcset="assets/photo/hero-m.jpg"><img class="hero-img" src="assets/photo/hero.jpg" alt="Woman with healthy, glowing skin in warm sunlight" fetchpriority="high" width="2800" height="1867"></picture>
<div class="wrap"><span class="status" data-status></span>
<h1 class="display split">Skin and hair,<br><em>chosen wisely.</em></h1>
<p class="lead rv">A skin and hair institute in Maninagar, Ahmedabad, led by two MD dermatologists. Acne, pigmentation, hair loss and FUE hair transplant, treated with evidence, not guesswork.</p>
<div class="hero-ctas rv d1"><a class="btn btn-white" href="book.html" data-book="">{CAL_SVG} Book a consultation</a><a class="btn glass" href="https://wa.me/{WA}" data-chat="">{WA_SVG} Chat on WhatsApp</a></div>
<div class="hero-foot rv d2"><a class="rating-pill" href="{REVIEWS}" target="_blank" rel="noopener"><b>5.0</b><span><span class="stars" aria-hidden="true">★★★★★</span><small>101 reviews on Google</small></span></a>
<a class="mini-res glass" href="results.html"><img src="assets/ba/ht-hairline-1-after.jpg?v=4" alt=""><span><small>Real patient results</small><b>See 13 before and afters →</b></span></a></div></div></section>

<div class="marquee" aria-hidden="true"><div class="track">{marq}</div></div>

<section class="sec" style="padding-bottom:0"><div class="wrap"><div class="trust">
<div class="rv"><b>5.0</b><span>Google rating from 101 patient reviews</span></div>
<div class="rv d1"><b>2</b><span>MD dermatologists and trichologists</span></div>
<div class="rv d2"><b>60+</b><span>Skin, hair, laser and surgical treatments</span></div>
<div class="rv d3"><b>1 day</b><span>FUE hair transplant, with US and Turkish instruments</span></div></div></div></section>

<section class="sec"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">What we do</span><h2 class="h2 split">Four disciplines,<br><em>one roof.</em></h2></div>
<p class="lead rv">Everything from a first pimple to a full hair transplant, handled by the same two doctors, so your care stays joined up.</p></div>
<div class="disc">{disc_html}</div></div></section>

<section class="sec paper"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Find your concern</span><h2 class="h2 split">What would you<br><em>like to treat?</em></h2></div>
<p class="lead rv">Pick a category and tap a concern to see how we treat it. Not sure? Message us a photo on WhatsApp and we will guide you.</p></div>
<div class="finder rv"><div class="tabs" role="tablist" aria-label="Treatment categories">{tabs}</div><div>{panels}</div></div></div></section>

<section class="sec" id="results"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Real patients, real results</span><h2 class="h2 split">Drag to see<br><em>the difference.</em></h2></div>
<p class="lead rv">Unretouched before and after photos from our own patients, shared with consent. Identities are protected.</p></div>
{results_grid([r[0] for r in RESULTS[:6]], "home-res", filters=False)}
<div style="margin-top:44px;display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap"><p class="res-note" style="margin:0">Individual results vary. Photos used with patient consent.</p><a class="btn btn-line" href="results.html">See all 13 results <span class="arrow">→</span></a></div></div></section>

<section class="sec paper" id="treatments"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Signature treatments</span><h2 class="h2 split">Care that is<br><em>specific to you.</em></h2></div>
<p class="lead rv">Every plan starts with a diagnosis. Here is where most of our patients begin.</p></div><div class="pcards">{cards}</div></div></section>

<section class="sec" id="doctors"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Your doctors</span><h2 class="h2 split">Two specialists.<br><em>Every single visit.</em></h2></div>
<p class="lead rv">You are always seen by an MD dermatologist, never handed to a technician for diagnosis.</p></div>{doctors_block()}</div></section>

<section class="sec ink"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Your first visit</span><h2 class="h2 split">Simple from<br><em>the first message.</em></h2></div>
<p class="lead rv">No pressure, no package selling. A clear diagnosis and a plan you understand.</p></div>
<div class="photo-band rv" style="margin:0 0 clamp(40px,6vw,70px)"><img src="assets/photo/glow-s.jpg" alt="Calm, clean treatment room experience" loading="lazy"></div>
<div class="steps"><div class="step rv"><h3>Reach out</h3><p>Book online in a minute or message us on WhatsApp. Photos help.</p></div>
<div class="step rv d1"><h3>Consult</h3><p>Your dermatologist examines your skin or scalp and finds the cause.</p></div>
<div class="step rv d2"><h3>Plan</h3><p>A written plan with sessions, timelines and what to expect at each step.</p></div>
<div class="step rv d3"><h3>Follow up</h3><p>Progress photos at every visit, and a team a message away.</p></div></div></div></section>

<section class="sec ink" style="padding-top:0"><div class="wrap"><div class="tl" data-stages='{E(json.dumps(stages))}'>
<div><span class="eyebrow">Hair transplant timeline</span><h2 class="h2 split" style="margin-top:16px">How your new hair<br><em>grows in.</em></h2>
<p class="tl-stage" aria-live="polite"></p><p class="lead tl-copy"></p>
<label class="sr" for="tl-r">Months after transplant</label><input id="tl-r" class="tl-range" type="range" min="0" max="4" step="1" value="0"><div class="tl-ticks">{ticks}</div>
<p style="margin-top:34px"><a class="btn btn-paper" href="hair-transplant-ahmedabad.html">Hair transplant at TRETĀ <span class="arrow">→</span></a></p></div>
<div class="scalp rv" aria-hidden="true"><svg viewBox="0 0 400 260"><path class="ground" d="M10 236 Q200 160 390 236 L390 260 L10 260Z"/></svg></div></div></div></section>

<section class="sec" id="reviews"><div class="wrap rev"><div class="rv"><span class="eyebrow">Loved by patients</span><p class="big-score" style="margin:18px 0 6px">5.0</p><span class="stars" style="font-size:22px">★★★★★</span>
<p class="lead" style="margin:16px 0 26px">Rated 5.0 from 101 reviews on Google. Read them in full, unfiltered.</p><a class="btn btn-line" href="{REVIEWS}" target="_blank" rel="noopener">Read reviews on Google <span class="arrow">↗</span></a></div>
<div class="quotes">{quotes}</div></div></section>

<section class="sec paper" id="faq"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Good questions</span><h2 class="h2 split">Straight answers,<br><em>from our doctors.</em></h2></div>
<p class="lead rv">Still curious? Ask us anything on WhatsApp. A real person from the clinic replies.</p></div>{faq_html(FAQS["ht"][:5] + FAQS["hair"][:1] + FAQS["acne"][:1] + FAQS["pig"][:1])}</div></section>
{visit_block()}
{cta_block()}'''
    schema = ld(dict(CLINIC, employee=[physician(d) for d in DOCTORS]),
                {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "TRETĀ Derma", "inLanguage": "en-IN", "publisher": {"@id": BASE + "#clinic"}},
                faq_ld(FAQS["ht"][:5] + FAQS["hair"][:1] + FAQS["acne"][:1] + FAQS["pig"][:1]))
    return page("index.html", "TRETĀ Derma | Dermatologist and Hair Transplant Clinic in Maninagar, Ahmedabad",
                "TRETĀ Derma Skin and Hair Institute in Maninagar, Ahmedabad. MD dermatologists for acne, pigmentation, hair fall, lasers and FUE hair transplant. Rated 5.0 on Google. Book on WhatsApp.",
                body, "home", schema)

# ------------------------------------------------------------------ treatment page
def treatment(t):
    i = T.index(t)
    glance = "".join(f"<div><small>{a}</small><b>{b}</b></div>" for a, b in t["glance"])
    treats = "".join(f"<li>{x}</li>" for x in t["treats"])
    how = "".join(f'<div class="rv"><b>0{k+1}</b><div><h3>{h}</h3><p>{p}</p></div></div>' for k, (h, p) in enumerate(t["how"]))
    res = ""
    if t["results"]:
        res = f'''<section class="sec"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Results</span><h2 class="h2 split">Before and after,<br><em>at TRETĀ.</em></h2></div><p class="lead rv">Real patients, photographed in clinic. Drag the handle to compare.</p></div>{results_grid(t["results"], "res-" + t["slug"], filters=False)}<p class="res-note">Individual results vary. Photos used with patient consent.</p></div></section>'''
    rel = "".join(f'<a href="{x["slug"]}.html">{x["nav"]} <span class="arrow">→</span></a>' for x in (T[(i+1) % len(T)], T[(i+2) % len(T)], T[(i+3) % len(T)]))
    qs = FAQS[t["faq"]]
    plain = t["h1"].replace("<em>", "").replace("</em>", "")
    body = f'''
<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span>/</span><a href="treatments.html">Treatments</a><span>/</span><span aria-current="page">{t["nav"]}</span></nav>
<div class="phero-grid"><div><h1 class="display split">{t["h1"]}</h1><p class="lead rv">{t["lead"]}</p>
<div class="hero-ctas rv d1" style="margin-top:30px"><a class="btn btn-ink" href="book.html" data-book="">{CAL_SVG} Book a consultation</a><a class="btn btn-line" href="https://wa.me/{WA}" data-chat="">{WA_SVG} Ask on WhatsApp</a></div></div>
<div class="phero-img rv d2">{photo(t["slug"], "")}</div></div><div class="glance strip rv">{glance}</div></div></section>
<section class="sec paper"><div class="wrap two"><div><span class="eyebrow">What we treat</span><h2 class="h2 split" style="margin:16px 0 30px">Common reasons<br><em>people come in.</em></h2><ul class="ticks rv">{treats}</ul></div>
<div><span class="eyebrow">How it works</span><div class="prose rv" style="margin:16px 0 26px"><p>{t["body"]}</p></div><div class="how">{how}</div></div></div></section>
{res}
<section class="sec{" paper" if res else ""}"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Questions</span><h2 class="h2 split">{t["nav"]},<br><em>answered.</em></h2></div><p class="lead rv">Timelines are typical. Your doctor confirms your exact plan after examining you.</p></div>{faq_html(qs)}</div></section>
<section class="sec" style="padding-top:0{";padding-top:clamp(80px,11vw,150px)" if not res else ""}"><div class="wrap"><span class="eyebrow">Also at TRETĀ</span><div class="related" style="margin-top:22px">{rel}</div></div></section>
{cta_block(preset="")}'''
    schema = ld({"@type": "MedicalWebPage", "name": t["title"], "url": BASE + t["slug"] + ".html", "about": {"@type": "MedicalProcedure", "name": t["nav"], "description": t["lead"]},
                 "audience": "https://schema.org/Patient", "inLanguage": "en-IN", "lastReviewed": "2026-10-24", "reviewedBy": {"@type": "Physician", "name": "Dr. Malhar Shah"}, "provider": {"@id": BASE + "#clinic"}},
                CLINIC, faq_ld(qs), crumbs_ld([("Home", ""), ("Treatments", "treatments.html"), (t["nav"], t["slug"] + ".html")]))
    return page(t["slug"] + ".html", t["title"], t["desc"], body, "ht" if t["slug"].startswith("hair-transplant") else "", schema, "article")

def treatments_hub():
    cards = "".join(pcard(t, i, t["short"] + ".") for i, t in enumerate(T))
    allf = "".join(f'<div class="rv" style="margin-bottom:34px"><h3 class="h3" style="margin-bottom:16px">{c} <span class="muted small" style="font-family:var(--sans)">{s}</span></h3><div class="pills">' + "".join(f'<a class="pill" href="{u}.html">{n}</a>' for n, u in items) + "</div></div>" for c, s, items in FACILITIES)
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span>/</span><span aria-current="page">Treatments</span></nav>
<div class="phero-grid"><div><h1 class="display split">Every treatment,<br><em>under one roof.</em></h1><p class="lead rv">Skin, anti-ageing, lasers, hair and minor surgery. More than 60 treatments, all planned by MD dermatologists in Maninagar, Ahmedabad.</p></div>
<div class="rv d1"><a class="btn btn-ink" href="book.html" data-book="">{CAL_SVG} Book a consultation</a></div></div></div></section>
<section class="sec paper" style="padding-top:80px"><div class="wrap"><div class="pcards">{cards}</div></div></section>
<section class="sec"><div class="wrap"><div class="sec-hd"><div><span class="eyebrow">Full menu</span><h2 class="h2 split">The complete<br><em>list.</em></h2></div><p class="lead rv">Tap any treatment to learn how it works.</p></div>{allf}</div></section>{cta_block()}'''
    schema = ld(CLINIC, crumbs_ld([("Home", ""), ("Treatments", "treatments.html")]))
    return page("treatments.html", "Skin, Hair and Laser Treatments in Ahmedabad | TRETĀ Derma", "All skin, hair, laser, anti-ageing and minor surgical treatments at TRETĀ Derma, Maninagar, Ahmedabad. Planned by MD dermatologists.", body, "", schema)

def results_page():
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span>/</span><span aria-current="page">Results</span></nav>
<div class="phero-grid"><div><h1 class="display split">Before and after,<br><em>unretouched.</em></h1><p class="lead rv">Thirteen real patient results across hair transplant, hair loss, acne, pigmentation and skin procedures. Drag any photo to compare.</p></div>
<div class="rv d1"><a class="btn btn-ink" href="book.html" data-book="">{CAL_SVG} Start your own</a></div></div></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap">{results_grid([r[0] for r in RESULTS])}<p class="res-note">Individual results vary. Patient identities are protected and photos are used with consent.</p></div></section>{cta_block("Your result<br><em>could be next.</em>")}'''
    schema = ld(CLINIC, crumbs_ld([("Home", ""), ("Results", "results.html")]))
    return page("results.html", "Before and After Results | Hair Transplant, Acne, Melasma | TRETĀ Derma Ahmedabad", "Real before and after photos from TRETĀ Derma patients in Ahmedabad: FUE hair transplant, GFC, alopecia, acne scars, melasma, warts and more.", body, "results", schema)

def doctors_page():
    body = f'''<section class="phero"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span>/</span><span aria-current="page">Doctors</span></nav>
<h1 class="display split">The doctors<br><em>behind TRETĀ.</em></h1><p class="lead rv">Two MD dermatologists, trichologists and hair transplant surgeons. Every consultation, every plan and every procedure is theirs.</p></div></section>
<section class="sec" style="padding-top:20px"><div class="wrap">{doctors_block(True)}</div></section>
<section class="sec paper"><div class="wrap two"><div><span class="eyebrow">Our approach</span><h2 class="h2 split" style="margin-top:16px">Be wise.<br><em>Choose right.</em></h2></div>
<div class="prose rv"><p>Skin and hair care is full of quick fixes and loud promises. We do the opposite. We diagnose first, explain clearly, and recommend only what your skin or scalp needs.</p><p>That is what the name stands for. TRETĀ is built on three things: an accurate diagnosis, evidence based treatment, and honest follow up.</p><p><a class="tlink" href="https://www.instagram.com/tretaderma/" target="_blank" rel="noopener">Follow our skin and hair education on Instagram ↗</a></p></div></div></section>
{cta_block("Meet your<br><em>dermatologist.</em>")}'''
    schema = ld(CLINIC, *[physician(d) for d in DOCTORS], crumbs_ld([("Home", ""), ("Doctors", "doctors.html")]))
    return page("doctors.html", "Dr. Malhar Shah and Dr. Sohini Soneji Shah | Dermatologists in Ahmedabad | TRETĀ Derma", "Meet Dr. Malhar Shah (MD, FIHTS) and Dr. Sohini Soneji Shah (MD Dermatology), dermatologists, trichologists and hair transplant surgeons at TRETĀ Derma, Maninagar, Ahmedabad.", body, "doctors", schema)

def book_page():
    body = f'''<section class="phero" style="padding-bottom:40px"><div class="wrap"><nav class="crumbs" aria-label="Breadcrumb"><a href="./">Home</a><span>/</span><span aria-current="page">Book</span></nav>
<div class="phero-grid" style="align-items:start"><div><h1 class="display split">Book your<br><em>visit.</em></h1><p class="lead rv">Choose a concern, a doctor and a time. Your request goes straight to the clinic on WhatsApp, and the team confirms your slot in reply.</p>
<div class="vcard rv" style="margin-top:34px"><dl style="margin:0"><div class="vrow"><dt>Prefer to call?</dt><dd><a class="tlink" href="tel:{PHONE}">{PHONE_D}</a></dd></div><div class="vrow"><dt>Hours</dt><dd>{HOURS_ROWS}</dd></div><div class="vrow"><dt>Status</dt><dd><span data-status class="status"></span></dd></div></dl></div></div>
<div class="booking-inline bk-inline rv d1"></div></div></div></section>{visit_block()}'''
    schema = ld(CLINIC, crumbs_ld([("Home", ""), ("Book", "book.html")]))
    return page("book.html", "Book a Dermatologist Appointment in Maninagar, Ahmedabad | TRETĀ Derma", "Book a skin, hair or hair transplant consultation at TRETĀ Derma, Maninagar, Ahmedabad. Pick a doctor and time online, confirm on WhatsApp.", body, "", schema)

def notfound():
    body = f'<section class="phero" style="min-height:70vh"><div class="wrap"><h1 class="display">Page not<br><em>found.</em></h1><p class="lead">The page may have moved. Try the home page or book a consultation.</p><div class="hero-ctas" style="margin-top:30px"><a class="btn btn-ink" href="/treta/">Go home</a><a class="btn btn-line" href="/treta/book.html">Book a visit</a></div></div></section>'
    s = page("404.html", "Page not found | TRETĀ Derma", "This page could not be found.", body)
    return s.replace('<head><meta charset="utf-8">', '<head><meta charset="utf-8"><base href="/tretaV2/"><meta name="robots" content="noindex">', 1).replace('<meta name="robots" content="index,follow,max-image-preview:large">', "")

# ------------------------------------------------------------------ write
def w(name, s):
    with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f: f.write(s)

from v2_home import home2
def home_v2():
    body, qs = home2(globals())
    schema = ld(dict(CLINIC, employee=[physician(d) for d in DOCTORS]), {"@type": "WebSite", "@id": BASE + "#site", "url": BASE, "name": "TRETĀ Derma", "inLanguage": "en-IN", "publisher": {"@id": BASE + "#clinic"}}, faq_ld(qs))
    return page("index.html", "TRETĀ Derma | Dermatologist and Hair Transplant Clinic in Maninagar, Ahmedabad", "TRETĀ Derma Skin and Hair Institute in Maninagar, Ahmedabad. MD dermatologists for acne, pigmentation, hair fall, lasers and FUE hair transplant. Rated 5.0 on Google. Book on WhatsApp.", body, "index", schema)

pages = {"index.html": home_v2(), "treatments.html": treatments_hub(), "results.html": results_page(), "doctors.html": doctors_page(), "book.html": book_page(), "404.html": notfound()}
for t in T: pages[t["slug"] + ".html"] = treatment(t)
for k, v in pages.items(): w(k, v)
urls = [""] + ["treatments.html", "results.html", "doctors.html", "book.html"] + [t["slug"] + ".html" for t in T]
w("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{BASE}{u}</loc><lastmod>2026-10-24</lastmod><priority>{'1.0' if not u else '0.8'}</priority></url>\n" for u in urls) + "</urlset>\n")
w("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {BASE}sitemap.xml\n")
w(".nojekyll", "")
bad = [k for k, v in pages.items() if "—" in v or "–" in v]
print("pages:", len(pages), "| dash check:", bad or "clean")
