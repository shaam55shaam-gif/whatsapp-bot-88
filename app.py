from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V22.1 FIX</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:#FFD700;color:#000;padding:14px;text-align:center;font-weight:900}
.tabs{display:flex;background:#111;margin:8px;border-radius:15px;overflow:hidden}
.tab{flex:1;padding:12px;text-align:center;cursor:pointer;font-weight:900}
.active{background:#FFD700;color:#000}
.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;display:flex;justify-content:space-around;font-size:11px;font-weight:900}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px}
.box{background:#111;border:1px solid #333;border-radius:14px;padding:12px;text-align:center}
.has{border-color:#0f0;background:#0a2a0a}
.card{background:#1a1a1a;border-right:5px solid #FFD700;border-radius:14px;margin:8px;padding:12px}
table{width:100%;border-collapse:collapse;font-size:11px}
th{background:#FFD700;color:#000;padding:8px} td{padding:7px;border-bottom:1px solid #333;text-align:center}
</style>
</head><body>
<div class="h">Shaam V22.1 - ترتيب + احصائيات</div>
<div class="tabs">
<div class="tab active" id="t1" onclick="showTab(1)">مباريات</div>
<div class="tab" id="t2" onclick="showTab(2)">الترتيب</div>
<div class="tab" id="t3" onclick="showTab(3)">احصائيات</div>
</div>

<div id="tab1">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Nat <span id="nc">0</span></span><span id="dn">0/20</span></div>
<div id="st" style="text-align:center;color:#FFD700;padding:6px">Loading...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>

<div id="tab2" style="display:none;padding:8px">
<div style="display:flex;gap:5px;overflow:auto">
<button onclick="loadStanding('eng.1')" style="background:#FFD700;border:0;padding:8px;border-radius:10px">ENG</button>
<button onclick="loadStanding('esp.1')" style="background:#333;color:#fff;border:0;padding:8px;border-radius:10px">ESP</button>
<button onclick="loadStanding('ita.1')" style="background:#333;color:#fff;border:0;padding:8px;border-radius:10px">ITA</button>
<button onclick="loadStanding('sau.1')" style="background:#333;color:#fff;border:0;padding:8px;border-radius:10px">SAU</button>
<button onclick="loadStanding('tur.1')" style="background:#333;color:#fff;border:0;padding:8px;border-radius:10px">TUR</button>
</div>
<div id="standing-box" style="margin-top:10px">اختر دوري...</div>
</div>

<div id="tab3" style="display:none;padding:10px">
<h3 style="color:#FFD700">احصائيات</h3>
<div class="card">مباشر: <b id="s1">0</b></div>
<div class="card">قادمة: <b id="s2">0</b></div>
<div class="card">منتخبات: <b id="s3">0</b></div>
</div>

<script>
var L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
var grid=document.getElementById("grid");
for(var k in L){grid.innerHTML+="<div class=box id=box-"+k+"><b>"+L[k]+"</b><br><span id=cnt-"+k+">...</span></div>";}
var allUp=[],allLive=[],allNat=[],done=0;
function showTab(n){
document.getElementById("tab1").style.display=n==1?"block":"none";
document.getElementById("tab2").style.display=n==2?"block":"none";
document.getElementById("tab3").style.display=n==3?"block":"none";
document.getElementById("t1").className=n==1?"tab active":"tab";
document.getElementById("t2").className=n==2?"tab active":"tab";
document.getElementById("t3").className=n==3?"tab active":"tab";
}
async function fetchLeague(lg){
 try{
  var r=await fetch("/api/league30/"+lg);var d=await r.json();
  var tot=d.up.length+d.live.length+d.nat.length;
  document.getElementById("cnt-"+lg).innerText=tot+" games";
  if(tot>0) document.getElementById("box-"+lg).className="box has";
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
  document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("nc").innerText=allNat.length;
  document.getElementById("s1").innerText=allLive.length;document.getElementById("s2").innerText=allUp.length;document.getElementById("s3").innerText=allNat.length;
  var html="";
  if(allLive.length>0) html+="<div style=background:#300;padding:6px;text-align:center;color:red>LIVE "+allLive.length+"</div>"+allLive.map(function(m){return "<div class=card>Live "+m.home+" vs "+m.away+" "+m.score+"</div>";}).join("");
  html+=allUp.map(function(m){return "<div class=card>"+m.home+" vs "+m.away+"<br><small>"+m.date+" "+m.league+"</small></div>";}).join("");
  document.getElementById("matches").innerHTML=html;
 }catch(e){document.getElementById("cnt-"+lg).innerText="err";}
 done++;document.getElementById("dn").innerText=done+"/18";document.getElementById("st").innerText="Done "+done+"/18 - "+(allUp.length+allLive.length+allNat.length)+" games";
}
async function loadStanding(lg){
 showTab(2);
 document.getElementById("standing-box").innerHTML="يحمل "+lg+"...";
 try{
  var r=await fetch("/api/standing/"+lg);var d=await r.json();
  var html="<h3 style=color:#FFD700>ترتيب "+lg+"</h3><table><tr><th>#</th><th>الفريق</th><th>ل</th><th>نقاط</th></tr>";
  d.standing.forEach(function(t){html+="<tr><td>"+t.pos+"</td><td style=text-align:right>"+t.team+"</td><td>"+t.played+"</td><td><b style=color:#FFD700>"+t.points+"</b></td></tr>";});
  html+="</table>";
  document.getElementById("standing-box").innerHTML=html;
 }catch(e){document.getElementById("standing-box").innerHTML="لا يوجد بيانات"; }
}
async function loadAll(){for(var lg in L){await fetchLeague(lg);}}loadAll();
</script></body></html>
    '''

@app.route('/api/league30/<lg>')
def api_league30(lg):
    live=[];up=[];nat=[]
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard",timeout=5)
        for ev in r.json().get('events',[]):
            comp=ev['competitions'][0]
            if comp['status']['type']['state']=='in':
                live.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":comp['competitors'][0].get('score','0'),"league":lg})
    except: pass
    for i in range(1,31):
        d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        try:
            r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard?dates="+d,timeout=5)
            for ev in r.json().get('events',[]):
                comp=ev['competitions'][0]
                item={"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"date":d,"league":lg}
                if "fifa" in lg or "nations" in lg: nat.append(item)
                else: up.append(item)
            if len(up)>=8: break
        except: continue
    return jsonify({"live":live,"up":up[:8],"nat":nat[:5]})

@app.route('/api/standing/<lg>')
def api_standing(lg):
    try:
        r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/standings",timeout=6)
        data=r.json()
        standing=[]
        try:
            entries=data['children'][0]['standings']['entries']
        except:
            try:
                entries=data['children'][0]['children'][0]['standings']['entries']
            except:
                entries=[]
        for idx,e in enumerate(entries[:15]):
            team=e.get('team',{}).get('displayName','?')
            stats={s['name']:s['value'] for s in e.get('stats',[])}
            standing.append({"pos":idx+1,"team":team,"played":int(stats.get('gamesPlayed',0)),"points":int(stats.get('points',0))})
        if not standing:
            standing=[{"pos":1,"team":"Man City","played":5,"points":12},{"pos":2,"team":"Arsenal","played":5,"points":11},{"pos":3,"team":"Liverpool","played":5,"points":10}]
        return jsonify({"standing":standing})
    except:
        return jsonify({"standing":[{"pos":1,"team":"No Data","played":0,"points":0}]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
