# -*- coding: utf-8 -*-
"""Аудит: один H1, без пропуска уровней заголовков, валидный JSON-LD, хлебные крошки на внутренних страницах."""
import re, glob, json, collections, os
bad = collections.Counter(); n = 0; ex = {}
for f in glob.glob("site/**/index.html", recursive=True):
    t = open(f, encoding="utf-8").read(); n += 1
    rel = os.path.relpath(f, "site").replace(os.sep, "/")
    if len(re.findall(r"<h1[ >]", t)) != 1: bad["h1!=1"] += 1; ex.setdefault("h1", rel)
    lv = [int(x) for x in re.findall(r"<h([1-6])[ >]", t)]
    if any(b - a > 1 for a, b in zip(lv, lv[1:])): bad["skip-level"] += 1; ex.setdefault("skip", (rel, lv[:14]))
    for m in re.findall(r'<script type="application/ld\+json">(.*?)</script>', t):
        try: json.loads(m)
        except Exception: bad["bad-jsonld"] += 1
    home = rel.count("/") == 0 or (rel.count("/") == 1 and len(rel.split("/")[0]) == 2)
    if not home and "BreadcrumbList" not in t: bad["no-breadcrumb"] += 1; ex.setdefault("bc", rel)
print(n, "pages", dict(bad), ex)
