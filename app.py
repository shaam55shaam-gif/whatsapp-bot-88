from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V26.1 FIXED</title>
<style>
*{box-sizing:border-box}body{background:#000;color:#fff;font-family:Arial;margin:0;padding-bottom:20px}
.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:14px;text-align:center;font-weight:900;font-size:16px;position:sticky;top:0;z-index:10}
.tabs{display:flex;background:#111;margin:8px;border-radius:15px;border:2px solid #FFD700;overflow:hidden}
.tab{flex:1;padding:12px;text-align:center;cursor:pointer;font-weight:900}
.active{background:#FFD700;color:#000}
.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;display:flex;justify-content:space-around;font-size:11px;font-weight:900}
.filters{display:flex;gap:6px;padding:8px;overflow:auto}
.fbtn{background:#222;color:#fff;border:1px solid #555;padding:8px 14px;border-radius:20px;white-space:nowrap;cursor:pointer}
.fbtnA{background:#FFD700;color:#000;border:0}
.search{margin:8px;background:#111;border:1px solid #333;border-radius:12px;padding:10px;display:flex;gap:6px}
.search input{flex:1;background:transparent;border:0;color:#fff;outline:none}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px}
.box{background:#111;border:1px solid #333;border-radius:14px;padding:12px;text-align:center;cursor:pointer}
.has{border-color:#0f0;background:#0a2a0a;box-shadow:0 0 10px #0f05}
.boxActive{border-color:#FFD700!important;background:#FFD700!important;color:#000!important}
.zero{opacity:0.5}
.card{background:#1a1a1a;border-right:5px solid #FFD700;border-radius:14px;margin:8px;padding:12px;display:flex;align-items:center;gap:10px}
.live-card{border-right-color:red;background:#2a0a0a}
.team-logo{width:30px;height:30px;object-fit:contain;background:#fff;border-radius:50%;padding:2px}
.vs{color:#FFD700;font-weight:900}
</style>
</head><body>
<div class="h">Shaam V26.1 FIXED - اضغط على الدوري للفلترة</div>
<div class="tabs"><div class="tab active" id="t1" onclick="showTab(1)">مباريات</div><div class="tab" id="t2" onclick="showTab(2)">ترتيب</div><div class="tab" id="t3" onclick="showTab(3)">احصائيات</div></div>
<div id="tab1">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc">0</span></span><span id="dn">0/18</span></div>
<div class="filters">
<button class="fbtnA fbtn" id="fb-all" onclick="filterMatches('all')">الكل</button>
<button class="fbtn" id="fb-live" onclick="filterMatches('live')">Live</button>
<button class="fbtn" onclick="filterMatches('eng.1')">ENG</button>
<button class="fbtn" onclick="filterMatches('esp.1')">ESP</button>
<button class="fbtn" onclick="filterMatches('uefa.champions')">UCL</button>
<button class="fbtn" onclick="clearFilter()">الغاء</button>
</div>
<div class="search"><span>🔍</span><input id="searchInput" placeholder="ابحث Real, Barca, Arsenal..." oninput="doSearch()"></div>
<div id="st" style="text-align:center;color:#FFD700;padding:8px;font-weight:900">يحمل...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>
<div id="tab2" style="display:none;padding:8px">
<div style="display:flex;gap:5px;overflow:auto"><button onclick="loadStanding('eng.1')" class="fbtnA fbtn">ENG</button><button onclick="loadStanding('esp.1')" class="fbtn">ESP</button><button onclick="loadStanding('sau.1')" class="fbtn">SAU</button><button onclick="loadStanding('tur.1')" class="fbtn">TUR</button></div>
<div id="standing-box" style="margin-top:10px">اختر دوري...</div>
</div>
<div id="tab3" style="display:none;padding:10px"><h3 style="color:#FFD700">احصائيات V26</h3><div class="card"><div>مباشر: <b id="s1">0</b></div></div><div class="card"><div>قادمة: <b id="s2">0</b></div></div><div class="card"><div>نشط: <b id="s4">0/18</b></div></div><div class="card"><div>المجموع: <b id="s5" style="color:#FFD700;font-size:20px">0</b></div></div></div>
<script>
var L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
function safeId(s){return s.split('.').join('-');}
var grid=document.getElementById("grid");
for(var k in L){var kk=safeId(k);grid.innerHTML+='<div class="box" id="box-'+kk+'" onclick="filterMatches(\\''+k+'\\')"><b>'+L[k]+'</b><br><span id="cnt-'+kk+'" style="color:#888;font-size:11px">...</span></div>';}
var allUp=[],allLive=[],done=0,activeLeagues=0,currentFilter='all',searchTerm='';
function showTab(n){document.getElementById("tab1").style.display=n==1?"block":"none";document.getElementById("tab2").style.display=n==2?"block":"none";document.getElementById("tab3").style.display=n==3?"block":"none";document.getElementById("t1").className=n==1?"tab active":"tab";document.getElementById("t2").className=n==2?"tab active":"tab";document.getElementById("t3").className=n==3?"tab active":"tab";}
function clearFilter(){currentFilter='all';searchTerm='';document.getElementById("searchInput").value='';document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive');});renderMatches();document.querySelectorAll('.fbtn').forEach(function(b){b.className='fbtn';});document.getElementById('fb-all').className='fbtnA fbtn';}
function filterMatches(lg){currentFilter=lg;document.querySelectorAll('.box').forEach(function(b){b.classList.remove('boxActive');});if(lg!='all'&&lg!='live'){var kk=safeId(lg);var box=document.getElementById('box-'+kk);if(box)box.classList.add('boxActive');}renderMatches();}
function doSearch(){searchTerm=document.getElementById("searchInput").value.toLowerCase();renderMatches();}
function renderMatches(){
 var list=[];if(currentFilter=='live')list=allLive;else if(currentFilter=='all')list=allLive.concat(allUp);else list=allLive.concat(allUp).filter(function(m){return m.league==currentFilter;});
 if(searchTerm)list=list.filter(function(m){return (m.home+m.away).toLowerCase().indexOf(searchTerm)!=-1;});
 var html='';if(allLive.length>0&& (currentFilter=='all'||currentFilter=='live')){var liveList=currentFilter=='live'?list:list.filter(function(m){return m.isLive;});if(liveList.length>0){html+='<div style="background:#300;padding:8px;text-align:center;color:#ff4444;font-weight:900">Live '+liveList.length+'</div>';html+=liveList.map(function(m){return '<div class="card live-card"><img class="team-logo" src="'+m.homeLogo+'" onerror="this.style.display=\\'none\\'"><div style="flex:1"><b>'+m.home+' vs '+m.away+'</b><br><span style="color:#FFD700">'+m.score+'</span> '+m.league+'</div><img class="team-logo" src="'+m.awayLogo+'" onerror="this.style.display=\\'none\\'"></div>';}).join('');}}
 var upList=list.filter(function(m){return!m.isLive;});if(currentFilter!='live'){if(currentFilter!='all')html+='<div style="text-align:center;color:#FFD700;padding:8px">'+currentFilter+' - '+upList.length+' مباراة</div>';html+=upList.slice(0,80).map(function(m){return '<div class="card"><img class="team-logo" src="'+m.homeLogo+'" onerror="this.style.display=\\'none\\'"><div style="flex:1"><b>'+m.home+' <span class="vs">vs</span> '+m.away+'</b><br><small>'+m.date+' | '+m.league+'</small></div><img class="team-logo" src="'+m.awayLogo+'" onerror="this.style.display=\\'none\\'"></div>';}).join('');}
 if(list.length==0)html='<div style="text-align:center;padding:30px;color:#888">لا يوجد</div>';document.getElementById("matches").innerHTML=html;
}
async function fetchLeague(lg){
 var tries=0;while(tries<2){try{var r=await fetch("/api/league30/"+lg);var d=await r.json();var tot=d.up.length+d.live.length;var kk=safeId(lg);var el=document.getElementById("cnt-"+kk);if(tot>0){if(el)el.innerText=tot+" games";document.getElementById("box-"+kk).className="box has";activeLeagues++;}else{if(el)el.innerText=d.msg||"0";document.getElementById("box-"+kk).className="box zero";}allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("tc").innerText=allUp.length+allLive.length;document.getElementById("s1").innerText=allLive.length;document.getElementById("s2").innerText=allUp.length;document.getElementById("s4").innerText=activeLeagues+"/18";document.getElementById("s5").innerText=allUp.length+allLive.length;break;}catch(e){tries++;await new Promise(function(res){setTimeout(res,500);});}}
 done++;document.getElementById("dn").innerText=done+"/18";document.getElementById("st").innerText=done==18?"خلص! "+(allUp.length+allLive.length)+" مباراة - اضغط على الدوري":"Done "+done+"/18";if(done%4==0||done==18)renderMatches();
}
async function loadStanding(lg){showTab(2);document.getElementById("standing-box").innerHTML="يحمل "+lg+"...";try{var r=await fetch("/api/standing/"+lg);var d=await r.json();var html='<h3 style="color:#FFD700">ترتيب '+lg+'</h3><table style="width:100%;border-collapse:collapse;font-size:13px"><tr style="background:#FFD700;color:#000"><th style="padding:10px">#</th><th>الفريق</th><th>نقاط</th></tr>';d.standing.forEach(function(t){html+='<tr style="border-bottom:1px solid #333"><td style="padding:10px;text-align:center">'+t.pos+'</td><td style="padding:10px"><b>'+t.team+'</b></td><td style="text-align:center"><b style="color:#FFD700">'+t.points+'</b></td></tr>';});html+='</table>';document.getElementById("standing-box").innerHTML=html;}catch(e){document.getElementById("standing-box").innerHTML="لا يوجد";}}
async function loadAll(){var keys=Object.keys(L);for(var i=0;i<keys.length;i+=4){var chunk=keys.slice(i,i+4);await Promise.all(chunk.map(function(k){return fetchLeague(k);}));await new Promise(function(r){setTimeout(r,400);});}}loadAll();
</script></body></html>
    '''

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
                base={"home":c0['team']['displayName'],"away":c1['team']['displayName'],"homeLogo":c0['team'].get('logo',''),"awayLogo":c1['team'].get('logo',''),"league":lg,"date":d,"isLive":comp['status']['type']['state']=='in',"score":f"{c0.get('score','0')}-{c1.get('score','0')}"}
                if base["isLive"]: live.append(base)
                else: up.append(base)
            if len(up)>=8: break
        except: continue
    msg="موسم منتهي" if len(up)==0 and len(live)==0 and lg in ['sau.1','egy.1'] else "0"
    return jsonify({"live":live,"up":up[:8],"msg":msg})

@app.route('/api/standing/<lg>')
def api_standing(lg
