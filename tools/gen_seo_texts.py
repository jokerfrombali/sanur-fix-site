# -*- coding: utf-8 -*-
"""SEO-тексты страниц (H2 + H3 + FAQ) через локальную Qwen → content/seo/<lang>/<key>.json.
key: home | svc-<slug> | area-<area> | area-<area>-<slug>. Пропускает готовые.
Запуск: python tools/gen_seo_texts.py en [фильтр-префикс]"""
import json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from areas import AREAS
DELEGATE = r"C:\Users\anich\Documents\Codex\2026-08-31\referenced-chatgpt-conversation-this-is-an\outputs\local-agent\delegate_to_qwen.py"
SLUGS = {"srv-santehnik": "plumber", "srv-protechki": "leak-repair", "srv-zasor": "blocked-drain", "srv-bojler": "water-heater",
         "srv-voda": "water-pump-filter", "srv-chistka-bassejna": "pool-cleaning", "srv-obsluzhivanie-bassejna": "pool-service",
         "srv-oborudovanie-bassejna": "pool-equipment", "srv-remont-bassejna": "pool-repair", "srv-septik": "septic",
         "srv-melkij-remont": "handyman", "srv-obsluzhivanie-villy": "villa-maintenance"}
SYSTEM = """You write SEO body text for the website of a private plumber and pool technician in Bali (brand: Bali Fix). Readers: villa owners, long-term tenants and villa managers, mostly foreigners.
Rules:
- Output ONLY valid JSON, no markdown fences.
- Useful, specific, natural language. The main keyword appears naturally in the first paragraph and in 1-2 headings, never stuffed.
- Use the local facts given. Do NOT invent prices, statistics, years, brands, licences, guarantees, response times, reviews or client stories. If price comes up: it depends on the job, quote from photos on WhatsApp.
- Contact is WhatsApp only. Never mention phone calls or Telegram.
- Do not repeat the same sentence patterns between sections."""

def ask(prompt):
    for _ in range(3):
        r = subprocess.run([sys.executable, DELEGATE, "--system", SYSTEM, "--max-tokens", "5000", prompt], capture_output=True, text=True, encoding="utf-8")
        t = re.sub(r"^```(?:json)?|```$", "", r.stdout.strip(), flags=re.M).strip()
        try:
            d = json.loads(t[t.index("{"): t.rindex("}") + 1])
            assert d["h2"] and d["intro"] and len(d["sections"]) >= 3 and all(s["h3"] and s["text"] for s in d["sections"])
            return d
        except Exception:
            continue
    return None

FORMAT = """Return JSON: {"h2": "section heading with the main keyword, max 70 chars", "intro": "2-3 sentences",
 "sections": [{"h3": "...", "text": "one paragraph, 60-90 words"}] (exactly 4 items),
 "faq": [{"q": "...", "a": "1-2 sentences"}] (exactly 3 items)}"""

def jobs(lang):
    L = json.loads((ROOT / "i18n" / f"{lang}.json").read_text(encoding="utf-8"))
    lname = "English" if lang == "en" else "Russian"
    sv = L["services"]
    yield "home", (f"Language: {lname}. Page: home page 'Plumber & Pool Service in Bali'. Main keyword: {'plumber Bali, pool service Bali' if lang == 'en' else 'сантехник Бали, обслуживание бассейна Бали'}.\n"
                   f"Services: {', '.join(v['name'] for v in sv.values())}. Areas: {', '.join(a[lang] for a in AREAS)}.\n"
                   "Cover: what the technician does, why villas in Bali have specific plumbing/pool problems (tanks, pumps, wells, rainy season, salt air), how ordering via WhatsApp works, which areas are covered.\n" + FORMAT)
    for sid, slug in SLUGS.items():
        v = sv[sid]
        yield f"svc-{slug}", (f"Language: {lname}. Page: service '{v['name']}' across Bali. Main keyword: '{v['name']} {'Bali' if lang == 'en' else 'Бали'}'.\n"
                              f"Service summary: {v['intro']} Typical jobs: {'; '.join(v['items'])}.\nAreas served: {', '.join(a[lang] for a in AREAS)}.\n"
                              "Cover: typical problems and causes in Bali villas, what the job includes, how to prepare / what to send on WhatsApp, prevention.\n" + FORMAT)
    for a in AREAS:
        facts = " ".join(f"{x}: {y}" for x, y in a["issues"][lang])
        yield f"area-{a['slug']}", (f"Language: {lname}. Page: area hub '{'Plumber & Pool Service in ' + a['en'] if lang == 'en' else 'Сантехник и мастер по бассейнам — ' + a['ru']}'.\n"
                                    f"Area: {a[lang]}. Neighbourhoods: {', '.join(a['subs'])}. Local facts: {a['intro'][lang]} {facts}\n"
                                    f"Services: {', '.join(v['name'] for v in sv.values())}.\nCover: local conditions and what breaks most often here, which services are most requested here, neighbourhoods covered, seasonal advice.\n" + FORMAT)
        for sid, slug in SLUGS.items():
            v = sv[sid]
            kw = f"{v['name']} {a['en']}" if lang == "en" else f"{v['name']} {a['ru']}"
            yield f"area-{a['slug']}-{slug}", (f"Language: {lname}. Page: '{v['name']}' in {a[lang]}, Bali. Main keyword: '{kw}'.\n"
                                                f"Service: {v['intro']} Typical jobs: {'; '.join(v['items'])}.\nArea facts: {a['intro'][lang]} {facts}\nNeighbourhoods: {', '.join(a['subs'])}.\n"
                                                "Cover: how this service relates to local conditions in this area, typical cases here, what to send on WhatsApp, prevention tips for this area. Mention 2-3 neighbourhoods naturally.\n" + FORMAT)

def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    flt = sys.argv[2] if len(sys.argv) > 2 else ""
    out = ROOT / "content" / "seo" / lang
    out.mkdir(parents=True, exist_ok=True)
    for key, prompt in jobs(lang):
        f = out / f"{key}.json"
        if f.exists() or not key.startswith(flt):
            continue
        d = ask(prompt)
        if d:
            f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
            print(key, "ok", flush=True)
        else:
            print(key, "FAILED", flush=True)

if __name__ == "__main__":
    main()
