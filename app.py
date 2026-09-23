from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam FINAL</title>
<style>body{background:#000;color:#fff;font-family:Arial;margin:0}.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:14px;text-align:center;font-weight:900;font-size:16px}.money{background:#111;border:2px solid #FFD700;padding:12px;border-radius:25px;margin:8px;display:flex;justify-content:space-around;font-weight:900}.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px}.box{background:#111;border:1px solid #333;border-radius:14px;padding:12px;text-align:center;transition:.3s}.has{border-color:#00ff00;background:linear-gradient(135deg,#0a2a0a,#111);box-shadow:0 0 15px #00ff0055}.card{background:#1a1a1a;border-right:5px solid #FFD700;border-radius:14px;margin:8px;padding:12px}</style>
</head><body><div class="h">🌍 شامي FINAL - 23 دوري - 30 يوم - كل الدوريات ✅</div>
<div class="money"><span>🔴 <span id="lc">0</span> مباشر</span><span>📅 <span id="uc">0</span> قادمة</span><span>🌍 <span id="nc">0</span> منتخبات</span><span id="dn">0/20</span></div>
<div id="st" style="text-align:center;color:#FFD700;padding:6px">⏳ يجيب كل الدوريات...</div>
<div class="grid" id="grid"></div><div id="matches"></div>
<script>
var L={ "eng.1":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 انكليزي","esp.1":"🇪🇸 اسباني","ita.1":"🇮🇹 ايطالي","ger.1":"🇩🇪 الماني","fra.1":"🇫🇷 فرنسي","tur.1":"🇹🇷 تركي","sau.1":"🇸🇦 سعودي","egy.1":"🇪🇬 مصري","uefa.champions":"🏆 ابطال","uefa.europa":"🏆 اوروبا","por.1":"🇵🇹 برتغالي","ned.1":"🇳🇱 هولندي","bel.1":"🇧🇪 بلجيكي","usa.1":"🇺🇸 امريكي","bra.1":"🇧🇷 برازيلي","arg.1":"🇦🇷 ارجنتيني","mex.1":"🇲🇽 مكسيكي","fifa.friendly":"🌍 وديه","uefa.nations":"🏆 امم","fifa.world.qual":"🌍 تصفيات"};
var grid=document.getElementById("grid");
for(var k in L){grid.innerHTML+="<div class=box id=box-"+k+"><b>"+L[k]+"</b><br><span id=cnt-"+k+">⏳</span></div>";}
var allUp=[],allLive=[],allNat=[],done=0;
async function fetchLeague(lg){
 try{
  var r=await fetch("/api/league30/"+lg);var d=await r.json();
  var tot=d.up.length+d.live.length+d.nat.length;
  document.getElementById("cnt-"+lg).innerText=tot>0?tot+" مباريات":"0";
  if(tot>0) document.getElementById("box-"+lg).className="box has";
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
  document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("nc").innerText=allNat.length;
  var html="";
  if(allLive.length>0) html+="<div style=background:#300;padding:8px;text-align:center;color:red;font-weight:900>🔴 مباشر الان "+allLive.length+"</div>"+allLive.map(function(m){return "<div class=card style=border-right-color:red>🔴 "+m.home+" vs "+m.away+" <b style=color:#FFD700>"+m.score+"</b></div>";}).join("");
  html+=allUp.map(function(m){return "<div class=card><b>"+m.home+" vs "+m.away+"</b><br><small>📅 "+m.date+" | "+m.league+" ✅</small></div>";}).join("");
  if(allNat.length>0) html+="<div style=background:#002233;padding:8px;text-align:center;color:#0bf>🌍 منتخبات "+allNat.length+"</div>"+allNat.map(function(m){return "<div class=card style=border-right-color:#0bf>🌍 "+m.home+" vs "+m.away+"</div>";}).join("");
  document.getElementById("matches").innerHTML=html;
 }catch(e){document.getElementById("cnt-"+lg).innerText="...";}
 done++;document.getElementById("dn").innerText=done+"/20";document.getElementById("st").innerText="✅ خلص "+done+"/20 - المجموع "+(allUp.length+allLive.length+allNat.length)+" مباراة حقيقية";
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
