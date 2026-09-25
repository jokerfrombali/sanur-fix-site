#!/bin/bash
# Каждые 20 минут: пересборка сайта и пуш новых статей. Выход, когда готовы 150 EN и 150 RU.
cd "$(dirname "$0")/.."
while true; do
  python build_site.py
  git add -A
  if ! git diff --cached --quiet; then
    git commit -qm "Статьи: EN $(ls content/en | wc -l)/150, RU $(ls content/ru 2>/dev/null | wc -l)/150

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git push -q
  fi
  [ "$(ls content/en | wc -l)" -ge 150 ] && [ "$(ls content/ru 2>/dev/null | wc -l)" -ge 150 ] && break
  sleep 1200
done
