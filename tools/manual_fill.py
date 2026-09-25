# -*- coding: utf-8 -*-
"""Ручной перевод ключей v2 для pl/cs/zh (локальная модель на них срывалась)."""
import json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
T = {
"pl": {"only": "Tylko Sanur", "call_or_wa": "Wyślij zdjęcie na WhatsApp albo zadzwoń {phone} — powiem, co trzeba zrobić i kiedy mogę przyjechać.",
 "local_eyebrow": "Lokalna wiedza", "local_h": "Hydraulika w Sanur jest inna",
 "local_intro": "Większość zgłoszeń w Sanur wynika z tych samych lokalnych warunków. Ich znajomość to połowa diagnozy — dlatego pracuję tylko w jednej okolicy.",
 "local_items": [["Wille sprzed 15–20 lat", "Wiele willi w Sanur ma wciąż oryginalne rury i złączki PVC. Rury na słońcu kruszeją, a połączenia zaczynają przeciekać. Często lepiej wymienić odcinek, niż znowu go łatać."],
  ["Słone powietrze przy plaży", "W Sindhu, Semawang i Mertasari morskie powietrze niszczy baterie, słuchawki prysznicowe, zawiasy i silniki pomp znacznie szybciej niż w głębi lądu. Dobre materiały oszczędzają powtórnych napraw."],
  ["Woda ze studni i PDAM", "Wiele willi łączy wodociąg PDAM ze studnią. Blisko morza woda ze studni bywa słonawa — filtry i wkłady szybciej się zapychają, a w bojlerach osadza się kamień."],
  ["Zbiorniki na dachu i pompy", "Ciśnienie wody zależy od zbiornika, pompy i presostatu. Większość zgłoszeń „słaby prysznic” i „pompa ciągle się włącza” zaczyna się tutaj, a nie w kranie."],
  ["Szamba i papier toaletowy", "Szamba są małe, a rury wąskie. Zatory i zapach zwykle oznaczają papier lub tłuszcz w instalacji albo szambo, które dawno trzeba było opróżnić."],
  ["Pora deszczowa", "Mniej więcej od listopada do marca ulewy sprawdzają dachy, rynny, odpływy, baseny i szamba. Najlepiej zrobić przegląd przed pierwszymi dużymi burzami."]],
 "hoods_h": "Cały Sanur", "hoods_txt": "Pracuję w całym Sanur: Sanur Kaja, Sanur Kauh, Sindhu, Semawang, Mertasari i Batujimbar — wzdłuż Jl. Danau Tamblingan, Jl. Danau Poso i Bypass Ngurah Rai. Wille, domy, apartamenty i małe pensjonaty.",
 "all_services": "Wszystkie usługi", "pricing_h": "Jak liczę cenę",
 "pricing_items": [["Cena przed pracą", "Wyślij zdjęcia lub film — cenę poznasz przed przyjazdem i ustalamy ją przed rozpoczęciem pracy."], ["Części z paragonem", "Części kupuję po cenie zakupu, a paragon dostajesz ty."], ["Raport ze zdjęciami", "Po pracy dostajesz na WhatsApp zdjęcia „przed” i „po”."]],
 "reviews_h": "Opinie klientów", "reviews_more": "Wszystkie opinie w Google", "projects": "Realizacje", "projects_h1": "Ostatnie realizacje w Sanur",
 "projects_lead": "Prawdziwe zlecenia w Sanur: co było zepsute i co zostało zrobione.", "emergency": "Pilne wezwania", "about_h": "O fachowcu",
 "years": "lat doświadczenia", "langs": "Języki", "warranty": "Gwarancja", "sample": "Dane przykładowe", "form_h": "Napisz, co się stało",
 "form_what": "Co się dzieje?", "form_when": "Na kiedy?", "when_opts": ["Dziś — pilne", "W tym tygodniu", "Tylko wycena"], "form_btn": "Wyślij na WhatsApp",
 "form_note": "Otworzy się WhatsApp z twoją wiadomością. Dodaj tam zdjęcie.", "rated": "Ocena {r} · {n} opinii", "serving": "Z dumą obsługujemy Sanur"},
"cs": {"only": "Jen Sanur", "call_or_wa": "Pošlete fotku přes WhatsApp nebo zavolejte {phone} — řeknu, co je potřeba a kdy můžu přijet.",
 "local_eyebrow": "Místní znalosti", "local_h": "Instalatérství v Sanuru je jiné",
 "local_intro": "Většina výjezdů v Sanuru má stejné místní příčiny. Znát je znamená mít půlku diagnózy — proto pracuji jen v jedné oblasti.",
 "local_items": [["Vily staré 15–20 let", "Mnoho vil v Sanuru má stále původní PVC potrubí a armatury. Trubky na slunci křehnou a spoje začnou prosakovat. Často je rozumnější vyměnit úsek než ho znovu záplatovat."],
  ["Slaný vzduch u pláže", "V Sindhu, Semawangu a Mertasari mořský vzduch ničí baterie, sprchové hlavice, panty a motory čerpadel mnohem rychleji než ve vnitrozemí. Správné materiály ušetří opakované opravy."],
  ["Studna a PDAM", "Mnoho vil kombinuje vodovod PDAM se studnou. Blízko moře bývá voda ze studny brakická — filtry a vložky se ucpávají rychleji a v bojlerech se usazuje vodní kámen."],
  ["Nádrže na střeše a čerpadla", "Tlak vody závisí na nádrži, čerpadle a tlakovém spínači. Většina hlášení „slabá sprcha“ a „čerpadlo pořád spíná“ začíná tady, ne v kohoutku."],
  ["Septiky a toaletní papír", "Septiky jsou malé a trubky úzké. Ucpání a zápach obvykle znamenají papír nebo tuk v systému, případně septik, který měl být dávno vyvezen."],
  ["Období dešťů", "Zhruba od listopadu do března prověří lijáky střechy, okapy, odpady, bazény i septiky. Nejlepší je kontrola ještě před prvními velkými bouřkami."]],
 "hoods_h": "Celý Sanur", "hoods_txt": "Pracuji v celém Sanuru: Sanur Kaja, Sanur Kauh, Sindhu, Semawang, Mertasari a Batujimbar — podél Jl. Danau Tamblingan, Jl. Danau Poso a Bypass Ngurah Rai. Vily, domy, apartmány i malé penziony.",
 "all_services": "Všechny služby", "pricing_h": "Jak počítám cenu",
 "pricing_items": [["Cena předem", "Pošlete fotky nebo video — cenu znáte před výjezdem a domluvíme ji před začátkem práce."], ["Díly s účtenkou", "Díly nakupuji za nákupní cenu a účtenku dostanete vy."], ["Fotoreport", "Po práci dostanete na WhatsApp fotky „před“ a „po“."]],
 "reviews_h": "Co říkají klienti", "reviews_more": "Všechny recenze na Googlu", "projects": "Práce", "projects_h1": "Nedávné práce v Sanuru",
 "projects_lead": "Skutečné zakázky v Sanuru: co bylo špatně a co se udělalo.", "emergency": "Urgentní výjezdy", "about_h": "O technikovi",
 "years": "let praxe", "langs": "Jazyky", "warranty": "Záruka", "sample": "Ukázková data", "form_h": "Napište, co se děje",
 "form_what": "Co se stalo?", "form_when": "Kdy to potřebujete?", "when_opts": ["Dnes — spěchá", "Tento týden", "Jen cenová nabídka"], "form_btn": "Poslat přes WhatsApp",
 "form_note": "Otevře se WhatsApp s vaší zprávou. Přidejte tam fotku.", "rated": "Hodnocení {r} · {n} recenzí", "serving": "Hrdě sloužíme Sanuru"},
"zh": {"only": "仅限沙努尔", "call_or_wa": "在 WhatsApp 发送照片或致电 {phone}——我会告诉您需要做什么以及何时能上门。",
 "local_eyebrow": "本地经验", "local_h": "沙努尔的水管问题与众不同",
 "local_intro": "沙努尔的大多数上门维修都源于相同的本地条件。了解这些条件就完成了一半的诊断——这也是我只在一个区域工作的原因。",
 "local_items": [["建成 15–20 年的别墅", "许多沙努尔别墅仍在使用最初的 PVC 管道和配件。长期日晒的管道会变脆，接口开始渗漏。很多时候更换一段管道比反复修补更划算。"],
  ["海边的含盐空气", "在 Sindhu、Semawang 和 Mertasari，海风对水龙头、花洒、合页和水泵电机的腐蚀比内陆快得多。选对材料可以避免反复维修。"],
  ["井水与 PDAM 自来水", "许多别墅同时使用 PDAM 自来水和井水。靠近海边的井水可能偏咸——过滤器和滤芯更容易堵塞，热水器也更容易结垢。"],
  ["屋顶水箱与水泵", "水压取决于水箱、水泵和压力开关。大多数“淋浴水小”和“水泵频繁启动”的问题出在这里，而不是水龙头。"],
  ["化粪池与卫生纸", "化粪池容量小、管道细。堵塞和异味通常是系统里有卫生纸或油脂，或者化粪池早该抽了。"],
  ["雨季", "大约 11 月到次年 3 月的暴雨会考验屋顶、排水槽、下水道、泳池和化粪池。最好在第一场大雨前做好检查。"]],
 "hoods_h": "覆盖整个沙努尔", "hoods_txt": "我在整个沙努尔提供服务：Sanur Kaja、Sanur Kauh、Sindhu、Semawang、Mertasari 和 Batujimbar——沿 Jl. Danau Tamblingan、Jl. Danau Poso 和 Bypass Ngurah Rai。别墅、住宅、公寓和小型民宿均可。",
 "all_services": "全部服务", "pricing_h": "如何报价",
 "pricing_items": [["先报价再施工", "发送照片或视频——上门前您就会收到报价，开工前双方确认。"], ["配件凭收据", "配件按原价购买，收据交给您。"], ["照片报告", "完工后通过 WhatsApp 发送施工前后照片。"]],
 "reviews_h": "客户评价", "reviews_more": "查看 Google 上的全部评价", "projects": "案例", "projects_h1": "沙努尔近期案例",
 "projects_lead": "沙努尔的真实维修：出了什么问题，做了哪些处理。", "emergency": "紧急上门", "about_h": "关于师傅",
 "years": "年经验", "langs": "语言", "warranty": "保修", "sample": "示例数据", "form_h": "告诉我出了什么问题",
 "form_what": "遇到什么问题？", "form_when": "什么时候需要？", "when_opts": ["今天——很紧急", "本周内", "只想了解价格"], "form_btn": "通过 WhatsApp 发送",
 "form_note": "将打开 WhatsApp 并附上您的留言，可在其中添加照片。", "rated": "评分 {r} · {n} 条评价", "serving": "专注服务沙努尔"},
}
for lang, add in T.items():
    f = ROOT / "i18n" / f"{lang}.json"
    d = json.loads(f.read_text(encoding="utf-8"))
    for k, v in add.items():
        d["ui"].setdefault(k, v)
    f.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    print(lang, "ok")
