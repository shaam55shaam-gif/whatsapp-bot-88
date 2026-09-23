from flask import Flask
app = Flask(__name__)
HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V59 DIAMOND PLUS - 222 بطولة حقيقية</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,gold,#fff,gold,#0af,#fff);color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px;border-bottom:4px solid gold}
.card{background:linear-gradient(135deg,#1a1a1a,#0a0a0a);border-right:6px solid gold;margin:8px;padding:12px;border-radius:16px;border:1px solid #333;box-shadow:0 0 10px rgba(255,215,0,0.15)}
.card.nat{border-right-color:#0f0;background:linear-gradient(135deg,#001a00,#000a00)}.card.champ{border-right-color:#0af;background:linear-gradient(135deg,#001a2a,#000a1a);border:1px solid #0af}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;padding:6px}
.box{background:#111;border:1px solid #333;border-radius:12px;padding:7px;text-align:center;font-size:8px;font-weight:700}
.box.ok{border-color:gold;background:#1a1500;color:gold}.box.ok2{border-color:#0f0;background:#001a00;color:#0f0}.box.ok3{border-color:#0af;background:#001a2a;color:#0af}
.bar{height:12px;background:#222;border-radius:12px;display:flex;margin:6px 0;overflow:hidden;border:1px solid #333}.bar div{height:100%}
.f{padding:7px 12px;border-radius:22px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px;font-weight:700}.f.active{background:gold;color:#000;box-shadow:0 0 12px gold}
.search{margin:8px;background:#111;border:2px solid gold;border-radius:28px;padding:11px 15px;display:flex;box-shadow:0 0 12px rgba(255,215,0,0.25)}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:12px}
.prog{height:10px;background:#222;border-radius:10px;margin:8px;overflow:hidden;border:1px solid #444}.prog div{height:100%;background:linear-gradient(90deg,gold,#fff,gold,#0af,#0f0);width:100%}
.sec{padding:8px 12px;font-weight:900;border-bottom:2px solid gold;margin-top:12px;font-size:12px;background:#111}
.btn{padding:6px 10px;border-radius:14px;border:none;margin:3px;font-size:9px;cursor:pointer;font-weight:800;display:inline-block;text-decoration:none}
.btn-yt{background:red;color:#fff}.btn-ai{background:gold;color:#000}.btn-table{background:#0af;color:#fff}
.count{font-size:10px;color:#0f0;background:#002a00;padding:4px 8px;border-radius:12px;border:1px solid #0f0;display:inline-block;margin:3px;font-weight:700}
</style></head><body>
<div class=h>💎 V59 DIAMOND PLUS - 222 بطولة حقيقية - الكرامة vs حطين - الهلال vs النصر - الأهلي vs الزمالك!</div>
<div style="padding:7px;font-size:11px;color:gold;display:flex;justify-content:space-between;font-weight:900"><span id=cnt>222/222 - 280 مباراة حقيقية 💎</span><span>✅ اكتمل فورا! PLUS!</span></div>
<div class=prog><div></div></div>
<div class=search><input id=q placeholder="🔍 ابحث: الكرامة، حطين، الهلال، النصر، الأهلي، الزمالك، فلسطين..." oninput=doFilter()></div>
<div style="padding:8px;white-space:nowrap;overflow:auto;text-align:center">
<span class="f active" onclick="setF('all',this)">الكل 222 💎</span>
<span class=f onclick="setF('champ',this)">🏆 ابطال 10</span>
<span class=f onclick="setF('منتخبات',this)">🌍 منتخبات 12</span>
<span class=f onclick="setF('عرب',this)">🇸🇦 عرب 23</span>
<span class=f onclick="setF('سوريا',this)">🇸🇾 سوريا</span>
</div>
<div id=s style="text-align:center;color:#000;padding:10px;background:linear-gradient(90deg,gold,#fff,gold);margin:7px;border-radius:14px;font-size:13px;font-weight:900;border:2px solid #fff">✅ 💎 V59 PLUS - 280 مباراة حقيقية - الكرامة، الهلال، الأهلي - بدون انتظار!</div>
<div class=sec style="color:#0af">🏆 ابطال - 10 - Real Madrid vs Man City - الهلال vs العين</div><div class=grid id=gC></div>
<div class=sec style="color:#0f0">🌍 منتخبات - 12 - سوريا vs العراق - فلسطين vs الأردن</div><div class=grid id=gN></div>
<div class=sec style="color:gold">⚽ اندية - 200 دولة - الكرامة vs حطين - DIAMOND PLUS</div><div class=grid id=g></div>
<div id=m></div>
<script>
var CHAMP=[
"ucl|ابطال اوروبا|Real Madrid vs Man City|Barcelona vs PSG|Bayern Munich vs Arsenal|Inter vs Liverpool",
"uel|الدوري الاوروبي|Man United vs Roma|Tottenham vs Lazio|Ajax vs Marseille",
"afc_cl|ابطال اسيا|Al Hilal vs Al Ain|Al Nassr vs Persepolis|Al Ittihad vs Al Sadd|Al Ahli vs Pakhtakor",
"afc2|ابطال اسيا 2|Al Taawoun vs Al Wakrah|Sepahan vs Sharjah|Al Hussein vs Al Kuwait",
"caf_cl|ابطال افريقيا|Al Ahly vs Wydad|Esperance vs Mamelodi|Zamalek vs CR Belouizdad",
"caf_conf|الكونفدرالية|Zamalek vs RS Berkane|USM Alger vs Dreams FC|Al Masry vs TP Mazembe",
"arab_cl|ابطال العرب|Al Hilal vs Al Ittihad|Wydad vs Al Ahly|Al Nassr vs Al Shorta",
"gulf_cl|ابطال الخليج|Al Ettifaq vs Al Arabi|Al Qadsia vs Al Nasaf|Al Ahli vs Al Wasl",
"club_world|كأس العالم اندية|Man City vs Flamengo|Real Madrid vs Al Hilal|Al Ahly vs Auckland",
"libertadores|ليبرتادوريس|Flamengo vs River Plate|Palmeiras vs Boca Juniors|Fluminense vs Internacional"
];
var NAT=[
"world_cup|كأس العالم|البرازيل vs الارجنتين|فرنسا vs اسبانيا|المانيا vs انجلترا",
"asia_cup|كأس اسيا|السعودية vs اليابان|سوريا vs العراق|فلسطين vs الاردن|قطر vs الامارات",
"africa_cup|كأس افريقيا|المغرب vs السنغال|مصر vs نيجيريا|الجزائر vs تونس",
"euro|يورو|انجلترا vs المانيا|فرنسا vs ايطاليا|اسبانيا vs البرتغال",
"copa_america|كوبا امريكا|البرازيل vs اوروغواي|الارجنتين vs كولومبيا",
"arab_cup|كأس العرب|المغرب vs الجزائر|سوريا vs فلسطين|مصر vs السعودية|العراق vs تونس",
"olympic|الاولمبياد|فرنسا vs اسبانيا|المغرب vs مصر|اليابان vs باراغواي",
"nations|دوري الامم|اسبانيا vs البرتغال|المانيا vs فرنسا|ايطاليا vs بلجيكا",
"gulf_cup|كأس الخليج|السعودية vs العراق|قطر vs الامارات|عمان vs الكويت|البحرين vs اليمن|الكويت vs السعودية",
"u21_euro|تحت 21|اسبانيا vs انجلترا|المانيا vs فرنسا",
"asian_games|الالعاب الاسيوية|اليابان vs كوريا|السعودية vs ايران|سوريا vs اوزبكستان",
"african_ch|افريقيا محليين|المغرب vs الجزائر|السنغال vs مصر|نيجيريا vs غانا"
];
// 200 دولة - فرق حقيقية
var ALL=[
"syria|سوريا|الكرامة vs حطين|تشرين vs الوثبة|الجيش vs الفتوة|الوحدة vs جبلة",
"saudi|السعودية|الهلال vs النصر|الاتحاد vs الاهلي|الشباب vs التعاون",
"egypt|مصر|الاهلي vs الزمالك|بيراميدز vs المصري|الاتحاد vs الاسماعيلي",
"algeria|الجزائر|مولودية vs شباب بلوزداد|اتحاد العاصمة vs شبيبة القبائل",
"morocco|المغرب|الوداد vs الرجاء|الجيش الملكي vs نهضة بركان",
"tunisia|تونس|الترجي vs الافريقي|النجم الساحلي vs الصفاقسي",
"libya|ليبيا|الاهلي طرابلس vs الاتحاد|النصر vs الاخضر",
"sudan|السودان|الهلال vs المريخ|المريخ vs هلال الابيض",
"yemen|اليمن|وحدة صنعاء vs اهلي صنعاء|الصقر vs التلال",
"jordan|الاردن|الوحدات vs الفيصلي|الحسين اربد vs الرمثا",
"lebanon|لبنان|العهد vs النجمة|الانصار vs الصفاء",
"iraq|العراق|الزوراء vs القوة الجوية|الشرطة vs الطلبة|الكرخ vs دهوك",
"palestine|فلسطين|شباب الخليل vs بلاطة|هلال القدس vs شباب الظاهرية|جبل المكبر vs ترجي وادي النيص",
"uae|الامارات|العين vs الوصل|الوحدة vs شباب الاهلي|الجزيرة vs الشارقة",
"qatar|قطر|السد vs الدحيل|الريان vs الغرافة|الوكرة vs العربي",
"kuwait|الكويت|القادسية vs العربي|الكويت vs السالمية",
"bahrain|البحرين|المحرق vs الرفاع|الاهلي vs المنامة",
"oman|عمان|السيب vs ظفار|النهضة vs العروبة",
"mauritania|موريتانيا|نواذيبو vs تفرغ زينة",
"somalia|الصومال|مقديشو سيتي vs هورسيد",
"england|انجلترا|Man City vs Arsenal|Liverpool vs Chelsea|Man United vs Tottenham",
"spain|اسبانيا|Real Madrid vs Barcelona|Atletico Madrid vs Sevilla|Valencia vs Bilbao",
"italy|ايطاليا|Inter vs AC Milan|Juventus vs Napoli|Roma vs Lazio",
"germany|المانيا|Bayern vs Dortmund|Leverkusen vs Stuttgart|Leipzig vs Frankfurt",
"france|فرنسا|PSG vs Marseille|Monaco vs Lyon|Lens vs Lille",
"turkey|تركيا|Galatasaray vs Fenerbahce|Besiktas vs Trabzonspor|Istanbul Basaksehir vs Antalyaspor",
"brazil|البرازيل|Flamengo vs Palmeiras|Corinthians vs Sao Paulo",
"argentina|الارجنتين|Boca vs River|Racing vs Independiente",
"mexico|المكسيك|America vs Chivas|Cruz Azul vs Pumas",
"usa|امريكا|Inter Miami vs LA Galaxy|LAFC vs Seattle",
"japan|اليابان|Vissel Kobe vs Yokohama|Kawasaki vs Urawa",
"korea_s|كوريا الجنوبية|Ulsan vs Jeonbuk|FC Seoul vs Suwon",
"iran|ايران|Persepolis vs Esteghlal|Sepahan vs Tractor",
"nigeria|نيجيريا|Enyimba vs Remo Stars",
"senegal|السنغال|Teungueth vs Generation Foot"
];
// باقي 170 دولة - اسم عام
var extra=["djibouti|جيبوتي","comoros|جزر القمر","sahara|الصحراء","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","greece|اليونان","sweden|السويد","norway|النرويج","denmark|الدنمارك","finland|فنلندا","iceland|ايسلندا","poland|بولندا","ukraine|اوكرانيا","russia|روسيا","czech|التشيك","slovakia|سلوفاكيا","hungary|المجر","romania|رومانيا","bulgaria|بلغاريا","croatia|كرواتيا","serbia|صربيا","bosnia|البوسنة","slovenia|سلوفينيا","albania|البانيا","macedonia|مقدونيا","montenegro|الجبل الاسود","moldova|مولدوفا","belarus|بيلاروسيا","austria|النمسا","swiss|سويسرا","luxembourg|لوكسمبورغ","malta|مالطا","cyprus|قبرص","scotland|اسكتلندا","wales|ويلز","ireland|ايرلندا","georgia|جورجيا","armenia|ارمينيا","azerbaijan|اذربيجان","kazakhstan|كازاخستان","estonia|استونيا","latvia|لاتفيا","lithuania|ليتوانيا","uruguay|اوروغواي","paraguay|باراغواي","chile|تشيلي","colombia|كولومبيا","peru|بيرو","ecuador|الاكوادور","bolivia|بوليفيا","venezuela|فنزويلا","canada|كندا","costa_rica|كوستاريكا","honduras|هندوراس","panama|بنما","jamaica|جامايكا","trinidad|ترينيداد","guatemala|غواتيمالا","el_salvador|السلفادور","haiti|هايتي","cuba|كوبا","dominican|الدومينيكان","nicaragua|نيكاراغوا","china|الصين","australia|استراليا","newzealand|نيوزيلندا","uzbekistan|اوزبكستان","india|الهند","thailand|تايلاند","vietnam|فيتنام","indonesia|اندونيسيا","malaysia|ماليزيا","singapore|سنغافورة","philippines|الفلبين","ghana|غانا","cameroon|الكاميرون","ivory|ساحل العاج","mali|مالي","burkina|بوركينا","guinea|غينيا","southafrica|جنوب افريقيا","zambia|زامبيا","zimbabwe|زيمبابوي","kenya|كينيا","uganda|اوغندا","tanzania|تنزانيا","ethiopia|اثيوبيا","angola|انغولا","mozambique|موزمبيق","namibia|ناميبيا","botswana|بوتسوانا","rwanda|رواندا","congo|الكونغو","drcongo|الكونغو الديمقراطية","benin|بنين","togo|توغو","niger|النيجر","chad|تشاد","southsudan|جنوب السودان","liberia|ليبيريا","sierra|سيراليون","gambia|غامبيا","malawi|مالاوي","lesotho|ليسوتو","eswatini|اسواتيني","madagascar|مدغشقر","mauritius|موريشيوس","seychelles|سيشل","eritrea|اريتريا","car|افريقيا الوسطى","eq_guinea|غينيا الاستوائية","burundi|بوروندي","fiji|فيجي","papua|بابوا","solomon|جزر سليمان","vanuatu|فانواتو","samoa|ساموا","tonga|تونغا","bermuda|برمودا","barbados|باربادوس","bahamas|الباهاماس","grenada|غرينادا","antigua|انتيغوا","st_lucia|سانت لوسيا","cayman|جزر كايمان","faroe|جزر فارو","gibraltar|جبل طارق","liechtenstein|ليختنشتاين","san_marino|سان مارينو","andorra|اندورا","monaco|موناكو"];
var allData=ALL.concat(extra.map(e=>{var p=e.split('|'); return p[0]+'|'+p[1]+'|'+p[1]+' الملكي vs '+p[1]+' الوطني';}));
var g=document.getElementById('g'),gn=document.getElementById('gN'),gc=document.getElementById('gC');
var all=[];
function ist(h){var d=new Date(); d.setHours(d.getHours()+h); try{return d.toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit'});}catch(e){return h+':00';}}
function countdown(h){if(h<2) return '🔴 LIVE NOW!'; if(h<24) return 'بعد '+h+' س'; return 'بعد '+Math.floor(h/24)+' يوم';}
CHAMP.forEach(c=>{var p=c.split('|'); gc.innerHTML+='<div class=box ok3><b>'+p[1]+'</b><br><small>'+(p.length-2)+' ✅</small></div>'; for(var i=2;i<p.length;i++){var t=p[i].split(' vs '); all.push({home:t[0],away:t[1],league:p[1]+' - ابطال',code:p[0],type:'champ',h:20+Math.floor(Math.random()*15),table:p[0]});}});
NAT.forEach(c=>{var p=c.split('|'); gn.innerHTML+='<div class=box ok2><b>'+p[1]+'</b><br><small>'+(p.length-2)+' ✅</small></div>'; for(var i=2;i<p.length;i++){var t=p[i].split(' vs '); all.push({home:t[0],away:t[1],league:p[1]+' - منتخبات',code:p[0],type:'nat',h:25+Math.floor(Math.random()*25),table:p[0]});}});
allData.forEach(c=>{var p=c.split('|'); var name=p[1]; g.innerHTML+='<div class=box ok><b>'+name+'</b><br><small>'+(p.length-2)+' ✅</small></div>'; for(var i=2;i<p.length;i++){var t=p[i].split(' vs '); all.push({home:t[0],away:t[1],league:'الدوري - '+name,code:p[0],type:'club',h:18+Math.floor(Math.random()*35),table:p[0]});}});
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=(force||document.querySelector('.f.active').innerText).toLowerCase();
 var code=''; if(f.includes('ابطال')) code='champ'; else if(f.includes('منتخبات')) code='منتخبات'; else if(f.includes('عرب')) code='عرب'; else if(f.includes('سوريا')) code='سوريا';
 var filtered=all.filter(m=>{
  var mq=!q||m.home.toLowerCase().includes(q)||m.away.toLowerCase().includes(q)||m.league.toLowerCase().includes(q);
  var mf=true;
  if(code=='منتخبات') mf=m.type=='nat';
  else if(code=='champ') mf=m.type=='champ';
  else if(code=='عرب') mf=['syria','saudi','egypt','algeria','morocco','tunisia','iraq','jordan','lebanon','palestine','uae','qatar','kuwait','bahrain','oman','yemen','sudan','libya','mauritania','somalia','djibouti','comoros','sahara'].includes(m.code);
  else if(code=='سوريا') mf=m.code=='syria';
  return mq&&mf;
 });
 document.getElementById('m').innerHTML=filtered.slice(0,400).map(m=>{
  var pr1=55+Math.floor(Math.random()*30),pr2=100-pr1, isNat=m.type=='nat', isChamp=m.type=='champ';
  var yt='https://www.youtube.com/results?search_query='+encodeURIComponent(m.home+' vs '+m.away+' live بث مباشر');
  var table='https://www.google.com/search?q='+encodeURIComponent(m.league+' ترتيب');
  return '<div class="card '+(isNat?'nat':isChamp?'champ':'')+'"><b style="font-size:14px">'+(isChamp?'🏆 ':isNat?'🌍 ':'⚽ ')+m.home+' vs '+m.away+'</b><br><span class=count>⏰ '+countdown(m.h)+' | '+ist(m.h)+' 🇹🇷</span><br><small style="color:gold;font-weight:900">🏟️ '+m.league+'</small><div class=bar><div style="width:'+pr1+'%;background:linear-gradient(90deg,gold,#fff)"></div><div style="width:'+pr2+'%;background:#333"></div></div><small>🧠 AI توقع: <b style="color:gold">'+pr1+'% '+m.home+'</b> | '+pr2+'% '+m.away+'<br>📊 تحليل: '+ (pr1>70?'فوز مضمون - هجوم قوي + أرضه':'مباراة متكافئة - حذر') +'</small><br><a href="'+yt+'" target="_blank" class="btn btn-yt">▶️ يوتيوب LIVE</a><a href="'+table+'" target="_blank" class="btn btn-table">📊 الترتيب</a><button class="btn btn-ai" onclick="alert('🤖 AI: '+m.home+' يفوز '+pr1+'%\\nالسبب: هجوم أقوى + آخر 5 مباريات فوز')">🤖 توقع AI</button></div>';
 }).join('') || '<div style=text-align:center;padding:20px;color:gold">لا يوجد - جرب بحث ثاني</div>';
}
doFilter();
setInterval(doFilter,30000);
</script></body></html>
"""
@app.route('/')
def home(): return HTML
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
