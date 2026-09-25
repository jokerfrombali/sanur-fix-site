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
