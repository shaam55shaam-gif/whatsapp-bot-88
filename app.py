from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V30.1 PRO MAX</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:#FFD700;color:#000;padding:12px;text-align:center;font-weight:900}
.tabs{display:flex;background:#111;margin:6px;border-radius:12px;border:2px solid #FFD700;overflow:hidden}
.tab{flex:1;padding:8px;text-align:center;cursor:pointer;font-weight:900;font-size:11px}
.active{background:#FFD700;color:#000}
.money{background:#111;border:1px solid #FFD700;padding:8px;border-radius:12px;margin:6px;display:flex;justify-content:space-around;font-size:11px;font-weight:900}
.filters{display:flex;gap:5px;padding:6px;overflow:auto}
.fbtn{background:#222;color:#fff;border:1px solid #555;padding:6px 12px;border-radius:15px;font-size:12px;white-space:nowrap;cursor:pointer}
.fbtnA{background:#FFD700;color:#000;border:0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:#111;border:1px solid #333;border-radius:10px;padding:10px;text-align:center;cursor:pointer}
.has{border-color:#0f0;background:#0a1a0a}
.boxActive{border:2px solid #FFD700!important;background:#FFD700!important;color:#000!important}
.zero{opacity:0.4}
.card{background:#151515;border-right:4px solid #FFD700;border-radius:10px;margin:6px;padding:10px;display:flex;align-items:center;gap:8px;font-size:13px;cursor:pointer}
.fav-card{border-color:gold;background:#1a1a00}
.live-card{border-color:red;background:#2a0a0a}
.team-logo{width:28px;height:28px;background:#fff;border-radius:50%;padding:2px}
.vs{color:#FFD700;font-weight:900}
.search{margin:6px;background:#111;border:1px solid #333;border-radius:8px;padding:8px;display:flex;gap:6px}
.search input{flex:1;background:transparent;border:0;color:#fff;outline:none}
#modal{position:fixed;inset:0;background:rgba(0,0,0,0.92);display:none;align-items:center;justify-content:center;z-index:999;padding:12px}
#modalBox{background:#1a1a1a;border:2px solid #FFD700;border-radius:16px;padding:16px;width:100%;max-width:360px}
.star{position:absolute;top:4px;left:6px;font-size:16px}
</style>
</head><body>
<div class="h">Shaam V30.1 - المفضلة + تحديث تلقائي</div>
<div class="tabs"><div class="tab active" id="t1" onclick="showTab(1)">مباريات</div><div class="tab" id="t2" onclick="showTab(2)">ترتيب</div><div class="tab" id="t3" onclick="showTab(3)">هدافين</div><div class="tab" id="t4" onclick="showTab(4)">احصائيات</div></div>
<div id="tab1">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc">0</span></span><span id="dn">0/18</span><span id="auto">🔄</span></div>
<div class="filters">
<button class="fbtnA fbtn" onclick="filterAll()">الكل</button>
<button class="fbtn" onclick="filterFav()">⭐ مفضلتي</button>
<button class="fbtn" onclick="filterLive()">Live</button>
<button class="fbtn" onclick="filterLg('eng.1')">ENG</button>
<button class="fbtn" onclick="filterLg('esp.1')">ESP</button>
<button class="fbtn" onclick="filterLg('sau.1')">SAU</button>
<button class="fbtn" onclick="clearFilter()">الغاء</button>
</div>
<div class="search"><span>🔍</span><input id="searchInput" placeholder="ابحث Real, Barca..." oninput="doSearch()"></div>
<div id="st" style="text-align:center;color:#FFD700;padding:6px">يحمل...</div>
<div id="favBar" style="display:none;background:#1a1a00;border:1px solid gold;border-radius:10px;margin:6px;padding:8px;text-align:center"><span style="color:gold">⭐ مفضلتك: </span><span id="favList"></span> <span onclick="clearFav()" style="color:red;cursor:pointer"> [مسح]</span></div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>
<div id="tab2" style="display:none;padding:6px"><div style="display:flex;gap:4px;overflow:auto"><button onclick="loadStanding('eng.1')" class="fbtnA fbtn">ENG</button><button onclick="loadStanding('esp.1')" class="fbtn">ESP</button><button onclick="loadStanding('sau.1')" class="fbtn">SAU</button><button onclick="loadStanding('egy.1')" class="fbtn">EGY</button></div><div id="standing-box" style="margin-top:8px">اختر دوري...</div></div>
<div id="tab3" style="display:none;padding:6px"><div style="display:flex;gap:4px;overflow:auto"><button onclick="loadScorers('eng.1')" class="fbtnA fbtn">ENG</button><button onclick="loadScorers('esp.1')" class="fbtn">ESP</button><button onclick="loadScorers('sau.1')" class="fbtn">SAU</button></div><div id="scorers-box" style="margin-top:8px">اختر دوري...</div></div>
<div id="tab4" style="display:none;padding:8px"><div class="card">مباشر: <b id="s1">0</b></div><div class="card">قادمة: <b id="s2">0</b></div><div class="card">نشط: <b id="s4">0/18</b></div><div class="card">المجموع: <b id="s5" style="color:gold;font-size:20px">0</b></div><div class="card">⭐ مفضلة: <b id="sFav">0</b></div><div class="card" style="border-color:#0f0">🔄 تحديث تلقائي كل 30 ثانية شغال</div></div>
<div id="modal" onclick="this.style.display='none'"><div id="modalBox" onclick="event.stopPropagation()"></div></div>
<script>
var L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
function safeId(s){return s.replaceAll('.','-');}
function formatDate(str){try{return str.substring(6,8)+"-"+str.substring(4,6);}catch(e){return str;}}
var favTeams=JSON.parse(localStorage.getItem('favTeams')||'[]');
var grid=document.getElementById("grid");
for(var k in L){var kk=safeId(k);grid.innerHTML+='<div class="box" id="box-'+kk+'" data-lg="'+k+'" onclick="filterLg(this.dataset.lg)"><b>'+L[k]+'</b><br><span id="cnt-'+kk+'" style="font-size:11px">...</span></div>';}
var allUp=[],allLive=[],done=0,currentFilter='all',searchTerm='';
function showTab(n){document.getElementById("tab1").style.display=n==1?"block":"none";document.getElementById("tab2").style.display=n==2?"block":"none";document.getElementById("tab3").style.display=n==3?"block":"none";document.getElementById("tab4").style.display=n==4?"block":"none";document.getElementById("t1").className=n==1?"tab active":"tab";document.getElementById("t2").className=n==2?"tab active":"tab";document.getElementById("t3").className=n==3?"tab active":"tab";document.getElementById("t4").className=n==4?"tab active":"tab";}
function toggleFav(team){var i=favTeams.indexOf(team);if(i>=0)favTeams.splice(i,1);else favTeams.push(team);if(favTeams.length>5)favTeams.shift();localStorage.setItem('favTeams',JSON.stringify(favTeams));updateFavBar();renderMatches();}
function clearFav(){favTeams=[];localStorage.removeItem('favTeams');updateFavBar();renderMatches();}
function updateFavBar(){if(favTeams.length>0){document.getElementById("favBar").style.display='block';document.getElementById("favList").innerText=favTeams.join(', ');document.getElementById("sFav").innerText=favTeams.length;}else{document.getElementById("favBar").style.display='none';document.getElementById("sFav").innerText='0';}}
updateFavBar();
function clearFilter(){currentFilter='all';searchTerm='';document.getElementById("searchInput").value='';document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive');});renderMatches();}
function filterAll(){currentFilter='all';renderMatches();}
function filterFav(){currentFilter='fav';renderMatches();}
function filterLive(){currentFilter='live';renderMatches();}
function filterLg(lg){currentFilter=lg;document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive');});var box=document.getElementById('box-'+safeId(lg));if(box)box.classList.add('boxActive');renderMatches();}
function doSearch(){searchTerm=document.getElementById("searchInput").value.toLowerCase();renderMatches();}
function openDetails(h,a,hl,al,dt,lg,sc){
 var isFH=favTeams.includes(h);var isFA=favTeams.includes(a);
 var html='<div style="text-align:center"><div style="display:flex;justify-content:space-between;align-items:center"><div><img src="'+hl+'" style="width:60px;height:60px;background:#fff;border-radius:50%;padding:5px"><br><span onclick="toggleFav(\\''+h+'\\');document.getElementById(\\'modal\\').style.display=\\'none\\'" style="cursor:pointer;color:'+(isFH?'gold':'#888')+'">⭐ '+(isFH?'مفضل':'اضف')+'</span></div><span style="color:gold;font-weight:900;font-size:20px">'+sc+'</span><div><img src="'+al+'" style="width:60px;height:60px;background:#fff;border-radius:50%;padding:5px"><br><span onclick="toggleFav(\\''+a+'\\');document.getElementById(\\'modal\\').style.display=\\'none\\'" style="cursor:pointer;color:'+(isFA?'gold':'#888')+'">⭐ '+(isFA?'مفضل':'اضف')+'</span></div></div><h3 style="margin:10px 0">'+h+' vs '+a+'</h3><div style="background:#000;padding:10px;border-radius:10px;text-align:right"><div>📅 '+formatDate(dt)+'</div><div>🏆 '+lg+'</div></div><button onclick="document.getElementById(\\'modal\\').style.display=\\'none\\'" style="margin-top:12px;width:100%;background:gold;border:0;padding:12px;border-radius:12px;font-weight:900">اغلاق</button></div>';
 document.getElementById("modalBox").innerHTML=html;document.getElementById("modal").style.display='flex';
}
function renderMatches(){
 var list=[];if(currentFilter=='live')list=allLive;else if(currentFilter=='all')list=allLive.concat(allUp);else if(currentFilter=='fav')list=allLive.concat(allUp).filter(function(m){return favTeams.some(function(f){return m.home.indexOf(f)>=0||m.away.indexOf(f)>=0;});});else list=allLive.concat(allUp).filter(function(m){return m.league==currentFilter;});
 if(searchTerm)list=list.filter(function(m){return (m.home+m.away).toLowerCase().includes(searchTerm);});
 list.sort(function(a,b){var af=favTeams.some(function(f){return a.home.indexOf(f)>=0||a.away.indexOf(f)>=0;});var bf=favTeams.some(function(f){return b.home.indexOf(f)>=0||b.away.indexOf(f)>=0;});return bf-af;});
 var html='';if(currentFilter=='fav'&&favTeams.length==0){html='<div style="text-align:center;padding:30px"><div style="font-size:40px">⭐</div><div>ما عندك فرق مفضلة</div><div style="color:#888;font-size:12px">افتح اي مباراة واضغط ⭐</div></div>';}
 else{
   if(allLive.length>0){var liveList=list.filter(function(m){return m.isLive;});if(liveList.length>0&& (currentFilter=='all'||currentFilter=='live'||currentFilter=='fav')){html+='<div style="background:#300;padding:6px;text-align:center;color:red;font-weight:900">🔴 مباشر '+liveList.length+'</div>'+liveList.map(function(m){var isF=favTeams.some(function(f){return m.home.indexOf(f)>=0||m.away.indexOf(f)>=0;});return '<div class="card '+(isF?'fav-card':'live-card')+'" onclick="openDetails(\\''+m.home+'\\',\\''+m.away+'\\',\\''+m.homeLogo+'\\',\\''+m.awayLogo+'\\',\\''+m.date+'\\',\\''+m.league+'\\',\\''+m.score+'\\')"><span class="star">'+(isF?'⭐':'')+'</span><img class="team-logo" src="'+m.homeLogo+'"><div style="flex:1"><b>'+m.home+' vs '+m.away+'</b><br><span style="color:gold">'+m.score+'</span></div><img class="team-logo" src="'+m.awayLogo+'"></div>';}).join('');}}
   var upList=list.filter(function(m){return!m.isLive;});
   html+=upList.slice(0,80).map(function(m){var isF=favTeams.some(function(f){return m.home.indexOf(f)>=0||m.away.indexOf(f)>=0;});return '<div class="card '+(isF?'fav-card':'')+'" onclick="openDetails(\\''+m.home+'\\',\\''+m.away+'\\',\\''+m.homeLogo+'\\',\\''+m.awayLogo+'\\',\\''+m.date+'\\',\\''+m.league+'\\',\\'VS\\')"><span class="star">'+(isF?'⭐':'')+'</span><img class="team-logo" src="'+m.homeLogo+'"><div style="flex:1"><b>'+m.home+' <span class="vs">vs</span> '+m.away+'</b><br><small>📅 '+formatDate(m.date)+' | '+m.league+'</small></div><img class="team-logo" src="'+m.awayLogo+'"></div>';}).join('');
   if(list.length==0&&currentFilter!='fav')html='<div style="text-align:center;padding:20px;color:#888">لا يوجد</div>';
 }
 document.getElementById("matches").innerHTML=html;
}
async function fetchLeague(lg){try{var r=await fetch("/api/league30/"+lg);var d=await r.json();var tot=d.up.length+d.live.length;var kk=safeId(lg);var el=document.getElementById("cnt-"+kk);if(tot>0){el.innerText=tot+" games";document.getElementById("box-"+kk).className="box has";}else{el.innerText=d.msg||"0";document.getElementById("box-"+kk).className="box zero";}if(done<18){allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);}else{allUp=allUp.filter(function(m){return m.league!=lg;}).concat(d.up);allLive=allLive.filter(function(m){return m.league!=lg;}).concat(d.live);}document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("tc").innerText=allUp.length+allLive.length;document.getElementById("s1").innerText=allLive.length;document.getElementById("s2").innerText=allUp.length;document.getElementById("s4").innerText=document.querySelectorAll('.has').length+"/18";document.getElementById("s5").innerText=allUp.length+allLive.length;}catch(e){}if(done<18){done++;document.getElementById("dn").innerText=done+"/18";document.getElementById("st").innerText=done==18?"خلص! "+(allUp.length+allLive.length)+" مباراة - ⭐ اضف مفضلتك":"Done "+done+"/18";if(done%3==0||done==18)renderMatches();}}
async function loadStanding(lg){showTab(2);document.getElementById("standing-box").innerHTML="يحمل...";try{var r=await fetch("/api/standing/"+lg);var d=await r.json();var h='<table style="width:100%;border-collapse:collapse"><tr style="background:gold;color:#000"><th>#</th><th>الفريق</th><th>نقاط</th></tr>';d.standing.forEach(function(t){h+='<tr style="border-bottom:1px solid #333"><td style="text-align:center;padding:8px">'+t.pos+'</td><td style="padding:8px"><b>'+t.team+'</b></td><td style="text-align:center;color:gold"><b>'+t.points+'</b></td></tr>';});h+='</table>';document.getElementById("standing-box").innerHTML=h;}catch(e){document.getElementById("standing-box").innerHTML="لا يوجد";}}
async function loadScorers(lg){showTab(3);document.getElementById("scorers-box").innerHTML="يحمل هدافين "+lg+"...";try{var r=await fetch("/api/scorers/"+lg);var d=await r.json();var h='<table style="width:100%;border-collapse:collapse"><tr style="background:gold;color:#000"><th>#</th><th>اللاعب</th><th>الفريق</th><th>اهداف</th></tr>';d.scorers.forEach(function(s
