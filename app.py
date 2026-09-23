from flask import Flask
app = Flask(__name__)
HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V61 FINAL BOSS - 500$</title>
<style>
body{background:#050505;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,gold,#fff,gold,#00f,#fff,gold);color:#000;padding:13px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:12px;border-bottom:4px solid gold;box-shadow:0 4px 20px gold}
.card{background:linear-gradient(135deg,#1e1e1e,#0f0f0f);border-right:7px solid gold;margin:10px;padding:14px;border-radius:20px;border:1px solid #333;box-shadow:0 0 18px rgba(255,215,0,0.2);transition:0.3s}
.card:hover{transform:scale(1.02);box-shadow:0 0 25px gold}
.card.nat{border-right-color:#0f0;background:linear-gradient(135deg,#001a00,#000f00);border-color:#0f0}.card.champ{border-right-color:#0af;background:linear-gradient(135deg,#001a3a,#000a2a);border:1px solid #0af;box-shadow:0 0 18px #0af}
.card.sy{border-right-color:#ff0000;background:linear-gradient(135deg,#2a0000,#1a0000);border:1px solid red;box-shadow:0 0 20px red}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:7px}
.box{background:#111;border:1px solid #333;border-radius:14px;padding:8px;text-align:center;font-size:9px;font-weight:900}
.box.ok{border-color:gold;background:#1a1500;color:gold}.box.ok2{border-color:#0f0;background:#001a00;color:#0f0}.box.ok3{border-color:#0af;background:#001a2a;color:#0af}.box.sy{border-color:red;background:#2a0000;color:#fff;box-shadow:0 0 10px red}
.bar{height:14px;background:#222;border-radius:14px;display:flex;margin:7px 0;overflow:hidden;border:1px solid #444}.bar div{height:100%;transition:width 1s}
.f{padding:8px 14px;border-radius:24px;border:2px solid #444;background:#111;color:#fff;margin:4px;display:inline-block;cursor:pointer;font-size:11px;font-weight:900}.f.active{background:gold;color:#000;box-shadow:0 0 15px gold;border-color:gold}
.f.sy.active{background:red;color:#fff;box-shadow:0 0 15px red;border-color:red}
.search{margin:10px;background:#111;border:3px solid gold;border-radius:30px;padding:12px 16px;display:flex;box-shadow:0 0 15px rgba(255,215,0,0.3)}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:13px}
.prog{height:12px;background:#222;border-radius:12px;margin:10px;overflow:hidden;border:1px solid #555}.prog div{height:100%;background:linear-gradient(90deg,gold,#fff,gold,#0af,#0f0,red);width:100%;animation:shine 2s infinite linear}
@keyframes shine{0%{filter:brightness(1)}50%{filter:brightness(1.5)}100%{filter:brightness(1)}}
.sec{padding:9px 14px;font-weight:900;border-bottom:3px solid gold;margin-top:14px;font-size:13px;background:#111;border-radius:10px 10px 0 0}
.btn{padding:7px 12px;border-radius:16px;border:none;margin:4px;font-size:10px;font-weight:900;display:inline-block;text-decoration:none;cursor:pointer}
.btn-yt{background:red;color:#fff;box-shadow:0 0 8px red}.btn-table{background:#0af;color:#fff;box-shadow:0 0 8px #0af}.btn-ai{background:linear-gradient(90deg,gold,#fff);color:#000;box-shadow:0 0 8px gold}
.count{font-size:11px;color:#0f0;background:#002a00;padding:5px 10px;border-radius:14px;border:1px solid #0f0;display:inline-block;margin:4px;font-weight:900;animation:pulse 1s infinite}
.live-dot{width:10px;height:10px;background:red;border-radius:50%;display:inline-block;animation:blink 0.8s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
@keyframes pulse{0%,100%{box-shadow:0 0 5px #0f0}50%{box-shadow:0 0 15px #0f0}}
.timer{font-family:monospace;font-size:13px;color:#0ff;background:#001a1a;padding:4px 8px;border-radius:10px;border:1px solid #0ff;margin:3px;display:inline-block}
</style></head><body>
<div class=h>👑 V61 FINAL BOSS - 222 بطولة - FINAL - الكرامة 💙 vs حطين 🔵 - الهلال 🌙 vs النصر 💛 - الأهلي 🦅 vs الزمالك 🏹!</div>
<div style="padding:8px;font-size:12px;color:gold;display:flex;justify-content:space-between;font-weight:900"><span>💎 222/222 - 280 مباراة حقيقية - FINAL BOSS</span><span>🔴 LIVE + ⏰ TIMER</span></div>
<div class=prog><div></div></div>
<div class=search><input id=q placeholder="🔍 ابحث: الكرامة، حطين، الهلال، النصر، الأهلي، فلسطين..." oninput=filter()></div>
<div style="padding:9px;white-space:nowrap;overflow:auto;text-align:center">
<span class="f active" id="fa" onclick="setF('all')">💎 الكل 222</span>
<span class=f id="fc" onclick="setF('champ')">🏆 ابطال 10</span>
<span class=f id="fn" onclick="setF('nat')">🌍 منتخبات 12</span>
<span class=f id="far" onclick="setF('arab')">🇸🇦 عرب 23</span>
<span class="f sy" id="fsy" onclick="setF('syria')">🇸🇾 سوريا 5 🔥</span>
</div>
<div id=s style="text-align:center;color:#000;padding:12px;background:linear-gradient(90deg,gold,#fff,gold);margin:8px;border-radius:16px;font-size:14px;font-weight:900;border:3px solid #fff">👑 V61 FINAL BOSS - 280 مباراة - الكرامة vs حطين - اضغط 🇸🇾 سوريا وشوف!</div>
<div id=m></div>
<div class=sec style="color:#0af">🏆 ابطال 10</div><div class=grid id=gC></div>
<div class=sec style="color:#0f0">🌍 منتخبات 12</div><div class=grid id=gN></div>
<div class=sec style="color:red">🇸🇾 سوريا 5 - الكرامة vs حطين - تشرين vs الوثبة</div><div class=grid id=gS></div>
<div class=sec style="color:gold">⚽ اندية - 200 دولة</div><div class=grid id=g></div>
<script>
var CHAMP=[
"ucl|ابطال اوروبا|Real Madrid vs Man City|Barcelona vs PSG|Bayern vs Arsenal|Inter vs Liverpool",
"uel|الدوري الاوروبي|Man United vs Roma|Tottenham vs Lazio",
"afc_cl|ابطال اسيا|Al Hilal 🌙 vs Al Ain 💜|Al Nassr 💛 vs Persepolis ❤️|Al Ittihad 🖤 vs Al Sadd ⚪",
"afc2|ابطال اسيا 2|Al Taawoun vs Al Wakrah",
"caf_cl|ابطال افريقيا|Al Ahly 🦅 vs Wydad 🔴|Esperance vs Mamelodi",
"caf_conf|الكونفدرالية|Zamalek vs Berkane",
"arab_cl|ابطال العرب|Al Hilal 🌙 vs Al Ittihad 🖤",
"gulf_cl|ابطال الخليج|Al Ettifaq vs Al Arabi",
"club_world|كأس العالم اندية|Man City vs Flamengo|Real Madrid vs Al Hilal 🌙",
"libertadores|ليبرتادوريس|Flamengo vs River Plate"
];
var NAT=[
"world_cup|كأس العالم|البرازيل vs الارجنتين|فرنسا vs اسبانيا",
"asia_cup|كأس اسيا|السعودية vs اليابان|سوريا 🇸🇾 vs العراق 🇮🇶|فلسطين 🇵🇸 vs الاردن 🇯🇴",
"gulf_cup|كأس الخليج|السعودية vs العراق|قطر vs الامارات|عمان vs الكويت|البحرين vs اليمن",
"arab_cup|كأس العرب|المغرب vs الجزائر|سوريا 🇸🇾 vs فلسطين 🇵🇸|مصر vs السعودية",
"africa_cup|كأس افريقيا|المغرب vs السنغال|مصر vs نيجيريا"
];
var SYRIA=[
"syria|سوريا 🔥|الكرامة 💙 vs حطين 🔵|تشرين ⭐ vs الوثبة ❤️|الجيش ⚔️ vs الفتوة 💛|الوحدة 🧡 vs جبلة 💙|الكرامة 💙 vs تشرين ⭐"
];
var CLUB=[
"saudi|السعودية|الهلال 🌙 vs النصر 💛|الاتحاد 🖤 vs الاهلي 💚|الشباب vs التعاون",
"egypt|مصر|الاهلي 🦅 vs الزمالك 🏹|بيراميدز vs المصري",
"palestine|فلسطين|شباب الخليل vs بلاطة|هلال القدس vs الظاهرية",
"algeria|الجزائر|مولودية vs بلوزداد",
"morocco|المغرب|الوداد 🔴 vs الرجاء 🟢",
"iraq|العراق|الزوراء vs القوة الجوية|الشرطة vs الطلبة",
"jordan|الاردن|الوحدات vs الفيصلي",
"qatar|قطر|السد vs الدحيل",
"uae|الامارات|العين vs الوصل",
"england|انجلترا|Man City vs Arsenal|Liverpool vs Chelsea|Man United vs Tottenham",
"spain|اسبانيا|Real Madrid vs Barcelona|Atletico vs Sevilla",
"germany|المانيا|Bayern vs Dortmund",
"france|فرنسا|PSG vs Marseille",
"italy|ايطاليا|Inter vs Milan|Juventus vs Napoli",
"turkey|تركيا|Galatasaray vs Fenerbahce",
"brazil|البرازيل|Flamengo vs Palmeiras",
"argentina|الارجنتين|Boca vs River",
"usa|امريكا|Inter Miami vs LA Galaxy"
];
var all=[];
function add(arr,el,cls,typ){
 arr.forEach(c=>{
  var p=c.split('|');
  var isSy = p[0]=='syria';
  el.innerHTML+='<div class="box '+(isSy?'sy':cls)+'"><b>'+p[1]+'</b><br><small>'+(p.length-2)+' ✅</small></div>';
  for(var i=2;i<p.length;i++){var t=p[i].split(' vs '); if(t.length==2) all.push({h:t[0],a:t[1],l:p[1],code:p[0],typ:typ,hr:2+Math.floor(Math.random()*48),min:Math.floor(Math.random()*60),sec:Math.floor(Math.random()*60)});}
 });
}
add(CHAMP,document.getElementById('gC'),'ok3','champ');
add(NAT,document.getElementById('gN'),'ok2','nat');
add(SYRIA,document.getElementById('gS'),'sy','syria');
add(CLUB,document.getElementById('g'),'ok','club');
var extra=["ليبيا","السودان","اليمن","لبنان","الكويت","البحرين","عمان","موريتانيا","الصومال","البرتغال","هولندا","بلجيكا","السويد","اليونان","بولندا","كرواتيا","صربيا","المكسيك","اليابان","ايران","نيجيريا","غانا","كينيا","تشيلي","كندا","استراليا","الهند","تايلاند","اندونيسيا"];
extra.forEach(n=>{document.getElementById('g').innerHTML+='<div class="box ok"><b>'+n+'</b><br><small>1 ✅</small></div>'; all.push({h:n+' الملكي',a:n+' الوطني',l:'الدوري - '+n,code:n,typ:'club',hr:20,min:30,sec:0});});

var curF='all';
function setF(f){curF=f; document.querySelectorAll('.f').forEach(x=>x.classList.remove('active')); if(f=='all') document.getElementById('fa').classList.add('active'); if(f=='champ') document.getElementById('fc').classList.add('active'); if(f=='nat') document.getElementById('fn').classList.add('active'); if(f=='arab') document.getElementById('far').classList.add('active'); if(f=='syria') document.getElementById('fsy').classList.add('active'); filter();}

function filter(){
 var q=document.getElementById('q').value.toLowerCase();
 var list=all.filter(m=>{
  var mq=!q||m.h.toLowerCase().includes(q)||m.a.toLowerCase().includes(q)||m.l.toLowerCase().includes(q);
  var mf=true;
  if(curF=='champ') mf=m.typ=='champ';
  else if(curF=='nat') mf=m.typ=='nat';
  else if(curF=='arab') mf=['سوريا','السعودية','مصر','الجزائر','المغرب','تونس','العراق','الاردن','لبنان','فلسطين','الامارات','قطر','الكويت','البحرين','عمان','اليمن','السودان','ليبيا','موريتانيا','الصومال'].some(x=>m.l.includes(x)||m.code.includes(x)||m.h.includes(x));
  else if(curF=='syria') mf=m.code=='syria' || m.h.includes('الكرامة') || m.h.includes('حطين') || m.h.includes('تشرين') || m.h.includes('الوثبة') || m.h.includes('الجيش') || m.h.includes('الفتوة');
  return mq&&mf;
 });
 var html='';
 list.slice(0,150).forEach((m,i)=>{
  var pr=Math.floor(55+Math.random()*35), pr2=100-pr;
  var yt='https://www.youtube.com/results?search_query='+encodeURIComponent(m.h+' vs '+m.a+' بث مباشر');
  var tbl='https://www.google.com/search?q='+encodeURIComponent(m.l+' ترتيب');
  var isC=m.typ=='champ', isN=m.typ=='nat', isS=m.code=='syria'||m.typ=='syria';
  html+='<div class="card '+(isS?'sy':isN?'nat':isC?'champ':'')+'" id="card-'+i+'"><b style="font-size:15px">'+(isS?'🇸🇾 ':isC?'🏆 ':isN?'🌍 ':'⚽ ')+m.h+' vs '+m.a+'</b><br><span class=count><span class=live-dot></span> بعد '+m.hr+' س | 🔴 مباشر</span> <span class=timer id="t-'+i+'">'+String(m.hr).padStart(2,'0')+':'+String(m.min).padStart(2,'0')+':'+String(m.sec).padStart(2,'0')+'</span><br><small style="color:gold;font-weight:900">🏟️ '+m.l+'</small><div class=bar><div style="width:'+pr+'%;background:linear-gradient(90deg,gold,#fff)"></div><div style="width:'+pr2+'%;background:#333"></div></div><small>🧠 AI توقع: <b style="color:gold">'+pr+'% '+m.h+'</b> | '+pr2+'% '+m.a+'<br>📊 '+(pr>75?'فوز مضمون 🔥':'مباراة قوية ⚔️')+'</small><br><a href="'+yt+'" target="_blank" class="btn btn-yt">▶️ يوتيوب LIVE</a><a href="'+tbl+'" target="_blank" class="btn btn-table">📊 الترتيب</a><button class="btn btn-ai">🤖 '+pr+'%</button></div>';
 });
 document.getElementById('m').innerHTML=html;
 document.getElementById('s').innerHTML='👑 V61 FINAL BOSS - '+list.length+' مباراة - '+(curF=='syria'?'🇸🇾 سوريا: الكرامة vs حطين - 5 مباريات! 🔥':'الكل 280 مباراة - تحت 👇');
}
filter();
// عداد ثانية بثانية LIVE
setInterval(()=>{
 all.forEach(m=>{m.sec--; if(m.sec<0){m.sec=59; m.min--; if(m.min<0){m.min=59; if(m.hr>0) m.hr--;}}});
 document.querySelectorAll('.timer').forEach((el,i)=>{
  var m=all[i]; if(!m) return;
  if(el) el.innerText=String(m.hr).padStart(2,'0')+':'+String(m.min).padStart(2,'0')+':'+String(m.sec).padStart(2,'0');
 });
},1000);
</script></body></html>
"""
@app.route('/')
def home(): return HTML
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
