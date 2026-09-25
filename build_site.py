# -*- coding: utf-8 -*-
"""Статический сайт мастера в Сануре: RU (корень) + EN (/en/). Запуск: python build_site.py → папка site/."""
import json, pathlib, shutil, html

# ======== ЗАПОЛНИТЬ ДАННЫМИ МАСТЕРА ========
DOMAIN = "https://jokerfrombali.github.io"  # домен сайта (без слэша в конце)
BASE = "/sanur-fix-site"                # подпапка; для своего домена — ""
PREVIEW = True                          # True = закрыт от индексации (просмотр на GitHub Pages)
BRAND = "Sanur Fix"                     # название (рабочее)
WHATSAPP = "6280000000000"              # номер WhatsApp без +
PHONE = "+62 800-0000-0000"
TELEGRAM = "username"                   # без @
GBP_URL = ""   # ссылка на карточку в Google Картах, когда появится
PRICES = {}   # {"srv-santehnik": "от 300 000 IDR"} — пусто = «по запросу»
# ===========================================

ROOT = pathlib.Path(__file__).parent / "site"
AREAS_EN = ["Sanur Kaja", "Sanur Kauh", "Sindhu", "Semawang", "Mertasari", "Batujimbar", "Jl. Danau Tamblingan", "Jl. Danau Poso", "Jl. Bypass Ngurah Rai"]
AREAS_RU = ["Санур Кайя", "Санур Кауф", "Синду", "Семаванг", "Мертасари", "Батуджимбар", "ул. Данау Тамблинган", "ул. Данау Посо", "Байпас Нгурах Рай"]

# id, ru_slug, en_slug, ru_name, en_name, ru_intro, en_intro, ru_items, en_items, faq_ru, faq_en
S = [
 ("srv-santehnik", "santehnik-sanur", "plumber-sanur", "Сантехник в Сануре", "Plumber in Sanur",
  "Частный мастер-сантехник в Сануре: приезжаю сам, нахожу причину и чиню. Смесители, унитазы, трубы, насосы, горячая вода — на виллах, в домах и апартаментах.",
  "A private plumber in Sanur: I come myself, find the cause and fix it. Taps, toilets, pipes, pumps and hot water — in villas, houses and apartments.",
  ["Течёт смеситель или кран", "Подтекает бачок унитаза", "Слабый напор воды", "Замена смесителей, сифонов, подводок", "Установка унитаза и раковины", "Подключение стиральной и посудомоечной машины"],
  ["Leaking taps and mixers", "Running or leaking toilet cistern", "Low water pressure", "Replacing mixers, traps and hoses", "Toilet and basin installation", "Washing machine and dishwasher hook-up"],
  [("Как быстро вы приедете?", "Зависит от загрузки на день. Напишите в WhatsApp с фото — сразу скажу, когда смогу быть."), ("Материалы покупаете вы или я?", "Как удобнее. Могу купить сам и приложить чек.")],
  [("How fast can you come?", "Depends on the day's schedule. Send a photo on WhatsApp and I'll tell you when I can be there."), ("Who buys the parts?", "Either way. I can buy them and give you the receipt.")]),
 ("srv-protechki", "protechki-sanur", "leak-repair-sanur", "Устранение протечек", "Water Leak Repair",
  "Ищу и устраняю протечки: под мойкой, в стенах, в душевых, на участке. Скрытая утечка заметна по счётчику PDAM или постоянно работающему насосу.",
  "Finding and fixing leaks: under sinks, in walls, showers and garden lines. A hidden leak often shows up on the PDAM meter or a pump that keeps running.",
  ["Течь под мойкой и раковиной", "Протекающая душевая и трап", "Скрытая утечка по счётчику", "Лопнувшие трубы PVC/PPR", "Протечки в садовом поливе"],
  ["Leaks under sinks", "Leaking showers and floor drains", "Hidden leaks found via the meter", "Burst PVC/PPR pipes", "Garden irrigation leaks"],
  [("Что делать до приезда?", "Перекройте главный кран и, если вода рядом с розетками, выключите электричество.")],
  [("What should I do before you arrive?", "Close the main valve and, if water is near sockets, switch off the power.")]),
 ("srv-zasor", "prochistka-zasorov-sanur", "blocked-drain-sanur", "Прочистка засоров", "Blocked Drains & Toilets",
  "Прочищаю засоры в унитазах, раковинах, душевых и канализации тросом, без агрессивной химии, которая портит трубы и септик.",
  "Clearing blocked toilets, sinks, showers and drain lines with a drain snake, without harsh chemicals that damage pipes and septic tanks.",
  ["Забитый унитаз", "Вода не уходит в душе или раковине", "Засор в канализационной трубе", "Запах из слива"],
  ["Blocked toilet", "Slow shower or sink drain", "Blocked sewer line", "Smell from drains"],
  [("Почему на Бали нельзя бросать бумагу в унитаз?", "Трубы узкие, а септики маленькие — бумага быстро забивает систему.")],
  [("Why no toilet paper in the toilet in Bali?", "Narrow pipes and small septic tanks — paper clogs the system quickly.")]),
 ("srv-bojler", "bojler-sanur", "water-heater-sanur", "Ремонт и установка бойлеров", "Water Heater Repair & Installation",
  "Нет горячей воды — разберусь, в чём дело: электрический бойлер, газовая колонка или солнечный нагреватель на крыше. Меняю ТЭН, термостат, анод, ставлю новые бойлеры.",
  "No hot water? I'll find out why — electric heater, gas heater or rooftop solar. Heating elements, thermostats, anodes and new installations.",
  ["Бойлер не греет", "Выбивает автомат", "Течёт бойлер", "Солнечный нагреватель чуть тёплый", "Установка нового бойлера"],
  ["Heater not heating", "Heater trips the breaker", "Leaking heater", "Lukewarm solar heater", "New heater installation"],
  [("Ремонтировать или менять?", "Если бак течёт — менять. Если сгорел ТЭН или термостат — обычно выгоднее ремонт.")],
  [("Repair or replace?", "A leaking tank means replace. A failed element or thermostat is usually worth repairing.")]),
 ("srv-voda", "nasosy-filtry-sanur", "water-pump-filter-sanur", "Насосы, фильтры, водоснабжение", "Water Pumps & Filters",
  "Насосы, реле давления, баки на крыше и фильтры для воды. У моря в Сануре вода из скважины бывает солоноватой — подберу фильтрацию или переход на PDAM.",
  "Pumps, pressure switches, rooftop tanks and water filters. Near the beach in Sanur, well water can be brackish — I'll help with filtration or switching to PDAM.",
  ["Насос постоянно включается", "Нет воды в доме", "Бак переливается или пустой", "Установка и замена фильтров", "Чистка бака на крыше"],
  ["Pump keeps cycling", "No water in the house", "Tank overflowing or empty", "Filter installation and cartridges", "Rooftop tank cleaning"],
  [("Как часто менять картриджи?", "Обычно раз в 3–6 месяцев, зависит от воды. Покажу, как понять по цвету и напору.")],
  [("How often to change cartridges?", "Usually every 3–6 months depending on the water. I'll show you what to look for.")]),
 ("srv-chistka-bassejna", "chistka-bassejna-sanur", "pool-cleaning-sanur", "Чистка бассейна", "Pool Cleaning",
  "Разовая чистка бассейна: сачок, щётка, пылесос, промывка фильтра, баланс воды. Возвращаю зелёную воду.",
  "One-off pool cleaning: skimming, brushing, vacuuming, filter backwash and water balance. Green pool recovery.",
  ["Чистка перед заездом гостей", "Зелёная или мутная вода", "Чистка плитки по ватерлинии", "Промывка фильтра"],
  ["Cleaning before guests arrive", "Green or cloudy water", "Waterline tile cleaning", "Filter backwash"],
  [("Сколько дней возвращается зелёный бассейн?", "Обычно 2–4 дня, зависит от состояния воды и фильтра.")],
  [("How long to fix a green pool?", "Usually 2–4 days, depending on the water and the filter.")]),
 ("srv-obsluzhivanie-bassejna", "obsluzhivanie-bassejna-sanur", "pool-service-sanur", "Регулярное обслуживание бассейна", "Regular Pool Service",
  "Обслуживание бассейна по графику. После каждого визита — отчёт в WhatsApp: фото, показатели воды, что сделано. Удобно, если вы не живёте на Бали постоянно.",
  "Scheduled pool service. After every visit you get a WhatsApp report: photos, water readings, work done. Ideal if you don't live in Bali full-time.",
  ["Визиты по графику", "Тест и баланс воды", "Пылесос, щётка, скиммер", "Проверка насоса и фильтра", "Отчёт после визита"],
  ["Scheduled visits", "Water testing and balancing", "Vacuum, brush, skimmer", "Pump and filter check", "Report after each visit"],
  [("Химия входит в цену?", "Обсуждаем заранее: либо включена, либо отдельно по чеку.")],
  [("Are chemicals included?", "Agreed upfront: either included or charged separately with receipts.")]),
 ("srv-oborudovanie-bassejna", "oborudovanie-bassejna-sanur", "pool-equipment-sanur", "Оборудование бассейна", "Pool Equipment",
  "Установка и ремонт насосов, песочных и картриджных фильтров, хлораторов, подсветки и автодолива.",
  "Installation and repair of pumps, sand and cartridge filters, chlorinators, lights and auto-fill.",
  ["Насос не качает или гудит", "Замена песка в фильтре", "Шестипозиционный клапан", "Солевой хлоратор", "Подсветка бассейна"],
  ["Pump not priming or noisy", "Filter sand replacement", "Multiport valve", "Salt chlorinator", "Pool lights"],
  [("Можно прислать фото техкомнаты?", "Да, это лучший способ — по фото пойму, что нужно взять с собой.")],
  [("Can I send a photo of the pump room?", "Yes — that's the best way for me to know what to bring.")]),
 ("srv-remont-bassejna", "remont-bassejna-sanur", "pool-repair-sanur", "Ремонт бассейна", "Pool Repair",
  "Протечки, отпавшая плитка, затирка, трубы. Многим бассейнам в Сануре 15–20 лет — помогу определить, что ремонтировать в первую очередь.",
  "Leaks, loose tiles, grout, pipework. Many pools in Sanur are 15–20 years old — I'll help decide what to fix first.",
  ["Уходит вода — поиск протечки", "Отпавшая плитка и мозаика", "Затирка швов", "Протечки в трубах бассейна"],
  ["Losing water — leak detection", "Loose tiles and mosaic", "Re-grouting", "Pool pipe leaks"],
  [("Как понять — испарение или протечка?", "Тест с ведром: ставим ведро с водой на ступеньку и сравниваем уровни через сутки.")],
  [("Evaporation or a leak?", "Bucket test: put a bucket of water on the step and compare both levels after 24 hours.")]),
 ("srv-septik", "septik-kanalizaciya-sanur", "septic-sanur", "Септик и канализация", "Septic & Sewer",
  "Запах, медленный слив, переполненный септик. Разберусь, где проблема, организую откачку и прочищу трубы.",
  "Smells, slow drains, full septic tank. I'll find the problem, arrange pumping and clear the lines.",
  ["Запах канализации", "Переполненный септик", "Засор канализации", "Жироуловитель"],
  ["Sewer smell", "Full septic tank", "Blocked sewer line", "Grease trap"],
  [("Как часто откачивать септик?", "Зависит от объёма и числа жильцов — в среднем раз в 1–3 года.")],
  [("How often to pump a septic tank?", "Depends on size and occupants — typically every 1–3 years.")]),
 ("srv-melkij-remont", "master-na-chas-sanur", "handyman-sanur", "Мелкий ремонт, мастер на час", "Handyman",
  "Мелкий бытовой ремонт одним выездом: двери, замки, москитные сетки, силикон, полки, мебель.",
  "Small home repairs in one visit: doors, locks, mosquito screens, silicone, shelves, furniture.",
  ["Разбухшие двери и петли", "Замки и ручки", "Москитные сетки", "Замена силикона в ванной", "Повесить полки, карнизы, ТВ", "Сборка мебели"],
  ["Sticking doors and hinges", "Locks and handles", "Mosquito screens", "Bathroom re-siliconing", "Shelves, curtain rails, TV mounting", "Furniture assembly"],
  [("Можно собрать список задач на один выезд?", "Да, так выгоднее. Пришлите список и фото.")],
  [("Can I list several jobs for one visit?", "Yes, that's the best value. Send the list with photos.")]),
 ("srv-obsluzhivanie-villy", "obsluzhivanie-villy-sanur", "villa-maintenance-sanur", "Обслуживание виллы", "Villa Maintenance",
  "Регулярный техосмотр виллы: сантехника, бассейн, насосы, бойлеры, крыша перед сезоном дождей. Для владельцев и управляющих.",
  "Regular villa check-ups: plumbing, pool, pumps, water heaters, roof before the rainy season. For owners and managers.",
  ["Плановый осмотр по чек-листу", "Подготовка к сезону дождей", "Проверка перед заездом гостей", "Отчёт владельцу"],
  ["Checklist inspections", "Rainy-season preparation", "Pre-arrival checks", "Owner reports"],
  [("Вы работаете с управляющими компаниями?", "Да, можно договориться о регулярном графике.")],
  [("Do you work with villa managers?", "Yes, we can set up a regular schedule.")]),
]

T = {
 "ru": dict(lang="ru", pre="", other="en", tagline="Сантехник и мастер по бассейнам в Сануре", wa="Написать в WhatsApp", tg="Telegram", call="Позвонить",
            wa_text="Здравствуйте! Нужен мастер в Сануре: ", services="Услуги", prices="Цены", areas="Зона выезда", contacts="Контакты",
            fix="Что делаю", how="Как это работает", faq="Частые вопросы", on_req="по запросу", work="Работа", price="Цена",
            steps=["Пришлите фото или видео проблемы в WhatsApp", "Скажу примерную цену и когда смогу приехать", "Приезжаю, чиню, показываю результат"],
            area_txt="Работаю только в Сануре — весь район:", switch="English",
            home_h1="Сантехник и мастер по бассейнам в Сануре",
            home_lead="Частный мастер: сантехника, протечки, бойлеры, насосы, чистка и ремонт бассейнов, мелкий ремонт на виллах Санура. Пришлите фото — отвечу в WhatsApp.",
            prices_h1="Цены на работы в Сануре", prices_note="Цена зависит от объёма работ. Точную стоимость скажу по фото до выезда. Материалы — отдельно по чеку.",
            areas_h1="Работаю только в Сануре", contacts_h1="Контакты", contacts_lead="Быстрее всего — WhatsApp с фото проблемы и районом.",
            nf="Страница не найдена", home="Главная"),
 "en": dict(lang="en", pre="en/", other="ru", tagline="Plumber & Pool Service in Sanur", wa="WhatsApp me", tg="Telegram", call="Call",
            wa_text="Hi! I need a technician in Sanur: ", services="Services", prices="Prices", areas="Service Area", contacts="Contact",
            fix="What I fix", how="How it works", faq="FAQ", on_req="on request", work="Job", price="Price",
            steps=["Send a photo or video of the problem on WhatsApp", "I'll give an estimate and a time I can come", "I come, fix it and show you the result"],
            area_txt="I work only in Sanur — the whole area:", switch="Русский",
            home_h1="Plumber & Pool Service in Sanur, Bali",
            home_lead="Private technician: plumbing, leaks, water heaters, pumps, pool cleaning and repair, small villa repairs in Sanur. Send a photo — I'll reply on WhatsApp.",
            prices_h1="Prices in Sanur", prices_note="Price depends on the job. I'll quote from photos before coming. Parts are charged separately with receipts.",
            areas_h1="Sanur Only", contacts_h1="Contact", contacts_lead="Fastest way: WhatsApp with a photo of the problem and your area.",
            nf="Page not found", home="Home"),
}


# ================== ВИЗУАЛ ==================
# Фото: Unsplash (бесплатно, коммерческое использование разрешено, хотлинк рекомендован Unsplash).
# ЗАМЕНИТЬ на реальные фото мастера и его работ, как только они будут — это важнее для доверия и Google.
U = "https://images.unsplash.com/"
def img(pid, w=900, h=None):
    return f"{U}{pid}?auto=format&fit=crop&w={w}{'&h=' + str(h) if h else ''}&q=70"
PH = {  # id: (photo, автор)
    "hero": ("photo-1720161263981-84281892ee4b", "Pepita Martasya"),
    "sanur": ("photo-1733281120655-8da3dc371514", "Didi Suprapta"),
    "sanur2": ("photo-1733281121312-6bec65d3c809", "Didi Suprapta"),
    "srv-santehnik": ("photo-1749532125405-70950966b0e5", "bhagya laxmi"),
    "srv-protechki": ("photo-1676210134188-4c05dd172f89", "Timur Shakerzianov"),
    "srv-zasor": ("photo-1676210134050-6f12c6898395", "Timur Shakerzianov"),
    "srv-bojler": ("photo-1676210134190-3f2c0d5cf58d", "Timur Shakerzianov"),
    "srv-voda": ("photo-1676210133055-eab6ef033ce3", "Timur Shakerzianov"),
    "srv-chistka-bassejna": ("photo-1605702755163-4f303492e55f", "Iosi Pratama"),
    "srv-obsluzhivanie-bassejna": ("photo-1742353980377-b8e42932c590", "Zhiqiang Wang"),
    "srv-oborudovanie-bassejna": ("photo-1614667288602-9ac6e37318a7", "Clark Tai"),
    "srv-remont-bassejna": ("photo-1724660583299-2356fe880e54", "Declan Sun"),
    "srv-septik": ("photo-1606340671662-27ee685dd111", "Compagnons"),
    "srv-melkij-remont": ("photo-1615974679600-665fb9468c4f", "Valentina Giarre"),
    "srv-obsluzhivanie-villy": ("photo-1634671651144-adbeca8623cb", "We Do Creative Films"),
}
ICON = {"srv-santehnik": "🔧", "srv-protechki": "💧", "srv-zasor": "🚽", "srv-bojler": "🔥", "srv-voda": "🚰", "srv-chistka-bassejna": "🏊",
        "srv-obsluzhivanie-bassejna": "🌊", "srv-oborudovanie-bassejna": "⚙️", "srv-remont-bassejna": "🧱", "srv-septik": "🛠️",
        "srv-melkij-remont": "🔨", "srv-obsluzhivanie-villy": "🌴"}

X = {
 "ru": dict(badge="Санур · Бали · выезд к вам", trust=[("📸", "Фото-отчёт в WhatsApp после каждой работы"), ("💬", "Цена по фото — до выезда"), ("🛵", "Работаю только в Сануре"), ("🧾", "Материалы по чеку")],
            why="Почему зовут меня", why_items=[("Приезжаю сам", "Не диспетчерская и не бригада — работу делает мастер, с которым вы переписываетесь."), ("Только Санур", "Не мотаюсь по всему Бали — работаю в одном районе и знаю его виллы: старые бассейны, солёную воду у моря, баки на крыше."), ("Отчёт владельцу", "Если вы не на Бали — пришлю фото «до» и «после» и что было сделано.")],
            master_h="Мастер", master_txt="Здесь будет фото и пара слов о мастере: как зовут, сколько лет работает, на каких языках общается. Клиенты на Бали выбирают человека, а не компанию.",
            master_ph="Фото мастера", gallery="Работы в Сануре", gallery_note="Сюда — реальные фото работ «до / после». Пока показаны иллюстрации.",
            map_h="Где работаю", ready="Сломалось? Пришлите фото — отвечу в WhatsApp", credits="Иллюстрации: Unsplash"),
 "en": dict(badge="Sanur · Bali · we come to you", trust=[("📸", "Photo report on WhatsApp after every job"), ("💬", "Quote from photos — before the visit"), ("🛵", "Sanur only — I live and work here"), ("🧾", "Parts with receipts")],
            why="Why people call me", why_items=[("I come myself", "Not a call centre or a crew — the technician you chat with does the job."), ("Sanur only", "I don't cross the whole island — one area, and I know its villas: old pools, brackish water near the beach, rooftop tanks."), ("Reports for owners", "Not in Bali? You get before/after photos and a list of what was done.")],
            master_h="Your technician", master_txt="Photo and a few words about the technician go here: name, years of experience, languages. In Bali people choose a person, not a company.",
            master_ph="Technician photo", gallery="Work in Sanur", gallery_note="Real before/after photos go here. Illustrations shown for now.",
            map_h="Where I work", ready="Something broken? Send a photo — I'll reply on WhatsApp", credits="Illustrations: Unsplash"),
}

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,800&family=Manrope:wght@400;600;800&display=swap');
:root{--bg:#fbf6ee;--fg:#1d2a2c;--muted:#58676a;--card:#fff;--line:#eadfcd;--sea:#0b8a92;--sea2:#06606a;--sun:#f28c28;--hib:#e2465b;--leaf:#2f8f5b;--wa:#1faa59;--shadow:0 10px 30px rgba(20,60,60,.12)}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#0f1a1b;--fg:#eef4f2;--muted:#a3b6b4;--card:#172628;--line:#26393b;--sea:#3cc2c9;--sea2:#8fe0e4;--shadow:0 10px 30px rgba(0,0,0,.4)}}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;font:17px/1.65 Manrope,system-ui,sans-serif;background:var(--bg);color:var(--fg)}
h1,h2,h3{font-family:Fraunces,Georgia,serif;line-height:1.12;letter-spacing:-.01em}
a{color:var(--sea)}img{max-width:100%;display:block}
.wrap{max-width:1140px;margin:0 auto;padding:0 16px}
.topbar{background:var(--sea2);color:#fff;font-size:14px}.topbar .wrap{display:flex;justify-content:space-between;gap:10px;padding:7px 16px;flex-wrap:wrap}
.topbar a{color:#fff;font-weight:800;text-decoration:none}
header{background:color-mix(in srgb,var(--card) 92%,transparent);backdrop-filter:blur(8px);position:sticky;top:0;z-index:20;border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;min-height:64px;gap:12px}
.logo{display:flex;align-items:center;gap:10px;font:800 21px Fraunces,serif;color:var(--fg);text-decoration:none}
.logo i{width:38px;height:38px;border-radius:12px;background:linear-gradient(135deg,var(--sea),var(--leaf));display:grid;place-items:center;font-style:normal;font-size:20px}
nav{display:flex;gap:18px;align-items:center}nav a{color:var(--muted);text-decoration:none;font-weight:600;font-size:15px}nav a:hover{color:var(--sea)}
.hcall{background:var(--wa);color:#fff!important;padding:9px 16px;border-radius:999px}
@media(max-width:860px){nav a:not(.hcall):not(.lang){display:none}}
.hero{position:relative;color:#fff;min-height:620px;display:flex;align-items:flex-end;overflow:hidden}
.hero>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(4,40,44,.15) 0%,rgba(4,40,44,.55) 45%,rgba(4,30,33,.92) 100%)}
.hero .wrap{position:relative;z-index:1;padding-bottom:56px;width:100%}
.badge{display:inline-block;background:rgba(255,255,255,.18);border:1px solid rgba(255,255,255,.35);padding:6px 14px;border-radius:999px;font-weight:600;font-size:14px;backdrop-filter:blur(6px)}
.hero h1{font-size:clamp(36px,6.4vw,70px);margin:16px 0 14px;max-width:860px}.hero p{font-size:clamp(17px,2.2vw,21px);max-width:680px;opacity:.95}
.btns{display:flex;gap:12px;flex-wrap:wrap;margin:26px 0 0}
.btn{display:inline-flex;align-items:center;gap:8px;padding:15px 24px;border-radius:14px;font-weight:800;text-decoration:none;border:2px solid transparent;transition:transform .15s}
.btn:hover{transform:translateY(-2px)}.btn.wa{background:var(--wa);color:#fff;box-shadow:0 8px 24px rgba(31,170,89,.4)}
.btn.tel{background:var(--sun);color:#fff}.btn.tg{background:rgba(255,255,255,.14);color:inherit;border-color:currentColor}
.trust{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px;margin-top:-34px;position:relative;z-index:3}
.trust div{background:var(--card);border-radius:16px;padding:16px 18px;box-shadow:var(--shadow);display:flex;gap:12px;align-items:center;font-weight:600;font-size:15px}
.trust b{font-size:26px}
section{padding:64px 0}h2{font-size:clamp(30px,4.2vw,44px);margin:0 0 10px}.sub{color:var(--muted);max-width:640px;margin:0 0 28px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:18px}
.scard{background:var(--card);border-radius:20px;overflow:hidden;text-decoration:none;color:var(--fg);box-shadow:var(--shadow);transition:transform .2s}
.scard:hover{transform:translateY(-4px)}.scard img{height:170px;width:100%;object-fit:cover}
.scard div{padding:16px 18px 20px}.scard b{font:700 20px Fraunces,serif;display:block;margin-bottom:4px}.scard span{color:var(--muted);font-size:15px}
.band{background:linear-gradient(135deg,#06606a,#0b8a92);color:#fff}.band .sub{color:#d9f3f3}
.steps{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px;counter-reset:s;padding:0;list-style:none}
.steps li{background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.25);border-radius:18px;padding:22px;counter-increment:s;font-weight:600}
.steps li:before{content:counter(s);display:grid;place-items:center;width:44px;height:44px;border-radius:50%;background:var(--sun);color:#fff;font:800 20px Fraunces;margin-bottom:12px}
.why{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:18px}.why div{border-left:4px solid var(--hib);padding:4px 0 4px 18px}
.why b{font:700 21px Fraunces,serif;display:block}
.master{display:grid;grid-template-columns:minmax(220px,360px) 1fr;gap:34px;align-items:center}
@media(max-width:760px){.master{grid-template-columns:1fr}}
.ph{aspect-ratio:4/5;border-radius:24px;border:3px dashed var(--sun);display:grid;place-items:center;text-align:center;color:var(--muted);background:repeating-linear-gradient(45deg,transparent 0 14px,rgba(242,140,40,.07) 14px 28px);font-weight:700;padding:20px}
.gal{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:12px}.gal img{border-radius:16px;aspect-ratio:1;object-fit:cover}
.areas{display:flex;flex-wrap:wrap;gap:8px;margin:14px 0 22px}.areas span{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:6px 14px;font-weight:600;font-size:15px}
.map{border:0;width:100%;height:380px;border-radius:20px;box-shadow:var(--shadow)}
.split{display:grid;grid-template-columns:1fr 1fr;gap:34px;align-items:center}@media(max-width:860px){.split{grid-template-columns:1fr}}
.split img{border-radius:24px;box-shadow:var(--shadow);aspect-ratio:4/3;object-fit:cover}
ul.check{list-style:none;padding:0}ul.check li{padding:8px 0 8px 34px;position:relative;border-bottom:1px solid var(--line)}
ul.check li:before{content:"✓";position:absolute;left:0;top:7px;width:24px;height:24px;border-radius:50%;background:var(--leaf);color:#fff;display:grid;place-items:center;font-size:14px;font-weight:800}
details{background:var(--card);border-radius:14px;padding:14px 18px;margin:10px 0;box-shadow:var(--shadow)}summary{font-weight:800;cursor:pointer}
table{width:100%;border-collapse:collapse;background:var(--card);border-radius:16px;overflow:hidden;box-shadow:var(--shadow)}td,th{padding:14px;text-align:left;border-bottom:1px solid var(--line)}th{background:var(--sea);color:#fff}
.phead{position:relative;color:#fff;padding:70px 0 50px;overflow:hidden}.phead>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.phead:after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(4,40,44,.92),rgba(4,40,44,.5))}.phead .wrap{position:relative;z-index:1}
.phead h1{font-size:clamp(32px,5vw,54px);margin:10px 0}.crumbs{font-size:14px;opacity:.85}.crumbs a{color:#fff}
.cta{background:linear-gradient(135deg,var(--sun),var(--hib));color:#fff;border-radius:28px;padding:40px;text-align:center;margin:30px 0}
.cta h2{color:#fff}.cta .btns{justify-content:center}
footer{background:#0a2f33;color:#cfe3e2;padding:44px 0 90px;font-size:15px}footer a{color:#fff}footer .cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:24px}
footer b{font-family:Fraunces,serif;font-size:19px;color:#fff}.cred{opacity:.6;font-size:13px;margin-top:20px}
.mbar{display:none}@media(max-width:760px){.mbar{display:grid;grid-template-columns:1fr 1fr;position:fixed;left:0;right:0;bottom:0;z-index:30}
.mbar a{padding:15px;text-align:center;font-weight:800;color:#fff;text-decoration:none}.mbar .w{background:var(--wa)}.mbar .t{background:var(--sun)}.float{display:none}}
.float{position:fixed;right:18px;bottom:18px;z-index:30;width:62px;height:62px;border-radius:50%;background:var(--wa);display:grid;place-items:center;box-shadow:0 8px 24px rgba(0,0,0,.3);animation:p 2.4s infinite}
@media(max-width:760px){.float{display:none}}
@keyframes p{0%{box-shadow:0 0 0 0 rgba(31,170,89,.55)}70%{box-shadow:0 0 0 18px rgba(31,170,89,0)}100%{box-shadow:0 0 0 0 rgba(31,170,89,0)}}
"""
WA_SVG = '<svg width="30" height="30" viewBox="0 0 24 24" fill="#fff" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 1.9 17.7L.3 23.7l6.1-1.6A11.8 11.8 0 0 0 20.5 3.5zM12 21.6c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.6.9 1-3.5-.2-.4A9.8 9.8 0 1 1 12 21.6zm5.4-7.3c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8 8 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1 1-1 2.5 1 2.9 1.2 3.1 2.1 3.2 5.1 4.5c1.9.8 2.6.9 3.6.7.6-.1 1.8-.7 2-1.4s.3-1.3.2-1.4-.3-.2-.6-.3z"/></svg>'

def wa_link(t, what=""):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(t['wa_text'] + what)}"

def url(lang, slug=""):
    return BASE + "/" + T[lang]["pre"] + (slug + "/" if slug else "")

TEL = "tel:" + PHONE.replace(" ", "").replace("-", "")

def buttons(t, what="", dark=True):
    return (f'<div class="btns"><a class="btn wa" href="{wa_link(t, what)}">{WA_SVG[:-6].replace("30", "22")}</svg> {t["wa"]}</a>'
            f'<a class="btn tel" href="{TEL}">📞 {PHONE}</a>'
            f'<a class="btn tg" href="https://t.me/{TELEGRAM}">✈️ {t["tg"]}</a>'
            + (f'<a class="btn tg" href="{GBP_URL}">⭐ Google</a>' if GBP_URL else '') + '</div>')

def page(lang, slug, title, descr, body, alt_slug, crumbs=None, schema=None, head=None):
    t, x, e = T[lang], X[lang], html.escape
    sv, pr, ar, ct = ("uslugi", "ceny", "rajony", "kontakty") if lang == "ru" else ("services", "prices", "areas", "contact")
    nav = "".join(f'<a href="{url(lang, s)}">{n}</a>' for s, n in [(sv, t["services"]), (pr, t["prices"]), (ar, t["areas"]), (ct, t["contacts"])])
    nav += f'<a class="lang" href="{url(t["other"], alt_slug)}" hreflang="{t["other"]}">{t["switch"]}</a><a class="hcall" href="{wa_link(t)}">WhatsApp</a>'
    top = ""
    if head:  # шапка внутренней страницы с фото
        cr = '<div class="crumbs"><a href="' + url(lang) + '">' + t["home"] + "</a> › " + " › ".join(
            f'<a href="{u}">{n}</a>' if u else n for n, u in (crumbs or [])) + "</div>"
        top = f'<div class="phead"><img src="{img(head[0], 1600, 700)}" alt="" fetchpriority="high"><div class="wrap">{cr}<h1>{head[1]}</h1><p style="max-width:680px;font-size:19px">{head[2]}</p>{buttons(t, head[1])}</div></div>'
    ld = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>' if schema else ""
    svc_links = "".join(f'<a href="{url(lang, s[1] if lang == "ru" else s[2])}">{s[3] if lang == "ru" else s[4]}</a><br>' for s in S[:8])
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(descr)}"><meta name="theme-color" content="#06606a">
<link rel="canonical" href="{DOMAIN}{url(lang, slug)}">
<link rel="alternate" hreflang="{lang}" href="{DOMAIN}{url(lang, slug)}"><link rel="alternate" hreflang="{t['other']}" href="{DOMAIN}{url(t['other'], alt_slug)}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url('en', alt_slug if lang == 'ru' else slug)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(descr)}"><meta property="og:image" content="{img(PH['hero'][0], 1200, 630)}">
<link rel="preconnect" href="https://images.unsplash.com"><link rel="stylesheet" href="{BASE}/style.css">{'<meta name="robots" content="noindex,nofollow">' if PREVIEW else ''}{ld}</head><body>
<div class="topbar"><div class="wrap"><span>🌴 {t['tagline']}</span><span><a href="{TEL}">📞 {PHONE}</a> · <a href="{wa_link(t)}">WhatsApp</a></span></div></div>
<header><div class="wrap"><a class="logo" href="{url(lang)}"><i>🌺</i>{BRAND}</a><nav>{nav}</nav></div></header>
<main>{top}{body}</main>
<footer><div class="wrap"><div class="cols"><div><b>{BRAND}</b><br>{t['tagline']}.<br>{', '.join(AREAS_RU if lang == 'ru' else AREAS_EN)}.</div>
<div><b>{t['services']}</b><br>{svc_links}</div>
<div><b>{t['contacts']}</b><br>📞 <a href="{TEL}">{PHONE}</a><br>💬 <a href="{wa_link(t)}">WhatsApp</a><br>✈️ <a href="https://t.me/{TELEGRAM}">@{TELEGRAM}</a></div></div>
<div class="cred">{x['credits']}: {', '.join(sorted({a for _, a in PH.values()}))}.</div></div></footer>
<a class="float" href="{wa_link(t)}" aria-label="WhatsApp">{WA_SVG}</a>
<div class="mbar"><a class="w" href="{wa_link(t)}">💬 WhatsApp</a><a class="t" href="{TEL}">📞 {t['call']}</a></div>
<script>document.addEventListener('click',e=>{{const a=e.target.closest('a[href^="https://wa.me"],a[href^="tel:"],a[href^="https://t.me"]');if(a&&window.gtag)gtag('event','generate_lead',{{method:a.href.split(':')[0]}})}});</script>
</body></html>"""

def biz_schema(lang):
    return {"@context": "https://schema.org", "@type": "Plumber", "name": BRAND, "url": DOMAIN + url(lang), "telephone": PHONE,
            "image": img(PH["hero"][0], 1200), "areaServed": {"@type": "Place", "name": "Sanur, Denpasar Selatan, Bali"}, "sameAs": [GBP_URL] if GBP_URL else []}

pages = []
def write(lang, slug, content):
    p = ROOT / T[lang]["pre"] / slug / "index.html" if slug else ROOT / T[lang]["pre"] / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    if slug != "404":
        pages.append((lang, slug))

MAP = '<iframe class="map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Sanur,+Denpasar+Selatan,+Bali&z=14&output=embed" title="Sanur map"></iframe>'

def build():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir()
    (ROOT / "style.css").write_text(CSS, encoding="utf-8")
    for lang in ("ru", "en"):
        t, x = T[lang], X[lang]
        ru = lang == "ru"
        slug_of = lambda s: s[1] if ru else s[2]
        name_of = lambda s: s[3] if ru else s[4]
        sv, pr, ar, ct = ("uslugi", "ceny", "rajony", "kontakty") if ru else ("services", "prices", "areas", "contact")
        osv, opr, oar, oct_ = ("services", "prices", "areas", "contact") if ru else ("uslugi", "ceny", "rajony", "kontakty")
        cards = "".join(f'<a class="scard" href="{url(lang, slug_of(s))}"><img loading="lazy" src="{img(PH[s[0]][0], 600, 400)}" alt="{name_of(s)}">'
                        f'<div><b>{ICON[s[0]]} {name_of(s)}</b><span>{(s[7] if ru else s[8])[0]} · {(s[7] if ru else s[8])[1].lower()}</span></div></a>' for s in S)
        trust = '<div class="wrap trust">' + "".join(f"<div><b>{i}</b>{txt}</div>" for i, txt in x["trust"]) + "</div>"
        steps = '<ol class="steps">' + "".join(f"<li>{s}</li>" for s in t["steps"]) + "</ol>"
        how = f'<section class="band"><div class="wrap"><h2>{t["how"]}</h2><p class="sub">{x["ready"]}</p>{steps}</div></section>'
        chips = '<div class="areas"><span>📍 Sanur</span>' + "".join(f"<span>{a}</span>" for a in (AREAS_RU if ru else AREAS_EN)) + "</div>"
        why = f'<section><div class="wrap"><h2>{x["why"]}</h2><div class="why">' + "".join(f"<div><b>{a}</b>{b}</div>" for a, b in x["why_items"]) + "</div></div></section>"
        master = (f'<section><div class="wrap master"><div class="ph">📷<br>{x["master_ph"]}<br><small>{"(заменить на реальное фото)" if ru else "(replace with a real photo)"}</small></div>'
                  f'<div><h2>{x["master_h"]}</h2><p class="sub">{x["master_txt"]}</p>{buttons(t)}</div></div></section>')
        gal = (f'<section><div class="wrap"><h2>{x["gallery"]}</h2><p class="sub">{x["gallery_note"]}</p><div class="gal">'
               + "".join(f'<img loading="lazy" src="{img(PH[k][0], 500, 500)}" alt="">' for k in ["srv-remont-bassejna", "srv-bojler", "srv-chistka-bassejna", "srv-zasor", "srv-oborudovanie-bassejna", "srv-melkij-remont"])
               + "</div></div></section>")
        where = f'<section><div class="wrap split"><div><h2>{x["map_h"]}</h2><p class="sub">{t["area_txt"]}</p>{chips}{buttons(t)}</div>{MAP}</div></section>'
        cta = f'<div class="wrap"><div class="cta"><h2>{x["ready"]}</h2>{buttons(t)}</div></div>'

        hero = (f'<div class="hero"><img src="{img(PH["hero"][0], 1800, 1000)}" alt="Villa pool in Bali" fetchpriority="high"><div class="wrap">'
                f'<span class="badge">🌺 {x["badge"]}</span><h1>{t["home_h1"]}</h1><p>{t["home_lead"]}</p>{buttons(t)}</div></div>')
        body = (hero + trust + f'<section><div class="wrap"><h2>{t["services"]}</h2><p class="sub">{t["home_lead"]}</p><div class="grid">{cards}</div></div></section>'
                + how + why + master + gal + where + cta)
        write(lang, "", page(lang, "", f"{t['home_h1']} | {BRAND}", t["home_lead"][:155], body, "", schema=biz_schema(lang)))

        write(lang, sv, page(lang, sv, f"{t['services']} — {t['tagline']}", t["home_lead"][:155],
                             f'<section><div class="wrap"><div class="grid">{cards}</div></div></section>{how}{cta}', osv,
                             [(t["services"], None)], head=(PH["sanur"][0], t["services"], t["home_lead"])))
        for s in S:
            n = name_of(s)
            h1 = n if ("Sanur" in n or "Сануре" in n) else n + (" в Сануре" if ru else " in Sanur")
            intro, items, faq_l = (s[5], s[7], s[9]) if ru else (s[6], s[8], s[10])
            faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_l)
            price = PRICES.get(s[0], t["on_req"])
            idx = S.index(s)
            near = [S[(idx + k) % len(S)] for k in (1, 2, 3)]
            others = "".join(f'<a class="scard" href="{url(lang, slug_of(o))}"><img loading="lazy" src="{img(PH[o[0]][0], 600, 400)}" alt="{name_of(o)}"><div><b>{ICON[o[0]]} {name_of(o)}</b></div></a>' for o in near)
            body = (trust + f'<section><div class="wrap split"><div><h2>{t["fix"]}</h2><ul class="check">' + "".join(f"<li>{i}</li>" for i in items)
                    + f'</ul><p><b>{t["price"]}:</b> {price} · <a href="{url(lang, pr)}">{t["prices"]}</a></p></div>'
                    f'<img loading="lazy" src="{img(PH[s[0]][0], 900, 675)}" alt="{h1}"></div></section>'
                    + how + f'<section><div class="wrap"><h2>{t["faq"]}</h2>{faq}</div></section>' + where
                    + f'<section><div class="wrap"><h2>{t["services"]}</h2><div class="grid">{others}</div></div></section>' + cta)
            sch = [{"@context": "https://schema.org", "@type": "Service", "name": h1, "areaServed": "Sanur, Bali", "provider": {"@type": "Plumber", "name": BRAND, "telephone": PHONE}},
                   {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_l]}]
            write(lang, slug_of(s), page(lang, slug_of(s), f"{h1} | {BRAND}", intro[:155], body, s[2] if ru else s[1],
                                         [(t["services"], url(lang, sv)), (n, None)], schema=sch, head=(PH[s[0]][0], h1, intro)))
        rows = "".join(f"<tr><td>{ICON[s[0]]} <a href='{url(lang, slug_of(s))}'>{name_of(s)}</a></td><td>{PRICES.get(s[0], t['on_req'])}</td></tr>" for s in S)
        write(lang, pr, page(lang, pr, f"{t['prices_h1']} | {BRAND}", t["prices_note"][:155],
                             f'<section><div class="wrap"><table><tr><th>{t["work"]}</th><th>{t["price"]}</th></tr>{rows}</table></div></section>{how}{cta}',
                             opr, [(t["prices"], None)], head=(PH["srv-melkij-remont"][0], t["prices_h1"], t["prices_note"])))
        write(lang, ar, page(lang, ar, f"{t['areas_h1']} | {BRAND}", t["area_txt"], where + f'<section><div class="wrap"><div class="grid">{cards}</div></div></section>' + cta,
                             oar, [(t["areas"], None)], head=(PH["sanur2"][0], t["areas_h1"], t["area_txt"] + " " + ", ".join(AREAS_RU if ru else AREAS_EN))))
        write(lang, ct, page(lang, ct, f"{t['contacts_h1']} | {BRAND}", t["contacts_lead"],
                             f'<section><div class="wrap split"><div><h2>📞 {PHONE}</h2><p class="sub">WhatsApp · Telegram @{TELEGRAM}</p>{chips}</div>{MAP}</div></section>{cta}',
                             oct_, [(t["contacts"], None)], schema=biz_schema(lang), head=(PH["sanur"][0], t["contacts_h1"], t["contacts_lead"])))
    write("en", "404", page("en", "404", "404", "", f"<section><div class='wrap'><h1>404</h1><p>{T['en']['nf']} · <a href='{BASE}/'>Главная</a> · <a href='{BASE}/en/'>Home</a></p></div></section>", "404"))
    shutil.move(str(ROOT / "en" / "404" / "index.html"), str(ROOT / "404.html"))
    (ROOT / "en" / "404").rmdir()
    (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}{BASE}/sitemap.xml\n", encoding="utf-8")
    sm = "".join(f"<url><loc>{DOMAIN}{url(l, s)}</loc></url>" for l, s in pages)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>', encoding="utf-8")
    print("pages:", len(pages))

if __name__ == "__main__":
    build()
