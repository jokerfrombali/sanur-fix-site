#!/bin/bash
# Каждые 20 минут: сборка и пуш, пока не готовы SEO-тексты (143 на язык).
cd "$(dirname "$0")/.."
while true; do
  set -o pipefail
  if python build_site.py > /dev/null; then
    git add -A
    if ! git diff --cached --quiet; then
      git commit -qm "SEO-тексты: EN $(ls content/seo/en | wc -l)/143, RU $(ls content/seo/ru 2>/dev/null | wc -l)/143

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" && git pull -q --rebase && git push -q
    fi
  fi
  [ "$(ls content/seo/en | wc -l)" -ge 143 ] && [ "$(ls content/seo/ru 2>/dev/null | wc -l)" -ge 143 ] && break
  sleep 1200
done
