from flask import Flask, jsonify, Response
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shaam V29 PRO</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#FFD700">
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:#FFD700;color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:99}
.tabs{display:flex;background:#111;margin:6px;border-radius:12px;border:2px solid #FFD700;overflow:hidden}
.tab{flex:1;padding:10px;text-align:center;cursor:pointer;font-weight:900}
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
.card:hover{background:#222}
.team-logo{width:28px;height:28px;background:#fff;border-radius:50%;padding:2px;object-fit:contain}
.vs{color:#FFD700;font-weight:900}
.search{margin:6px;background:#111;border:1px solid #333;border-radius:8px;padding:8px;display:flex;gap:6px}
.search input{flex:1;background:transparent;border:0;color:#fff;outline:none}
#modal{position:fixed;inset:0;background:rgba(0,0,0,0.85);display:none;align-items:center;justify-content:center;z-index:999;padding:12px}
#modalBox{background:#111;border:2px solid #FFD700;border-radius:16px;padding:14px;width:100%;max-width:380px;max-height:85vh;overflow:auto}
.install{background:#FFD700;color:#000;padding:8px;text-align:center;font-weight:900;cursor:pointer;display:none}
</style>
</head><body>
<div class="install" id="installBtn" onclick="installPWA()">⬇️ اضغط لتثبيت التطبيق على موبايلك</div>
<div class="h">Shaam V29 PRO - اضغط على المباراة للتفاصيل</div>
<div class="tabs"><div class="tab active" id="t1" onclick="showTab(1)">مباريات</div><div class="tab" id="t2" onclick="showTab(2)">ترتيب</div><div class="tab" id="t3" onclick="showTab(3)">احصائيات</div></div>
<div id="tab1">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc">0</span></span><span id="dn">0/18</span></div>
<div class="filters">
<button class="fbtnA fbtn" onclick="filterAll()">الكل</button>
<button class="fbtn" onclick="filterLive()">Live</button>
<button class="fbtn" onclick="filterLg('eng.1')">ENG</button>
<button class="fbtn" onclick="filterLg('esp.1')">ESP</button>
<button class="fbtn" onclick="filterLg('sau.1')">SAU</button>
<button class="fbtn" onclick="filterLg('uefa.champions')">UCL</button>
<button class="fbtn" onclick="clearFilter()">الغاء</button>
</div>
<div class="search"><span>🔍</span><input id="searchInput" placeholder="ابحث Real, Barca..." oninput="doSearch()"></div>
<div id="st" style="text-align:center;color:#FFD700;padding:6px">يحمل 18 دوري...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>
<div id="tab2" style="display:none;padding:6px"><div style="display:flex;gap:4px;overflow:auto"><button onclick="loadStanding('eng.1')" class="fbtnA fbtn">ENG</button><button onclick="loadStanding('esp.1')" class="fbtn">ESP</button><button onclick="loadStanding('sau.1')" class="fbtn">SAU</button><button onclick="loadStanding('egy.1')" class="fbtn">EGY</button><button onclick="loadStanding('tur.1')" class="fbtn">TUR</button></div><div id="standing-box" style="margin-top:8px">اختر دوري...</div></div>
<div id="tab3" style="display:none;padding:8px"><div class="card">🔴 مباشر: <b id="s1">0</b></div><div class="card">📅 قادمة: <b id="s2">0</b></div><div class="card">✅ نشط: <b id="s4">0/18</b></div><div class="card">🏆 المجموع: <b id="s5" style="color:#FFD700;font-size:22px">0</b></div><div class="card">💡 اضغط على اي مباراة للتفاصيل + ثبت التطبيق من فوق</div></div>

<div id="modal" onclick="closeModal()"><div id="modalBox" onclick="event.stopPropagation()"></div></div>

<script>
var L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
function safeId(s){return s.replaceAll('.','-');}
function formatDate(str){try{var y=str.substring(0,4);var m=str.substring(4,6);var d=str.substring(6,8);return d+"-"+m+"-"+y;}catch(e){return str;}}
var grid=document.getElementById("grid");
for(var k in L){var kk=safeId(k);grid.innerHTML+='<div class="box" id="box-'+kk+'" data-lg="'+k+'" onclick="filterLg(this.dataset.lg)"><b>'+L[k]+'</b><br><span id="cnt-'+kk+'" style="font-size:11px">...</span></div>';}
var allUp=[],allLive=[],done=0,activeLeagues=0,currentFilter='all',searchTerm='';
function showTab(n){document.getElementById("tab1").style.display=n==1?"block":"none";document.getElementById("tab2").style.display=n==2?"block":"none";document.getElementById("tab3").style.display=n==3?"block":"none";document.getElementById("t1").className=n==1?"tab active":"tab";document.getElementById("t2").className=n==2?"tab active":"tab";document.getElementById("t3").className=n==3?"tab active":"tab";}
function clearFilter(){currentFilter='all';searchTerm='';document.getElementById("searchInput").value='';document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive');});renderMatches();}
function filterAll(){currentFilter='all';renderMatches();}
function filterLive(){currentFilter='live';renderMatches();}
function filterLg(lg){currentFilter=lg;document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive');});var box=document.getElementById('box-'+safeId(lg));if(box)box.classList.add('boxActive');renderMatches();}
function doSearch(){searchTerm=document.getElementById("searchInput").value.toLowerCase();renderMatches();}
function openDetails(id,lg){fetch("/api/match/"+lg+"/"+id).then(function(r){return r.json();}).then(function(d){
 var h='<div style="text-align:center"><div style="display:flex;justify-content:space-between;align-items:center"><img src="'+d.homeLogo+'" style="width:50px;height:50px;background:#fff;border-radius:50%;padding:4px"><span style="color:#FFD700;font-weight:900">VS</span><img src="'+d.awayLogo+'" style="width:50px;height:50px;background:#fff;border-radius:50%;padding:4px"></div>';
 h+='<h3 style="margin:10px 0">'+d.home+' vs '+d.away+'</h3><div style="color:#FFD700">'+d.score+'</div>';
 h+='<div style="text-align:right;margin-top:12px;background:#000;padding:8px;border-radius:8px"><div>📅 '+d.date+'</div><div>🏟️ '+d.venue+'</div><div>🏆 '+d.league+'</div><div>⏰ '+d.status+'</div></div>';
 h+='<button onclick="closeModal()" style="margin-top:12px;width:100%;background:#FFD700;border:0;padding:10px;border-radius:10px;font-weight:900">اغلاق</button></div>';
 document.getElementById("modalBox").innerHTML=h;document.getElementById("modal").style.display='flex';
});}
function closeModal(){document.getElementById("modal").style.display='none';}
function renderMatches(){
 var list=[];if(currentFilter=='live')list=allLive;else if(currentFilter=='all')list=allLive.concat(allUp);else list=allLive.concat(allUp).filter(function(m){return m.league==currentFilter;});
 if(searchTerm)list=list.filter(function(m){return (m.home+m.away).toLowerCase().includes(searchTerm);});
 var html='';if(allLive.length>0&&(currentFilter=='all'||currentFilter=='live')){var liveList=list.filter(function(m){return m.isLive;});if(liveList.length>0){html+='<div style="background:#300;padding:6px;text-align:center;color:red">🔴 مباشر '+liveList.length+'</div>'+liveList.map(function(m){return '<div class="card" style="border-color:red" onclick="openDetails(\\''+m.id+'\\',\\''+m.league+'\\')"><img class="team-logo" src="'+m.homeLogo+'"><div style="flex:1"><b>'+m.home+' vs '+m.away+'</b><br><span style="color:#FFD700">'+m.score+'</span> '+m.league+'</div><img class="team-logo" src="'+m.awayLogo+'"></div>';}).join('');}}
 var upList=list.filter(function(m){return!m.isLive;});html+=upList.slice(0,60).map(function(m){return '<div class="card" onclick="openDetails(\\''+m.id+'\\',\\''+m.league+'\\')"><img class="team-logo" src="'+m.homeLogo+'"><div style="flex:1"><b>'+m.home+' <span class="vs">vs</span> '+m.away+'</b><br><small>📅 '+formatDate(m.date)+' | 🏆 '+m.league+'</small></div><img class="team-logo" src="'+m.awayLogo+'"></div>';}).join('');
 if(list.length==0)html='<div style="text-align:center;padding:20px;color:#888">لا يوجد</div>';
 document.getElementById("matches").innerHTML=html;
}
async function fetchLeague(lg){try{var r=await fetch("/api/league30/"+lg);var d=await r.json();var tot=d.up.length+d.live.length;var kk=safeId(lg);var el=document.getElementById("cnt-"+kk);if(tot>0){el.innerText=tot+" games";document.getElementById("box-"+kk).className="box has";activeLeagues++;}else{el.innerText=d.msg||"0";document.getElementById("box-"+kk).className="box zero";}allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("tc").innerText=allUp.length+allLive.length;document.getElementById("s1").innerText=allLive.length;document.getElementById("s2").innerText=allUp.length;document.getElementById("s4").innerText=activeLeagues+"/18";document.getElementById("s5").innerText=allUp.length+allLive.length;}catch(e){}done++;document.getElementById("dn").innerText=done+"/18";document.getElementById("st").innerText=done==18?"خلص! "+(allUp.length+allLive.length)+" مباراة - اضغط على اي مباراة":"يحمل "+done+"/18";if(done%3==0||done==18)renderMatches();}
async function loadStanding(lg){showTab(2);document.getElementById("standing-box").innerHTML="يحمل...";try{var r=await fetch("/api/standing/"+lg);var d=await r.json();var html='<table style="width:100%;border-collapse:collapse"><tr style="background:#FFD700;color:#000"><th>#</th><th>الفريق</th><th>نقاط</th></tr>';d.standing.forEach(function(t){html+='<tr style="border-bottom:1px solid #333"><td style="text-align:center;padding:8px">'+t.pos+'</td><td style="padding:8px"><b>'+t.team+'</b></td><td style="text-align:center;color:#FFD700"><b>'+t.points+'</b></td></tr>';});html+='</table>';document.getElementById("standing-box").innerHTML=html;}catch(e){document.getElementById("standing-box").innerHTML="لا يوجد";}}
async function loadAll(){var keys=Object.keys(L);for(var i=0;i<keys.length;i+=3){var chunk=keys.slice(i,i+3);await Promise.all(chunk.map(function(k){return fetchLeague(k);}));await new Promise(function(r){setTimeout(r,400);});}}loadAll();

// PWA
if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js');}
var deferredPrompt;window.addEventListener('beforeinstallprompt',function(e){e.preventDefault();deferredPrompt=e;document.getElementById('installBtn').style.display='block';});
function installPWA(){if(deferredPrompt){deferredPrompt.prompt();deferredPrompt.userChoice.then(function(){document.getElementById('installBtn').style.display='none';});}}
</script></body></html>
    """

@app.route('/manifest.json')
def manifest():
    return jsonify({"name":"Shaam V29 PRO","short_name":"Shaam","start_url":"/","display":"standalone","background_color":"#000000","theme_color":"#FFD700","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/53/53283.png","sizes":"512x512","type":"image/png"}]})

@app.route('/sw.js')
def sw():
    return Response("self.addEventListener('install',e=>self.skipWaiting());self.addEventListener('fetch',e=>e.respondWith(fetch(e.request).catch(()=>caches.match(e.request))));", mimetype='application/javascript')

@app.route('/api/league30/<lg>')
def api_league30(lg):
    live=[];up=[]
    for i in range(1,61):
        d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=4)
            for ev in r.json().get('events',[]):
                comp=ev['competitions'][0]
                c0=comp['competitors'][0]; c1=comp['competitors'][1]
                base={"id":ev['id'],"home":c0['team']['displayName'],"away":c1['team']['displayName'],"homeLogo":c0['team'].get('logo',''),"awayLogo":c1['team'].get('logo',''),"league":lg,"date":d,"isLive":comp['status']['type']['state']=='in',"score":c0.get('score','0')+"-"+c1.get('score','0')}
                if base["isLive"]: live.append(base)
                else: up.append(base)
            if len(up)>=8: break
        except: continue
    msg="موسم منتهي" if lg in ['sau.1','egy.1'] and len(up)==0 else "0"
    return jsonify({"live":live,"up":up[:8],"msg":msg})

@app.route('/api/match/<lg>/<mid>')
def api_match(lg,mid):
    try:
        r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=5)
        for ev in r.json().get('events',[]):
            if ev['id']==mid:
                comp=ev['competitions'][0]
                c0=comp['competitors'][0]; c1=comp['competitors'][1]
                return jsonify({"home":c0['team']['displayName'],"away":c1['team']['displayName'],"homeLogo":c0['team'].get('logo',''),"awayLogo":c1['team'].get('logo',''),"score":c0.get('score','0')+" - "+c1.get('score','0'),"date":comp['date'][:10],"venue":comp.get('venue',{}).get('fullName','غير معروف'),"league":lg,"status":comp['status']['type']['description']})
    except: pass
    return jsonify({"home":"فريق 1","away":"فريق 2","homeLogo":"","awayLogo":"","score":"0-0","date":"قريبا","venue":"ملعب","league":lg,"status":"قادمة"})

@app.route('/api/standing/<lg>')
def api_standing(lg):
    try:
        r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/standings",timeout=5)
        data=r.json()
        entries=data['children'][0]['standings']['entries
