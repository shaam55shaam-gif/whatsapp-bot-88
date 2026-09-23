from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

HTML = '''
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V20 ULTIMATE</title>
<style>body{background:#000;color:#fff;font-family:Arial;margin:0}.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:12px;text-align:center;font-weight:900;font-size:14px}.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;text-align:center;font-weight:900;display:flex;justify-content:space-around;font-size:11px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.box{background:#111;border:1px solid #333;border-radius:12px;padding:10px;text-align:center;font-size:10px}.box.has{background:#0a2a0a;border-color:#00ff00;box-shadow:0 0 8px #00ff00}.box.zero{background:#1a1a1a;opacity:.6}.card{background:#1a1a1a;border-right:4px solid #FFD700;border-radius:12px;margin:7px;padding:10px;font-size:12px}.live{border-right-color:red}</style>
</head><body><div class="h">Shaam V20 ULTIMATE - 23 دوري - 30 يوم بحث - كل الدوريات</div>
<div class="money"><span>Live <span id="liveC">0</span></span><span>Up <span id="upC">0</span></span><span>Nat <span id="natC">0</span></span><span id="done">0/23</span></div>
<div id="status" style="text-align:center;color:#FFD700;font-size:11px;padding:5px">يبحث 30 يوم - ليشوف الأوروبي بعد التوقف الدولي...</div>
<div class="grid" id="grid"></div><div id="matches" style="padding:5px"></div>
<script>
const L={"eng.1":"ENG انكليزي","esp.1":"ESP اسباني","ita.1":"ITA ايطالي","ger.1":"GER الماني","fra.1":"FRA فرنسي","tur.1":"TUR تركي","sau.1":"SAU سعودي","egy.1":"EGY مصري","uefa.champions":"UCL ابطال","uefa.europa":"UEL اوروبا","por.1":"POR برتغالي","ned.1":"NED هولندي","bel.1":"BEL بلجيكي","usa.1":"USA امريكي","bra.1":"BRA برازيلي","arg.1":"ARG ارجنتيني","mex.1":"MEX مكسيكي","fifa.friendly":"FRIENDLY وديه","uefa.nations":"NATIONS امم","fifa.world.qual":"QUAL تصفيات"};
let grid=document.getElementById("grid");for(let k in L){grid.innerHTML+="<div class=box id=box-"+k+"><b>"+L[k]+"</b><br><small>"+k+"</small><br><span id=cnt-"+k+">...</span></div>";}
let allUp=[],allLive=[],allNat=[],done=0;
async function fetchLeague(lg){
 try{
  let r=await fetch("/api/league30/"+lg);let d=await r.json();
  let tot=d.up.length+d.live.length+d.nat.length;
  document.getElementById("cnt-"+lg).innerText=tot>0?tot+" مباريات":"0 - توقف دولي";
  document.getElementById("box-"+lg).className=tot>0?"box has":"box zero";
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
  document.getElementById("liveC").innerText=allLive.length;document.getElementById("upC").innerText=allUp.length;document.getElementById("natC").innerText=allNat.length;
  let html="";
  if(allLive.length>0) html+="<div style=background:#300;padding:6px;text-align:center;color:red>Live "+allLive.length+"</div>"+allLive.map(function(m){return "<div class=card style=border-right-color:red>Live "+m.home+" vs "+m.away+" "+m.score+"</div>";}).join("");
  html+="<div style=background:#222;padding:6px;text-align:center;color:#FFD700>القادمة 30 يوم - "+allUp.length+" مباراة</div>"+allUp.map(function(m){return "<div class=card>"+m.home+" vs "+m.away+"<br><small>"+m.date+" - "+m.league+" حقيقي</small></div>";}).join("");
  if(allNat.length>0) html+="<div style=background:#002233;padding:6px;text-align:center;color:#00bfff>منتخبات "+allNat.length+"</div>"+allNat.map(function(m){return "<div class=card style=border-right-color:#00bfff>"+m.home+" vs "+m.away+"<br><small>"+m.date+"</small></div>";}).join("");
  document.getElementById("matches").innerHTML=html;
 }catch(e){document.getElementById("cnt-"+lg).innerText="err";}
 done++;document.getElementById("done").innerText=done+"/20";document.getElementById("status").innerText="خلص "+done+"/20 - المجموع "+(allUp.length+allLive.length+allNat.length)+" مباراة حقيقية";
}
async function loadAll(){for(let lg in L){await fetchLeague(lg);}}loadAll();
</script></body></html>
'''

@app.route('/')
def home(): return HTML

@app.route('/api/league30/<lg>')
def api_league30(lg):
    live=[];up=[];nat=[]
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard",timeout=5)
        for ev in r.json().get('events',[]):
            comp=ev['competitions'][0]
            if comp['status']['type']['state']=='in':
                live.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":comp['competitors'][0].get('score','0')+"-"+comp['competitors'][1].get('score','0'),"league":lg})
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

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
