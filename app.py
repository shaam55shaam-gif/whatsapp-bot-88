from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shaam V30</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:#FFD700;color:#000;padding:10px;text-align:center;font-weight:900}
.tabs{display:flex;background:#111;margin:6px;border-radius:12px;border:2px solid gold;overflow:hidden}
.tab{flex:1;padding:10px;text-align:center;font-weight:900;cursor:pointer}
.active{background:gold;color:#000}
.info{background:#111;border:1px solid gold;margin:6px;padding:8px;border-radius:10px;display:flex;justify-content:space-around;font-weight:900;font-size:12px}
.filters{display:flex;gap:5px;padding:6px;overflow:auto}
.btn{background:#222;color:#fff;border:1px solid #555;padding:6px 12px;border-radius:15px;white-space:nowrap}
.btnA{background:gold;color:#000}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:#111;border:1px solid #333;border-radius:10px;padding:10px;text-align:center}
.has{border-color:#0f0;background:#0a1a0a}
.zero{opacity:0.4}
.boxSel{border:2px solid gold!important;background:gold!important;color:#000!important}
.card{background:#151515;border-right:4px solid gold;margin:6px;padding:10px;border-radius:10px;display:flex;align-items:center;gap:8px;cursor:pointer}
.cardFav{border-color:gold;background:#1a1a00}
.vs{color:gold;font-weight:900}
.srch{margin:6px;background:#111;border:1px solid #333;border-radius:8px;padding:8px;display:flex;gap:6px}
.srch input{flex:1;background:0;border:0;color:#fff;outline:0}
</style>
</head><body>
<div class="h">Shaam V30 - ⭐ المفضلة + 90 يوم</div>
<div class="tabs"><div class="tab active" id="tb1" onclick="tab(1)">مباريات</div><div class="tab" id="tb2" onclick="tab(2)">ترتيب</div><div class="tab" id="tb3" onclick="tab(3)">احصائيات</div></div>
<div id="p1">
<div class="info"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc">0</span></span><span id="dn">0/18</span></div>
<div class="filters">
<button class="btn btnA" id="fAll" onclick="filter('all')">الكل</button>
<button class="btn" onclick="filter('fav')">⭐ مفضلتي</button>
<button class="btn" onclick="filter('live')">Live</button>
<button class="btn" onclick="filter('eng.1')">ENG</button>
<button class="btn" onclick="filter('sau.1')">SAU</button>
<button class="btn" onclick="filter('all');document.getElementById('q').value='';search=''">الغاء</button>
</div>
<div class="srch">🔍<input id="q" placeholder="ابحث Real, Barca..." oninput="doSearch()"></div>
<div id="favBar" style="display:none;background:#1a1a00;border:1px solid gold;margin:6px;padding:6px;border-radius:8px;text-align:center">⭐ <span id="favList"></span> <button onclick="clearFav()" style="background:red;color:#fff;border:0;border-radius:10px;padding:2px 8px">مسح</button></div>
<div id="status" style="text-align:center;color:gold;padding:6px">يحمل...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>
<div id="p2" style="display:none;padding:6px"><button onclick="loadTable('eng.1')" class="btn btnA">ENG</button><button onclick="loadTable('esp.1')" class="btn">ESP</button><button onclick="loadTable('sau.1')" class="btn">SAU</button><div id="tableBox" style="margin-top:8px">اختر دوري</div></div>
<div id="p3" style="display:none;padding:6px"><div class="card">مباشر: <b id="st1">0</b></div><div class="card">قادمة: <b id="st2">0</b></div><div class="card">المجموع: <b id="st3" style="color:gold;font-size:22px">0</b></div></div>
<script>
var LEAGUES={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
function sid(s){return s.replaceAll('.','-')}
var fav=JSON.parse(localStorage.getItem('favTeams')||'[]');
var allUp=[],allLive=[],done=0,curFilter='all',search='';
var grid=document.getElementById('grid');
for(var k in LEAGUES){var id=sid(k);grid.innerHTML+='<div class="box" id="box-'+id+'" onclick="filter(\\''+k+'\\')"><b>'+LEAGUES[k]+'</b><br><small id="cnt-'+id+'">...</small></div>'}
function tab(n){document.getElementById('p1').style.display=n==1?'block':'none';document.getElementById('p2').style.display=n==2?'block':'none';document.getElementById('p3').style.display=n==3?'block':'none';document.getElementById('tb1').className=n==1?'tab active':'tab';document.getElementById('tb2').className=n==2?'tab active':'tab';document.getElementById('tb3').className=n==3?'tab active':'tab'}
function updateFavBar(){if(fav.length>0){document.getElementById('favBar').style.display='block';document.getElementById('favList').innerText=fav.join(', ')}else{document.getElementById('favBar').style.display='none'}}
updateFavBar();
function toggleFav(team){var i=fav.indexOf(team);if(i>=0)fav.splice(i,1);else fav.push(team);localStorage.setItem('favTeams',JSON.stringify(fav));updateFavBar();renderMatches();alert(team+(i>=0?' انحذف':' انضاف ⭐'))}
function clearFav(){fav=[];localStorage.removeItem('favTeams');updateFavBar();renderMatches()}
function filter(f){curFilter=f;document.querySelectorAll('.box').forEach(b=>b.classList.remove('boxSel'));if(LEAGUES[f])document.getElementById('box-'+sid(f)).classList.add('boxSel');renderMatches()}
function doSearch(){search=document.getElementById('q').value.toLowerCase();renderMatches()}
function renderMatches(){
 var list=curFilter=='live'?allLive:curFilter=='all'?allLive.concat(allUp):curFilter=='fav'?allLive.concat(allUp).filter(m=>fav.some(t=>m.home.includes(t)||m.away.includes(t))):allLive.concat(allUp).filter(m=>m.league==curFilter);
 if(search)list=list.filter(m=>(m.home+m.away).toLowerCase().includes(search));
 var html='';
 if(curFilter=='fav'&&fav.length==0)html='<div style="text-align:center;padding:20px">⭐ ما عندك فرق مفضلة<br><small>اضغط على اي مباراة واضف فريق</small></div>';
 else{
  html=list.filter(m=>!m.isLive).slice(0,80).map(m=>{var isFav=fav.some(t=>m.home.includes(t)||m.away.includes(t));return '<div class="card '+(isFav?'cardFav':'')+'" onclick="if(confirm(\\'تضيف '+m.home+' للمفضلة؟\\'))toggleFav(\\''+m.home+'\\')"><div style="flex:1"><b>'+(isFav?'⭐ ':'')+m.home+' <span class=vs>vs</span> '+m.away+'</b><br><small>📅 '+m.date.slice(6,8)+'-'+m.date.slice(4,6)+' | '+m.league+'</small></div></div>'}).join('');
  if(list.length==0)html='<div style="text-align:center;padding:20px;color:#888">لا يوجد مباريات</div>';
 }
 document.getElementById('matches').innerHTML=html;
}
async function fetchLg(lg){
 try{
  var r=await fetch('/api/league30/'+lg);var d=await r.json();
  var tot=d.up.length+d.live.length;var el=document.getElementById('cnt-'+sid(lg));
  if(tot>0){el.innerText=tot+' games';document.getElementById('box-'+sid(lg)).className='box has'}else{el.innerText=d.msg;document.getElementById('box-'+sid(lg)).className='box zero'}
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);
  document.getElementById('lc').innerText=allLive.length;document.getElementById('uc').innerText=allUp.length;document.getElementById('tc').innerText=allUp.length+allLive.length;
  document.getElementById('st1').innerText=allLive.length;document.getElementById('st2').innerText=allUp.length;document.getElementById('st3').innerText=allUp.length+allLive.length;
 }catch(e){}
 done++;document.getElementById('dn').innerText=done+'/18';document.getElementById('status').innerText=done==18?'خلص! '+allUp.length+' مباراة':'يحمل '+done+'/18';
 if(done%3==0||done==18)renderMatches();
}
async function loadTable(lg){tab(2);document.getElementById('tableBox').innerHTML='يحمل...';try{var r=await fetch('/api/standing/'+lg);var d=await r.json();var h='<table style="width:100%;border-collapse:collapse"><tr style="background:gold;color:#000"><th>#</th><th>فريق</th><th>نقاط</th></tr>';d.standing.forEach(s=>{h+='<tr style="border-bottom:1px solid #333"><td style="padding:8px;text-align:center">'+s.pos+'</td><td style="padding:8px">'+s.team+'</td><td style="padding:8px;text-align:center;color:gold">'+s.points+'</td></tr>'});h+='</table>';document.getElementById('tableBox').innerHTML=h}catch(e){document.getElementById('tableBox').innerHTML='لا يوجد'}}
async function loadAll(){var keys=Object.keys(LEAGUES);for(var i=0;i<keys.length;i+=3){await Promise.all(keys.slice(i,i+3).map(k=>fetchLg(k)));await new Promise(r=>setTimeout(r,300))}}loadAll();
</script></body></html>
    """

@app.route('/api/league30/<lg>')
def api_league30(lg):
    up=[];live=[]
    for i in range(1,91):
        d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=4)
            for ev in r.json().get('events',[]):
                comp=ev['competitions'][0]
                c0=comp['competitors'][0];c1=comp['competitors'][1]
                base={"home":c0['team']['displayName'],"away":c1['team']['displayName'],"league":lg,"date":d,"isLive":False}
                up.append(base)
                if len(up)>=8: break
            if len(up)>=8: break
        except: continue
    return jsonify({"live":live,"up":up[:8],"msg": str(len(up)) if up else "موسم منتهي"})

@app.route('/api/standing/<lg>')
def api_standing(lg):
    try:
        r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/standings",timeout=5)
        ent=r.json()['children'][0]['standings']['entries']
        st=[{"pos":i+1,"team":e['team']['displayName'],"points":int({s['name']:s['value'] for s in e['stats']}.get('points',0))} for i,e in enumerate(ent[:12])]
        return jsonify({"standing":st})
    except:
        return jsonify({"standing":[]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
