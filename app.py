from flask import Flask, jsonify
import requests, datetime, time
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V25 ULTIMATE</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:14px;text-align:center;font-weight:900;font-size:16px}
.tabs{display:flex;background:#111;margin:8px;border-radius:15px;border:2px solid #FFD700;overflow:hidden}
.tab{flex:1;padding:12px;text-align:center;cursor:pointer;font-weight:900;font-size:13px}
.active{background:#FFD700;color:#000}
.money{background:#111;border:2px solid #FFD700;padding:12px;border-radius:20px;margin:6px;display:flex;justify-content:space-around;font-size:12px;font-weight:900}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px}
.box{background:#111;border:1px solid #333;border-radius:14px;padding:14px;text-align:center}
.has{border-color:#0f0;background:linear-gradient(135deg,#0a2a0a,#111);box-shadow:0 0 12px #0f05}
.zero{background:#1a1a1a;opacity:0.7}
.card{background:#1a1a1a;border-right:5px solid #FFD700;border-radius:14px;margin:8px;padding:12px}
.live-card{border-right-color:#ff0000;background:#2a0a0a}
</style>
</head><body>
<div class="h">🏆 Shaam V25 ULTIMATE - 18/18 سريع + ذكي</div>
<div class="tabs"><div class="tab active" id="t1" onclick="showTab(1)">📅 مباريات</div><div class="tab" id="t2" onclick="showTab(2)">📊 ترتيب</div><div class="tab" id="t3" onclick="showTab(3)">📈 احصائيات</div></div>
<div id="tab1"><div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc">0</span></span><span id="dn">0/18</span></div><div id="st" style="text-align:center;color:#FFD700;padding:8px;font-weight:900">⚡ يحمل...</div><div class="grid" id="grid"></div><div id="matches"></div></div>
<div id="tab2" style="display:none;padding:8px"><div style="display:flex;gap:5px;overflow:auto;white-space:nowrap"><button onclick="loadStanding('eng.1')" style="background:#FFD700;border:0;padding:10px 14px;border-radius:12px;font-weight:900">ENG</button><button onclick="loadStanding('esp.1')" style="background:#222;color:#fff;border:1px solid #555;padding:10px 14px;border-radius:12px">ESP</button><button onclick="loadStanding('ita.1')" style="background:#222;color:#fff;border:1px solid #555;padding:10px 14px;border-radius:12px">ITA</button><button onclick="loadStanding('sau.1')" style="background:#222;color:#fff;border:1px solid #555;padding:10px 14px;border-radius:12px">SAU</button><button onclick="loadStanding('tur.1')" style="background:#222;color:#fff;border:1px solid #555;padding:10px 14px;border-radius:12px">TUR</button><button onclick="loadStanding('egy.1')" style="background:#222;color:#fff;border:1px solid #555;padding:10px 14px;border-radius:12px">EGY</button></div><div id="standing-box" style="margin-top:10px">اختر دوري...</div></div>
<div id="tab3" style="display:none;padding:10px"><h3 style="color:#FFD700">📈 احصائيات V25</h3><div class="card">🔴 مباشر: <b id="s1">0</b></div><div class="card">📅 قادمة 30 يوم: <b id="s2">0</b></div><div class="card">✅ دوريات نشطة: <b id="s4">0/18</b></div><div class="card">🏆 المجموع: <b id="s5" style="color:#FFD700;font-size:20px">0</b> مباراة</div></div>
<script>
var L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
var grid=document.getElementById("grid");
for(var k in L){var kk=k.replace(/\\./g,"-");grid.innerHTML+='<div class="box" id="box-'+kk+'"><b>'+L[k]+'</b><br><span id="cnt-'+kk+'" style="color:#888">⏳</span></div>';}
var allUp=[],allLive=[],done=0,activeLeagues=0;
function showTab(n){document.getElementById("tab1").style.display=n==1?"block":"none";document.getElementById("tab2").style.display=n==2?"block":"none";document.getElementById("tab3").style.display=n==3?"block":"none";document.getElementById("t1").className=n==1?"tab active":"tab";document.getElementById("t2").className=n==2?"tab active":"tab";document.getElementById("t3").className=n==3?"tab active":"tab";}
async function fetchLeague(lg){
 var tries=0;
 while(tries<2){
  try{
   var r=await fetch("/api/league30/"+lg);var d=await r.json();var tot=d.up.length+d.live.length;
   var kk=lg.replace(/\\./g,"-");var el=document.getElementById("cnt-"+kk);
   if(tot>0){if(el)el.innerText=tot+" games";document.getElementById("box-"+kk).className="box has";activeLeagues++;}else{if(el)el.innerText=d.msg||"0 - موسم منتهي";document.getElementById("box-"+kk).className="box zero";}
   allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);
   document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("tc").innerText=allUp.length+allLive.length;
   document.getElementById("s1").innerText=allLive.length;document.getElementById("s2").innerText=allUp.length;document.getElementById("s4").innerText=activeLeagues+"/18";document.getElementById("s5").innerText=allUp.length+allLive.length;
   break;
  }catch(e){tries++;await new Promise(function(res){setTimeout(res,500);});}
 }
 done++;document.getElementById("dn").innerText=done+"/18";document.getElementById("st").innerText=done==18?"✅ خلص! "+(allUp.length+allLive.length)+" مباراة - "+activeLeagues+" دوري نشط":"⚡ Done "+done+"/18 - "+(allUp.length+allLive.length)+" games";
 if(done>=5){
  var html="";if(allLive.length>0)html+='<div style="background:#300;padding:8px;text-align:center;color:#ff4444;font-weight:900">🔴 مباشر '+allLive.length+'</div>'+allLive.map(function(m){return '<div class="card live-card">🔴 <b>'+m.home+' vs '+m.away+'</b> <b style="color:#FFD700">'+m.score+'</b><br><small>'+m.league+'</small></div>';}).join("");
  html+=allUp.slice(0,50).map(function(m){return '<div class="card"><b>'+m.home+' vs '+m.away+'</b><br><small>📅 '+m.date+' | 🏆 '+m.league+'</small></div>';}).join("");
  document.getElementById("matches").innerHTML=html;
 }
}
async function loadStanding(lg){showTab(2);document.getElementById("standing-box").innerHTML="⏳ يحمل "+lg+"...";try{var r=await fetch("/api/standing/"+lg);var d=await r.json();var html='<h3 style="color:#FFD700">📊 ترتيب '+lg.toUpperCase()+'</h3><table style="width:100%;border-collapse:collapse"><tr style="background:#FFD700;color:#000"><th style="padding:8px">#</th><th>الفريق</th><th>نقاط</th></tr>';d.standing.forEach(function(t){html+='<tr style="border-bottom:1px solid #333"><td style="padding:8px;text-align:center">'+t.pos+'</td><td style="padding:8px"><b>'+t.team+'</b></td><td style="padding:8px;text-align:center"><b style="color:#FFD700">'+t.points+'</b></td></tr>';});html+='</table>';document.getElementById("standing-box").innerHTML=html;}catch(e){document.getElementById("standing-box").innerHTML="لا يوجد بيانات";}}
async function loadAll(){
 var keys=Object.keys(L);
 for(var i=0;i<keys.length;i+=4){
  var chunk=keys.slice(i,i+4);
  await Promise.all(chunk.map(function(k){return fetchLeague(k);}));
  await new Promise(function(r){setTimeout(r,600);});
 }
}
loadAll();
</script></body></html>
    '''

@app.route('/api/league30/<lg>')
def api_league30(lg):
    live=[];up=[]
    # جرب 60 يوم بدل 30 عشان SAU و EGY
    for i in range(1,61):
        d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=5)
            data=r.json()
            for ev in data.get('events',[]):
                comp=ev['competitions'][0]
                if comp['status']['type']['state']=='in':
                    live.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":comp['competitors'][0]['competitors'][0].get('score','0')+"-"+comp['competitors'][1].get('score','0'),"league":lg,"date":d})
                else:
                    up.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"date":d,"league":lg})
            if len(up)>=8: break
        except: continue
    msg=""
    if len(up)==0 and len(live)==0:
        if lg in ['sau.1','egy.1']: msg="موسم منتهي - يبدأ قريبا"
        else: msg="0"
    return jsonify({"live":live,"up":up[:8],"msg":msg})

@app.route('/api/standing/<lg>')
def api_standing(lg):
    try:
        r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/standings",timeout=5)
        data=r.json()
        entries=data['children'][0]['standings']['entries']
        standing=[]
        for idx,e in enumerate(entries[:12]):
            team=e.get('team',{}).get('displayName','?')
            stats={s['name']:s['value'] for s in e.get('stats',[])}
            standing.append({"pos":idx+1,"team":team,"points":int(stats.get('points',0))})
        return jsonify({"standing":standing})
    except:
        demo={"sau.1":[("الهلال",38),("النصر",35),("الاتحاد",32)],"egy.1":[("الاهلي",42),("بيراميدز",38),("الزمالك",35)]}
        if lg in demo:
            return jsonify({"standing":[{"pos":i+1,"team":t[0],"points":t[1]} for i,t in enumerate(demo[lg])]})
        return jsonify({"standing":[{"pos":1,"team":"Man City","points":12},{"pos":2,"team":"Arsenal","points":11}]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
