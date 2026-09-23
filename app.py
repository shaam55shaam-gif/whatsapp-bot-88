from flask import Flask
app = Flask(__name__)
HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1"><style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#fff,gold,#fff,#0af,#fff);color:#000;padding:11px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px;border-bottom:3px solid gold}
.card{background:#1a1a1a;border-right:5px solid gold;margin:7px;padding:11px;border-radius:14px;border:1px solid #333}
.card.nat{border-right-color:gold}.card.champ{border-right-color:#0af;background:#001a2a}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;padding:6px}
.box{background:#111;border:1px solid #333;border-radius:10px;padding:6px;text-align:center;font-size:8px}
.box.ok{border-color:gold;background:#1a1500}.box.ok2{border-color:gold;background:#2a2a00}.box.ok3{border-color:#0af;background:#001a2a}
.bar{height:10px;background:#222;border-radius:10px;display:flex;margin:5px 0}.bar div{height:100%}
.f{padding:6px 11px;border-radius:20px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:gold;color:#000;font-weight:900}
.search{margin:8px;background:#111;border:2px solid gold;border-radius:25px;padding:10px 14px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:8px;background:#222;border-radius:8px;margin:8px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,gold,#fff,gold,#0af);width:100%}
.sec{padding:7px 11px;font-weight:900;border-bottom:2px solid gold;margin-top:10px;font-size:11px;background:#111}
.btn{padding:5px 9px;border-radius:12px;border:none;margin:3px;font-size:9px;cursor:pointer;font-weight:700}
.btn-yt{background:red;color:#fff}.btn-ai{background:gold;color:#000}
.count{font-size:10px;color:#0f0;background:#002a00;padding:3px 7px;border-radius:10px;border:1px solid #0f0;display:inline-block;margin:3px}
</style></head><body>
<div class=h>💎 DIAMOND V58.3 INSTANT - 200 دولة + 12 منتخب + 10 ابطال = 222 بطولة - يحمل فورا!</div>
<div style="padding:6px;font-size:11px;color:gold;display:flex;justify-content:space-between"><span id=cnt>222/222 - 250 مباراة 💎</span><span id=upd>✅ اكتمل فورا! DIAMOND!</span></div>
<div class=prog><div style="width:100%"></div></div>
<div class=search><input id=q placeholder="ابحث: سوريا، فلسطين، الهلال، Real Madrid..." oninput=doFilter()></div>
<div style="padding:7px;white-space:nowrap;overflow:auto;text-align:center"><span class="f active" onclick="setF('all',this)">الكل 222 💎</span><span class=f onclick="setF('champ',this)">ابطال</span><span class=f onclick="setF('منتخبات',this)">منتخبات</span><span class=f onclick="setF('عرب',this)">عرب 23</span></div>
<div id=s style="text-align:center;color:#000;padding:9px;background:linear-gradient(90deg,gold,#fff,gold);margin:6px;border-radius:10px;font-size:12px;font-weight:900">✅ 💎 222/222 - 250 مباراة - DIAMOND INSTANT - بدون انتظار!</div>
<div class=sec style="color:#0af">ابطال - 10</div><div class=grid id=gC></div>
<div class=sec style="color:gold">منتخبات - 12</div><div class=grid id=gN></div>
<div class=sec style="color:#0f0">اندية - 200 دولة - DIAMOND</div><div class=grid id=g></div>
<div id=m></div>
<script>
var CHAMP=["ucl|ابطال اوروبا|Real Madrid vs Man City|Barcelona vs PSG","uel|الدوري الاوروبي|Man United vs Roma|Tottenham vs Lazio","afc_cl|ابطال اسيا|Al Hilal vs Al Ain|Al Nassr vs Persepolis","afc2|ابطال اسيا 2|Taawoun vs Wakrah|Sepahan vs Sharjah","caf_cl|ابطال افريقيا|Al Ahly vs Wydad|Esperance vs Mamelodi","caf_conf|الكونفدرالية|Zamalek vs Berkane|USM Alger vs Dreams","arab_cl|ابطال العرب|Al Hilal vs Al Ittihad|Wydad vs Al Ahly","gulf_cl|ابطال الخليج|Al Ettifaq vs Al Arabi|Qadsia vs Nasaf","club_world|كأس العالم اندية|Man City vs Flamengo|Real Madrid vs Al Hilal","libertadores|ليبرتادوريس|Flamengo vs River Plate|Palmeiras vs Boca"];
var NAT=["world_cup|كأس العالم|البرازيل vs الارجنتين|فرنسا vs اسبانيا","asia_cup|كأس اسيا|السعودية vs اليابان|سوريا vs العراق","africa_cup|كأس افريقيا|المغرب vs السنغال|مصر vs نيجيريا","euro|يورو|انجلترا vs المانيا|فرنسا vs ايطاليا","copa_america|كوبا امريكا|البرازيل vs اوروغواي|الارجنتين vs كولومبيا","arab_cup|كأس العرب|المغرب vs الجزائر|سوريا vs فلسطين","olympic|الاولمبياد|فرنسا vs اسبانيا|المغرب vs مصر","nations|دوري الامم|اسبانيا vs البرتغال|المانيا vs فرنسا","gulf_cup|كأس الخليج|السعودية vs العراق|قطر vs الامارات|عمان vs الكويت|البحرين vs اليمن","u21_euro|تحت 21|اسبانيا vs انجلترا|المانيا vs فرنسا","asian_games|الالعاب الاسيوية|اليابان vs كوريا|السعودية vs ايران","african_ch|افريقيا محليين|المغرب vs الجزائر|السنغال vs مصر"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الاردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الامارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","mauritania|موريتانيا","somalia|الصومال","djibouti|جيبوتي","comoros|جزر القمر","sahara|الصحراء","england|انجلترا","spain|اسبانيا","italy|ايطاليا","germany|المانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","turkey|تركيا","greece|اليونان","sweden|السويد","norway|النرويج","denmark|الدنمارك","finland|فنلندا","iceland|ايسلندا","poland|بولندا","ukraine|اوكرانيا","russia|روسيا","czech|التشيك","slovakia|سلوفاكيا","hungary|المجر","romania|رومانيا","bulgaria|بلغاريا","croatia|كرواتيا","serbia|صربيا","bosnia|البوسنة","slovenia|سلوفينيا","albania|البانيا","macedonia|مقدونيا","montenegro|الجبل الاسود","moldova|مولدوفا","belarus|بيلاروسيا","austria|النمسا","swiss|سويسرا","luxembourg|لوكسمبورغ","malta|مالطا","cyprus|قبرص","scotland|اسكتلندا","wales|ويلز","ireland|ايرلندا","georgia|جورجيا","armenia|ارمينيا","azerbaijan|اذربيجان","kazakhstan|كازاخستان","estonia|استونيا","latvia|لاتفيا","lithuania|ليتوانيا","brazil|البرازيل","argentina|الارجنتين","uruguay|اوروغواي","paraguay|باراغواي","chile|تشيلي","colombia|كولومبيا","peru|بيرو","ecuador|الاكوادور","bolivia|بوليفيا","venezuela|فنزويلا","mexico|المكسيك","usa|امريكا","canada|كندا","costa_rica|كوستاريكا","honduras|هندوراس","panama|بنما","jamaica|جامايكا","trinidad|ترينيداد","guatemala|غواتيمالا","el_salvador|السلفادور","haiti|هايتي","cuba|كوبا","dominican|الدومينيكان","nicaragua|نيكاراغوا","japan|اليابان","korea_s|كوريا الجنوبية","china|الصين","australia|استراليا","newzealand|نيوزيلندا","iran|ايران","uzbekistan|اوزبكستان","india|الهند","thailand|تايلاند","vietnam|فيتنام","indonesia|اندونيسيا","malaysia|ماليزيا","singapore|سنغافورة","philippines|الفلبين","nigeria|نيجيريا","senegal|السنغال","ghana|غانا","cameroon|الكاميرون","ivory|ساحل العاج","mali|مالي","burkina|بوركينا","guinea|غينيا","southafrica|جنوب افريقيا","zambia|زامبيا","zimbabwe|زيمبابوي","kenya|كينيا","uganda|اوغندا","tanzania|تنزانيا","ethiopia|اثيوبيا","angola|انغولا","mozambique|موزمبيق","namibia|ناميبيا","botswana|بوتسوانا","rwanda|رواندا","congo|الكونغو","drcongo|الكونغو الديمقراطية","benin|بنين","togo|توغو","niger|النيجر","chad|تشاد","southsudan|جنوب السودان","liberia|ليبيريا","sierra|سيراليون","gambia|غامبيا","malawi|مالاوي","lesotho|ليسوتو","eswatini|اسواتيني","madagascar|مدغشقر","mauritius|موريشيوس","seychelles|سيشل","eritrea|اريتريا","car|افريقيا الوسطى","eq_guinea|غينيا الاستوائية","burundi|بوروندي","fiji|فيجي","papua|بابوا","solomon|جزر سليمان","vanuatu|فانواتو","samoa|ساموا","tonga|تونغا","bermuda|برمودا","barbados|باربادوس","bahamas|الباهاماس","grenada|غرينادا","antigua|انتيغوا","st_lucia|سانت لوسيا","cayman|جزر كايمان","faroe|جزر فارو","gibraltar|جبل طارق","liechtenstein|ليختنشتاين","san_marino|سان مارينو","andorra|اندورا","monaco|موناكو"];
var g=document.getElementById('g'),gn=document.getElementById('gN'),gc=document.getElementById('gC');
var all=[];
function ist(h){var d=new Date(); d.setHours(d.getHours()+h); return d.toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit'})}
function countdown(h){if(h<2) return 'LIVE NOW!'; if(h<24) return 'بعد '+h+' س'; return 'بعد '+Math.floor(h/24)+' يوم';}
CHAMP.forEach(c=>{var p=c.split('|'); gc.innerHTML+='<div class=box ok3><b>'+p[1]+'</b><br><small>2 ✅</small></div>'; for(var i=2;i<p.length;i++){var t=p[i].split(' vs '); all.push({home:t[0],away:t[1],league:p[1]+' - ابطال',code:p[0],type:'champ',h:20+Math.floor(Math.random()*10)});}});
NAT.forEach(c=>{var p=c.split('|'); gn.innerHTML+='<div class=box ok2><b>'+p[1]+'</b><br><small>'+(p.length-2)+' ✅</small></div>'; for(var i=2;i<p.length;i++){var t=p[i].split(' vs '); all.push({home:t[0],away:t[1],league:p[1]+' - منتخبات',code:p[0],type:'nat',h:25+Math.floor(Math.random()*20)});}});
ALL.forEach(c=>{var p=c.split('|'); g.innerHTML+='<div class=box ok><b>'+p[1]+'</b><br><small>1 ✅</small></div>'; all.push({home:p[1]+' الملكي',away:p[1]+' الوطني',league:'الدوري - '+p[1],code:p[0],type:'club',h:18+Math.floor(Math.random()*30)});});
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=(force||document.querySelector('.f.active').innerText).toLowerCase();
 var code=''; if(f.includes('ابطال')||f=='champ') code='champ'; else if(f.includes('منتخبات')) code='منتخبات'; else if(f.includes('عرب')) code='عرب';
 var filtered=all.filter(m=>{var mq=!q||m.home.toLowerCase().includes(q)||m.league.toLowerCase().includes(q); var mf=true;
  if(code=='منتخبات') mf=m.type=='nat'; else if(code=='champ') mf=m.type=='champ'; else if(code=='عرب') mf=['syria','saudi','egypt','algeria','morocco','tunisia','iraq','jordan','lebanon','palestine','uae','qatar','kuwait','bahrain','oman','yemen','sudan','libya','mauritania','somalia','djibouti','comoros','sahara'].includes(m.code);
  return mq&&mf;});
 document.getElementById('m').innerHTML=filtered.map(m=>{
  var pr1=55+Math.floor(Math.random()*25),pr2=100-pr1, isNat=m.type=='nat', isChamp=m.type=='champ';
  var yt='https://www.youtube.com/results?search_query='+encodeURIComponent(m.home+' vs '+m.away+' live');
  return '<div class="card '+(isNat?'nat':isChamp?'champ':'')+'"><b>'+(isChamp?'🏆 ':isNat?'🌍 ':'⚽ ')+m.home+' vs '+m.away+'</b><br><span class=count>⏰ '+countdown(m.h)+' | '+ist(m.h)+'</span><br><small style="color:gold">'+m.league+'</small><div class=bar><div style="width:'+pr1+'%;background:gold"></div><div style="width:'+pr2+'%;background:#333"></div></div><small>🧠 AI: <b style="color:gold">'+pr1+'% '+m.home+'</b></small><br><a href="'+yt+'" target="_blank" class="btn btn-yt">▶️ يوتيوب LIVE</a><button class="btn btn-ai">🤖 '+pr1+'% توقع</button></div>';
 }).join('');
}
doFilter();
setInterval(doFilter,30000);
</script></body></html>
"""
@app.route('/')
def home(): return HTML
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
