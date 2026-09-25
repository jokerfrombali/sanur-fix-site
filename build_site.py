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
BRAND = "Sanur Fix"                     # название (рабочее)
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
    MASTER = {"name": "Made", "photo": "https://images.unsplash.com/photo-1749532125405-70950966b0e5?auto=format&fit=crop&w=900&h=1125&q=70",
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

SRV = list(L["en"]["services"])  # порядок услуг
SLUGS = {"srv-santehnik": ("plumber-sanur", "santehnik-sanur"), "srv-protechki": ("leak-repair-sanur", "protechki-sanur"), "srv-zasor": ("blocked-drain-sanur", "prochistka-zasorov-sanur"), "srv-bojler": ("water-heater-sanur", "bojler-sanur"), "srv-voda": ("water-pump-filter-sanur", "nasosy-filtry-sanur"), "srv-chistka-bassejna": ("pool-cleaning-sanur", "chistka-bassejna-sanur"), "srv-obsluzhivanie-bassejna": ("pool-service-sanur", "obsluzhivanie-bassejna-sanur"), "srv-oborudovanie-bassejna": ("pool-equipment-sanur", "oborudovanie-bassejna-sanur"), "srv-remont-bassejna": ("pool-repair-sanur", "remont-bassejna-sanur"), "srv-septik": ("septic-sanur", "septik-kanalizaciya-sanur"), "srv-melkij-remont": ("handyman-sanur", "master-na-chas-sanur"), "srv-obsluzhivanie-villy": ("villa-maintenance-sanur", "obsluzhivanie-villy-sanur")}
SEC_EN = dict(sv="services", pr="prices", ar="area", ct="contact", gd="guides")
SEC_RU = dict(sv="uslugi", pr="ceny", ar="rajon", ct="kontakty", gd="stati")
def sec(lang, k):
    return (SEC_RU if lang == "ru" else SEC_EN)[k]
def sslug(lang, sid):
    return SLUGS[sid][1] if lang == "ru" else SLUGS[sid][0]
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
    b = f'<div class="btns"><a class="btn wa" href="{wa_link(u, what)}">{wa_i()} {u["wa"]}</a><a class="btn ghost" href="{TEL}">{ph_i()} {PHONE}</a>'
    if GBP_URL:
        b += f'<a class="btn ghost" href="{GBP_URL}">Google</a>'
    return b + "</div>"

def page(lang, slug, title, descr, body, alts, crumbs=None, schema=None, head=None, og=None, has_guides=True):
    """alts: {lang: slug} — языковые версии этой страницы (для hreflang и переключателя)."""
    u = L[lang]["ui"]
    gl = lang if has_guides else "en"
    links = [(url(lang, sec(lang, "sv")), u["services"]), (url(gl, sec(gl, "gd")), u["guides"] if has_guides else u.get("guides_en", "Guides")),
             (url(lang, sec(lang, "pr")), u["prices"]), (url(lang, sec(lang, "ar")), u["areas"]), (url(lang, sec(lang, "ct")), u["contacts"])]
    if PROJECTS:
        links.insert(2, (url(lang, "work"), u["projects"]))
    ll = "".join(f'<a class="{"on" if c == lang else ""}" href="{url(c, alts.get(c, ""))}" hreflang="{c}" lang="{c}">{LANG_NAME[c]}</a>' for c in ACTIVE)
    srv_links = "".join(f'<a href="{url(lang, sslug(lang, s))}">{L[lang]["services"][s]["name"]}</a>' for s in SRV)
    dd = (f'<div class="dd"><a class="m" href="{links[0][0]}">{links[0][1]} ▾</a><div class="ddm">{srv_links}'
          f'<a class="all" href="{links[0][0]}">{u["all_services"]} →</a></div></div>')
    nav = (dd + "".join(f'<a class="m" href="{h}">{n}</a>' for h, n in links[1:])
           + f'<details class="langsel"><summary>{lang.upper()} ▾</summary><div class="ll">{ll}</div></details>'
           + f'<a class="hbtn" href="{wa_link(u)}">{wa_i(16)} WhatsApp</a>'
           + f'<button class="burger" aria-label="{u.get("menu", "Menu")}" onclick="document.body.classList.toggle(\'menu-open\')"><span></span></button>')
    mnav = (f'<div class="mnav">' + "".join(f'<a class="big" href="{h}">{n}</a>' for h, n in links)
            + f'<a class="big" href="{TEL}">{PHONE}</a><h4>{u["services"]}</h4><div class="ll">{srv_links}</div>'
            + f'<h4>{u.get("language", "Language")}</h4><div class="ll">{ll}</div></div>')
    topbar = (f'<div class="topbar"><div class="wrap"><span>{u["tagline"]} · <b>{u["only"]}</b>'
              + (f' · <b class="urg">{u["emergency"]}{" · " + u["sample"] if DEMO else ""}</b>' if EMERGENCY else "")
              + f'</span><span><a href="{wa_link(u)}">WhatsApp</a> · <a href="{TEL}">{PHONE}</a></span></div></div>')
    top = ""
    if head:
        cr = '<div class="crumbs"><a href="' + url(lang) + '">' + u["home"] + "</a> / " + " / ".join(
            f'<a href="{h}">{n}</a>' if h else n for n, h in (crumbs or [])) + "</div>"
        top = (f'<div class="phead"><img src="{img(head[0], 1800, 900)}" alt="" fetchpriority="high"><div class="wrap">{cr}'
               f'<h1>{head[1]}</h1><p>{head[2]}</p>{buttons(u, head[1])}</div></div>')
    sch = schema if isinstance(schema, list) else ([schema] if schema else [])
    ld = "".join(f'<script type="application/ld+json">{json.dumps(s, ensure_ascii=False)}</script>' for s in sch)
    hl = "".join(f'<link rel="alternate" hreflang="{c}" href="{DOMAIN}{url(c, s)}">' for c, s in alts.items())
    if "en" in alts:
        hl += f'<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url("en", alts["en"])}">'
    svc = "".join(f'<a href="{url(lang, sslug(lang, s))}">{L[lang]["services"][s]["name"]}</a><br>' for s in SRV[:6])
    hubs = "".join(f'<a href="{url(gl, sec(gl, "gd") + "/" + HUB_EN[h][0])}">{L[gl]["hubs"][h]}</a><br>' for h in HUB_EN)
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(descr)}"><meta name="theme-color" content="#003483"><link rel="icon" href="{FAVICON}">
{'<meta name="robots" content="noindex,nofollow">' if PREVIEW else ''}<link rel="canonical" href="{DOMAIN}{url(lang, slug)}">{hl}
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(descr)}"><meta property="og:image" content="{img(og or (head[0] if head else PH['hero']), 1200, 630)}"><meta property="og:locale" content="{lang}">
<link rel="preconnect" href="https://images.unsplash.com"><link rel="stylesheet" href="{BASE}/style.css?v={CSS_V}">{ld}</head><body>
{topbar}<header><div class="wrap"><a class="logo" href="{url(lang)}">{LOGO}Sanur<span>Fix</span></a><nav>{nav}</nav></div></header>{mnav}
<main>{top}{body}</main>
<footer><div class="wrap"><div class="cols"><div><a class="logo" href="{url(lang)}">{LOGO}Sanur<span>Fix</span></a><p>{u['tagline']}.<br>{u['badge']}.</p>
<p><a href="{wa_link(u)}">WhatsApp</a> · <a href="{TEL}">{PHONE}</a></p></div>
<div><h4>{u['services']}</h4>{svc}</div><div><h4>{u['guides']}</h4>{hubs}</div>
<div><h4>{u['contacts']}</h4><a href="{wa_link(u)}">WhatsApp</a><br><a href="{TEL}">{PHONE}</a><br><a href="{url(lang, sec(lang, 'ar'))}">{u['areas']}</a><br><a href="{url(lang, sec(lang, 'pr'))}">{u['prices']}</a></div></div>
<div class="cred">{u['credits']}.</div></div></footer>
<script>document.addEventListener('click',e=>{{const a=e.target.closest('a[href^="https://wa.me"],a[href^="tel:"]');if(a&&window.gtag)gtag('event','generate_lead',{{method:a.href.split(':')[0]}});if(e.target.closest('.mnav a'))document.body.classList.remove('menu-open')}});</script>
</body></html>"""

def biz_schema(lang):
    return {"@context": "https://schema.org", "@type": "Plumber", "name": BRAND, "url": DOMAIN + url(lang), "telephone": PHONE, "image": img(PH["hero"], 1200),
            "areaServed": {"@type": "Place", "name": "Sanur, Denpasar Selatan, Bali"}, "sameAs": [GBP_URL] if GBP_URL else []}

pages = []
def write(lang, slug, content):
    p = ROOT / pre(lang) / slug / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    if slug != "404":
        pages.append((lang, slug))

MAP = '<iframe class="map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Sanur,+Denpasar+Selatan,+Bali&z=14&output=embed" title="Sanur map"></iframe>'

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

def all_alts(fn):
    return {c: fn(c) for c in ACTIVE}

CSS_V = ""
def build():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir()
    global CSS_V
    PRO_FONTS = "@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');\n"
    (ROOT / "style.css").write_text(((PRO_FONTS if THEME == "pro" else "")
                                   + (HERE / "tools" / "style.css").read_text(encoding="utf-8")
                                   + ((HERE / "tools" / "theme_pro.css").read_text(encoding="utf-8") if THEME == "pro" else "")), encoding="utf-8")
    CSS_V = hashlib.md5((ROOT / "style.css").read_bytes()).hexdigest()[:8]
    ARTS = load_articles()
    gpath = lambda lang, a: sec(lang, "gd") + "/" + HUB_EN[a["hub"]][0] + "/" + a["slug"]
    for lang in ACTIVE:
        D = L[lang]; u = D["ui"]; SV = D["services"]
        arts = ARTS[lang]
        has_g = bool(arts)
        areas_l = D["areas"]
        cards = "".join(f'<a class="card" href="{url(lang, sslug(lang, s))}"><div class="im"><img loading="lazy" src="{img(PH[s], 700, 525)}" alt="{e(SV[s]["name"])}"></div>'
                        f'<h3>{SV[s]["name"]}</h3><p>{SV[s]["items"][0]} · {SV[s]["items"][1]}</p></a>' for s in SRV)
        strip = '<div class="strip"><div class="wrap">' + "".join(f"<div>{CHECK_ICO}<span>{v}</span></div>" for v in u["trust"]) + "</div></div>"
        steps = '<ol class="steps">' + "".join(f"<li>{s}</li>" for s in u["steps"]) + "</ol>"
        how = f'<section class="dark"><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["how"]}</div><h2>{u["ready"]}</h2></div><p>{u["ready_sub"]}</p></div>{steps}</div></section>'
        chips = '<div class="chips"><span>Sanur</span>' + "".join(f"<span>{a}</span>" for a in areas_l) + "</div>"
        why = (f'<section><div class="wrap"><div class="shead"><h2>{u["why"]}</h2></div><div class="why">'
               + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in u["why_items"]) + "</div></div></section>")
        demo = f'<span class="demo">{u["sample"]}</span>' if DEMO else ""
        # (1) блок доверия: реальные данные мастера; пустые поля не выводятся
        mphoto = (f'<img class="mimg" src="{MASTER["photo"] if MASTER["photo"].startswith("http") else BASE + MASTER["photo"]}" alt="{e(MASTER["name"])}">'
                  if MASTER["photo"] else f'<div class="ph">{u["master_ph"]}<br>{u.get("photo_note", "")}</div>')
        facts = [(u["years"], MASTER["years"]), (u["langs"], MASTER["languages"]), (u["warranty"], tx(lang, MASTER["warranty"]))]
        facts_html = "".join(f'<div><b>{v}</b><span>{k}</span></div>' for k, v in facts if v)
        promises = "".join(f"<li>{t}</li>" for t in u["trust"])
        master = (f'<section style="padding-top:0"><div class="wrap master">{mphoto}'
                  f'<div><div class="eyebrow">{u["about_h"]} {demo}</div><h2>{MASTER["name"] or u["master_h"]}</h2>'
                  + (f'<div class="facts">{facts_html}</div>' if facts_html else f'<p>{u["master_txt"]}</p>')
                  + f'<ul class="check">{promises}</ul><div style="margin-top:26px">{buttons(u)}</div></div></div></section>')
        # (10) телефон/WhatsApp прямо в тексте
        tel_a = f'<a href="{TEL}">{PHONE}</a>'
        inline = lambda: f'<p class="inl">{u["call_or_wa"].replace("{phone}", tel_a).replace("WhatsApp", f"<a href={chr(34)}{wa_link(u)}{chr(34)}>WhatsApp</a>", 1)}</p>'
        # (2)(3) местная специфика и кварталы
        def local(full=True):
            if not has(lang, "local_items"):
                return ""
            items = u["local_items"] if full else u["local_items"][:3]
            more = "" if full else f'<p style="margin-top:28px"><a class="more" href="{url(lang, sslug(lang, "srv-santehnik"))}">{u["local_h"]} →</a></p>'
            return (f'<section class="{"" if full else "alt"}"><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["local_eyebrow"]}</div><h2>{u["local_h"]}</h2></div>'
                    f'<p>{u["local_intro"]}</p></div><div class="local">' + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in items) + f"</div>{more}</div></section>")
        hoods = (f'<section style="padding-top:0"><div class="wrap narrow"><div class="eyebrow">{u["areas"]}</div><h2 class="h2s">{u["hoods_h"]}</h2>'
                 f'<p class="big">{u["hoods_txt"]}</p>{chips}{inline()}</div></section>') if has(lang, "hoods_txt") else ""
        # (4) отзывы — только настоящие
        stars = lambda n: "★" * int(n) + "☆" * (5 - int(n))
        reviews = (f'<section class="alt"><div class="wrap"><div class="shead"><h2>{u["reviews_h"]} {demo}</h2>'
                   + (f'<p><a href="{GBP_URL}">{u["reviews_more"]} →</a></p>' if GBP_URL else "") + '</div><div class="revs">'
                   + "".join(f'<figure><div class="st">{stars(r.get("stars", 5))}</div><blockquote>{e(r["text"])}</blockquote><figcaption>{e(r["name"])}</figcaption></figure>' for r in REVIEWS[:6])
                   + "</div></div></section>") if REVIEWS else ""
        # (5) работы
        def pcard(p):
            return (f'<a class="card" href="{url(lang, "work/" + p["slug"])}"><div class="im ba"><img loading="lazy" src="{p["before"]}" alt=""><img loading="lazy" src="{p["after"]}" alt=""></div>'
                    f'<h3>{e(tx(lang, p["title"]))}</h3><p>{e(p["area"])}</p></a>')
        projects = (f'<section><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["projects"]} {demo}</div><h2>{u["projects_h1"]}</h2></div>'
                    f'<p><a href="{url(lang, "work")}">{u["projects_lead"]} →</a></p></div><div class="grid">{"".join(pcard(p) for p in PROJECTS[:3])}</div></div></section>') if PROJECTS else ""
        where = (f'<section><div class="wrap split"><div><div class="eyebrow">{u["areas"]}</div><h2>{u["map_h"]}</h2>'
                 f'<p style="color:var(--muted)">{u["area_txt"]}</p>{chips}{buttons(u)}</div>{MAP}</div></section>')
        cta = (f'<section style="padding-top:0"><div class="wrap"><div class="cta"><div><h2>{u["ready"]}</h2><p>{u["ready_sub"]}</p></div>'
               f'<div class="btns"><a class="btn wa" href="{wa_link(u)}">{wa_i()} {u["wa"]}</a><a class="btn ghost" href="{TEL}">{ph_i()} {PHONE}</a></div></div></div></section>')
        def acard(a):
            return (f'<a class="card" href="{url(lang, gpath(lang, a))}"><div class="im"><img loading="lazy" src="{img(art_photo(a), 700, 525)}" alt=""></div>'
                    f'<h3>{e(a["title"])}</h3><p>{e(a["meta"][:120])}…</p><span class="more">{u["read"]} →</span></a>')
        latest = list(arts.values())[:6]
        guides_block = (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["guides"]}</div><h2>{u["guides_h1"]}</h2></div>'
                        f'<p><a href="{url(lang, sec(lang, "gd"))}">{u["all_guides"]} ({len(arts)}) →</a></p></div><div class="grid">{"".join(acard(a) for a in latest)}</div></div></section>') if latest else ""
        P = lambda slug, title, descr, body, alts, **kw: write(lang, slug, page(lang, slug, title, descr, body, alts, has_guides=has_g, **kw))

        # главная
        h1 = u["home_h1"].replace("Sanur", "<em>Sanur</em>", 1) if "Sanur" in u["home_h1"] else u["home_h1"].replace("Сануре", "<em>Сануре</em>")
        hero = (f'<div class="hero"><img src="{img(PH["hero"], 2000, 1200)}" alt="" fetchpriority="high"><div class="wrap">'
                f'<div class="eyebrow">{u["eyebrow"]}</div><h1>{h1}</h1><p>{u["home_lead"]}</p>{buttons(u)}</div></div>')
        if THEME == "pro":
            rating = ""
            if REVIEWS:
                avg = sum(r.get("stars", 5) for r in REVIEWS) / len(REVIEWS)
                rating = f'<div class="rating"><span class="st">★★★★★</span>{u["rated"].replace("{r}", f"{avg:.1f}").replace("{n}", str(len(REVIEWS)))} {demo}</div>'
            feat = '<ul class="feat">' + "".join(f"<li>{CHECK_ICO}<span>{t}</span></li>" for t in u["trust"]) + "</ul>"
            opts = "".join(f"<option>{e(SV[x]['name'])}</option>" for x in SRV)
            wopts = "".join(f"<option>{e(w)}</option>" for w in u["when_opts"])
            form = (f'<form class="lead-form" data-wa="https://wa.me/{WHATSAPP}?text=" data-pre="{e(u["wa_text"])}" '
                    f'onsubmit="event.preventDefault();location.href=this.dataset.wa+encodeURIComponent(this.dataset.pre+this.w.value+String.fromCharCode(32,8212,32)+this.t.value)">'
                    f'<h3>{u["form_h"]}</h3><label>{u["form_what"]}</label><select name="w">{opts}</select><label>{u["form_when"]}</label><select name="t">{wopts}</select>'
                    f'<button class="btn wa" type="submit">{wa_i()} {u["form_btn"]}</button><p>{u["form_note"]}</p></form>')
            hero = (f'<div class="hero pro"><img src="{img(PH["hero"], 2000, 1200)}" alt="" fetchpriority="high"><div class="wrap"><div>{rating}<h1>{h1}</h1>'
                    f'<p>{u["home_lead"]}</p>{feat}<a class="pcard" href="{TEL}"><i>{ph_i(20)}</i><span><small>{u["call"]} · WhatsApp</small><b>{PHONE}</b></span></a></div>{form}</div></div>')
            tc = [(MASTER["years"] + " " + u["years"]) if MASTER["years"] else u["only"], u["only"], u["pricing_items"][0][0], (f"★ {len(REVIEWS)} Google" if REVIEWS else u["pricing_items"][2][0])]
            tsub = [MASTER["languages"] or u["badge"], u["badge"], u["pricing_items"][0][1][:60] + "…", u["reviews_h"] if REVIEWS else u["pricing_items"][2][1][:60] + "…"]
            strip = ('<div class="wrap"><div class="tcards">' + "".join(f"<div><b>{a}</b><span>{b}</span></div>" for a, b in zip(tc, tsub)) + "</div></div>"
                     f'<div class="serving" style="margin-top:48px">{u["serving"]}</div>')
        P("", f"{u['home_h1']} | {BRAND}", u["home_lead"][:155],
          hero + strip + f'<section><div class="wrap"><div class="shead"><div><div class="eyebrow">{u["services"]}</div><h2>{u["tagline"]}</h2></div><p>{u["ready_sub"]}</p></div><div class="grid">{cards}</div></div></section>'
          + how + master + local(False) + reviews + projects + why + guides_block + where + cta, all_alts(lambda c: ""), schema=biz_schema(lang))
        # услуги
        P(sec(lang, "sv"), f"{u['services']} — {u['tagline']}", u["home_lead"][:155],
          strip + f'<section><div class="wrap"><div class="grid">{cards}</div></div></section>{how}{cta}', all_alts(lambda c: sec(c, "sv")),
          crumbs=[(u["services"], None)], head=(PH["sanur"], u["services"], u["home_lead"]))
        for i, s in enumerate(SRV):
            v = SV[s]
            n = v["name"]
            h1s = n if "Sanur" in n or "Санур" in n else n + {"en": " in Sanur", "ru": " в Сануре"}.get(lang, " — Sanur")
            faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in v["faq"])
            hub = next((h for h, x in HUB_SRV.items() if x == s), None)
            rel = [a for a in arts.values() if a["hub"] == hub][:3] if hub else []
            near = [SRV[(i + k) % len(SRV)] for k in (1, 2, 3)]
            ncards = "".join(f'<a class="card" href="{url(lang, sslug(lang, o))}"><div class="im"><img loading="lazy" src="{img(PH[o], 700, 525)}" alt="{e(SV[o]["name"])}"></div><h3>{SV[o]["name"]}</h3></a>' for o in near)
            main_page = s == "srv-santehnik"  # (2) главная городская страница «Plumber in Sanur»
            svc_list = ""
            if main_page:
                svc_list = (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{u["all_services"]}</h2></div><div class="grid">'
                            + "".join(f'<a class="card" href="{url(lang, sslug(lang, o))}"><div class="im"><img loading="lazy" src="{img(PH[o], 700, 525)}" alt="{e(SV[o]["name"])}"></div><h3>{SV[o]["name"]}</h3><p>{SV[o]["items"][0]}</p></a>' for o in SRV if o != s)
                            + "</div></div></section>")
            body = (strip + f'<section><div class="wrap split"><div><div class="eyebrow">{u["fix"]}</div><h2>{n}</h2><ul class="check">' + "".join(f"<li>{x}</li>" for x in v["items"])
                    + f'</ul><p style="margin-top:22px"><b>{u["price"]}:</b> {PRICES.get(s, u["on_req"])} · <a href="{url(lang, sec(lang, "pr"))}">{u["prices"]}</a></p>{inline()}</div>'
                    f'<img class="side" loading="lazy" src="{img(PH[s], 900, 1125)}" alt="{e(h1s)}"></div></section>'
                    + (local(True) + hoods + svc_list if main_page else "") + master
                    + how + f'<section><div class="wrap narrow"><div class="eyebrow">{u["faq_h"]}</div><h2 style="font-size:48px;margin:10px 0 20px">{u["faq"]}</h2>{faq}{inline()}</div></section>' + reviews
                    + (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{u["related"]}</h2></div><div class="grid">{"".join(acard(a) for a in rel)}</div></div></section>' if rel else "")
                    + where + f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{u["services"]}</h2></div><div class="grid">{ncards}</div></div></section>' + cta)
            sch = [{"@context": "https://schema.org", "@type": "Service", "name": h1s, "areaServed": "Sanur, Bali", "provider": {"@type": "Plumber", "name": BRAND, "telephone": PHONE}},
                   {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in v["faq"]]}]
            P(sslug(lang, s), f"{h1s} | {BRAND}", v["intro"][:155], body, all_alts(lambda c: sslug(c, s)),
              crumbs=[(u["services"], url(lang, sec(lang, "sv"))), (n, None)], schema=sch, head=(PH[s], h1s, v["intro"]))
        # цены / район / контакты
        rows = "".join(f"<tr><td><a href='{url(lang, sslug(lang, s))}'>{SV[s]['name']}</a></td><td>{PRICES.get(s, u['on_req'])}</td></tr>" for s in SRV)
        P(sec(lang, "pr"), f"{u['prices_h1']} | {BRAND}", u["prices_note"][:155],
          f'<section><div class="wrap"><div class="shead"><h2>{u["pricing_h"]}</h2></div><div class="why">'
          + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in u["pricing_items"]) + "</div></div></section>"
          f'<section style="padding-top:0"><div class="wrap narrow"><table><tr><th>{u["work"]}</th><th>{u["price"]}</th></tr>{rows}</table>{inline()}</div></section>{how}{cta}',
          all_alts(lambda c: sec(c, "pr")), crumbs=[(u["prices"], None)], head=(PH["srv-melkij-remont"], u["prices_h1"], u["prices_note"]))
        # (5) страницы работ
        if PROJECTS:
            P("work", f"{u['projects_h1']} | {BRAND}", u["projects_lead"], f'<section><div class="wrap"><div class="grid">{"".join(pcard(p) for p in PROJECTS)}</div></div></section>{cta}',
              all_alts(lambda c: "work"), crumbs=[(u["projects"], None)], head=(PH["sanur"], u["projects_h1"], u["projects_lead"] + " " + demo))
            for p in PROJECTS:
                ps = p.get("service", "srv-santehnik")
                P("work/" + p["slug"], f"{tx(lang, p['title'])} — {p['area']}, Sanur | {BRAND}", tx(lang, p["text"])[:155],
                  f'<section><div class="wrap split"><div><div class="eyebrow">{e(p["area"])}, Sanur {demo}</div><h2>{e(tx(lang, p["title"]))}</h2><p class="big">{e(tx(lang, p["text"]))}</p>'
                  f'<p><a href="{url(lang, sslug(lang, ps))}">{SV[ps]["name"]} →</a></p>{inline()}</div><div class="ba2"><img src="{p["before"]}" alt="before"><img src="{p["after"]}" alt="after"></div></div></section>{cta}',
                  all_alts(lambda c: "work/" + p["slug"]), crumbs=[(u["projects"], url(lang, "work")), (e(tx(lang, p["title"])), None)], head=(PH["sanur"], e(tx(lang, p["title"])), e(p["area"]) + ", Sanur"))
        P(sec(lang, "ar"), f"{u['areas_h1']} | {BRAND}", u["area_txt"], hoods + local(False) + where + f'<section style="padding-top:0"><div class="wrap"><div class="grid">{cards}</div></div></section>' + cta,
          all_alts(lambda c: sec(c, "ar")), crumbs=[(u["areas"], None)], head=(PH["sanur2"], u["areas_h1"], u["area_txt"] + " " + ", ".join(areas_l) + "."))
        P(sec(lang, "ct"), f"{u['contacts_h1']} | {BRAND}", u["contacts_lead"],
          f'<section><div class="wrap split"><div><div class="eyebrow">WhatsApp · {u["call"]}</div><h2>{PHONE}</h2>{buttons(u)}{chips}</div>{MAP}</div></section>',
          all_alts(lambda c: sec(c, "ct")), crumbs=[(u["contacts"], None)], schema=biz_schema(lang), head=(PH["sanur"], u["contacts_h1"], u["contacts_lead"]))
        # статьи (только для языков, где они есть)
        if not has_g:
            continue
        g_alts = {c: sec(c, "gd") for c in ACTIVE if ARTS[c]}
        def hubnav(on=None):
            return ('<div class="hubs">' + f'<a class="{"on" if on is None else ""}" href="{url(lang, sec(lang, "gd"))}">{u["all_guides"]}</a>'
                    + "".join(f'<a class="{"on" if on == h else ""}" href="{url(lang, sec(lang, "gd") + "/" + HUB_EN[h][0])}">{D["hubs"][h]}</a>' for h in HUB_EN) + "</div>")
        P(sec(lang, "gd"), f"{u['guides_h1']} | {BRAND}", u["guides_lead"],
          f'<section><div class="wrap">{hubnav()}<div class="grid">{"".join(acard(a) for a in arts.values())}</div></div></section>{cta}',
          g_alts, crumbs=[(u["guides"], None)], head=(PH["sanur"], u["guides_h1"], u["guides_lead"]))
        for h, (hs, _) in HUB_EN.items():
            ha = [a for a in arts.values() if a["hub"] == h]
            P(sec(lang, "gd") + "/" + hs, f"{D['hubs'][h]} — {u['guides']} | {BRAND}", u["guides_lead"],
              f'<section><div class="wrap">{hubnav(h)}<div class="grid">{"".join(acard(a) for a in ha)}</div></div></section>{cta}',
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
                          f'<a class="btn wa" href="{wa_link(u, a["title"])}">{wa_i()} WhatsApp</a><a class="btn ghost" href="{TEL}">{ph_i()} {u["call"]}</a></div>')
            if a.get("faq"):
                c += f'<h2 id="faq">{u["faq_h"]}</h2>' + "".join(f'<details><summary>{e(q["q"])}</summary><p>{e(q["a"])}</p></details>' for q in a["faq"])
            c += (f'<div class="inline-cta"><div><b>{SV[srv]["name"]}</b><br><span style="color:var(--muted)">{u["ready_sub"]}</span></div>'
                  f'<a class="btn ghost" href="{url(lang, sslug(lang, srv))}">{u["services"]} →</a></div>')
            rel = [o for o in arts.values() if o["hub"] == a["hub"] and o is not a][:3]
            body = (f'<div class="wrap art"><aside class="toc"><b>{u["toc"]}</b>{toc}</aside><article class="prose">{c}</article></div>'
                    + (f'<section style="padding-top:24px"><div class="wrap"><div class="shead"><h2>{u["related"]}</h2></div><div class="grid">{"".join(acard(o) for o in rel)}</div></div></section>' if rel else "") + cta)
            photo = art_photo(a)
            sch = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["meta"], "image": img(photo, 1200), "inLanguage": lang,
                    "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}}]
            if a.get("faq"):
                sch.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in a["faq"]]})
            alts = {c: gpath(c, ARTS[c][a["id"]]) for c in ACTIVE if a["id"] in ARTS[c]}
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
