# -*- coding: utf-8 -*-
"""Дозаполнить в переведённых i18n/*.json ключи ui, которые появились в en.json позже."""
import json, pathlib, sys
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from translate_i18n import tr, LANGS, ROOT
en = json.loads((ROOT / "i18n" / "en.json").read_text(encoding="utf-8"))["ui"]
for lang in LANGS:
    f = ROOT / "i18n" / f"{lang}.json"
    if not f.exists():
        continue
    d = json.loads(f.read_text(encoding="utf-8"))
    miss = {k: v for k, v in en.items() if k not in d["ui"]}
    if miss:
        d["ui"].update(tr(miss, lang))
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(lang, "filled", len(miss), flush=True)
