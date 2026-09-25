# -*- coding: utf-8 -*-
"""Черновики статей через локальную Qwen (delegate_to_qwen.py) → content/<lang>/<id>.json.
Пропускает уже готовые. Запуск: python tools/gen_articles.py en [лимит]"""
import json, pathlib, re, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
DELEGATE = r"C:\Users\anich\Documents\Codex\2026-08-31\referenced-chatgpt-conversation-this-is-an\outputs\local-agent\delegate_to_qwen.py"
sys.path.insert(0, str(ROOT / "tools"))
from articles_plan import ARTICLES, HUB_EN

SYSTEM = """You write practical home-maintenance articles for the website of a private plumber and pool technician who works ONLY in Sanur, Bali. Readers: expat villa owners and long-term tenants in Sanur.
Rules:
- Output ONLY valid JSON, no markdown fences, no comments.
- Plain, friendly, expert tone. Short paragraphs. Concrete steps. Mention Sanur/Bali context only where it is genuinely relevant (sea air, rainy season, PDAM water, wells, rooftop tanks, septic tanks, old villas).
- Do NOT invent prices, statistics, brand claims, laws, guarantees, response times, years of experience, customer stories or reviews. If money is relevant, say the price depends on the job and the technician quotes from photos on WhatsApp.
- Safety: for gas smell, electrics near water, or chlorine mixing, tell the reader to stop and call a professional.
- Never mention Telegram."""

def prompt(a, lang):
    language = "English" if lang == "en" else "Russian"
    return f"""Write an article in {language}, 750-1000 words in total.
Topic (working title, in Russian): {a['h1']}
Main search query (Russian): {a['mq']}
Related queries: {', '.join(a['sups'])}
Planned sections (Russian, translate and keep the order; you may merge or rephrase slightly): {' | '.join(h.replace('~', ' / ') for h in a['h2s'])}

Return JSON with exactly these keys:
{{"title": "H1, max 65 chars, natural search phrasing", "slug": "latin-kebab-case, 3-6 words",
 "meta": "meta description, 140-160 chars", "intro": "2-4 sentence direct answer",
 "sections": [{{"h2": "...", "paragraphs": ["..."], "bullets": ["optional list items"]}}],
 "faq": [{{"q": "...", "a": "..."}}, 3 items],
 "cta": "one sentence inviting the reader to send a photo on WhatsApp"}}"""

def main():
    lang = sys.argv[1] if len(sys.argv) > 1 else "en"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 999
    out = ROOT / "content" / lang
    out.mkdir(parents=True, exist_ok=True)
    done = 0
    for a in ARTICLES:
        f = out / f"{a['id']}.json"
        if f.exists() or done >= limit:
            continue
        for attempt in range(3):
            r = subprocess.run([sys.executable, DELEGATE, "--system", SYSTEM, "--max-tokens", "6000", prompt(a, lang)],
                               capture_output=True, text=True, encoding="utf-8")
            txt = r.stdout.strip()
            txt = re.sub(r"^```(?:json)?|```$", "", txt, flags=re.M).strip()
            try:
                data = json.loads(txt[txt.index("{"): txt.rindex("}") + 1])
                assert data["title"] and data["sections"] and len(data["sections"]) >= 3
                data["id"], data["hub"], data["status"] = a["id"], a["hub"], "draft-qwen"
                f.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
                print(a["id"], "ok", data["slug"], flush=True)
                done += 1
                break
            except Exception as e:
                print(a["id"], "retry", attempt, type(e).__name__, r.stderr[-200:], flush=True)

if __name__ == "__main__":
    main()
