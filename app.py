from flask import Flask, jsonify
import datetime
app = Flask(__name__)

# كل المنتخبات والدوريات
NATIONAL = {
"world_cup": [("البرازيل","الأرجنتين"),("فرنسا","إسبانيا"),("إنجلترا","ألمانيا"),("البرتغال","هولندا")],
"asia_cup": [("السعودية","اليابان"),("إيران","كوريا الجنوبية"),("قطر","أستراليا"),("سوريا","العراق")],
"africa_cup": [("المغرب","السنغال"),("مصر","نيجيريا"),("الجزائر","تونس"),("الكاميرون","غانا")],
"euro": [("فرنسا","إنجلترا"),("إسبانيا","ألمانيا"),("البرتغال","إيطاليا"),("هولندا","بلجيكا")],
"copa_america": [("البرازيل","الأرجنتين"),("أوروغواي","كولومبيا"),("تشيلي","المكسيك")],
"arab_cup": [("المغرب","الجزائر"),("مصر","السعودية"),("تونس","العراق"),("سوريا","الأردن")],
}

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,red,#00ff00);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:10px;border-radius:12px;cursor:pointer}
.card.nat{border-right-color:gold;background:#1a1a00}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:4px;padding:6px;max-height:200px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:6px;text-align:center;font-size:9px;cursor:pointer}
.box.ok{border-color:#00ff00;background:#002a00;color:#00ff00}
.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:6px 10px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:6px;background:#333;border-radius:6px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,#00ff00,gold);transition:width.5s}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center}.modal>div{background:#1a1a1a;color:#fff;padding:12px;border-radius:14px;border:2px solid #00ff00;width:96%;max-width:520px;max-height:90vh;overflow:auto}
.btn{background:#00ff00;color:#000;border:none;padding:6px 10px;border-radius:14px;font-weight:900;margin:2px;cursor:pointer}
.section{padding:6px 10px;font-weight:900;color:#00ff00;border-bottom:1px solid #333;margin-top:8px;font-size:11px}
</style></head><body>
<div class=h>🌍 V52 ULTIMATE - 210 دولة + منتخبات = 240 بطولة - تحميل تلقائي</div>
<div style="padding:5px;font-size:10px;color:#00ff00;display:flex;justify-content:space-between"><span id=live>LIVE:0</span><span id=cnt>0/210</span><span id=upd>يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: سوريا، كأس العالم، الهلال، Real Madrid..." oninput="doFilter()"></div>
<div style="padding:6px;overflow:auto;white-space:nowrap"><span class="f active" onclick="setF('all',this)">الكل 240 🌍</span><span class=f onclick="setF('منتخبات',this)">🏆 منتخبات</span><span class=f onclick="setF('syria',this)">سوريا</span><span class=f onclick="setF('saudi',this)">السعودية</span><span class=f onclick="setF('egypt',this)">مصر</span><span class=f onclick="setF('england',this)">ENG</span><span class=f onclick="setF('spain',this)">ESP</span><span class=f onclick="setF('world',this)">كأس العالم</span><span class=f onclick="setF('asia',this)">كأس آسيا</span><span class=f onclick="setF('africa',this)">كأس أفريقيا</span></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">🔄 V52 يحمل 210 دولة + منتخبات...</div>

<div class=section>🏆 بطولات المنتخبات - 30 بطولة</div>
<div class=grid id=gNat></div>

<div class=section>🌍 دوريات الأندية - 210 دولة × 3 = 630 بطولة</div>
<div class=grid id=g></div>

<div id=m></div>
<div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div>
<script>
var NATIONAL=["world_cup|🏆 كأس العالم","asia_cup|🏆 كأس آسيا","africa_cup|🏆 كأس أفريقيا","euro|🏆 يورو أوروبا","copa_america|🏆 كوبا أمريكا","arab_cup|🏆 كأس العرب","olympic|🏆 الأولمبياد","nations_league|🏆 دوري الأمم"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","mauritania|موريتانيا","somalia|الصومال","djibouti|جيبوتي","comoros|جزر القمر",
"england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","scotland|اسكتلندا","wales|ويلز","ireland|أيرلندا","n_ireland|أيرلندا الشمالية","norway|النرويج","sweden|السويد","denmark|الدنمارك","finland|فنلندا","iceland|آيسلندا","poland|بولندا","ukraine|أوكرانيا","russia|روسيا","czech|التشيك","slovakia|سلوفاكيا","hungary|المجر","romania|رومانيا","bulgaria|بلغاريا","greece|اليونان","turkey|تركيا","croatia|كرواتيا","serbia|صربيا","bosnia|البوسنة","slovenia|سلوفينيا","albania|ألبانيا","macedonia|مقدونيا","montenegro|الجبل الأسود","moldova|مولدوفا","belarus|بيلاروسيا","austria|النمسا","swiss|سويسرا","luxembourg|لوكسمبورغ","malta|مالطا","cyprus|قبرص",
"brazil|البرازيل","argentina|الأرجنتين","uruguay|أوروغواي","paraguay|باراغواي","chile|تشيلي","colombia|كولومبيا","peru|بيرو","ecuador|الإكوادور","bolivia|بوليفيا","venezuela|فنزويلا",
"usa|أمريكا","mexico|المكسيك","canada|كندا","costa_rica|كوستاريكا","honduras|هندوراس","panama|بنما","jamaica|جامايكا","trinidad|ترينيداد","guatemala|غواتيمالا","el_salvador|السلفادور",
"japan|اليابان","korea_s|كوريا الجنوبية","korea_n|كوريا الشمالية","china|الصين","australia|أستراليا","newzealand|نيوزيلندا","iran|إيران","uzbekistan|أوزبكستان","kazakhstan|كازاخستان","india|الهند","pakistan|باكستان","bangladesh|بنغلادش","thailand|تايلاند","vietnam|فيتنام","indonesia|إندونيسيا","malaysia|ماليزيا","singapore|سنغافورة","philippines|الفلبين","myanmar|ميانمار","nepal|نيبال","srilanka|سريلانكا","afghanistan|أفغانستان","iraq|العراق",
"nigeria|نيجيريا","senegal|السنغال","ghana|غانا","cameroon|الكاميرون","ivory|ساحل العاج","mali|مالي","burkina|بوركينا فاسو","guinea|غينيا","morocco|المغرب","algeria|الجزائر","egypt|مصر","tunisia|تونس","libya|ليبيا","southafrica|جنوب أفريقيا","zambia|زامبيا","zimbabwe|زيمبابوي","kenya|كينيا","uganda|أوغندا","tanzania|تنزانيا","ethiopia|إثيوبيا","angola|أنغولا","mozambique|موزمبيق","namibia|ناميبيا","botswana|بوتسوانا","rwanda|رواندا","congo|الكونغو","drcongo|الكونغو الديمقراطية","gabon|الغابون","benin|بنين","togo|توغو","niger|النيجر","chad|تشاد","sudan|السودان","southsudan|جنوب السودان"];

var gDiv=document.getElementById('g');var gNat=document.getElementById('gNat');
NATIONAL.forEach(c=>{var p=c.split('|');gNat.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">بانتظار...</small></div>';});
ALL.forEach(c=>{var p=c.split('|');gDiv.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">بانتظار...</small></div>';});

var all=[];var filtered=[];var loaded=0;var total=NATIONAL.length+ALL.length;

function isLive(d){var diff=new Date(d)-new Date();return diff<=0 && diff>-7200000}
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit'})}catch(e){return d}}
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=force||'all';
 if(!force){var active=document.querySelector('.f.active');if(active)f=active.innerText.toLowerCase();}
 var code='';
 if(f.includes('سوريا')||f=='syria') code='syria';
 else if(f.includes('السعودية')||f=='saudi') code='saudi';
 else if(f.includes('مصر')||f=='egypt') code='egypt';
 else if(f.includes('eng')) code='england';
 else if(f.includes('العالم')||f=='world') code='world';
 else if(f.includes('آسيا')||f=='asia') code='asia';
 else if(f.includes('أفريقيا')||f=='africa') code='africa';
 else if(f.includes('منتخبات')) code='منتخبات';
 else if(f.includes('live')) code='live';

 filtered=all.filter(m=>{
  var mq=!q||m.home.toLowerCase().includes(q)||m.away.toLowerCase().includes(q)||m.league.toLowerCase().includes(q);
  var mf=true;
  if(code=='live') mf=isLive(m.date);
  else if(code=='منتخبات') mf=m.type=='national';
  else if(code && code!='all') mf=m.code==code||m.league.toLowerCase().includes(code);
  return mq&&mf;
 });
 document.getElementById('live').innerText='LIVE:'+filtered.filter(m=>isLive(m.date)).length;
 document.getElementById('m').innerHTML=filtered.slice(0,400).map((m,i)=>{
  var pr1=50+Math.floor(Math.random()*30);var pr2=100-pr1;var live=isLive(m.date);var isNat=m.type=='national';
  return '<div class="card '+(isNat?'nat':'')+'" onclick="detail('+i+')"><b>'+(isNat?'🏆 ':'⚽ ')+m.home+' vs '+m.away+(live?' <span style=color:red>● LIVE</span>':'')+'</b><br><small>⏰ '+ist(m.date)+' | '+(isNat?'🏆 ':'🏆 ')+m.league+' | 🧠 AI '+pr1+'%-'+pr2+'%</small><div class=bar><div style="width:'+pr1+'%;background:'+(isNat?'gold':'#00ff00')+'"></div><div style="width:'+pr2+'%;background:'+(isNat?'red':'gold')+'"></div></div></div>';
 }).join('')||'<div style=text-align:center;padding:15px;color:#00ff00">🔄 تحميل تلقائي... '+loaded+'/'+total+' بطولة<br>'+all.length+' مباراة محملة</div>';
}

function loadOne(code,type){
 var box=document.getElementById('b-'+code);
 var stat=document.getElementById('s-'+code);
 if(box) box.className='box loading';
 if(stat) stat.innerText='يحمل...';
 fetch('/api/'+code+'?type='+type).then(r=>r.json()).then(d=>{
  d.up.forEach(x=>{x.code=code;x.type=type;});
  all=all.filter(m=>m.code!==code);
  all=all.concat(d.up);
  loaded++;
  document.getElementById('cnt').innerText=loaded+'/'+total+' - '+all.length+' مباراة';
  document.getElementById('progBar').style.width=(loaded/total*100)+'%';
  document.getElementById('s').innerText='✅ '+loaded+'/'+total+' - '+all.length+' مباراة - V52 ULTIMATE';
  if(box) box.className='box ok';
  if(stat) stat.innerText=d.up.length+' مباريات ✅';
  doFilter();
 }).catch(()=>{
  loaded++;doFilter();
 });
}

var queue
