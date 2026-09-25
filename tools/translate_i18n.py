# -*- coding: utf-8 -*-
"""Перевод i18n/en.json на другие языки через локальную Qwen. Пропускает готовые. python tools/translate_i18n.py [коды]"""
import json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parent.parent
DELEGATE = r"C:\Users\anich\Documents\Codex\2026-08-31\referenced-chatgpt-conversation-this-is-an\outputs\local-agent\delegate_to_qwen.py"
LANGS = {"id": "Indonesian", "nl": "Dutch", "de": "German", "fr": "French", "it": "Italian", "es": "Spanish", "pt": "Portuguese",
         "pl": "Polish", "uk": "Ukrainian", "cs": "Czech", "sv": "Swedish", "da": "Danish", "nb": "Norwegian Bokmål", "fi": "Finnish",
         "tr": "Turkish", "zh": "Simplified Chinese", "ja": "Japanese", "ko": "Korean"}
SYSTEM = ("You are a professional website translator. Translate ONLY the JSON string values from English into the target language; "
          "keep every key, array length and structure exactly. Keep place names (Sanur, Bali, PDAM, WhatsApp) as is. "
          "Natural, concise marketing tone for a local plumber and pool technician. Output only valid JSON, nothing else.")

def tr(obj, lang):
    for _ in range(3):
        r = subprocess.run([sys.executable, DELEGATE, "--system", SYSTEM, "--max-tokens", "8000",
                            f"Target language: {LANGS[lang]}.\n\n" + json.dumps(obj, ensure_ascii=False)],
                           capture_output=True, text=True, encoding="utf-8")
        t = r.stdout.strip()
        try:
            out = json.loads(t[t.index("{"): t.rindex("}") + 1])
            if set(out) == set(obj):
                return out
        except Exception:
            pass
        print(lang, "retry", flush=True)
    raise SystemExit(f"{lang}: translation failed")

src = json.loads((ROOT / "i18n" / "en.json").read_text(encoding="utf-8"))
for lang in (sys.argv[1:] or LANGS):
    f = ROOT / "i18n" / f"{lang}.json"
    if f.exists():
        continue
    ui = tr(src["ui"], lang)
    svc = {}
    items = list(src["services"].items())
    for i in range(0, len(items), 4):
        svc.update(tr(dict(items[i:i + 4]), lang))
    hubs = tr(src["hubs"], lang)
    f.write_text(json.dumps({"lang": lang, "ui": ui, "services": svc, "hubs": hubs, "areas": src["areas"]}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(lang, "ok", flush=True)
