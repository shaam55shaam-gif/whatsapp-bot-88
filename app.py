from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V20.1</title>
<style>body{background:#000;color:#fff;font-family:Arial;margin:0}.h{background:#FFD700;color:#000;padding:12px;text-align:center;font-weight:900}.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;display:flex;justify-content:space-around;font-size:11px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.box{background:#111;border:1px solid #333;border-radius:12px;padding:10px;text-align:center;font-size:10px}.has{border-color:#0f0;background:#0a2a0a}.card{background:#1a1a1a;border-right:4px solid #FFD700;border-radius:12px;margin:7px;padding:10px;font-size:12px}</style>
</head><body><div class="h">Shaam V20.1 - 23 دوري - 30 يوم</div>
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Nat <span id="nc">0</span></span><span id="dn">0/20</span></div>
<div id="st" style="text-align:center;color:#FFD700;font-size:11px;padding:5px">Loading 30 days...</div>
<div class="grid" id="grid"></div><div id="matches"></div>
<script>
var L={ "eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","bel.1":"BEL","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS","fifa.world.qual":"QUAL"};
var grid=document.getElementById("grid");
for(var k in L){grid.innerHTML+="<div class=box id=box-"+k+"><b>"+L[k]+"</b><br><span id=cnt-"+k+">...</span></div>";}
var allUp=[],allLive=[],allNat=[],done=0;
async function fetchLeague(lg){
 try{
  var r=await fetch("/api/league30/"+lg);var d=await r.json();
  var tot=d.up.length+d.live.length+d.nat.length;
  document.getElementById("cnt-"+lg).innerText=tot+" games";
  if(tot>0) document.getElementById("box-"+lg).className="box has";
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
  document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("nc").innerText=allNat.length;
  var html="";
  if(allLive.length>0) html+="<b style=color:red>LIVE</b>"+allLive.map(function(m){return "<div class=card>"+m.home+" vs "+m.away+" "+m.score+"</div>";}).join("");
  html+=allUp.map(function(m){return "<div class=card>"+m.home+" vs "+m.away+"<br><small>"+m.date+" "+m.league+"</small></div>";}).join("");
  if(allNat.length>0) html+="<b style=color:#0bf>National</b>"+allNat.map(function(m){return "<div class=card>"+m.home+" vs "+m.away+"</div>";}).join("");
  document.getElementById("matches").innerHTML=html;
 }catch(e){document.getElementById("cnt-"+lg).innerText="err";}
 done++;document.getElementById("dn").innerText=done+"/20";document.getElementById("st").innerText="Done "+done+"/20 - "+(allUp.length+allLive.length+allNat.length)+" games";
}
async function loadAll(){for(var lg in L){await fetchLeague(lg);}}loadAll();
</script></body></html>
    """

@app.route('/api/league30/<lg>')
def api_league30(lg):
    live=[];up=[];nat=[]
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard",timeout=5)
        for ev in r.json().get('events',[]):
            comp=ev['competitions'][0]
            if comp['status']['type']['state']=='in':
                live.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":comp['competitors'][0].get('score','0'),"league":lg})
    except:
        pass
    for i in range(1,31):
        d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        try:
            r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard?dates="+d,timeout=5)
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
