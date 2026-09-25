(function(){try{
 var T={en:["This site is available in English","Open","No, thanks"],ru:["Сайт есть на русском языке","Открыть","Нет, спасибо"],id:["Situs ini tersedia dalam Bahasa Indonesia","Buka","Tidak"],
 nl:["Deze site is beschikbaar in het Nederlands","Openen","Nee, bedankt"],de:["Diese Seite gibt es auf Deutsch","Öffnen","Nein, danke"],fr:["Ce site est disponible en français","Ouvrir","Non, merci"],
 it:["Il sito è disponibile in italiano","Apri","No, grazie"],es:["Este sitio está disponible en español","Abrir","No, gracias"],pt:["Este site está disponível em português","Abrir","Não, obrigado"],
 pl:["Strona jest dostępna po polsku","Otwórz","Nie, dziękuję"],uk:["Сайт доступний українською","Відкрити","Ні, дякую"],cs:["Stránka je dostupná v češtině","Otevřít","Ne, děkuji"],
 sv:["Sidan finns på svenska","Öppna","Nej tack"],da:["Siden findes på dansk","Åbn","Nej tak"],nb:["Siden finnes på norsk","Åpne","Nei takk"],fi:["Sivusto on saatavilla suomeksi","Avaa","Ei kiitos"],
 tr:["Bu site Türkçe olarak mevcut","Aç","Hayır, teşekkürler"],zh:["本网站提供中文版本","打开","不用了"],ja:["このサイトは日本語でもご覧いただけます","開く","いいえ"],ko:["이 사이트는 한국어로도 제공됩니다","열기","괜찮습니다"]};
 var cur=document.documentElement.lang, K="sf_lang_choice";
 var st=null;try{st=localStorage.getItem(K)}catch(e){}
 if(st)return;
 var alts={};[].forEach.call(document.querySelectorAll('link[rel=alternate][hreflang]'),function(l){alts[l.hreflang]=l.href});
 var want=null,ls=navigator.languages||[navigator.language||""];
 for(var i=0;i<ls.length;i++){var c=(ls[i]||"").toLowerCase().split("-")[0];if(c==="no"||c==="nn")c="nb";if(c===cur)return;if(alts[c]&&T[c]){want=c;break}}
 if(!want)return;
 var b=document.createElement("div");b.className="langbar";b.setAttribute("lang",want);
 b.innerHTML='<span>'+T[want][0]+'</span><a class="lb-yes" href="'+alts[want]+'">'+T[want][1]+'</a><button class="lb-no" type="button">'+T[want][2]+'</button>';
 function save(v){try{localStorage.setItem(K,v)}catch(e){}}
 b.querySelector(".lb-yes").onclick=function(){save(want)};
 b.querySelector(".lb-no").onclick=function(){save(cur);b.remove()};
 document.addEventListener("click",function(e){var a=e.target.closest(".ll a[hreflang]");if(a)save(a.getAttribute("hreflang"))});
 setTimeout(function(){document.body.appendChild(b)},900);
}catch(e){}})();
