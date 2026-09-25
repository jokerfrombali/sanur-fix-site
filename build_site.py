# -*- coding: utf-8 -*-
"""Статический сайт мастера в Сануре, до 20 языков.
Тексты: i18n/<lang>.json (en — основной, в корне сайта). Статьи: content/<lang>/A###.json. Стили: tools/style.css.
Запуск: python build_site.py → папка site/."""
import hashlib, html, json, pathlib, re, shutil, sys
from urllib.parse import quote

# ======== ЗАПОЛНИТЬ ДАННЫМИ МАСТЕРА ========
DOMAIN = "https://jokerfrombali.github.io"  # домен сайта (без слэша в конце)
BASE = "/sanur-fix-site"                # подпапка; для своего домена — ""
PREVIEW = True                          # True = закрыт от индексации (просмотр на GitHub Pages)
BRAND = "Bali Fix"                      # название
WHATSAPP = "6280000000000"              # номер WhatsApp без +
PHONE = "+62 800-0000-0000"
GBP_URL = ""   # ссылка на карточку в Google Картах, когда появится
PRICES = {}    # {"srv-santehnik": "from 300,000 IDR"} — пусто = «по запросу»
EMERGENCY = False  # True — только если мастер реально выезжает вечером/в выходные: пометка в шапке
# Мастер: заполнить реальными данными. Пустые поля не показываются. photo — URL или путь от корня сайта.
MASTER = {"name": "", "photo": "", "years": "", "languages": "", "warranty": {"en": "", "ru": ""}}
# Отзывы — только настоящие (копия из Google). [{"name": "Anna", "text": "...", "stars": 5}]
REVIEWS = []
# Работы «было/стало». [{"slug": "pool-leak-sindhu", "area": "Sindhu", "title": {"en": "...", "ru": "..."},
#   "text": {"en": "...", "ru": "..."}, "before": "URL", "after": "URL", "service": "srv-remont-bassejna"}]
PROJECTS = []
# DEMO = True: подставляются примерные мастер/отзывы/работы/срочный вызов с пометкой «Пример» на каждом блоке.
# Перед запуском: заполнить MASTER/REVIEWS/PROJECTS реальными данными и поставить DEMO = False.
DEMO = True
if DEMO:
    EMERGENCY = True
    MASTER = {"name": "Jupri", "bio": {"en": "Sample profile: Jupri has fixed villa plumbing, water heaters and pools in Bali for 12 years. He comes himself, explains what is wrong in plain English and sends photos after every job.", "ru": "Пример профиля: Джупри 12 лет чинит сантехнику, бойлеры и бассейны на виллах Бали. Приезжает сам, понятно объясняет, что сломалось, и присылает фото после каждой работы."}, "photo": "https://images.unsplash.com/photo-1749532125405-70950966b0e5?auto=format&fit=crop&w=900&h=1125&q=70",
              "years": "12", "languages": "English, Bahasa", "warranty": {"en": "3 months on work", "ru": "3 месяца на работу"}}
    REVIEWS = [
        {"name": "Sample — Anna, Sindhu", "stars": 5, "text": "Sample review: our pool pump stopped the day before guests arrived. Sent a photo on WhatsApp, got a price in ten minutes, fixed the same afternoon."},
        {"name": "Sample — Mark, Semawang", "stars": 5, "text": "Sample review: found a hidden leak under the kitchen that two other people missed. Sent before-and-after photos, very clear pricing."},
        {"name": "Sample — Olga, Sanur Kaja", "stars": 5, "text": "Sample review: regular pool service while we are in Europe. Report with photos after every visit — exactly what we needed."},
    ]
    _u = lambda p: f"https://images.unsplash.com/{p}?auto=format&fit=crop&w=700&h=900&q=70"
    PROJECTS = [
        {"slug": "sample-pool-leak-sindhu", "area": "Sindhu", "service": "srv-remont-bassejna",
         "title": {"en": "Sample: pool losing 3 cm a day", "ru": "Пример: бассейн терял 3 см в день"},
         "text": {"en": "Sample project. Bucket test confirmed a leak, pressure test found a cracked return line. Section replaced, pool refilled, level stable after a week.",
                  "ru": "Пример работы. Тест с ведром подтвердил протечку, опрессовка нашла треснувшую трубу возврата. Участок заменён, бассейн долит, уровень стабилен через неделю."},
         "before": _u("photo-1724660583299-2356fe880e54"), "after": _u("photo-1509600110300-21b9d5fedeb7")},
        {"slug": "sample-water-heater-semawang", "area": "Semawang", "service": "srv-bojler",
         "title": {"en": "Sample: no hot water in a 3-bedroom villa", "ru": "Пример: нет горячей воды на вилле с 3 спальнями"},
         "text": {"en": "Sample project. Heating element burnt out from scale (brackish well water). Element and anode replaced, filter added before the heater.",
                  "ru": "Пример работы. ТЭН сгорел из-за накипи (солоноватая вода из скважины). Заменены ТЭН и анод, перед бойлером поставлен фильтр."},
         "before": _u("photo-1676210134190-3f2c0d5cf58d"), "after": _u("photo-1595514535431-1243b02c3b70")},
        {"slug": "sample-green-pool-mertasari", "area": "Mertasari", "service": "srv-chistka-bassejna",
         "title": {"en": "Sample: green pool back to clear in 3 days", "ru": "Пример: зелёный бассейн чистый за 3 дня"},
         "text": {"en": "Sample project. Shock treatment, brushing, filter backwash twice a day, water balanced. Weekly service set up afterwards.",
                  "ru": "Пример работы. Шоковое хлорирование, щётка, промывка фильтра дважды в день, баланс воды. После — еженедельное обслуживание."},
         "before": _u("photo-1614667288602-9ac6e37318a7"), "after": _u("photo-1596178067639-5c6e68aea6dc")},
    ]
# ===========================================

HERE = pathlib.Path(__file__).parent
ROOT = HERE / "site"
THEME = "pro"  # pro — основной дизайн (синий + белый + зелёный WhatsApp); classic — прежний вариант в цветах Five Star
sys.path.insert(0, str(HERE / "tools"))
from articles_plan import HUB_EN

# порядок = порядок в переключателе; en — в корне
LANGS = [("en", "English"), ("ru", "Русский"), ("id", "Bahasa Indonesia"), ("nl", "Nederlands"), ("de", "Deutsch"), ("fr", "Français"),
         ("it", "Italiano"), ("es", "Español"), ("pt", "Português"), ("pl", "Polski"), ("uk", "Українська"), ("cs", "Čeština"),
         ("sv", "Svenska"), ("da", "Dansk"), ("nb", "Norsk"), ("fi", "Suomi"), ("tr", "Türkçe"), ("zh", "中文"), ("ja", "日本語"), ("ko", "한국어")]
L = {}
for code, _ in LANGS:
    f = HERE / "i18n" / f"{code}.json"
    if f.exists():
        L[code] = json.loads(f.read_text(encoding="utf-8"))
LANG_NAME = dict(LANGS)
ACTIVE = [c for c, _ in LANGS if c in L]
# ключи, которых ещё нет в переводе, берутся из en; длинные блоки (local_*) показываются только если переведены
RAW_UI = {c: dict(L[c]["ui"]) for c in ACTIVE}
for c in ACTIVE:
    L[c]["ui"] = {**L["en"]["ui"], **RAW_UI[c]}
def has(lang, key):
    return key in RAW_UI[lang]
def tx(lang, d):
    """строка из словаря {lang: text} с откатом на en"""
    return d.get(lang) or d.get("en", "") if isinstance(d, dict) else d

# услуги: общий порядок и переводы с откатом на en
SRV = list(L["en"]["services"])
for c in ACTIVE:
    L[c]["services"] = {s: {**L["en"]["services"][s], **L[c]["services"].get(s, {})} for s in SRV}

from areas import AREAS, SERVICE_ISSUE
AREA_LANGS = ("en", "ru")  # страницы районов — только на этих языках (тексты районов есть только на них)
SLUGS = {"srv-santehnik": "plumber", "srv-protechki": "leak-repair", "srv-zasor": "blocked-drain", "srv-bojler": "water-heater",
         "srv-voda": "water-pump-filter", "srv-chistka-bassejna": "pool-cleaning", "srv-obsluzhivanie-bassejna": "pool-service",
         "srv-oborudovanie-bassejna": "pool-equipment", "srv-remont-bassejna": "pool-repair", "srv-septik": "septic",
         "srv-melkij-remont": "handyman", "srv-obsluzhivanie-villy": "villa-maintenance"}
SEC_EN = dict(sv="services", pr="prices", ar="areas", ct="contact", gd="guides")
SEC_RU = dict(sv="services", pr="prices", ar="areas", ct="contact", gd="stati")
def sec(lang, k):
    return (SEC_RU if lang == "ru" else SEC_EN)[k]
def sslug(lang, sid):
    return "services/" + SLUGS[sid]
def aname(lang, a):
    return a.get(lang) or a["en"]
def pre(lang):
    return "" if lang == "en" else lang + "/"
def url(lang, slug=""):
    return BASE + "/" + pre(lang) + (slug + "/" if slug else "")
# ---------- фото (Unsplash, заменить на реальные) ----------
U = "https://images.unsplash.com/"
def img(pid, w=900, h=None):
    return f"{U}{pid}?auto=format&fit=crop&w={w}{'&h=' + str(h) if h else ''}&q=70"
PH = {"hero": "photo-1676210134188-4c05dd172f89", "hero_villa": "photo-1720161263981-84281892ee4b", "sanur": "photo-1733281120655-8da3dc371514", "sanur2": "photo-1733281121312-6bec65d3c809",
      "srv-santehnik": "photo-1749532125405-70950966b0e5", "srv-protechki": "photo-1694875119129-d79757ef3780", "srv-zasor": "photo-1676210134050-6f12c6898395",
      "srv-bojler": "photo-1676210134190-3f2c0d5cf58d", "srv-voda": "photo-1676210133055-eab6ef033ce3", "srv-chistka-bassejna": "photo-1605702755163-4f303492e55f",
      "srv-obsluzhivanie-bassejna": "photo-1742353980377-b8e42932c590", "srv-oborudovanie-bassejna": "photo-1614667288602-9ac6e37318a7",
      "srv-remont-bassejna": "photo-1724660583299-2356fe880e54", "srv-septik": "photo-1606340671662-27ee685dd111", "srv-melkij-remont": "photo-1615974679600-665fb9468c4f",
      "srv-obsluzhivanie-villy": "photo-1634671651144-adbeca8623cb"}
LOGO = '''<svg width="38" height="38" viewBox="0 0 40 40" aria-hidden="true"><rect class="lg-bg" width="40" height="40" rx="9" fill="#003483"/><path d="M5 14h15a6 6 0 0 1 6 6v15" stroke="#fff" stroke-width="6" fill="none"/><rect x="15.5" y="9" width="4" height="10" rx="1" class="lg-acc" fill="#bb0b0e"/><rect x="21" y="23.5" width="10" height="4" rx="1" class="lg-acc" fill="#bb0b0e"/><path d="M27.5 9.5l3 3 5.5-6.5" class="lg-ok" stroke="#bb0b0e" stroke-width="2.8" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'''
FAVICON = "data:image/svg+xml," + quote(LOGO.replace('width="38" height="38" ', ''))
HUB_PHOTOS = json.loads((HERE / "tools" / "photos.json").read_text(encoding="utf-8"))
HUB_SRV = {"S": "srv-santehnik", "W": "srv-voda", "PC": "srv-chistka-bassejna", "PE": "srv-oborudovanie-bassejna",
           "PR": "srv-remont-bassejna", "K": "srv-septik", "R": "srv-melkij-remont", "V": "srv-obsluzhivanie-villy"}

WA_ICO = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 1.9 17.7L.3 23.7l6.1-1.6A11.8 11.8 0 0 0 20.5 3.5zM12 21.6c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.6.9 1-3.5-.2-.4A9.8 9.8 0 1 1 12 21.6zm5.4-7.3c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8 8 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1 1-1 2.5 1 2.9 1.2 3.1 2.1 3.2 5.1 4.5c1.9.8 2.6.9 3.6.7.6-.1 1.8-.7 2-1.4s.3-1.3.2-1.4-.3-.2-.6-.3z"/></svg>'
PHONE_ICO = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
CHECK_ICO = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
wa_i = lambda s=20: WA_ICO.format(s=s)
ph_i = lambda s=18: PHONE_ICO.format(s=s)
TEL = "tel:" + PHONE.replace(" ", "").replace("-", "")
e = html.escape

def wa_link(u, what=""):
    return f"https://wa.me/{WHATSAPP}?text={quote(u['wa_text'] + what)}"

def buttons(u, what=""):
    b = f'<div class="btns"><a class="btn wa" href="{wa_link(u, what)}">{wa_i()} {u["wa"]}</a>'
    if GBP_URL:
        b += f'<a class="btn ghost" href="{GBP_URL}">Google</a>'
    return b + "</div>"

def page(lang, slug, title, descr, body, alts, crumbs=None, schema=None, head=None, og=None, has_guides=True, wa_what=""):
    """alts: {lang: slug} — языковые версии этой страницы (для hreflang и переключателя)."""
    u = L[lang]["ui"]
    gl = lang if has_guides else "en"
    al = lang if lang in AREA_LANGS else "en"
    srv_links = "".join(f'<a href="{url(lang, sslug(lang, s))}">{L[lang]["services"][s]["name"]}</a>' for s in SRV)
    area_links = "".join(f'<a href="{url(al, a["slug"])}">{aname(al, a)}</a>' for a in AREAS)
    dd = lambda label, href, items, more: (f'<div class="dd"><a class="m" href="{href}">{label} <span class="car">▾</span></a><div class="ddm">{items}'
                                           f'<a class="all" href="{href}">{more} →</a></div></div>')
    ll = "".join(f'<a class="{"on" if c == lang else ""}" href="{url(c, alts.get(c, ""))}" hreflang="{c}" lang="{c}">{LANG_NAME[c]}</a>' for c in ACTIVE)
    links = [(url(gl, sec(gl, "gd")), u["guides"] if has_guides else u.get("guides_en", "Guides")),
             (url(lang, sec(lang, "pr")), u["prices"]), (url(lang, sec(lang, "ct")), u["contacts"])]
    if PROJECTS:
        links.insert(1, (url(lang, "work"), u["projects"]))
    nav = (f'<nav class="main">' + dd(u["services"], url(lang, sec(lang, "sv")), srv_links, u["all_services"])
           + dd(u["areas"], url(al, sec(al, "ar")), area_links, u["areas_h1"])
           + "".join(f'<a class="m" href="{h}">{n}</a>' for h, n in links) + "</nav>")
    tools_ = (f'<div class="htools">'
              f'<details class="langsel"><summary aria-label="{u["language"]}"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="9.5"/><path d="M2.5 12h19M12 2.5c2.6 2.8 3.9 6 3.9 9.5s-1.3 6.7-3.9 9.5c-2.6-2.8-3.9-6-3.9-9.5S9.4 5.3 12 2.5z"/></svg><span>{lang.upper()}</span></summary><div class="ll">{ll}</div></details>'
              f'<a class="hbtn" href="{wa_link(u, wa_what)}">{wa_i(18)} WhatsApp</a>'
              f'<button class="burger" aria-label="{u.get("menu", "Menu")}" onclick="document.body.classList.toggle(\'menu-open\')"><span></span></button></div>')
    mnav = (f'<div class="mnav"><h4>{u["services"]}</h4><div class="ll">{srv_links}</div><h4>{u["areas"]}</h4><div class="ll">{area_links}</div>'
            + "".join(f'<a class="big" href="{h}">{n}</a>' for h, n in links)
            + f'<h4>{u.get("language", "Language")}</h4><div class="ll">{ll}</div></div>')
    top = ""
    if head:
        cr = '<div class="crumbs"><a href="' + url(lang) + '">' + u["home"] + "</a> / " + " / ".join(
            f'<a href="{h}">{n}</a>' if h else n for n, h in (crumbs or [])) + "</div>"
        top = (f'<div class="phead"><img src="{img(head[0], 1920, 900)}" alt="" fetchpriority="high"><div class="wrap">{cr}'
               f'<h1>{head[1]}</h1><p>{head[2]}</p>{buttons(u, wa_what or head[1])}</div></div>')
    sch = schema if isinstance(schema, list) else ([schema] if schema else [])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in sch)
    hl = "".join(f'<link rel="alternate" hreflang="{c}" href="{DOMAIN}{url(c, s)}">' for c, s in alts.items())
    if "en" in alts:
        hl += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url("en", alts["en"])}">'
    svc = "".join(f'<a href="{url(lang, sslug(lang, s))}">{L[lang]["services"][s]["name"]}</a><br>' for s in SRV[:8])
    ars = "".join(f'<a href="{url(al, a["slug"])}">{aname(al, a)}</a><br>' for a in AREAS)
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(descr)}"><meta name="theme-color" content="#0b1f3a"><meta name="google" content="notranslate"><link rel="icon" href="{FAVICON}">
{'<meta name="robots" content="noindex,nofollow">' if PREVIEW else ''}<link rel="canonical" href="{DOMAIN}{url(lang, slug)}">{hl}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(descr)}"><meta property="og:image" content="{img(og or (head[0] if head else PH['hero']), 1200, 630)}"><meta property="og:locale" content="{lang}">
<link rel="preconnect" href="https://images.unsplash.com"><link rel="stylesheet" href="{BASE}/style.css?v={CSS_V}">{ld}</head><body>
<header><div class="wrap"><a class="logo" href="{url(lang)}">{LOGO}Bali<span>Fix</span></a>{nav}{tools_}</div></header>{mnav}
<main>{top}{body}</main>
<footer><div class="wrap"><div class="cols"><div><a class="logo" href="{url(lang)}">{LOGO}Bali<span>Fix</span></a><p>{u['tagline']}.<br>{u['badge']}.</p>
<p><a href="{wa_link(u)}">WhatsApp</a> · <a href="{TEL}">{PHONE}</a></p></div>
<div><h4>{u['services']}</h4>{svc}</div><div><h4>{u['areas']}</h4>{ars}</div>
<div><h4>{u['contacts']}</h4><a href="{wa_link(u)}">WhatsApp</a><br><a href="{TEL}">{PHONE}</a><br><a href="{url(gl, sec(gl, 'gd'))}">{u['guides']}</a><br><a href="{url(lang, sec(lang, 'pr'))}">{u['prices']}</a></div></div>
<div class="cred">{u['credits']}.</div></div></footer>
<script>document.addEventListener('click',e=>{{const a=e.target.closest('a[href^="https://wa.me"],a[href^="tel:"]');if(a&&window.gtag)gtag('event','generate_lead',{{method:a.href.split(':')[0]}});if(e.target.closest('.mnav a'))document.body.classList.remove('menu-open')}});(function(){{var h=document.querySelector('.hero,.phead'),lim=h?h.offsetHeight*0.6:300;function f(){{document.body.classList.toggle('scrolled',scrollY>lim)}}addEventListener('scroll',f,{{passive:true}});f()}})();</script>
<script src="{BASE}/lang.js?v={CSS_V}" defer></script>
</body></html>"""

def biz_schema(lang, area=None):
    served = [{"@type": "Place", "name": a["en"] + ", Bali"} for a in ([area] if area else AREAS)]
    return {"@context": "https://schema.org", "@type": "Plumber", "name": BRAND, "url": DOMAIN + url(lang), "telephone": PHONE, "image": img(PH["hero"], 1200),
            "areaServed": served, "sameAs": [GBP_URL] if GBP_URL else []}

pages = []
def write(lang, slug, content):
    p = ROOT / pre(lang) / slug / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    if slug != "404":
        pages.append((lang, slug))

def mapframe(q):
    return f'<iframe class="map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q={quote(q)}&z=13&output=embed" title="{e(q)}"></iframe>'
MAP = mapframe("Bali, Indonesia").replace("z=13", "z=10")

def load_articles():
    res = {}
    for lang in ACTIVE:
        d = HERE / "content" / lang
        res[lang] = {}
        seen = set()
        for f in sorted(d.glob("A*.json")) if d.exists() else []:
            try:
                a = json.loads(f.read_text(encoding="utf-8"))
            except Exception:
                continue
            a["slug"] = re.sub(r"[^a-z0-9-]+", "-", a["slug"].lower()).strip("-") or a["id"].lower()
            while a["slug"] in seen:
                a["slug"] += "-" + a["id"].lower()
            seen.add(a["slug"])
            res[lang][a["id"]] = a
    return res

def art_photo(a):
    pool = HUB_PHOTOS[a["hub"]]
    return pool[int(a["id"][1:]) % len(pool)][0]

def all_alts(fn, langs=None):
    return {c: fn(c) for c in (langs or ACTIVE)}

CSS_V = ""
def build():
    global CSS_V
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir()
    PRO_FONTS = "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');\n"
    (ROOT / "style.css").write_text(((PRO_FONTS if THEME == "pro" else "")
                                   + (HERE / "tools" / "style.css").read_text(encoding="utf-8")
                                   + ((HERE / "tools" / "theme_pro.css").read_text(encoding="utf-8") if THEME == "pro" else "")), encoding="utf-8")
    CSS_V = hashlib.md5((ROOT / "style.css").read_bytes()).hexdigest()[:8]
    (ROOT / "lang.js").write_text((HERE / "tools" / "langsuggest.js").read_text(encoding="utf-8"), encoding="utf-8")
    ARTS = load_articles()
    gpath = lambda lang, a: sec(lang, "gd") + "/" + HUB_EN[a["hub"]][0] + "/" + a["slug"]
    area_alts = lambda fn: {c: fn(c) for c in AREA_LANGS if c in ACTIVE}
    for lang in ACTIVE:
        D = L[lang]; u = D["ui"]; SV = D["services"]
        arts = ARTS[lang]
        has_g = bool(arts)
        has_a = lang in AREA_LANGS
        al = lang if has_a else "en"
        demo = f'<span class="demo">{u["sample"]}</span>' if DEMO else ""
        P = lambda slug, title, descr, body, alts, **kw: write(lang, slug, page(lang, slug, title, descr, body, alts, has_guides=has_g, **kw))

        # ---- общие блоки ----
        def scards(area=None, skip=None):
            return "".join(
                f'<a class="card" href="{url(lang, (area["slug"] + "/" + SLUGS[s]) if area else sslug(lang, s))}"><div class="im"><img loading="lazy" src="{img(PH[s], 700, 525)}" alt="{e(SV[s]["name"])}"></div>'
                f'<h3>{SV[s]["name"]}</h3><p>{SV[s]["items"][0]} · {SV[s]["items"][1]}</p></a>' for s in SRV if s != skip)
        def acards(exclude=None):
            return "".join(f'<a class="card area" href="{url(al, a["slug"])}"><div class="im"><img loading="lazy" src="{img(a["photo"], 700, 525)}" alt="{e(aname(al, a))}"></div>'
                           f'<h3>{aname(al, a)}</h3><p>{", ".join(a["subs"][:3])}</p></a>' for a in AREAS if a is not exclude)
        strip = '<div class="strip"><div class="wrap">' + "".join(f"<div>{CHECK_ICO}<span>{v}</span></div>" for v in u["trust"]) + "</div></div>"
        STEP_ICO = ['<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 8h3l2-3h6l2 3h3v11H4z"/><circle cx="12" cy="13" r="3.5"/></svg>',
                    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M3 12V4h8l10 10-8 8z"/><circle cx="7.5" cy="8.5" r="1.5"/></svg>',
                    '<svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.5-.5-.5-2.5z"/></svg>']
        steps = '<ol class="steps2">' + "".join(f'<li><i>{STEP_ICO[i]}</i><span class="n">0{i + 1}</span><b>{s}</b></li>' for i, s in enumerate(u["steps"])) + "</ol>"
        how = (f'<section class="how2"><div class="wrap"><div class="how-l"><div class="eyebrow">{u["how"]}</div><h2>{u["ready"]}</h2><p>{u["ready_sub"]}</p>'
               f'<a class="btn wa" href="{wa_link(u)}">{wa_i()} {u["wa"]}</a></div>{steps}</div></section>')
        why = (f'<section><div class="wrap"><div class="shead"><h2>{u["why"]}</h2></div><div class="why">'
               + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in u["why_items"]) + "</div></div></section>")
        mphoto = (f'<img class="mimg" src="{MASTER["photo"] if MASTER["photo"].startswith("http") else BASE + MASTER["photo"]}" alt="{e(MASTER["name"])}">'
                  if MASTER["photo"] else f'<div class="ph">{u["master_ph"]}<br>{u.get("photo_note", "")}</div>')
        facts = [(u["years"], MASTER["years"]), (u["langs"], MASTER["languages"]), (u["warranty"], tx(lang, MASTER["warranty"]))]
        facts_html = "".join(f'<div><b>{v}</b><span>{k}</span></div>' for k, v in facts if v)
        bio = tx(lang, MASTER.get("bio", {})) or u["master_txt"]
        master = (f'<section class="master2"><div class="wrap"><div class="m-photo">{mphoto}'
                  + (f'<div class="m-badge"><b>{e(MASTER["name"])}</b><span>{u["badge"]}</span></div>' if MASTER["name"] else "")
                  + f'</div><div class="m-body"><div class="eyebrow">{u["about_h"]} {demo}</div><h2>{e(MASTER["name"]) or u["master_h"]}</h2><p class="big">{e(bio)}</p>'
                  + (f'<div class="facts2">{facts_html}</div>' if facts_html else "")
                  + '<ul class="check two">' + "".join(f"<li>{t}</li>" for t in u["trust"]) + f'</ul>{buttons(u)}</div></div></section>')
        tel_a = f'<a href="{TEL}">{PHONE}</a>'
        inline = lambda what="": f'<p class="inl"><a href="{wa_link(u, what)}">{wa_i(18)} {u["ready"]}</a> {u["ready_sub"]}</p>'
        stars = lambda n: "★" * int(n) + "☆" * (5 - int(n))
        reviews = (f'<section class="alt"><div class="wrap"><div class="shead"><h2>{u["reviews_h"]} {demo}</h2>'
                   + (f'<p><a href="{GBP_URL}">{u["reviews_more"]} →</a></p>' if GBP_URL else "") + '</div><div class="revs">'
                   + "".join(f'<figure><div class="st">{stars(r.get("stars", 5))}</div><blockquote>{e(r["text"])}</blockquote><figcaption>{e(r["name"])}</figcaption></figure>' for r in REVIEWS[:6])
                   + "</div></div></section>") if REVIEWS else ""
        def pcard(p):
            return (f'<a class="card" href="{url(lang, "work/" + p["slug"])}"><div class="im ba"><img loading="lazy" src="{p["before"]}" alt=""><img loading="lazy" src="{p["after"]}" alt=""></div>'
                    f'<h3>{e(tx(lang, p["title"]))}</h3><p>{e(p["area"])}</p></a>')
        projects = (f'<section><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["projects"]} {demo}</div><h2>{u["projects_h1"]}</h2></div>'
                    f'<p><a href="{url(lang, "work")}">{u["projects_lead"]} →</a></p></div><div class="grid">{"".join(pcard(p) for p in PROJECTS[:4])}</div></div></section>') if PROJECTS else ""
        cta = (f'<section style="padding-top:0"><div class="wrap"><div class="cta"><div><h2>{u["ready"]}</h2><p>{u["ready_sub"]}</p></div>'
               f'<div class="btns"><a class="btn wa" href="{wa_link(u)}">{wa_i()} {u["wa"]}</a></div></div></div></section>')
        def acard_art(a):
            return (f'<a class="card" href="{url(lang, gpath(lang, a))}"><div class="im"><img loading="lazy" src="{img(art_photo(a), 700, 525)}" alt=""></div>'
                    f'<h3>{e(a["title"])}</h3><p>{e(a["meta"][:110])}…</p><span class="more">{u["read"]} →</span></a>')
        latest = list(arts.values())[:4]
        guides_block = (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["guides"]}</div><h2>{u["guides_h1"]}</h2></div>'
                        f'<p><a href="{url(lang, sec(lang, "gd"))}">{u["all_guides"]} ({len(arts)}) →</a></p></div><div class="grid">{"".join(acard_art(a) for a in latest)}</div></div></section>') if latest else ""
        areas_block = (f'<section class="alt"><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["areas"]}</div><h2>{u["choose_area"]}</h2></div>'
                       f'<p>{u["areas_lead"]}</p></div><div class="grid areas5">{acards()}</div></div></section>')
        def lead_form(what_default=""):
            opts = "".join(f"<option>{e(SV[x]['name'])}</option>" for x in SRV)
            wopts = "".join(f"<option>{e(w)}</option>" for w in u["when_opts"])
            return (f'<form class="lead-form" data-wa="https://wa.me/{WHATSAPP}?text=" data-pre="{e(u["wa_text"] + what_default)}" '
                    f'onsubmit="event.preventDefault();location.href=this.dataset.wa+encodeURIComponent(this.dataset.pre+this.w.value+String.fromCharCode(32,8212,32)+this.t.value)">'
                    f'<h3>{u["form_h"]}</h3><label>{u["form_what"]}</label><select name="w">{opts}</select><label>{u["form_when"]}</label><select name="t">{wopts}</select>'
                    f'<button class="btn wa" type="submit">{wa_i()} {u["form_btn"]}</button><p>{u["form_note"]}</p></form>')
        def hero(h1, lead, photo, what=""):
            rating = ""
            if REVIEWS:
                avg = sum(r.get("stars", 5) for r in REVIEWS) / len(REVIEWS)
                rating = f'<div class="rating"><span class="st">★★★★★</span>{u["rated"].replace("{r}", f"{avg:.1f}").replace("{n}", str(len(REVIEWS)))} {demo}</div>'
            feat = '<ul class="feat">' + "".join(f"<li>{CHECK_ICO}<span>{t}</span></li>" for t in u["trust"]) + "</ul>"
            plain = re.sub(r"<[^>]+>", "", h1)
            hcls = "xl" if len(plain) > 44 else ("l" if len(plain) > 32 else "s")
            return (f'<div class="hero pro"><img src="{img(photo, 2200, 1300)}" alt="" fetchpriority="high"><div class="wrap"><div>{rating}<h1 class="h-{hcls}">{h1}</h1>'
                    f'<p>{lead}</p>{feat}</div>{lead_form(what)}</div></div>')
        tc = [(MASTER["years"] + " " + u["years"]) if MASTER["years"] else u["only"], u["only"], u["pricing_items"][0][0], (f"★ {len(REVIEWS)} Google" if REVIEWS else u["pricing_items"][2][0])]
        tsub = [MASTER["languages"] or u["badge"], u["badge"], u["pricing_items"][0][1][:70] + "…", u["reviews_h"] if REVIEWS else u["pricing_items"][2][1][:70] + "…"]
        tcards = '<div class="wrap"><div class="tcards">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in zip(tc, tsub)) + "</div></div>"

        # ---- главная ----
        h1 = u["home_h1"].replace("Bali", "<em>Bali</em>", 1).replace("Бали", "<em>Бали</em>", 1)
        P("", f"{u['home_h1']} | {BRAND}", u["home_lead"][:155],
          hero(h1, u["home_lead"], PH["hero"]) + tcards
          + f'<section><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["services"]}</div><h2>{u["tagline"]}</h2></div><p>{u["ready_sub"]}</p></div><div class="grid">{scards()}</div></div></section>'
          + areas_block + how + master + reviews + projects + why + guides_block + cta,
          all_alts(lambda c: ""), schema=biz_schema(lang))

        # ---- услуги (общие по Бали) ----
        P(sec(lang, "sv"), f"{u['services']} — {u['tagline']}", u["home_lead"][:155],
          strip + f'<section><div class="wrap"><div class="grid">{scards()}</div></div></section>{areas_block}{how}{cta}', all_alts(lambda c: sec(c, "sv")),
          crumbs=[(u["services"], None)], head=(PH["sanur"], u["services"], u["home_lead"]))
        def service_body(s, area=None):
            v = SV[s]
            aN = aname(lang, area) if area else ""
            faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in v["faq"])
            hub = next((h for h, x in HUB_SRV.items() if x == s), None)
            rel = [a for a in arts.values() if a["hub"] == hub][:4] if hub else []
            local = ""
            if area and has_a:
                iss = [area["issues"][lang][i] for i in SERVICE_ISSUE[s]]
                local = (f'<section class="alt"><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["local_eyebrow"]}</div>'
                         f'<h2>{u["area_local_h"].replace("{area}", aN)}</h2></div><p>{area["intro"][lang]}</p></div><div class="local two">'
                         + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in iss)
                         + f'</div><p class="subs"><b>{u["area_subs_h"].replace("{area}", aN)}:</b> {", ".join(area["subs"])}.</p></div></section>')
            where = (f'<section><div class="wrap split"><div><div class="eyebrow">{u["areas"]}</div><h2>{u["map_h"]}</h2>'
                     + (f'<p class="big">{aN}: {", ".join(area["subs"])}.</p>' if area else f'<p class="big">{u["area_txt"]} {", ".join(aname(al, a) for a in AREAS)}.</p>')
                     + f'{inline(v["name"] + (" — " + aN if aN else ""))}</div>{mapframe(area["map"]) if area else MAP}</div></section>')
            other = ""
            if area:
                other = (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{v["name"]} — {u["other_areas"]}</h2></div><div class="chips">'
                         + "".join(f'<a href="{url(lang, x["slug"] + "/" + SLUGS[s])}">{v["name"]} — {aname(lang, x)}</a>' for x in AREAS if x is not area) + "</div></div></section>")
            else:
                other = (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{u["choose_area"]}</h2></div><div class="chips">'
                         + "".join(f'<a href="{url(al, x["slug"] + "/" + SLUGS[s])}">{v["name"]} — {aname(al, x)}</a>' for x in AREAS) + "</div></div></section>")
            return (strip + f'<section><div class="wrap split"><div><div class="eyebrow">{u["fix"]}</div><h2>{v["name"]}{(" — " + aN) if aN else ""}</h2><ul class="check">'
                    + "".join(f"<li>{x}</li>" for x in v["items"])
                    + f'</ul><p style="margin-top:22px"><b>{u["price"]}:</b> {PRICES.get(s, u["on_req"])} · <a href="{url(lang, sec(lang, "pr"))}">{u["prices"]}</a></p>{inline(v["name"])}</div>'
                    f'<img class="side" loading="lazy" src="{img(PH[s], 900, 1125)}" alt="{e(v["name"])}"></div></section>'
                    + local + how + master
                    + f'<section><div class="wrap narrow"><div class="eyebrow">{u["faq_h"]}</div><h2 class="h2s">{u["faq"]}</h2>{faq}{inline(v["name"])}</div></section>'
                    + reviews
                    + (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{u["related"]}</h2></div><div class="grid">{"".join(acard_art(a) for a in rel)}</div></div></section>' if rel else "")
                    + where + other + cta)
        for s in SRV:
            v = SV[s]
            sch = [{"@context": "https://schema.org", "@type": "Service", "name": v["name"] + " — Bali", "areaServed": [a["en"] + ", Bali" for a in AREAS], "provider": {"@type": "Plumber", "name": BRAND, "telephone": PHONE}},
                   {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in v["faq"]]}]
            h1s = v["name"] + {"en": " in Bali", "ru": " на Бали"}.get(lang, " — Bali")
            P(sslug(lang, s), f"{h1s} | {BRAND}", v["intro"][:155], service_body(s), all_alts(lambda c: sslug(c, s)),
              crumbs=[(u["services"], url(lang, sec(lang, "sv"))), (v["name"], None)], schema=sch, head=(PH[s], h1s, v["intro"]))

        # ---- районы: список, хаб района, район × услуга (только en/ru) ----
        if has_a:
            P(sec(lang, "ar"), f"{u['areas_h1']} | {BRAND}", u["areas_lead"],
              f'<section><div class="wrap"><div class="grid areas5">{acards()}</div></div></section>{how}{cta}',
              area_alts(lambda c: sec(c, "ar")), crumbs=[(u["areas"], None)], head=(PH["sanur2"], u["areas_h1"], u["areas_lead"]))
            for a in AREAS:
                aN = aname(lang, a)
                h1a = u["area_hub_h"].replace("{area}", aN)
                local = (f'<section><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["local_eyebrow"]}</div><h2>{u["area_local_h"].replace("{area}", aN)}</h2></div>'
                         f'<p>{a["intro"][lang]}</p></div><div class="local two">' + "".join(f"<div><h3>{x}</h3><p>{y}</p></div>" for x, y in a["issues"][lang])
                         + f'</div></div></section>')
                subs = (f'<section style="padding-top:0"><div class="wrap split"><div><div class="eyebrow">{aN}</div><h2 class="h2s">{u["area_subs_h"].replace("{area}", aN)}</h2>'
                        f'<div class="chips">' + "".join(f"<span>{x}</span>" for x in a["subs"]) + f'</div>{inline(aN)}</div>{mapframe(a["map"])}</div></section>')
                others = (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{u["other_areas"]}</h2></div><div class="grid areas5">{acards(exclude=a)}</div></div></section>')
                sch = [biz_schema(lang, a), {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": u["home"], "item": DOMAIN + url(lang)},
                    {"@type": "ListItem", "position": 2, "name": aN, "item": DOMAIN + url(lang, a["slug"])}]}]
                P(a["slug"], f"{h1a} | {BRAND}", a["intro"][lang][:155],
                  hero(h1a.replace(aN, f"<em>{aN}</em>", 1), a["intro"][lang], a["photo"], aN) + tcards
                  + local + f'<section class="alt"><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["services"]}</div><h2>{u["area_services_h"].replace("{area}", aN)}</h2></div></div><div class="grid">{scards(a)}</div></div></section>'
                  + how + subs + master + reviews + others + cta,
                  area_alts(lambda c: a["slug"]), schema=sch, wa_what=aN)
                for s in SRV:
                    v = SV[s]
                    h1s = f'{v["name"]} {u["in_area"].replace("{area}", aN)}'
                    intro = f'{a["intro"][lang]} {v["intro"]}'
                    sch = [{"@context": "https://schema.org", "@type": "Service", "name": h1s, "areaServed": a["en"] + ", Bali", "provider": {"@type": "Plumber", "name": BRAND, "telephone": PHONE}},
                           {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": ans}} for q, ans in v["faq"]]}]
                    P(a["slug"] + "/" + SLUGS[s], f"{h1s}, Bali | {BRAND}", intro[:155], service_body(s, a), area_alts(lambda c: a["slug"] + "/" + SLUGS[s]),
                      crumbs=[(aN, url(lang, a["slug"])), (v["name"], None)], schema=sch, head=(a["photo"], h1s, intro), wa_what=h1s)

        # ---- работы ----
        if PROJECTS:
            P("work", f"{u['projects_h1']} | {BRAND}", u["projects_lead"], f'<section><div class="wrap"><div class="grid">{"".join(pcard(p) for p in PROJECTS)}</div></div></section>{cta}',
              all_alts(lambda c: "work"), crumbs=[(u["projects"], None)], head=(PH["sanur"], u["projects_h1"], u["projects_lead"] + " " + demo))
            for p in PROJECTS:
                ps = p.get("service", "srv-santehnik")
                P("work/" + p["slug"], f"{tx(lang, p['title'])} — {p['area']} | {BRAND}", tx(lang, p["text"])[:155],
                  f'<section><div class="wrap split"><div><div class="eyebrow">{e(p["area"])}, Bali {demo}</div><h2>{e(tx(lang, p["title"]))}</h2><p class="big">{e(tx(lang, p["text"]))}</p>'
                  f'<p><a href="{url(lang, sslug(lang, ps))}">{SV[ps]["name"]} →</a></p>{inline()}</div><div class="ba2"><img src="{p["before"]}" alt="before"><img src="{p["after"]}" alt="after"></div></div></section>{cta}',
                  all_alts(lambda c: "work/" + p["slug"]), crumbs=[(u["projects"], url(lang, "work")), (e(tx(lang, p["title"])), None)], head=(PH["sanur"], e(tx(lang, p["title"])), e(p["area"])))
        # ---- цены / контакты ----
        rows = "".join(f"<tr><td><a href='{url(lang, sslug(lang, s))}'>{SV[s]['name']}</a></td><td>{PRICES.get(s, u['on_req'])}</td></tr>" for s in SRV)
        P(sec(lang, "pr"), f"{u['prices_h1']} | {BRAND}", u["prices_note"][:155],
          f'<section><div class="wrap"><div class="shead"><h2>{u["pricing_h"]}</h2></div><div class="why">'
          + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in u["pricing_items"]) + "</div></div></section>"
          f'<section style="padding-top:0"><div class="wrap narrow"><table><tr><th>{u["work"]}</th><th>{u["price"]}</th></tr>{rows}</table>{inline()}</div></section>{how}{cta}',
          all_alts(lambda c: sec(c, "pr")), crumbs=[(u["prices"], None)], head=(PH["srv-melkij-remont"], u["prices_h1"], u["prices_note"]))
        P(sec(lang, "ct"), f"{u['contacts_h1']} | {BRAND}", u["contacts_lead"],
          f'<section><div class="wrap split"><div><div class="eyebrow">WhatsApp · {u["call"]}</div><h2>{PHONE}</h2>{buttons(u)}'
          f'<div class="chips">' + "".join(f'<a href="{url(al, a["slug"])}">{aname(al, a)}</a>' for a in AREAS) + f'</div></div>{MAP}</div></section>',
          all_alts(lambda c: sec(c, "ct")), crumbs=[(u["contacts"], None)], schema=biz_schema(lang), head=(PH["sanur"], u["contacts_h1"], u["contacts_lead"]))

        # ---- статьи ----
        if not has_g:
            continue
        g_alts = {c: sec(c, "gd") for c in ACTIVE if ARTS[c]}
        def hubnav(on=None):
            return ('<div class="hubs">' + f'<a class="{"on" if on is None else ""}" href="{url(lang, sec(lang, "gd"))}">{u["all_guides"]}</a>'
                    + "".join(f'<a class="{"on" if on == h else ""}" href="{url(lang, sec(lang, "gd") + "/" + HUB_EN[h][0])}">{D["hubs"][h]}</a>' for h in HUB_EN) + "</div>")
        P(sec(lang, "gd"), f"{u['guides_h1']} | {BRAND}", u["guides_lead"],
          f'<section><div class="wrap">{hubnav()}<div class="grid">{"".join(acard_art(a) for a in arts.values())}</div></div></section>{cta}',
          g_alts, crumbs=[(u["guides"], None)], head=(PH["sanur"], u["guides_h1"], u["guides_lead"]))
        for h, (hs, _) in HUB_EN.items():
            ha = [a for a in arts.values() if a["hub"] == h]
            P(sec(lang, "gd") + "/" + hs, f"{D['hubs'][h]} — {u['guides']} | {BRAND}", u["guides_lead"],
              f'<section><div class="wrap">{hubnav(h)}<div class="grid">{"".join(acard_art(a) for a in ha)}</div></div></section>{cta}',
              {c: sec(c, "gd") + "/" + hs for c in g_alts}, crumbs=[(u["guides"], url(lang, sec(lang, "gd"))), (D["hubs"][h], None)],
              head=(HUB_PHOTOS[h][0][0], D["hubs"][h], u["guides_lead"]))
        for a in arts.values():
            srv = HUB_SRV[a["hub"]]
            secs = a["sections"]
            toc = "".join(f'<a href="#s{i}">{e(x["h2"])}</a>' for i, x in enumerate(secs, 1))
            c = f'<p class="lead">{e(a["intro"])}</p>'
            for i, x in enumerate(secs, 1):
                c += f'<h2 id="s{i}">{e(x["h2"])}</h2>' + "".join(f"<p>{e(p)}</p>" for p in x.get("paragraphs", []))
                if x.get("bullets"):
                    c += "<ul>" + "".join(f"<li>{e(b)}</li>" for b in x["bullets"]) + "</ul>"
                if i == 2:
                    c += (f'<div class="inline-cta"><div><b>{u["need_help"]}</b><br><span style="color:var(--muted)">{e(a.get("cta") or u["ready_sub"])}</span></div>'
                          f'<a class="btn wa" href="{wa_link(u, a["title"])}">{wa_i()} WhatsApp</a></div>')
            if a.get("faq"):
                c += f'<h2 id="faq">{u["faq_h"]}</h2>' + "".join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in a["faq"])
            c += (f'<div class="inline-cta"><div><b>{SV[srv]["name"]}</b><br><span style="color:var(--muted)">{u["ready_sub"]}</span></div>'
                  f'<a class="btn ghost" href="{url(lang, sslug(lang, srv))}">{u["services"]} →</a></div>')
            c += '<div class="chips">' + "".join(f'<a href="{url(al, x["slug"] + "/" + SLUGS[srv])}">{SV[srv]["name"]} — {aname(al, x)}</a>' for x in AREAS) + "</div>"
            rel = [o for o in arts.values() if o["hub"] == a["hub"] and o is not a][:4]
            body = (f'<div class="wrap art"><aside class="toc"><b>{u["toc"]}</b>{toc}</aside><article class="prose">{c}</article></div>'
                    + (f'<section style="padding-top:24px"><div class="wrap"><div class="shead"><h2>{u["related"]}</h2></div><div class="grid">{"".join(acard_art(o) for o in rel)}</div></div></section>' if rel else "") + cta)
            photo = art_photo(a)
            sch = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["meta"], "image": img(photo, 1200), "inLanguage": lang,
                    "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}}]
            if a.get("faq"):
                sch.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in a["faq"]]})
            alts = {c2: gpath(c2, ARTS[c2][a["id"]]) for c2 in ACTIVE if a["id"] in ARTS[c2]}
            P(gpath(lang, a), f"{a['title']} | {BRAND}", a["meta"], body, alts,
              crumbs=[(u["guides"], url(lang, sec(lang, "gd"))), (D["hubs"][a["hub"]], url(lang, sec(lang, "gd") + "/" + HUB_EN[a["hub"]][0])),
                      (e(a["title"][:40]) + ("…" if len(a["title"]) > 40 else ""), None)],
              schema=sch, head=(photo, e(a["title"]), e(a["intro"][:220])), og=photo)
    # 404, robots, sitemap
    u = L["en"]["ui"]
    write("en", "404", page("en", "404", "404", "", f"<section><div class='wrap'><h1>404</h1><p>{u['nf']} · <a href='{BASE}/'>Home</a></p></div></section>", {"en": ""}))
    shutil.move(str(ROOT / "404" / "index.html"), str(ROOT / "404.html"))
    (ROOT / "404").rmdir()
    (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}{BASE}/sitemap.xml\n", encoding="utf-8")
    sm = "".join(f"<url><loc>{DOMAIN}{url(l, s)}</loc></url>" for l, s in pages)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>', encoding="utf-8")
    print("pages:", len(pages), "| langs:", ",".join(ACTIVE), "| articles:", {k: len(v) for k, v in ARTS.items() if v})

if __name__ == "__main__":
    build()
