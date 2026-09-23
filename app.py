from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shaam V21 ULTIMATE</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:14px;text-align:center;font-weight:900;font-size:16px}
.money{background:#111;border:2px solid #FFD700;padding:12px;border-radius:25px;margin:8px;text-align:center;font-weight:900;display:flex;justify-content:space-around;font-size:12px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:#111;border:1px solid #333;border-radius:12px;padding:10px;text-align:center;font-size:10px;min-height:55px}
.box.has{background:#0a2a0a;border-color:#00ff00;box-shadow:0 0 10px #0f0}
.box.zero{background:#1a1a1a;opacity:.5}
.card{background:#1a1a1a;border-right:4px solid #FFD700;border-radius:12px;margin:7px;padding:10px;font-size:12px}
.live{border-right-color:red;animation:blink 1s infinite}
@keyframes blink{0%{opacity:1}50%{opacity:.6}100%{opacity:1}}
</style>
</head>
<body>
<div class="h">🌍 Shaam V21 ULTIMATE - 23 دوري - 30 يوم - كل الدوريات الحقيقية</div>
<div class="money"><span>🔴 Live <span id="liveC">0</span></span><span>📅 Up <span id="upC">0</span></span><span>🌍 Nat <span id="natC">0</span></span><span>⏳ <span id="done">0</span>/23</span></div>
<div id="status" style="text-align:center;color:#FFD700;font-size:11px;padding:6px">⏳ يبحث 30 يوم لكل الدوريات...</div>
<div class="grid" id="grid"></div>
<div id="matches" style="padding:6px"></div>
<script>
const L={"eng.1":"ENG انكليزي","esp.1":"ESP اسباني","ita.1":"ITA ايطالي","ger.1":"GER الماني","fra.1":"FRA فرنسي","tur.1":"TUR تركي","sau.1":"SAU سعودي","egy.1":"EGY مصري","uae.1":"UAE اماراتي","qat.1":"QAT قطري","uefa.champions":"UCL ابطال اوروبا","uefa.europa":"UEL الدوري الاوروبي","por.1":"POR برتغالي","ned.1":"NED هولندي","bel.1":"BEL بلجيكي","usa.1":"USA امريكي","bra.1":"BRA برازيلي","arg.1":"ARG ارجنتيني","mex.1":"MEX مكسيكي","fifa.friendly":"FRIENDLY وديه","uefa.nations":"NATIONS دوري الامم","fifa.world.qual":"QUAL تصفيات المونديال","caf.champions":"CAF ابطال افريقيا"};
let grid=document.getElementById("grid");
for(let k in L){
 grid.innerHTML+="<div class=box id=box-"+k+"><b>"+L[k]+"</b><br><small>"+k+"</small><br><span id=cnt-"+k+">⏳</span></div>";
}
let allUp=[],allLive=[],allNat=[],done=0;
async function fetchLeague(lg){
 try{
  let r=await fetch("/api/v21/"+lg);
  let d=await r.json();
  let tot=d.up.length+d.live.length+d.nat.length;
  document.getElementById("cnt-"+lg).innerText=tot>0?tot+" مباريات":"0 - توقف";
  document.getElementById("box-"+lg).className=tot>0?"box has":"box zero";
  allUp=allUp.concat(d.up);
  allLive=allLive.concat(d.live);
  allNat=allNat.concat(d.nat);
  document.getElementById("liveC").innerText=allLive.length;
  document.getElementById("upC").innerText=allUp.length;
  document.getElementById("natC").innerText=allNat.length;
  let html="";
  if(allLive.length>0){
   html+="<div style=background:#300;padding:8px;text-align:center;color:red;font-weight:900>🔴 مباشر الان "+allLive.length+"</div>";
   html+=allLive.map(function(m){return "<div class=card live>🔴 <b>"+m.home+" vs "+m.away+"</b> <b style=color:#FFD700>"+m.score+"</b><br><small>"+m.league+"</small></div>";}).join("");
  }
  html+="<div style=background:#222;padding:8px;text-align:center;color:#FFD700;font-weight:900>📅 القادمة 30 يوم - "+allUp.length+" مباراة حقيقية</div>";
  html+=allUp.map(function(m){return "<div class=card>📅 <b>"+m.home+" vs "+m.away+"</b><br><small>📅 "+m.date+" | "+m.league+" ✅ حقيقي من ESPN</small></div>";}).join("");
  if(allNat.length>0){
   html+="<div style=background:#002233;padding:8px;text-align:center;color:#00bfff;font-weight:900>🌍 منتخبات "+allNat.length+"</div>";
   html+=allNat.map(function(m){return "<div class=card style=border-right-color:#00bfff>🌍 <b>"+m.home+" vs "+m.away+"</b><br><small>"+m.date+" | "+m.league+"</small></div>";}).join("");
  }
  document.getElementById("matches").innerHTML=html||"<div class=card>📭 لا يوجد مباريات</div>";
 }catch(e){
  document.getElementById("cnt-"+lg).innerText="خطأ";
 }
 done++;
 document.getElementById("done").innerText=done+"/23";
 document.getElementById("status").innerText="✅ خلص "+done+"/23 - المجموع "+(allUp.length+allLive.length+allNat.length)+" مباراة حقيقية من ESPN";
}
async function loadAll(){
 for(let lg in L){
  await fetchLeague(lg);
 }
}
loadAll();
</script>
</body></html>
'''

@app.route('/')
def home():
    return HTML

@app.route('/api/v21/<lg>')
def api_v21(lg):
    live=[]
    up=[]
    nat=[]
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard",timeout=5)
        data=r.json()
        for ev in data.get('events',[]):
            comp=ev['competitions'][0]
            if comp['status']['type']['state']=='in':
                h=comp['competitors'][0]['team']['displayName']
                a=comp['competitors'][1]
