from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return '''
<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V23 FIXED</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:14px;text-align:center;font-weight:900}
.tabs{display:flex;background:#111;margin:8px;border-radius:15px;overflow:hidden;border:2px solid #FFD700}
.tab{flex:1;padding:12px;text-align:center;cursor:pointer;font-weight:900}
.active{background:#FFD700;color:#000}
.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;display:flex;justify-content:space-around;font-size:11px;font-weight:900}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:7px;padding:7px}
.box{background:#111;border:1px solid #333;border-radius:14px;padding:12px;text-align:center}
.has{border-color:#0f0;background:#0a2a0a;box-shadow:0 0 10px #0f05}
.zero{opacity:.5}
.card{background:#1a1a1a;border-right:5px solid #FFD700;border-radius:14px;margin:8px;padding:12px}
table{width:100%;border-collapse:collapse;font-size:12px} th{background:#FFD700;color:#000;padding:8px} td{padding:7px;border-bottom:1px solid #333;text-align:center}
.btn{background:#222;color:#fff;border:1px solid #555;padding:8px 12px;border-radius:10px;margin:3px}
.btnA{background:#FFD700;color:#000;border:0;padding:8px 12px;border-radius:10px;margin:3px;font-weight:900}
</style>
</head><body>
<div class="h">🌍 Shaam V23 FIXED - كل الدوريات + ترتيب + احصائيات ✅</div>
<div class="tabs">
<div class="tab active" id="t1" onclick="showTab(1)">📅 مباريات</div>
<div class="tab" id="t2" onclick="showTab(2)">📊 الترتيب</div>
<div class="tab" id="t3" onclick="showTab(3)">📈 احصائيات</div>
</div>

<div id="tab1">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Nat <span id="nc">0</span></span><span id="dn">0/18</span></div>
<div id="st" style="text-align:center;color:#FFD700;padding:6px">⏳ يحمل...</div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>

<div id="tab2" style="display:none;padding:8px">
<div style="display:flex;gap:5px;overflow:auto;padding:5px">
<button class="btnA" onclick="loadStanding('eng.1',this)">ENG</button>
<button class="btn" onclick="loadStanding('esp.1',this)">ESP</button>
<button class="btn" onclick="loadStanding('ita.1',this)">ITA</button>
<button class="btn" onclick="loadStanding('ger.1',this)">GER</button>
<button class="btn" onclick="loadStanding('sau.1',this)">SAU</button>
<button class="btn" onclick="loadStanding('tur.1',this)">TUR</button>
</div>
<div id="standing-box">اختر دوري...</div>
</div>

<div id="tab3" style="display:none;padding:10px">
<h3 style="color:#FFD700">📈 احصائيات</h3>
<div class="card">🔴 مباشر: <b id="s1">0</b></div>
<div class="card">📅 قادمة 30 يوم: <b id="s2">0</b></div>
<div class="card">🌍 منتخبات: <b id="s3">0</b></div>
<div class="card">🏆 المجموع: <b id="s5">0</b> مباراة</div>
</div>

<script>
var L={"eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","uefa.champions":"UCL","uefa.europa":"UEL","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","fifa.friendly":"FRIENDLY","uefa.nations":"NATIONS"};
function safeId(s){return s.replace(/\\./g,"-").replace(/\\//g,"-");}
var grid=document.getElementById("grid");
for(var k in L){
  var sid=safeId(k);
  grid.innerHTML += '<div class="box" id="box-'+sid+'"><b>'+L[k]+'</b><br><small>'+k+'</small><br><span id="cnt-'+sid+'">...</span></div>';
}
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
  var r=await fetch("/api/league30/"+lg);
  var d=await r.json();
  var tot=d.up.length+d.live.length+d.nat.length;
  var sid=safeId(lg);
  var el=document.getElementById("cnt-"+sid);
  if(el) el.innerText=tot+" games";
  var box=document.getElementById("box-"+sid);
  if(box) box.className=tot>0?"box has":"box zero";
  allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
  document.getElementById("lc").innerText=allLive.length;
  document.getElementById("uc").innerText=allUp.length;
  document.getElementById("nc").innerText=allNat.length;
  document.getElementById("s1").innerText=allLive.length;
  document.getElementById("s2").innerText=allUp.length;
  document.getElementById("s3").innerText=allNat.length;
  document.getElementById("s5").innerText=allUp.length+allLive.length+allNat.length;
  var html="";
  if(allLive.length>0) html+='<div style="background:#300;padding:6px;text-align:center;color:red">LIVE '+allLive.length+'</div>'+allLive.map(function(m){return '<div class="card">🔴 '+m.home+' vs '+m.away+' <b>'+m.score+'</b></div>';}).join("");
  html+=allUp.map(function(m){return '<div class="card"><b>'+m.home+' vs '+m.away+'</b><br><small>📅 '+m.date+' | '+m.league+'</small></div>';}).join("");
  if(allNat.length>0) html+='<div style="background:#002233;padding:6px;text-align:center;color:#0bf">منتخبات '+allNat.length+'</div>'+allNat.map(function(m){return '<div class="card">🌍 '+m.home+' vs '+m.away+'<br><small>'+m.date+'</small></div>';}).join("");
  document.getElementById("matches").innerHTML=html;
 }catch(e){ console.log(e); }
 done++;
 document.getElementById("dn").innerText=done+"/18";
 document.getElementById("st").innerText="✅ Done "+done+"/18 - "+(allUp.length+allLive.length+allNat.length)+" games";
}
async function loadStanding(lg,btn){
 if(btn){
  var btns=document.querySelectorAll(".btn,.btnA");
  for(var i=0;i<btns.length;i++) btns[i].className="btn";
  btn.className="btnA";
 }
 showTab(2);
 document.getElementById("standing-box").innerHTML="⏳ يحمل "+lg+"...";
 try{
  var r=await fetch("/api/standing/"+lg);
  var d=await r.json();
  var html='<h3 style="color:#FFD700">ترتيب '+lg.toUpperCase()+'</h3><table><tr><th>#</th><th>الفريق</th><th>ل</th><th>نقاط</th></tr>';
  d.standing.forEach(function(t){ html+='<tr><td>'+t.pos+'</td><td><b>'+t.team+'</b></td><td>'+t.played+'</td><td><b style="color:#FFD700">'+t.points+'</b></td></tr>'; });
  html+='</table>';
  document.getElementById("standing-box").innerHTML=html;
 }catch(e){ document.getElementById("standing-box").innerHTML="لا يوجد بيانات"; }
}
async function loadAll(){ for(var lg in L){ await fetchLeague(lg); } }
