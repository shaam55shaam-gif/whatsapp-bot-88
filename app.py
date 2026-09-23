from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shaam V31 - PRO</title>
<style>
*{box-sizing:border-box}body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#FFD700,#FFA500);color:#000;padding:12px;text-align:center;font-weight:900;font-size:18px;position:sticky;top:0;z-index:100}
.tabs{display:flex;background:#111;margin:6px;border-radius:14px;border:2px solid gold;overflow:hidden}
.tab{flex:1;padding:12px;text-align:center;font-weight:900;cursor:pointer;transition:0.2s}
.active{background:gold;color:#000}
.info{background:#111;border:1px solid gold;margin:6px;padding:10px;border-radius:12px;display:flex;justify-content:space-around;font-weight:900;font-size:12px}
.filters{display:flex;gap:5px;padding:6px;overflow:auto;scrollbar-width:none}
.btn{background:#222;color:#fff;border:1px solid #444;padding:7px 14px;border-radius:20px;white-space:nowrap;font-size:12px}
.btnA{background:gold;color:#000;font-weight:900;border-color:gold}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:#151515;border:1px solid #333;border-radius:12px;padding:12px;text-align:center;transition:0.2s}
.has{border-color:#0f0;background:linear-gradient(135deg,#0a1a0a,#111);box-shadow:0 0 8px #0f03}
.zero{opacity:0.3}
.boxSel{border:2px solid gold!important;background:gold!important;color:#000!important;transform:scale(1.05)}
.card{background:linear-gradient(135deg,#1a1a1a,#151515);border-right:4px solid gold;margin:6px;padding:12px;border-radius:14px;display:flex;align-items:center;gap:10px;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,0.5)}
.cardFav{border-color:gold;background:linear-gradient(135deg,#1a1a00,#222200);box-shadow:0 0 12px rgba(255,215,0,0.3)}
.vs{color:gold;font-weight:900;margin:0 6px}
.srch{margin:6px;background:#111;border:1px solid #333;border-radius:12px;padding:10px;display:flex;gap:8px;align-items:center}
.srch input{flex:1;background:0;border:0;color:#fff;outline:0;font-size:14px}
.modal{position:fixed;inset:0;background:rgba(0,0,0,0.92);display:none;align-items:center;justify-content:center;z-index:9999;padding:12px}
.modalBox{background:#1a1a1a;border:2px solid gold;border-radius:18px;padding:16px;width:100%;max-width:380px;max-height:90vh;overflow:auto}
.liveDot{width:8px;height:8px;background:red;border-radius:50%;display:inline-block;animation:blink 1s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
</style>
</head><body>
<div class="h">👑 Shaam V31 PRO - 18/18 + كل الميزات</div>
<div class="tabs"><div class="tab active" id="tb1" onclick="tab(1)">⚽ مباريات</div><div class="tab" id="tb2" onclick="tab(2)">📊 ترتيب</div><div class="tab" id="tb3" onclick="tab(3)">📈 احصائيات</div></div>

<div id="p1">
<div class="info"><span><span class="liveDot"></span> Live <span id="lc" style="color:#0f0">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc" style="color:gold">0</span></span><span id="dn">0/18</span></div>
<div class="filters">
<button class="btn btnA" onclick="filter('all')">الكل</button>
<button class="btn" onclick="filter('fav')">⭐ مفضلتي</button>
<button class="btn" style="border-color:red;color:#ff6b6b" onclick="filter('live')">🔴 Live</button>
<button class="btn" onclick="filter('eng.1')">ENG</button>
<button class="btn" onclick="filter('esp.1')">ESP</button>
<button class="btn" onclick="filter('sau.1')">SAU</button>
<button class="btn" onclick="filter('uefa.champions')">UCL</button>
<button class="btn" onclick="enableNotif()">🔔 تفعيل التنبيهات</button>
<button class="btn" onclick="filter('all');document.getElementById('q').value='';search=''">الغاء</button>
</div>
<div class="srch">🔍<input id="q" placeholder="ابحث Real, Barca, City..." oninput="doSearch()"></div>
<div id="favBar" style="display:none;background:linear-gradient(90deg,#1a1a00,#2a2a00);border:1px solid gold;margin:6px;padding:8px;border-radius:12px;text-align:center">⭐ <span id="favList"></span> <button onclick="clearFav()" style="background:red;color:#fff;border:0;border-radius:12px;padding:3px 10px;margin-right:6px">مسح</button></div>
<div id="status" style="text-align:center;color:gold;padding:8px;font-weight:900">🚀 يحمل 90 يوم قدام...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>

<div id="p2" style="display:none;padding:6px"><div style="display:flex;gap:4px;overflow:auto;padding:4px"><button onclick="loadTable('eng.1')" class="btn btnA">ENG</button><button onclick="loadTable('esp.1')" class="btn">ESP</button><button onclick="loadTable('sau.1')" class="btn">SAU</button><button onclick="loadTable('tur.1')" class="btn">TUR</button><button onclick="loadTable('uefa.champions')" class="btn">UCL</button></div><div id="tableBox" style="margin-top:10px">اختر دوري...</div></div>

<div id="p3" style="display:none;padding:8px">
<div class="card">🔴 مباشر: <b id="st1" style="font-size:20px;color:#0f0">0</b></div>
<div class="card">⏰ قادمة: <b id="st2" style="font-size:20px">0</b></div>
<div class="card">⭐ مفضلتي: <b id="stFav" style="font-size:20px;color:gold">0</b></div>
<div class="card" style="background:linear-gradient(90deg,gold,#FFA500);color:#000">🏆 المجموع: <b id="st3" style="font-size:26px">0</b> مباراة</div>
<div style="margin-top:12px;background:#111;border-radius:12px;padding:12px;border:1px solid #333"><h4 style="margin:0 0 8px;color:gold">🔔 التنبيهات</h4><small style="color:#888">اذا فريقك المفضل صار Live رح يجيك اشعار حتى لو مسكر المتصفح - اضغط تفعيل التنبيهات فوق</small><div style="margin-top:8px"><button onclick="enableNotif()" style="background:gold;color:#000;border:0;padding:8px 16px;border-radius:12px;font-weight:900;width:100%">تفعيل التنبيهات 🔔</button></div></div>
</div>

<div class="modal" id="modal" onclick="this.style.display='none'"><div class="modalBox" id="modalBox" onclick="event.stopPropagation()"></div></div>

<script>
var LEAGUES={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
function sid(s){return s.replaceAll('.','-')}
var fav=JSON.parse(localStorage.getItem('favTeams')||'[]');
var allUp=[],allLive=[],done=0,curFilter='all',search='';
var grid=document.getElementById('grid');
for(var k in LEAGUES){var id=sid(k);grid.innerHTML+='<div class="box" id="box-'+id+'" onclick="filter(\\''+k+'\\')"><b>'+LEAGUES[k]+'</b><br><small id="cnt-'+id+'" style="font-size:11px">...</small></div>'}
function tab(n){document.getElementById('p1').style.display=n==1?'block':'none';document.getElementById('p2').style.display=n==2?'block':'none';document.getElementById('p3').style.display=n==3?'block':'none';document.getElementById('tb1').className=n==1?'tab active':'tab';document.getElementById('tb2').className=n==2?'tab active':'tab';document.getElementById('tb3').className=n==3?'tab active':'tab'}
function updateFavBar(){if(fav.length>0){document.getElementById('favBar').style.display='block';document.getElementById('favList').innerText=fav.join(', ');document.getElementById('stFav').innerText=fav.length}else{document.getElementById('favBar').style.display='none';document.getElementById('stFav').innerText='0'}}
updateFavBar();
function enableNotif(){if('Notification' in window){Notification.requestPermission().then(p=>{if(p=='granted'){new Notification('✅ تم تفعيل التنبيهات',{body:'رح نبهك لما فريقك المفضل يلعب!'});alert('✅ تم التفعيل!')}else alert('❌ لازم توافق على التنبيهات')})}else alert('متصفحك ما بيدعم التنبيهات')}
function checkFavLive(){if(fav.length==0||allLive.length==0)return;var favLive=allLive.filter(m=>fav.some(t=>m.home.includes(t)||m.away.includes(t)));if(favLive.length>0&&Notification.permission=='granted'){favLive.forEach(m=>{new Notification('🔴 '+m.home+' Live الآن!',{body:m.home+' vs '+m.away+' - '+m.league})})}}
function toggleFav(team){var i=fav.indexOf(team);if(i>=0)fav.splice(i,1);else fav.push(team);localStorage.setItem('favTeams',JSON.stringify(fav));updateFavBar();renderMatches();if(i<0&&Notification.permission!='granted')if(confirm('بدك نفعل تنبيهات لـ '+team+'؟'))enableNotif()}
function clearFav(){if(!confirm('تمسح الكل؟'))return;fav=[];localStorage.removeItem('favTeams');updateFavBar();renderMatches()}
function filter(f){curFilter=f;document.querySelectorAll('.box').forEach(b=>b.classList.remove('boxSel'));if(LEAGUES[f]){var el=document.getElementById('box-'+sid(f));if(el)el.classList.add('boxSel')}renderMatches()}
function doSearch(){search=document.getElementById('q').value.toLowerCase();renderMatches()}
function openDetails(m){
var html='<div style="text-align:center">'
+'<div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px"><div style="text-align:center"><div style="width:60px;height:60px;background:#fff;border-radius:50%;display
