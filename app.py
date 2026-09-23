from flask import Flask, jsonify
import datetime
app = Flask(__name__)

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,red,#00ff00);color:#000;padding:9px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:10px;border-radius:12px}
.card.nat{border-right-color:gold;background:#1a1a00}.card.champ{border-right-color:#00aaff;background:#001a2a}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:6px;max-height:200px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:5px;text-align:center;font-size:9px}
.box.ok{border-color:#00ff00;background:#002a00}.box.ok2{border-color:gold;background:#2a2a00}.box.ok3{border-color:#00aaff;background:#001a2a}
.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:6px 10px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:6px;background:#333;border-radius:6px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,#00ff00,gold,#00aaff);transition:width.5s}
.sec{padding:6px 10px;font-weight:900;border-bottom:1px solid #333;margin-top:8px;font-size:11px}
</style></head><body>
<div class=h>V54 CHAMPIONS - 200 دولة + 12 منتخب + 10 أبطال = 222 بطولة AUTO</div>
<div style="padding:5px;font-size:10px;color:#00ff00;display:flex;justify-content:space-between"><span id=live>LIVE:0</span><span id=cnt>0/222</span><span id=upd>يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: الهلال، Real Madrid، كأس العالم، سوريا..." oninput="doFilter()"></div>
<div style="padding:6px;white-space:nowrap;overflow:auto"><span class="f active" onclick="setF('all',this)">الكل 222</span><span class=f onclick="setF('champ',this)">🏆 أبطال</span><span class=f onclick="setF('منتخبات',this)">🌍 منتخبات</span><span class=f onclick="setF('عرب',this)">🇸🇦 عرب</span><span class=f onclick="setF('ucl',this)">أوروبا</span><span class=f onclick="setF('afc',this)">آسيا</span></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">V54 CHAMPIONS يحمل...</div>
<div class=sec style="color:#00aaff">🏆 دوري الأبطال - 10 بطولات</div><div class=grid id=gC></div>
<div class=sec style="color:gold">🌍 منتخبات - 12 بطولة</div><div class=grid id=gN></div>
<div class=sec style="color:#00ff00">🌍 أندية - 200 دولة</div><div class=grid id=g></div>
<div id=m></div>
<script>
var CHAMP=["ucl|دوري أبطال أوروبا","uel|الدوري الأوروبي","afc_cl|دوري أبطال آسيا","afc2|دوري أبطال آسيا 2","caf_cl|دوري أبطال أفريقيا","caf_conf|الكونفدرالية","arab_cl|دوري أبطال العرب","gulf_cl|دوري أبطال الخليج","club_world|كأس العالم للأندية","libertadores|ليبرتادوريس"];
var NAT=["world_cup|كأس العالم","asia_cup|كأس آسيا","africa_cup|كأس أفريقيا","euro|يورو","copa_america|كوبا أمريكا","arab_cup|كأس العرب","olympic|الأولمبياد","nations|دوري الأمم","gulf_cup|كأس الخليج","u21_euro|يورو تحت 21","asian_games|الألعاب الآسيوية","african_ch|أفريقيا محليين"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","mauritania|موريتانيا","somalia|الصومال",
"england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","turkey|تركيا","greece|اليونان","sweden|السويد","norway|النرويج","denmark|الدنمارك","poland|بولندا","ukraine|أوكرانيا","russia|روسيا","croatia|كرواتيا","serbia|صربيا","swiss|سويسرا","austria|النمسا","czech|التشيك","scotland|اسكتلندا","wales|ويلز","ireland|أيرلندا",
"brazil|البرازيل","argentina|الأرجنتين","uruguay|أوروغواي","colombia|كولومبيا","chile|تشيلي","mexico|المكسيك","usa|أمريكا","canada|كندا","japan|اليابان","korea_s|كوريا","china|الصين","australia|أستراليا","iran|إيران","india|الهند","nigeria|نيجيريا","senegal|السنغال","ghana|غانا","cameroon|الكاميرون","southafrica|جنوب أفريقيا","kenya|كينيا"];

var g=document.getElementById('g'),gn=document.getElementById('gN'),gc=document.getElementById('gC');
CHAMP.forEach(c=>{var p=c.split('|');gc.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
NAT.forEach(c=>{var p=c.split('|');gn.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
ALL.forEach(c=>{var p=c.split('|');g.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
var all=[],loaded=0,total=CHAMP.length+NAT.length+ALL.length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit'})}catch(e){return d}}
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=(force||document.querySelector('.f.active').innerText).toLowerCase();
 var code=''; if(f.includes('أبطال')||f=='champ'||f.includes('ucl')||f.includes('afc')) code=f; else if(f.includes('منتخبات')) code='منتخبات'; else if(f.includes('عرب')) code='عرب';
 var filtered=all.filter(m=>{var mq=!q||m.home.toLowerCase().includes(q)||m.league.toLowerCase().includes(q); var mf=true;
  if(code=='منتخبات') mf=m.type=='nat'; else if(code=='عرب') mf=['syria','saudi','egypt','algeria','morocco','tunisia','iraq','jordan','lebanon','palestine','uae','qatar','kuwait','bahrain','oman','yemen','sudan','libya'].includes(m.code);
  else if(code=='champ'||code.includes('أبطال')) mf=m.type=='champ'; else if(code) mf=m.code==code||m.league.toLowerCase().includes(code);
  return mq&&mf;});
 document.getElementById('m').innerHTML=filtered.slice(0,500).map(m=>{
  var pr1=50+Math.floor(Math.random()*30),pr2=100-pr1,
