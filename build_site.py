# -*- coding: utf-8 -*-
"""Статический сайт мастера в Сануре: EN (корень) + RU (/ru/) + статьи из content/. Запуск: python build_site.py → site/."""
import json, pathlib, shutil, html

# ======== ЗАПОЛНИТЬ ДАННЫМИ МАСТЕРА ========
DOMAIN = "https://jokerfrombali.github.io"  # домен сайта (без слэша в конце)
BASE = "/sanur-fix-site"                # подпапка; для своего домена — ""
PREVIEW = True                          # True = закрыт от индексации (просмотр на GitHub Pages)
BRAND = "Sanur Fix"                     # название (рабочее)
WHATSAPP = "6280000000000"              # номер WhatsApp без +
PHONE = "+62 800-0000-0000"
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
 "ru": dict(lang="ru", pre="ru/", other="en", tagline="Сантехник и мастер по бассейнам в Сануре", wa="Написать в WhatsApp", tg="Telegram", call="Позвонить",
            wa_text="Здравствуйте! Нужен мастер в Сануре: ", services="Услуги", prices="Цены", areas="Зона выезда", contacts="Контакты",
            fix="Что делаю", how="Как это работает", faq="Частые вопросы", on_req="по запросу", work="Работа", price="Цена",
            steps=["Пришлите фото или видео проблемы в WhatsApp", "Скажу примерную цену и когда смогу приехать", "Приезжаю, чиню, показываю результат"],
            area_txt="Работаю только в Сануре — весь район:", switch="English",
            home_h1="Сантехник и мастер по бассейнам в Сануре",
            home_lead="Частный мастер: сантехника, протечки, бойлеры, насосы, чистка и ремонт бассейнов, мелкий ремонт на виллах Санура. Пришлите фото — отвечу в WhatsApp.",
            prices_h1="Цены на работы в Сануре", prices_note="Цена зависит от объёма работ. Точную стоимость скажу по фото до выезда. Материалы — отдельно по чеку.",
            areas_h1="Работаю только в Сануре", contacts_h1="Контакты", contacts_lead="Быстрее всего — WhatsApp с фото проблемы и районом.",
            nf="Страница не найдена", home="Главная"),
 "en": dict(lang="en", pre="", other="ru", tagline="Plumber & Pool Service in Sanur", wa="WhatsApp me", tg="Telegram", call="Call",
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



# ================== ВИЗУАЛ И СБОРКА ==================
# Фото: Unsplash (бесплатная лицензия, хотлинк). ЗАМЕНИТЬ на реальные фото мастера и работ.
import sys
sys.path.insert(0, str(pathlib.Path(__file__).parent / "tools"))
from articles_plan import HUB_EN
U = "https://images.unsplash.com/"
def img(pid, w=900, h=None):
    return f"{U}{pid}?auto=format&fit=crop&w={w}{'&h=' + str(h) if h else ''}&q=70"
PH = {
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
HUB_PHOTOS = json.loads((pathlib.Path(__file__).parent / "tools" / "photos.json").read_text(encoding="utf-8"))
HUB_SRV = {"S": "srv-santehnik", "W": "srv-voda", "PC": "srv-chistka-bassejna", "PE": "srv-oborudovanie-bassejna",
           "PR": "srv-remont-bassejna", "K": "srv-septik", "R": "srv-melkij-remont", "V": "srv-obsluzhivanie-villy"}
HUB_RU = {"S": "Сантехника", "W": "Вода и насосы", "PC": "Уход за бассейном", "PE": "Оборудование бассейна", "PR": "Ремонт бассейна",
          "K": "Септик и канализация", "R": "Мелкий ремонт", "V": "Обслуживание виллы"}
CREDITS = {a for _, a in PH.values()}

X = {
 "en": dict(badge="Sanur only · Bali", guides="Guides", guides_h1="Villa & Pool Guides for Sanur", guides_lead="Practical guides from a technician who works only in Sanur: leaks, hot water, pumps, pools, septic tanks and small repairs.",
            toc="In this guide", related="Related guides", read="Read guide", all_guides="All guides", need_help="Need it fixed?", faq_h="Questions",
            trust=["Photo report on WhatsApp after every job", "Quote from your photos before I come", "Sanur only — I live and work here", "Parts charged with receipts"],
            why="Why Sanur villa owners call me", why_items=[("I come myself", "Not a call centre and not a crew. The person you message is the person who does the job."), ("One area only", "I don't cross the island. I know Sanur villas: old pools, brackish wells near the beach, rooftop tanks."), ("Reports for owners", "Abroad? You get before-and-after photos and a short list of what was done.")],
            master_h="Your technician", master_txt="A photo and a few words about the technician go here: name, years of experience, languages. In Bali people choose a person, not a company.",
            master_ph="Technician photo", map_h="Where I work", ready="Something broken? Send a photo on WhatsApp.",
            ready_sub="I'll reply with what's needed, a price and when I can come.", credits="Photos: Unsplash", eyebrow="Plumbing · Pools · Repairs"),
 "ru": dict(badge="Только Санур · Бали", guides="Статьи", guides_h1="Советы по вилле и бассейну в Сануре", guides_lead="Практические статьи от мастера, который работает только в Сануре: протечки, горячая вода, насосы, бассейны, септики, мелкий ремонт.",
            toc="Содержание", related="Похожие статьи", read="Читать", all_guides="Все статьи", need_help="Нужно починить?", faq_h="Вопросы",
            trust=["Фото-отчёт в WhatsApp после каждой работы", "Цена по фото — до выезда", "Только Санур — живу и работаю здесь", "Материалы по чеку"],
            why="Почему меня зовут владельцы вилл", why_items=[("Приезжаю сам", "Не диспетчерская и не бригада. С кем переписываетесь — тот и делает работу."), ("Только Санур", "Не мотаюсь по острову. Знаю виллы Санура: старые бассейны, солоноватые скважины у моря, баки на крыше."), ("Отчёт владельцу", "Вы не на Бали? Пришлю фото «до» и «после» и что было сделано.")],
            master_h="Мастер", master_txt="Здесь будет фото и пара слов о мастере: имя, опыт, языки. На Бали выбирают человека, а не компанию.",
            master_ph="Фото мастера", map_h="Где работаю", ready="Сломалось? Пришлите фото в WhatsApp.",
            ready_sub="Отвечу, что нужно, сколько стоит и когда смогу приехать.", credits="Фото: Unsplash", eyebrow="Сантехника · Бассейны · Ремонт"),
}
T["en"]["steps"] = ["Send a photo or short video on WhatsApp", "Get a price and a time that suits you", "I fix it and send you the result"]
T["ru"]["steps"] = ["Пришлите фото или видео в WhatsApp", "Получите цену и удобное время", "Чиню и присылаю результат"]

CSS = """
@import url('https://fonts.googleapis.com/css2?family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600;700&display=swap');
:root{--bg:#f6f3ee;--paper:#fffdf9;--ink:#1c2422;--muted:#66706c;--line:#e6e0d6;--green:#1f3b35;--green2:#2c5249;--brass:#a8834a;--wa:#1f9d57;--r:18px;--shadow:0 1px 2px rgba(28,36,34,.04),0 12px 32px rgba(28,36,34,.07)}
@media (prefers-color-scheme:dark){:root:not([data-theme=light]){--bg:#121816;--paper:#18201e;--ink:#ece8e1;--muted:#9aa39f;--line:#29332f;--green:#1a2f2a;--green2:#244039;--brass:#c9a46a;--shadow:0 12px 32px rgba(0,0,0,.35)}}
*{box-sizing:border-box}html{scroll-behavior:smooth;-webkit-text-size-adjust:100%}
body{margin:0;font:16.5px/1.7 Inter,system-ui,sans-serif;background:var(--bg);color:var(--ink);-webkit-font-smoothing:antialiased}
h1,h2,h3{font-family:"Instrument Serif",Georgia,serif;font-weight:400;line-height:1.08;letter-spacing:-.01em;margin:0}
h1 em,h2 em{font-style:italic;color:var(--brass)}
a{color:inherit}img{max-width:100%;display:block}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}.narrow{max-width:760px}
.eyebrow{font-size:12.5px;letter-spacing:.16em;text-transform:uppercase;color:var(--brass);font-weight:600}
header{position:sticky;top:0;z-index:40;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:saturate(1.4) blur(12px);border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:68px;gap:16px}
.logo{font:400 26px "Instrument Serif",serif;text-decoration:none;letter-spacing:-.01em}.logo span{color:var(--brass);font-style:italic}
nav{display:flex;align-items:center;gap:26px}nav a{text-decoration:none;font-size:14.5px;color:var(--muted);font-weight:500}nav a:hover{color:var(--ink)}
.lang{border:1px solid var(--line);border-radius:999px;padding:4px 10px;font-size:13px}
.lang b{color:var(--ink)}
.hbtn{background:var(--wa);color:#fff!important;padding:9px 16px;border-radius:999px;display:inline-flex;gap:7px;align-items:center}
@media(max-width:900px){nav a.m{display:none}nav{gap:12px}}
.btns{display:flex;gap:10px;flex-wrap:wrap}
.btn{display:inline-flex;align-items:center;gap:10px;padding:15px 22px;border-radius:999px;font-weight:600;font-size:15.5px;text-decoration:none;transition:transform .15s,background .15s;border:1px solid transparent}
.btn:hover{transform:translateY(-1px)}.btn svg{flex:none}
.btn.wa{background:var(--wa);color:#fff}.btn.wa:hover{background:#188a4b}
.btn.ghost{border-color:currentColor;color:inherit;background:transparent}
.hero{position:relative;min-height:min(88vh,760px);display:flex;align-items:flex-end;color:#fff;overflow:hidden}
.hero>img,.phead>img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.hero:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,20,18,.1) 20%,rgba(15,20,18,.72) 100%)}
.hero .wrap{position:relative;z-index:1;padding-bottom:72px;width:100%}
.hero .eyebrow{color:#e9d6b3}
.hero h1{font-size:clamp(46px,7.4vw,96px);max-width:900px;margin:14px 0 18px}.hero h1 em{color:#e9d6b3}
.hero p{font-size:clamp(17px,1.9vw,20px);max-width:600px;color:rgba(255,255,255,.88);margin:0 0 30px}
.strip{background:var(--green);color:#e8ece9}
.strip .wrap{display:grid;grid-template-columns:repeat(4,1fr);gap:0}.strip div{padding:22px 20px;border-left:1px solid rgba(255,255,255,.1);font-size:14.5px;display:flex;gap:12px;align-items:flex-start}
.strip div:first-child{border-left:0;padding-left:0}.strip svg{flex:none;margin-top:3px;color:#e9d6b3}
@media(max-width:860px){.strip .wrap{grid-template-columns:1fr 1fr}.strip div:nth-child(3){border-left:0;padding-left:0}}
section{padding:96px 0}@media(max-width:700px){section{padding:64px 0}}
.shead{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;margin-bottom:40px;flex-wrap:wrap}
.shead h2{font-size:clamp(38px,5vw,62px);max-width:720px;margin-top:10px}.shead p{color:var(--muted);max-width:420px;margin:0}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:22px}
.card{text-decoration:none;display:block;group:1}.card .im{border-radius:var(--r);overflow:hidden;aspect-ratio:4/3;background:var(--line)}
.card img{width:100%;height:100%;object-fit:cover;transition:transform .5s}.card:hover img{transform:scale(1.04)}
.card h3{font-size:25px;margin:16px 0 4px}.card p{color:var(--muted);font-size:14.5px;margin:0}
.card .more{display:inline-block;margin-top:8px;font-size:14px;font-weight:600;color:var(--brass)}
.dark{background:var(--green);color:#eef1ee}.dark .shead p{color:#b9c5c0}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:28px;list-style:none;padding:0;margin:0;counter-reset:s}
@media(max-width:760px){.steps{grid-template-columns:1fr}}
.steps li{counter-increment:s;border-top:1px solid rgba(255,255,255,.2);padding-top:22px;font-size:17px}
.steps li:before{content:"0" counter(s);display:block;font:italic 400 44px "Instrument Serif",serif;color:#e9d6b3;margin-bottom:6px}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:36px}@media(max-width:860px){.why{grid-template-columns:1fr}}
.why h3{font-size:30px;margin-bottom:8px}.why p{color:var(--muted);margin:0}
.master{display:grid;grid-template-columns:5fr 7fr;gap:60px;align-items:center}@media(max-width:860px){.master{grid-template-columns:1fr;gap:28px}}
.ph{aspect-ratio:4/5;border-radius:var(--r);border:1px dashed var(--brass);display:grid;place-items:center;text-align:center;color:var(--muted);font-size:14px;padding:20px;background:var(--paper)}
.master h2{font-size:clamp(38px,4.6vw,56px);margin:10px 0 16px}.master p{color:var(--muted);font-size:17.5px;max-width:560px;margin:0 0 28px}
.split{display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center}@media(max-width:860px){.split{grid-template-columns:1fr;gap:28px}}
.split h2{font-size:clamp(36px,4.4vw,54px);margin:10px 0 16px}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 28px}.chips span{border:1px solid var(--line);background:var(--paper);border-radius:999px;padding:6px 14px;font-size:14px}
.map{border:0;width:100%;aspect-ratio:4/3;border-radius:var(--r);filter:grayscale(.35) contrast(1.02)}
.phead{position:relative;color:#fff;padding:140px 0 64px;overflow:hidden}
.phead:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(15,20,18,.25),rgba(15,20,18,.78))}
.phead .wrap{position:relative;z-index:1}.phead h1{font-size:clamp(40px,6vw,76px);max-width:900px;margin:12px 0 16px}
.phead p{max-width:640px;font-size:18px;color:rgba(255,255,255,.88);margin:0 0 28px}
.crumbs{font-size:13px;color:rgba(255,255,255,.8)}.crumbs a{text-decoration:none}.crumbs a:hover{text-decoration:underline}
ul.check{list-style:none;padding:0;margin:0}ul.check li{padding:14px 0 14px 34px;border-bottom:1px solid var(--line);position:relative}
ul.check li:before{content:"";position:absolute;left:4px;top:22px;width:12px;height:7px;border-left:2px solid var(--brass);border-bottom:2px solid var(--brass);transform:rotate(-45deg)}
.split img.side{border-radius:var(--r);aspect-ratio:4/5;object-fit:cover;width:100%}
details{border-bottom:1px solid var(--line);padding:20px 0}summary{font-weight:600;cursor:pointer;list-style:none;display:flex;justify-content:space-between;gap:20px}
summary:after{content:"+";font-size:22px;color:var(--brass);line-height:1}details[open] summary:after{content:"–"}details p{color:var(--muted);margin:10px 0 0}
table{width:100%;border-collapse:collapse}td,th{padding:18px 0;text-align:left;border-bottom:1px solid var(--line)}th{font-size:12.5px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:600}
td:last-child,th:last-child{text-align:right;color:var(--muted)}td a{text-decoration:none;font-weight:500}
.cta{background:var(--green);color:#eef1ee;border-radius:28px;padding:64px 48px;display:grid;grid-template-columns:1.4fr 1fr;gap:32px;align-items:center}
.cta h2{font-size:clamp(34px,4.4vw,52px)}.cta p{color:#b9c5c0;margin:12px 0 0}.cta .btns{justify-content:flex-end}
@media(max-width:860px){.cta{grid-template-columns:1fr;padding:40px 26px}.cta .btns{justify-content:flex-start}}
.art{display:grid;grid-template-columns:240px minmax(0,720px);gap:64px;justify-content:center;padding:64px 0}
@media(max-width:980px){.art{grid-template-columns:1fr;gap:0}.toc{display:none}}
.toc{position:sticky;top:96px;align-self:start;font-size:14px}.toc b{display:block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.toc a{display:block;text-decoration:none;color:var(--muted);padding:6px 0;border-left:2px solid var(--line);padding-left:14px}.toc a:hover{color:var(--ink);border-color:var(--brass)}
.prose{font-size:18px;line-height:1.75}.prose .lead{font-size:21px;line-height:1.6;color:var(--ink);margin:0 0 12px}
.prose h2{font-size:clamp(30px,3.4vw,40px);margin:52px 0 14px;scroll-margin-top:90px}.prose p{margin:0 0 18px;color:color-mix(in srgb,var(--ink) 86%,var(--muted))}
.prose ul{padding-left:20px;margin:0 0 20px}.prose li{margin:6px 0}
.inline-cta{background:var(--paper);border:1px solid var(--line);border-left:3px solid var(--brass);border-radius:14px;padding:24px 26px;margin:36px 0;display:flex;gap:20px;justify-content:space-between;align-items:center;flex-wrap:wrap}
.inline-cta b{font:400 26px "Instrument Serif",serif}
.hubs{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:36px}.hubs a{border:1px solid var(--line);border-radius:999px;padding:8px 16px;font-size:14px;text-decoration:none;background:var(--paper)}.hubs a:hover,.hubs a.on{background:var(--green);color:#fff;border-color:var(--green)}
footer{background:#141c1a;color:#aeb8b4;padding:72px 0 110px;font-size:14.5px}footer a{text-decoration:none;color:#e8ece9}
footer .cols{display:grid;grid-template-columns:2fr 1fr 1fr 1fr;gap:36px}@media(max-width:860px){footer .cols{grid-template-columns:1fr 1fr}}
footer h4{font:400 13px Inter;letter-spacing:.14em;text-transform:uppercase;color:#6f7b77;margin:0 0 14px}footer .logo{color:#fff;font-size:30px}
.cred{margin-top:48px;font-size:12px;color:#5f6b67}
.float{position:fixed;right:22px;bottom:22px;z-index:50;width:58px;height:58px;border-radius:50%;background:var(--wa);display:grid;place-items:center;box-shadow:0 10px 26px rgba(0,0,0,.22)}
.mbar{display:none}
@media(max-width:760px){.float{display:none}.mbar{display:grid;grid-template-columns:1fr 1fr;gap:8px;position:fixed;left:10px;right:10px;bottom:10px;z-index:50}
.mbar a{display:flex;align-items:center;justify-content:center;gap:8px;padding:14px;border-radius:999px;font-weight:600;text-decoration:none;box-shadow:0 8px 24px rgba(0,0,0,.2)}
.mbar .w{background:var(--wa);color:#fff}.mbar .t{background:var(--paper);color:var(--ink);border:1px solid var(--line)}}
"""

WA_ICO = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.5 3.5A11.8 11.8 0 0 0 1.9 17.7L.3 23.7l6.1-1.6A11.8 11.8 0 0 0 20.5 3.5zM12 21.6c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.6.9 1-3.5-.2-.4A9.8 9.8 0 1 1 12 21.6zm5.4-7.3c-.3-.1-1.8-.9-2-1s-.5-.1-.7.1-.8 1-1 1.2-.4.2-.7.1a8 8 0 0 1-4-3.5c-.3-.5.3-.5.9-1.6.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4s-1 1-1 2.5 1 2.9 1.2 3.1 2.1 3.2 5.1 4.5c1.9.8 2.6.9 3.6.7.6-.1 1.8-.7 2-1.4s.3-1.3.2-1.4-.3-.2-.6-.3z"/></svg>'
PHONE_ICO = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>'
CHECK_ICO = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
wa_i = lambda s=20: WA_ICO.format(s=s)
ph_i = lambda s=18: PHONE_ICO.format(s=s)
TEL = "tel:" + PHONE.replace(" ", "").replace("-", "")

def wa_link(t, what=""):
    from urllib.parse import quote
    return f"https://wa.me/{WHATSAPP}?text={quote(t['wa_text'] + what)}"

def url(lang, slug=""):
    return BASE + "/" + T[lang]["pre"] + (slug + "/" if slug else "")

def buttons(t, what="", light=True):
    b = f'<div class="btns"><a class="btn wa" href="{wa_link(t, what)}">{wa_i()} {t["wa"]}</a><a class="btn ghost" href="{TEL}">{ph_i()} {PHONE}</a>'
    if GBP_URL:
        b += f'<a class="btn ghost" href="{GBP_URL}">Google reviews</a>'
    return b + "</div>"

SL = {"en": dict(sv="services", pr="prices", ar="area", ct="contact", gd="guides"),
      "ru": dict(sv="uslugi", pr="ceny", ar="rajon", ct="kontakty", gd="stati")}

def page(lang, slug, title, descr, body, alt_slug, crumbs=None, schema=None, head=None, og=None):
    t, x, e, sl = T[lang], X[lang], html.escape, SL[lang]
    other = t["other"]
    nav = "".join(f'<a class="m" href="{url(lang, s)}">{n}</a>' for s, n in [(sl["sv"], t["services"]), (sl["gd"], x["guides"]), (sl["pr"], t["prices"]), (sl["ar"], t["areas"]), (sl["ct"], t["contacts"])])
    lab = "<b>EN</b> · RU" if lang == "en" else "EN · <b>RU</b>"
    nav += f'<a class="lang" href="{url(other, alt_slug)}" hreflang="{other}">{lab}</a><a class="hbtn" href="{wa_link(t)}">{wa_i(16)} WhatsApp</a>'
    top = ""
    if head:
        cr = '<div class="crumbs"><a href="' + url(lang) + '">' + t["home"] + "</a> / " + " / ".join(
            f'<a href="{u}">{n}</a>' if u else n for n, u in (crumbs or [])) + "</div>"
        top = (f'<div class="phead"><img src="{img(head[0], 1800, 900)}" alt="" fetchpriority="high"><div class="wrap">{cr}'
               f'<h1>{head[1]}</h1><p>{head[2]}</p>{buttons(t, head[1])}</div></div>')
    ld = "".join(f'<script type="application/ld+json">{json.dumps(sc, ensure_ascii=False)}</script>' for sc in (schema if isinstance(schema, list) else [schema] if schema else []))
    svc = "".join(f'<a href="{url(lang, s[2] if lang == "en" else s[1])}">{s[4] if lang == "en" else s[3]}</a><br>' for s in S[:6])
    hubs = "".join(f'<a href="{url(lang, sl["gd"] + "/" + HUB_EN[h][0])}">{HUB_EN[h][1] if lang == "en" else HUB_RU[h]}</a><br>' for h in HUB_EN)
    ogimg = og or (head[0] if head else PH["hero"][0])
    return f"""<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(descr)}"><meta name="theme-color" content="#1f3b35">
{'<meta name="robots" content="noindex,nofollow">' if PREVIEW else ''}
<link rel="canonical" href="{DOMAIN}{url(lang, slug)}">
<link rel="alternate" hreflang="{lang}" href="{DOMAIN}{url(lang, slug)}"><link rel="alternate" hreflang="{other}" href="{DOMAIN}{url(other, alt_slug)}">
<link rel="alternate" hreflang="x-default" href="{DOMAIN}{url('en', slug if lang == 'en' else alt_slug)}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(descr)}"><meta property="og:image" content="{img(ogimg, 1200, 630)}">
<link rel="preconnect" href="https://images.unsplash.com"><link rel="stylesheet" href="{BASE}/style.css">{ld}</head><body>
<header><div class="wrap"><a class="logo" href="{url(lang)}">Sanur<span>Fix</span></a><nav>{nav}</nav></div></header>
<main>{top}{body}</main>
<footer><div class="wrap"><div class="cols"><div><a class="logo" href="{url(lang)}">Sanur<span>Fix</span></a><p>{t['tagline']}.<br>{x['badge']}.</p>
<p><a href="{wa_link(t)}">WhatsApp</a> · <a href="{TEL}">{PHONE}</a></p></div>
<div><h4>{t['services']}</h4>{svc}</div><div><h4>{x['guides']}</h4>{hubs}</div>
<div><h4>{t['contacts']}</h4><a href="{wa_link(t)}">WhatsApp</a><br><a href="{TEL}">{PHONE}</a><br><a href="{url(lang, sl['ar'])}">{t['areas']}</a><br><a href="{url(lang, sl['pr'])}">{t['prices']}</a></div></div>
<div class="cred">{x['credits']}.</div></div></footer>
<a class="float" href="{wa_link(t)}" aria-label="WhatsApp" style="color:#fff">{wa_i(28)}</a>
<div class="mbar"><a class="w" href="{wa_link(t)}">{wa_i(18)} WhatsApp</a><a class="t" href="{TEL}">{ph_i(16)} {t['call']}</a></div>
<script>document.addEventListener('click',e=>{{const a=e.target.closest('a[href^="https://wa.me"],a[href^="tel:"]');if(a&&window.gtag)gtag('event','generate_lead',{{method:a.href.split(':')[0]}})}});</script>
</body></html>"""

def biz_schema(lang):
    return {"@context": "https://schema.org", "@type": "Plumber", "name": BRAND, "url": DOMAIN + url(lang), "telephone": PHONE,
            "image": img(PH["hero"][0], 1200), "areaServed": {"@type": "Place", "name": "Sanur, Denpasar Selatan, Bali"},
            "sameAs": [GBP_URL] if GBP_URL else []}

pages = []
def write(lang, slug, content):
    base = ROOT / T[lang]["pre"] if T[lang]["pre"] else ROOT
    p = base / slug / "index.html" if slug else base / "index.html"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    if slug != "404":
        pages.append((lang, slug))

MAP = '<iframe class="map" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://maps.google.com/maps?q=Sanur,+Denpasar+Selatan,+Bali&z=14&output=embed" title="Sanur map"></iframe>'

def load_articles():
    """content/<lang>/A###.json → {lang: {id: data}}"""
    res = {}
    for lang in ("en", "ru"):
        d = pathlib.Path(__file__).parent / "content" / lang
        res[lang] = {}
        for f in sorted(d.glob("A*.json")) if d.exists() else []:
            a = json.loads(f.read_text(encoding="utf-8"))
            a["slug"] = re.sub(r"[^a-z0-9-]+", "-", a["slug"].lower()).strip("-")
            res[lang][a["id"]] = a
    # уникальность слагов
    for lang, arts in res.items():
        seen = set()
        for a in arts.values():
            while a["slug"] in seen:
                a["slug"] += "-" + a["id"].lower()
            seen.add(a["slug"])
    return res

def art_photo(a):
    pool = HUB_PHOTOS[a["hub"]]
    p = pool[int(a["id"][1:]) % len(pool)]
    CREDITS.add(p[1])
    return p[0]

import re

def build():
    if ROOT.exists():
        shutil.rmtree(ROOT)
    ROOT.mkdir()
    (ROOT / "style.css").write_text(CSS, encoding="utf-8")
    ARTS = load_articles()
    for lang in ("en", "ru"):
        t, x, sl, ru = T[lang], X[lang], SL[lang], lang == "ru"
        osl = SL[t["other"]]
        slug_of = lambda s: s[1] if ru else s[2]
        name_of = lambda s: s[3] if ru else s[4]
        areas_l = AREAS_RU if ru else AREAS_EN
        arts = ARTS[lang]
        other_arts = ARTS[t["other"]]
        gpath = lambda a: sl["gd"] + "/" + HUB_EN[a["hub"]][0] + "/" + a["slug"]
        def alt_art(a):
            o = other_arts.get(a["id"])
            return (osl["gd"] + "/" + HUB_EN[o["hub"]][0] + "/" + o["slug"]) if o else osl["gd"]

        cards = "".join(f'<a class="card" href="{url(lang, slug_of(s))}"><div class="im"><img loading="lazy" src="{img(PH[s[0]][0], 700, 525)}" alt="{name_of(s)}"></div>'
                        f'<h3>{name_of(s)}</h3><p>{(s[7] if ru else s[8])[0]} · {(s[7] if ru else s[8])[1].lower()}</p></a>' for s in S)
        strip = '<div class="strip"><div class="wrap">' + "".join(f"<div>{CHECK_ICO}<span>{v}</span></div>" for v in x["trust"]) + "</div></div>"
        steps = '<ol class="steps">' + "".join(f"<li>{s}</li>" for s in t["steps"]) + "</ol>"
        how = f'<section class="dark"><div class="wrap"><div class="shead"><div><div class="eyebrow">{t["how"]}</div><h2>{x["ready"]}</h2></div><p>{x["ready_sub"]}</p></div>{steps}</div></section>'
        chips = '<div class="chips"><span>Sanur</span>' + "".join(f"<span>{a}</span>" for a in areas_l) + "</div>"
        why = (f'<section><div class="wrap"><div class="shead"><h2>{x["why"]}</h2></div><div class="why">'
               + "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in x["why_items"]) + "</div></div></section>")
        master = (f'<section style="padding-top:0"><div class="wrap master"><div class="ph">{x["master_ph"]}<br>'
                  f'{"(заменить на реальное фото)" if ru else "(replace with a real photo)"}</div>'
                  f'<div><div class="eyebrow">{x["badge"]}</div><h2>{x["master_h"]}</h2><p>{x["master_txt"]}</p>{buttons(t)}</div></div></section>')
        where = (f'<section><div class="wrap split"><div><div class="eyebrow">{t["areas"]}</div><h2>{x["map_h"]}</h2>'
                 f'<p style="color:var(--muted)">{t["area_txt"]}</p>{chips}{buttons(t)}</div>{MAP}</div></section>')
        cta = (f'<section style="padding-top:0"><div class="wrap"><div class="cta"><div><h2>{x["ready"]}</h2><p>{x["ready_sub"]}</p></div>'
               f'<div class="btns"><a class="btn wa" href="{wa_link(t)}">{wa_i()} {t["wa"]}</a><a class="btn ghost" href="{TEL}">{ph_i()} {PHONE}</a></div></div></div></section>')
        def acard(a):
            return (f'<a class="card" href="{url(lang, gpath(a))}"><div class="im"><img loading="lazy" src="{img(art_photo(a), 700, 525)}" alt=""></div>'
                    f'<h3>{html.escape(a["title"])}</h3><p>{html.escape(a["meta"][:120])}…</p><span class="more">{x["read"]} →</span></a>')
        latest = list(arts.values())[:6]
        guides_block = (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><div><div class="eyebrow">{x["guides"]}</div><h2>{x["guides_h1"]}</h2></div>'
                        f'<p><a href="{url(lang, sl["gd"])}">{x["all_guides"]} ({len(arts)}) →</a></p></div><div class="grid">{"".join(acard(a) for a in latest)}</div></div></section>') if latest else ""

        # --- главная ---
        h1 = t["home_h1"].replace("Sanur", "<em>Sanur</em>").replace("Сануре", "<em>Сануре</em>")
        hero = (f'<div class="hero"><img src="{img(PH["hero"][0], 2000, 1200)}" alt="" fetchpriority="high"><div class="wrap">'
                f'<div class="eyebrow">{x["eyebrow"]}</div><h1>{h1}</h1><p>{t["home_lead"]}</p>{buttons(t)}</div></div>')
        body = (hero + strip + f'<section><div class="wrap"><div class="shead"><div><div class="eyebrow">{t["services"]}</div><h2>{t["tagline"]}</h2></div><p>{x["ready_sub"]}</p></div><div class="grid">{cards}</div></div></section>'
                + how + why + master + guides_block + where + cta)
        write(lang, "", page(lang, "", f"{t['home_h1']} | {BRAND}", t["home_lead"][:155], body, "", schema=biz_schema(lang)))
        # --- услуги ---
        write(lang, sl["sv"], page(lang, sl["sv"], f"{t['services']} — {t['tagline']}", t["home_lead"][:155],
                                   strip + f'<section><div class="wrap"><div class="grid">{cards}</div></div></section>{how}{cta}', osl["sv"],
                                   [(t["services"], None)], head=(PH["sanur"][0], t["services"], t["home_lead"])))
        for s in S:
            n = name_of(s)
            h1s = n if ("Sanur" in n or "Сануре" in n) else n + (" в Сануре" if ru else " in Sanur")
            intro, items, faq_l = (s[5], s[7], s[9]) if ru else (s[6], s[8], s[10])
            faq = "".join(f"<details><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_l)
            price = PRICES.get(s[0], t["on_req"])
            hub = next(h for h, v in HUB_SRV.items() if v == s[0]) if s[0] in HUB_SRV.values() else None
            rel = [a for a in arts.values() if a["hub"] == hub][:3] if hub else []
            idx = S.index(s)
            near = [S[(idx + k) % len(S)] for k in (1, 2, 3)]
            ncards = "".join(f'<a class="card" href="{url(lang, slug_of(o))}"><div class="im"><img loading="lazy" src="{img(PH[o[0]][0], 700, 525)}" alt="{name_of(o)}"></div><h3>{name_of(o)}</h3></a>' for o in near)
            body = (strip + f'<section><div class="wrap split"><div><div class="eyebrow">{t["fix"]}</div><h2>{n}</h2><ul class="check">' + "".join(f"<li>{i}</li>" for i in items)
                    + f'</ul><p style="margin-top:22px"><b>{t["price"]}:</b> {price} · <a href="{url(lang, sl["pr"])}">{t["prices"]}</a></p></div>'
                    f'<img class="side" loading="lazy" src="{img(PH[s[0]][0], 900, 1125)}" alt="{h1s}"></div></section>'
                    + how + f'<section><div class="wrap narrow"><div class="eyebrow">{x["faq_h"]}</div><h2 style="font-size:48px;margin:10px 0 20px">{t["faq"]}</h2>{faq}</div></section>'
                    + (f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{x["related"]}</h2></div><div class="grid">{"".join(acard(a) for a in rel)}</div></div></section>' if rel else "")
                    + where + f'<section style="padding-top:0"><div class="wrap"><div class="shead"><h2>{t["services"]}</h2></div><div class="grid">{ncards}</div></div></section>' + cta)
            sch = [{"@context": "https://schema.org", "@type": "Service", "name": h1s, "areaServed": "Sanur, Bali", "provider": {"@type": "Plumber", "name": BRAND, "telephone": PHONE}},
                   {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq_l]}]
            write(lang, slug_of(s), page(lang, slug_of(s), f"{h1s} | {BRAND}", intro[:155], body, s[2] if ru else s[1],
                                         [(t["services"], url(lang, sl["sv"])), (n, None)], schema=sch, head=(PH[s[0]][0], h1s, intro)))
        # --- цены / район / контакты ---
        rows = "".join(f"<tr><td><a href='{url(lang, slug_of(s))}'>{name_of(s)}</a></td><td>{PRICES.get(s[0], t['on_req'])}</td></tr>" for s in S)
        write(lang, sl["pr"], page(lang, sl["pr"], f"{t['prices_h1']} | {BRAND}", t["prices_note"][:155],
                                   f'<section><div class="wrap narrow"><table><tr><th>{t["work"]}</th><th>{t["price"]}</th></tr>{rows}</table></div></section>{how}{cta}',
                                   osl["pr"], [(t["prices"], None)], head=(PH["srv-melkij-remont"][0], t["prices_h1"], t["prices_note"])))
        write(lang, sl["ar"], page(lang, sl["ar"], f"{t['areas_h1']} | {BRAND}", t["area_txt"], where + f'<section style="padding-top:0"><div class="wrap"><div class="grid">{cards}</div></div></section>' + cta,
                                   osl["ar"], [(t["areas"], None)], head=(PH["sanur2"][0], t["areas_h1"], t["area_txt"] + " " + ", ".join(areas_l) + ".")))
        write(lang, sl["ct"], page(lang, sl["ct"], f"{t['contacts_h1']} | {BRAND}", t["contacts_lead"],
                                   f'<section><div class="wrap split"><div><div class="eyebrow">WhatsApp · {t["call"]}</div><h2>{PHONE}</h2>{buttons(t)}{chips}</div>{MAP}</div></section>',
                                   osl["ct"], [(t["contacts"], None)], schema=biz_schema(lang), head=(PH["sanur"][0], t["contacts_h1"], t["contacts_lead"])))
        # --- статьи ---
        def hubnav(on=None):
            return '<div class="hubs">' + f'<a class="{"on" if on is None else ""}" href="{url(lang, sl["gd"])}">{x["all_guides"]}</a>' + "".join(
                f'<a class="{"on" if on == h else ""}" href="{url(lang, sl["gd"] + "/" + HUB_EN[h][0])}">{HUB_EN[h][1] if not ru else HUB_RU[h]}</a>' for h in HUB_EN) + "</div>"
        write(lang, sl["gd"], page(lang, sl["gd"], f"{x['guides_h1']} | {BRAND}", x["guides_lead"],
                                   f'<section><div class="wrap">{hubnav()}<div class="grid">{"".join(acard(a) for a in arts.values())}</div></div></section>{cta}',
                                   osl["gd"], [(x["guides"], None)], head=(PH["sanur"][0], x["guides_h1"], x["guides_lead"])))
        for h, (hs, hn) in HUB_EN.items():
            hname = HUB_RU[h] if ru else hn
            ha = [a for a in arts.values() if a["hub"] == h]
            write(lang, sl["gd"] + "/" + hs, page(lang, sl["gd"] + "/" + hs, f"{hname} — {x['guides']} | {BRAND}", x["guides_lead"],
                  f'<section><div class="wrap">{hubnav(h)}<div class="grid">{"".join(acard(a) for a in ha)}</div></div></section>{cta}',
                  osl["gd"] + "/" + hs, [(x["guides"], url(lang, sl["gd"])), (hname, None)], head=(HUB_PHOTOS[h][0][0], hname, x["guides_lead"])))
        for a in arts.values():
            srv = next(s for s in S if s[0] == HUB_SRV[a["hub"]])
            secs = a["sections"]
            toc = "".join(f'<a href="#s{i}">{html.escape(sc["h2"])}</a>' for i, sc in enumerate(secs, 1))
            content = f'<p class="lead">{html.escape(a["intro"])}</p>'
            for i, sc in enumerate(secs, 1):
                content += f'<h2 id="s{i}">{html.escape(sc["h2"])}</h2>' + "".join(f"<p>{html.escape(p)}</p>" for p in sc.get("paragraphs", []))
                if sc.get("bullets"):
                    content += "<ul>" + "".join(f"<li>{html.escape(b)}</li>" for b in sc["bullets"]) + "</ul>"
                if i == 2:
                    content += (f'<div class="inline-cta"><div><b>{x["need_help"]}</b><br><span style="color:var(--muted)">{html.escape(a.get("cta") or x["ready_sub"])}</span></div>'
                                f'<a class="btn wa" href="{wa_link(t, a["title"])}">{wa_i()} WhatsApp</a></div>')
            if a.get("faq"):
                content += f'<h2 id="faq">{x["faq_h"]}</h2>' + "".join(f'<details><summary>{html.escape(q["q"])}</summary><p>{html.escape(q["a"])}</p></details>' for q in a["faq"])
            content += (f'<div class="inline-cta"><div><b>{name_of(srv)}</b><br><span style="color:var(--muted)">{x["ready_sub"]}</span></div>'
                        f'<a class="btn ghost" href="{url(lang, slug_of(srv))}">{t["services"]} →</a></div>')
            rel = [o for o in arts.values() if o["hub"] == a["hub"] and o is not a][:3]
            body = (f'<div class="wrap art"><aside class="toc"><b>{x["toc"]}</b>{toc}</aside><article class="prose">{content}</article></div>'
                    + (f'<section style="padding-top:24px"><div class="wrap"><div class="shead"><h2>{x["related"]}</h2></div><div class="grid">{"".join(acard(o) for o in rel)}</div></div></section>' if rel else "") + cta)
            photo = art_photo(a)
            hname = HUB_RU[a["hub"]] if ru else HUB_EN[a["hub"]][1]
            sch = [{"@context": "https://schema.org", "@type": "Article", "headline": a["title"], "description": a["meta"], "image": img(photo, 1200),
                    "author": {"@type": "Organization", "name": BRAND}, "publisher": {"@type": "Organization", "name": BRAND}}]
            if a.get("faq"):
                sch.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q["q"], "acceptedAnswer": {"@type": "Answer", "text": q["a"]}} for q in a["faq"]]})
            write(lang, gpath(a), page(lang, gpath(a), f"{a['title']} | {BRAND}", a["meta"], body, alt_art(a),
                                       [(x["guides"], url(lang, sl["gd"])), (hname, url(lang, sl["gd"] + "/" + HUB_EN[a["hub"]][0])), (a["title"][:40] + ("…" if len(a["title"]) > 40 else ""), None)],
                                       schema=sch, head=(photo, html.escape(a["title"]), html.escape(a["intro"][:220])), og=photo))
    # 404, robots, sitemap
    write("en", "404", page("en", "404", "404", "", f"<section><div class='wrap'><h1>404</h1><p>{T['en']['nf']} · <a href='{BASE}/'>Home</a> · <a href='{BASE}/ru/'>Главная</a></p></div></section>", "404"))
    shutil.move(str(ROOT / "404" / "index.html"), str(ROOT / "404.html"))
    (ROOT / "404").rmdir()
    (ROOT / "robots.txt").write_text("User-agent: *\nDisallow: /\n" if PREVIEW else f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}{BASE}/sitemap.xml\n", encoding="utf-8")
    sm = "".join(f"<url><loc>{DOMAIN}{url(l, s)}</loc></url>" for l, s in pages)
    (ROOT / "sitemap.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{sm}</urlset>', encoding="utf-8")
    print("pages:", len(pages), "| articles en/ru:", len(ARTS["en"]), len(ARTS["ru"]))

if __name__ == "__main__":
    build()
