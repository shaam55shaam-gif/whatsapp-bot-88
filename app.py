from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V26 SUPER</title>
<style>
*{box-sizing:border-box}body{background:#000;color:#fff;font-family:Arial;margin:0;padding-bottom:20px}
.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:14px;text-align:center;font-weight:900;font-size:16px;position:sticky;top:0;z-index:10}
.tabs{display:flex;background:#111;margin:8px;border-radius:15px;border:2px solid #FFD700;overflow:hidden}
.tab{flex:1;padding:12px;text-align:center;cursor:pointer;font-weight:900;font-size:13px}
.active{background:#FFD700;color:#000}
.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;display:flex;justify-content:space-around;font-size:11px;font-weight:900}
.filters{display:flex;gap:6px;padding:8px;overflow:auto}
.fbtn{background:#222;color:#fff;border:1px solid #555;padding:8px 14px;border-radius:20px;white-space:nowrap;cursor:pointer;font-size:12px;font-weight:700}
.fbtnA{background:#FFD700;color:#000;border:0}
.search{margin:8px;background:#111;border:1px solid #333;border-radius:12px;padding:10px;display:flex;gap:6px}
.search input{flex:1;background:transparent;border:0;color:#fff;outline:none;font-size:14px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px}
.box{background:#111;border:1px solid #333;border-radius:14px;padding:12px;text-align:center;cursor:pointer;transition:0.2s}
.box:hover{transform:scale(1.03)}
.has{border-color:#0f0;background:linear-gradient(135deg,#0a2a0a,#111);box-shadow:0 0 10px #0f05}
.boxActive{border-color:#FFD700!important;background:#FFD700!important;color:#000!important;box-shadow:0 0 15px #FFD70099}
.zero{opacity:0.5}
.card{background:#1a1a1a;border-right:5px solid #FFD700;border-radius:14px;margin:8px;padding:12px;display:flex;align-items:center;gap:10px;cursor:pointer}
.live-card{border-right-color:red;background:#2a0a0a}
.team-logo{width:32px;height:32px;object-fit:contain;background:#fff;border-radius:50%;padding:2px}
.vs{color:#FFD700;font-weight:900}
.league-tag{font-size:10px;background:#333;padding:2px 6px;border-radius:6px;margin-top:4px;display:inline-block}
</style>
</head><body>
<div class="h">🏆 Shaam V26 SUPER - اضغط على الدوري للفلترة ⚡</div>
<div class="tabs"><div class="tab active" id="t1" onclick="showTab(1)">📅 مباريات</div><div class="tab" id="t2" onclick="showTab(2)">📊 ترتيب</div><div class="tab" id="t3" onclick="showTab(3)">📈 احصائيات</div></div>

<div id="tab1">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc">0</span></span><span id="dn">0/18</span></div>
<div class="filters">
<button class="fbtnA fbtn" id="fb-all" onclick="filterMatches('all')">الكل</button>
<button class="fbtn" id="fb-live" onclick="filterMatches('live')">🔴 Live</button>
<button class="fbtn" id="fb-eng" onclick="filterMatches('eng.1')">ENG</button>
<button class="fbtn" id="fb-esp" onclick="filterMatches('esp.1')">ESP</button>
<button class="fbtn" id="fb-ucl" onclick="filterMatches('uefa.champions')">UCL</button>
<button class="fbtn" onclick="clearFilter()">❌ الغاء الفلتر</button>
</div>
<div class="search"><span>🔍</span><input id="searchInput" placeholder="ابحث عن فريق... Real, Barca, Arsenal..." oninput="doSearch()"></div>
<div id="st" style="text-align:center;color:#FFD700;padding:8px;font-weight:900">⚡ يحمل 18 دوري...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>

<div id="tab2" style="display:none;padding:8px">
<div style="display:flex;gap:5px;overflow:auto;white-space:nowrap;padding:5px">
<button onclick="loadStanding('eng.1',this)" class="fbtnA fbtn">ENG</button>
<button onclick="loadStanding('esp.1',this)" class="fbtn">ESP</button>
<button onclick="loadStanding('ita.1',this)" class="fbtn">ITA</button>
<button onclick="loadStanding('ger.1',this)" class="fbtn">GER</button>
<button onclick="loadStanding('sau.1',this)" class="fbtn">SAU</button>
<button onclick="loadStanding('tur.1',this)" class="fbtn">TUR</button>
<button onclick="loadStanding('egy.1',this)" class="fbtn">EGY</button>
</div>
<div id="standing-box" style="margin-top:10px">اختر دوري...</div>
</div>

<div id="tab3" style="display:none;padding:10px">
<h3 style="color:#FFD700">📈 احصائيات V26</h3>
<div class="card"><div>🔴 مباشر: <b id="s1">0</b></div></div>
<div class="card"><div>📅 قادمة: <b id="s2">0</b></div></div>
<div class="card"><div>✅ دوريات نشطة: <b id="s4">0/18</b></div></div>
<div class="card"><div>🏆 المجموع: <b id="s5" style="color:#FFD700;font-size:22px">0</b> مباراة</div></div>
</div>

<script>
var L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
var LEAGUE_ICON={"eng.1":"🏴󠁧󠁢󠁥󠁮󠁧󠁿","esp.1":"🇪🇸","ita.1":"🇮🇹","ger.1":"🇩🇪","fra.1":"🇫🇷","tur.1":"🇹🇷","sau.1":"🇸🇦","egy.1":"🇪🇬","uefa.champions":"🏆","uefa.europa":"🏆","usa.1":"🇺🇸"};
var grid=document.getElementById("grid");
for(var k in L){
  var kk=k.replace(/\\./g,"-");
  var icon=LEAGUE_ICON[k]||"⚽";
  grid.innerHTML+='<div class="box" id="box-'+kk+'" onclick="filterMatches(\\''+k+'\\')"><div style="font-size:18px">'+icon+'</div><b>'+L[k]+'</b><br><small style="font-size:9px;opacity:0.6">'+k+'</small><br><span id="cnt-'+kk+'" style="color:#888;font-size:11px">⏳</span></div>';
}
var allUp=[],allLive=[],done=0,activeLeagues=0,currentFilter='all',searchTerm='';
function showTab(n){
  document.getElementById("tab1").style.display=n==1?"block":"none";
  document.getElementById("tab2").style.display=n==2?"block":"none";
  document.getElementById("tab3").style.display=n==3?"block":"none";
  document.getElementById("t1").className=n==1?"tab active":"tab";
  document.getElementById("t2").className=n==2?"tab active":"tab";
  document.getElementById("t3").className=n==3?"tab active":"tab";
}
function clearFilter(){
  currentFilter='all';searchTerm='';document.getElementById("searchInput").value='';
  document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive'); if(b.className.includes('has')){} });
  renderMatches();
  document.querySelectorAll('.fbtn').forEach(function(b){b.className='fbtn';}); document.getElementById('fb-all').className='fbtnA fbtn';
}
function filterMatches(lg){
  currentFilter=lg;
  document.querySelectorAll('.fbtn').forEach(function(b){b.className='fbtn';});
  var fb=document.getElementById('fb-'+lg.split('.')[0]); if(fb) fb.className='fbtnA fbtn';
  if(lg=='all') document.getElementById('fb-all').className='fbtnA fbtn';
  if(lg=='live') document.getElementById('fb-live').className='fbtnA fbtn';
  // highlight box
  document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive');});
  if(lg!='all' && lg!='live'){ var kk=lg.replace(/\\./g,"-"); var box=document.getElementById('box-'+kk); if(box) box.classList.add('boxActive'); }
  renderMatches();
}
function doSearch(){searchTerm=document.getElementById("searchInput").value.toLowerCase(); renderMatches();}
function renderMatches(){
  var list=[];
  if(currentFilter=='live') list=allLive;
  else if(currentFilter=='all') list=allLive.concat(allUp);
  else list=allLive.concat(allUp).filter(function(m){return m.league==currentFilter;});
  if(searchTerm) list=list.filter(function(m){return (m.home+m.away).toLowerCase().includes(searchTerm);});
  var html='';
  if(allLive.length>0 && (currentFilter=='all' || currentFilter=='live')){
    var liveList=currentFilter=='live'?list:list.filter(function(m){return m.isLive;});
    if(liveList.length>0){
      html+='<div style="background:#300;padding:8px;text-align:center;color:#ff4444;font-weight:900;border-radius:10px;margin:8px">🔴 مباشر الان - '+liveList.length+'</div>';
      html+=liveList.map(function(m){
        return '<div class="card live-card"><img class="team-logo" src="'+(m.homeLogo||'https://a.espncdn.com/combiner/i?img=%2Fi%2Fteamlogos%2Fsoccer%2F500%2Fdefault.png')+'" onerror="this.style.display=\\'none\\'"><div style="flex:1"><b>'+m.home+' <span class="vs">vs</span> '+m.away+'</b><br><span style="color:#FFD700">'+m.score+'</span> <span class="league-tag">'+m.league+'</span></div><img class="team-logo" src="'+(m.awayLogo||'')+'" onerror="this.style.display=\\'none\\'"></div>';
      }).join('');
    }
  }
  var upList=list.filter(function(m){return!m.isLive;});
  if(currentFilter!='live'){
    if(currentFilter!='all') html+='<div style="text-align:center;color:#FFD700;padding:8px">🏆 '+currentFilter.toUpperCase()+' - '+upList.length+' مباراة</div>';
    html+=upList.slice(0,80).map(function(m){
      return '<div class="card"><img class="team-logo" src="'+(m.homeLogo||'https://a.espncdn.com/combiner/i?img=%2Fi%2Fteamlogos%2Fsoccer%2F500%2Fdefault.png')+'" onerror="this.style.display=\\'none\\'"><div style="flex:1"><b>'+m.home+' <span class="vs">vs</span> '+m.away+'</b><br><small>📅 '+m.date+' | <span class="league-tag">'+m.league+'</span></small></div><img class="team-logo" src="'+(m.awayLogo||'')+'" onerror="this.style.display=\\'none\\'"></div>';
    }).join('');
  }
  if(list.length==0) html='<div style="text-align:center;padding:30px;color:#888">لا
