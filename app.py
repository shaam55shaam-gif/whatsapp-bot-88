from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

HTML = '''
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V19.1 FIX</title>
<style>body{background:#000;color:#fff;font-family:Arial;margin:0}.h{background:#FFD700;color:#000;padding:12px;text-align:center;font-weight:900}.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;text-align:center;font-weight:900;display:flex;justify-content:space-around;font-size:11px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;padding:5px}.box{background:#111;border:1px solid #333;border-radius:10px;padding:8px;text-align:center;font-size:10px}.box.has{background:#1a2e1a;border-color:#0f0}.card{background:#1a1a1a;border-right:4px solid #FFD700;border-radius:12px;margin:6px;padding:9px;font-size:12px}</style>
</head><body><div class="h">Shaam V19.1 FIX - 23 دوري - 14 يوم</div>
<div class="money"><span>Live <span id="liveC">0</span></span><span>Up <span id="upC">0</span></span><span>Nat <span id="natC">0</span></span><span id="done">0/23</span></div>
<div id="status" style="text-align:center;color:#FFD700;font-size:11px">Loading 14 days...</div>
<div class="grid" id="grid"></div><div id="matches" style="padding:5px"></div>
<script>
const L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","bel.1":"BEL","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS","fifa.world.qual":"QUAL"};
let grid=document.getElementById("grid");for(let k in L){grid.innerHTML+="<div class=box id=box-"+k+"><b>"+L[k]+"</b><br><small>"+k+"</small><br><span id=cnt-"+k+">...</span></div>";}
let allUp=[],allLive=[],allNat=[],done=0;
async function fetchLeague(lg){
 try{
  let r=await fetch("/api/league14/"+lg);let d=await r.json();
  let tot=d.up.length+d.live.length+d.nat.length;
  document.getElementById("cnt-"+lg).innerText=tot>0?tot+" games":"0";
  if(tot>0) document.getElementById("box-"+lg).classList.add("has");
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
  document.getElementById("liveC").innerText=allLive.length;document.getElementById("upC").innerText=allUp.length;document.getElementById("natC").innerText=allNat.length;
  let html="";
  if(allLive.length>0) html+="<b style=color:red>LIVE "+allLive.length+"</b>"+allLive.map(function(m){return "<div class=card>Live "+m.home+" vs "+m.away+" "+m.score+"</div>";}).join("");
  html+=allUp.map(function(m){return "<div class=card>"+m.home+" vs "+m.away+" - "+m.date+" "+m.league+"</div>";}).join("");
  if(allNat.length>0) html+="<b style=color:#0bf>National "+allNat.length+"</b>"+allNat.map(function(m){return "<div class=card>Nat "+m.home+" vs "+m.away+"</div>";}).join("");
  document.getElementById("matches").innerHTML=html;
 }catch(e){document.getElementById("cnt-"+lg).innerText="err";}
 done++;document.getElementById("done").innerText=done+"/23";document.getElementById("status").innerText="Done "+done+"/23 - "+(allUp.length+allLive.length+allNat.length)+" games";
}
async function loadAll(){for(let lg in L){await fetchLeague(lg);}}loadAll();
</script></body></html>
'''

@app.route('/')
def home():
    return HTML

@app.route('/api/league14/<lg>')
def api_league14(lg):
    live=[];up=[];nat=[]
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard",timeout=4)
        for ev in r.json().get('events',[]):
            comp=ev['competitions'][0]
            if comp['status']['type']['state']=='in':
                live.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":comp['competitors'][0].get('score','0')+"-"+comp['competitors'][1].get('score','0'),"league":lg})
    except:
        pass
    for i in range(1,15):
        d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        try:
            r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard?dates="+d,timeout=4)
            for ev in r.json().get('events',[]):
                comp=ev['competitions'][0]
                item={"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"date":d,"league":lg}
                if "fifa" in lg or "nations" in lg:
                    nat.append(item)
                else:
                    up.append(item)
            if len(up)>=8:
                break
        except:
            continue
    return jsonify({"live":live,"up":up[:8],"nat":nat[:5]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
