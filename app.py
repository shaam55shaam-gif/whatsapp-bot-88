from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V22 PRO</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:14px;text-align:center;font-weight:900;font-size:16px}
.tabs{display:flex;background:#111;margin:8px;border-radius:15px;overflow:hidden}
.tab{flex:1;padding:12px;text-align:center;cursor:pointer;font-weight:900}
.tab.active{background:#FFD700;color:#000}
.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;display:flex;justify-content:space-around;font-size:11px;font-weight:900}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px}
.box{background:#111;border:1px solid #333;border-radius:14px;padding:12px;text-align:center;cursor:pointer}
.box.has{border-color:#0f0;background:#0a2a0a}
.card{background:#1a1a1a;border-right:5px solid #FFD700;border-radius:14px;margin:8px;padding:12px;cursor:pointer}
.card:hover{background:#222}
table{width:100%;border-collapse:collapse;font-size:11px}
th{background:#FFD700;color:#000;padding:8px}
td{padding:7px;border-bottom:1px solid #333;text-align:center}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:999;overflow:auto}
.modal-content{background:#111;margin:5% auto;padding:15px;border-radius:20px;width:95%;max-width:500px;border:2px solid #FFD700}
</style>
</head><body>
<div class="h">🌍 شامي V22 PRO - ترتيب + احصائيات + تفاصيل</div>
<div class="tabs">
<div class="tab active" onclick="showTab('matches')">📅 مباريات</div>
<div class="tab" onclick="showTab('standing')">📊 الترتيب</div>
<div class="tab" onclick="showTab('stats')">📈 احصائيات</div>
</div>

<div id="tab-matches">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Nat <span id="nc">0</span></span><span id="dn">0/20</span></div>
<div id="st" style="text-align:center;color:#FFD700;padding:6px">Loading...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>

<div id="tab-standing" style="display:none;padding:8px">
<div style="display:flex;gap:5px;overflow:auto;padding:5px">
<button onclick="loadStanding('eng.1')" style="background:#FFD700;border:0;padding:8px 12px;border-radius:10px;font-weight:900">ENG</button>
<button onclick="loadStanding('esp.1')" style="background:#333;color:#fff;border:0;padding:8px 12px;border-radius:10px">ESP</button>
<button onclick="loadStanding('ita.1')" style="background:#333;color:#fff;border:0;padding:8px 12px;border-radius:10px">ITA</button>
<button onclick="loadStanding('ger.1')" style="background:#333;color:#fff;border:0;padding:8px 12px;border-radius:10px">GER</button>
<button onclick="loadStanding('sau.1')" style="background:#333;color:#fff;border:0;padding:8px 12px;border-radius:10px">SAU</button>
<button onclick="loadStanding('tur.1')" style="background:#333;color:#fff;border:0;padding:8px 12px;border-radius:10px">TUR</button>
</div>
<div id="standing-box" style="margin-top:10px">اختر دوري لعرض الترتيب...</div>
</div>

<div id="tab-stats" style="display:none;padding:10px">
<div id="stats-box">
<h3 style="color:#FFD700">📈 احصائيات عامة</h3>
<div class="card">🔴 مباريات مباشرة: <b id="stat-live">0</b></div>
<div class="card">📅 قادمة 30 يوم: <b id="stat-up">0</b></div>
<div class="card">🌍 منتخبات: <b id="stat-nat">0</b></div>
<div class="card">🏆 أكثر دوري مباريات: <b id="stat-most">...</b></div>
</div>
</div>

<div id="modal" class="modal" onclick="this.style.display='none'">
<div class="modal-content" id="modal-content" onclick="event.stopPropagation()"></div>
</div>

<script>
var L={ "eng.1":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 انكليزي","esp.1":"🇪🇸 اسباني","ita.1":"🇮🇹 ايطالي","ger.1":"🇩🇪 الماني","fra.1":"🇫🇷 فرنسي","tur.1":"🇹🇷 تركي","sau.1":"🇸🇦 سعودي","egy.1":"🇪🇬 مصري","uefa.champions":"🏆 ابطال","uefa.europa":"🏆 اوروبا","por.1":"🇵🇹 برتغالي","ned.1":"🇳🇱 هولندي","bel.1":"🇧🇪 بلجيكي","usa.1":"🇺🇸 امريكي","bra.1":"🇧🇷 برازيلي","arg.1":"🇦🇷 ارجنتيني","mex.1":"🇲🇽 مكسيكي","fifa.friendly":"🌍 وديه","uefa.nations":"🏆 امم","fifa.world.qual":"🌍 تصفيات"};
var grid=document.getElementById("grid");
for(var k in L){grid.innerHTML+="<div class=box has-hover id=box-"+k+" onclick=loadStanding('"+k+"')><b>"+L[k]+"</b><br><span id=cnt-"+k+">⏳</span></div>";}
var allUp=[],allLive=[],allNat=[],done=0;
function showTab(t){
 document.getElementById("tab-matches").style.display=t=='matches'?'block':'none';
 document.getElementById("tab-standing").style.display=t=='standing'?'block':'none';
 document.getElementById("tab-stats").style.display=t=='stats'?'block':'none';
 document.querySelectorAll('.tab').forEach(function(el,i){el.className=i==(t=='matches'?0:t=='standing'?1:2)?'tab active':'tab'});
}
async function fetchLeague(lg){
 try{
  var r=await fetch("/api/league30/"+lg);var d=await r.json();
  var tot=d.up.length+d.live.length+d.nat.length;
  document.getElementById("cnt-"+lg).innerText=tot+" مباريات";
  if(tot>0) document.getElementById("box-"+lg).className="box has";
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
  document.getElementById("lc").innerText=allLive.length;document.getElementById("uc").innerText=allUp.length;document.getElementById("nc").innerText=allNat.length;
  document.getElementById("stat-live").innerText=allLive.length;document.getElementById("stat-up").innerText=allUp.length;document.getElementById("stat-nat").innerText=allNat.length;
  var html="";
  if(allLive.length>0) html+="<div style=background:#300;padding:8px;text-align:center;color:red;font-weight:900>🔴 مباشر "+allLive.length+"</div>"+allLive.map(function(m){return "<div class=card onclick=showDetails('"+m.id+"','"+m.league+"')>🔴 <b>"+m.home+" vs "+m.away+"</b> <b style=color:#FFD700>"+m.score+"</b><br><small>اضغط للتفاصيل</small></div>";}).join("");
  html+=allUp.map(function(m){return "<div class=card onclick=showDetails('"+m.id+"','"+m.league+"')><b>"+m.home+" vs "+m.away+"</b><br><small>📅 "+m.date+" | "+m.league+" - اضغط للتفاصيل</small></div>";}).join("");
  document.getElementById("matches").innerHTML=html;
  document.getElementById("stat-most").innerText="ENG + ESP ("+allUp.length+" مباراة)";
 }catch(e){document.getElementById("cnt-"+lg).innerText="...";}
 done++;document.getElementById("dn").innerText=done+"/20";document.getElementById("st").innerText="✅ "+done+"/20 - "+(allUp.length+allLive.length+allNat.length)+" مباراة";
}
async function loadStanding(lg){
 showTab('standing');
 document.getElementById("standing-box").innerHTML="⏳ يحمل ترتيب "+lg+"...";
 try{
  var r=await fetch("/api/standing/"+lg);var d=await r.json();
  var html="<h3 style=color:#FFD700>📊 ترتيب "+lg+"</h3><table><tr><th>#</th><th>الفريق</th><th>ل</th><th>ف</th><th>نقاط</th></tr>";
  d.standing.forEach(function(t){html+="<tr><td>"+t.pos+"</td><td style=text-align:right><b>"+t.team+"</b></td><td>"+t.played+"</td><td>"+t.wins+"</td><td><b style=color:#FFD700>"+t.points+"</b></td></tr>";});
  html+="</table><br><small style=color:#888>المصدر: ESPN</small>";
  document.getElementById("standing-box").innerHTML=html;
 }catch(e){document.getElementById("standing-box").innerHTML="❌ لا يوجد ترتيب لهذا الدوري حاليا"; }
}
async function showDetails(id,lg){
 if(!id || id=="undefined"){document.getElementById("modal-content").innerHTML="<h3>تفاصيل المباراة</h3><p>الدوري: "+lg+"</p><p>سيتم اضافة التشكيلة والاحصائيات قريبا</p><button onclick=document.getElementById('modal').style.display='none' style=background:#FFD700;border:0;padding:10px;border-radius:10px;width:100%>اغلاق</button>";document.getElementById("modal").style.display="block";return;}
 document.getElementById("modal-content").innerHTML="⏳ يحمل تفاصيل...";
 document.getElementById("modal").style.display="block";
 try{
  var r=await fetch("/api/match/"+lg+"/"+id);var d=await r.json();
  document.getElementById("modal-content").innerHTML="<h3 style=color:#FFD700>"+d.home+" vs "+d.away+"</h3><p>📅 "+d.date+"<br>🏟️ "+d.status+"<br>⚽ النتيجة: <b>"+d.score+"</b></p><hr><p><b>التفاصيل:</b><br>"+d.detail+"</p><button onclick=document.getElementById('modal').style.display='none' style=background:#FFD700;color:#000;border:0;padding:12px;border-radius:12px;width:100%;font-weight:900;margin-top:10px>اغلاق</button>";
 }catch(e){document.getElementById("modal-content").innerHTML="تفاصيل غير متوفرة حاليا<br><button onclick=document.getElementById('modal').style.display='none'>اغلاق</button>";}
}
async function loadAll(){for(var lg in L){await fetchLeague(lg);}}loadAll();
loadStanding('eng.1');
</script></body></html>
    """

@app.route('/api/league30/<lg>')
def api_league30(lg):
    live=[];up=[];nat=[]
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/"+lg+"/scoreboard",timeout=5)
        for ev in r.json().get('
