from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

HTML = """<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V19 ALL 35 - 14 DAYS 🌍</title><style>body{background:#000;color:#fff;font-family:Arial;margin:0}.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:12px;text-align:center;font-weight:900}.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;text-align:center;font-weight:900;display:flex;justify-content:space-around;font-size:11px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;padding:5px}.box{background:#111;border:1px solid #333;border-radius:10px;padding:8px;text-align:center;font-size:10px;min-height:50px}.box.has{background:#1a2e1a;border-color:#00ff00}.box.zero{background:#2a1111}.card{background:#1a1a1a;border-right:4px solid #FFD700;border-radius:12px;margin:6px;padding:9px;font-size:12px}.live{border-right-color:red}</style></head><body><div class="h">🌍 Shaam V19 - كل الـ 35 دوري - بحث 14 يوم ✅</div><div class="money"><span>🔴 <span id="liveC">0</span> مباشر</span><span>📅 <span id="upC">0</span> قادمة</span><span>🌍 <span id="natC">0</span> منتخبات</span><span>⏳ <span id="done">0</span>/35</span></div><div id="status" style="text-align:center;color:#FFD700;font-size:11px;padding:4px">⏳ يبحث 14 يوم قدام لكل الدوريات...</div><div class="grid" id="grid"></div><h3 style="text-align:center;color:#FFD700;margin:8px 0">📅 كل المباريات الحقيقية - 14 يوم</h3><div id="matches">⏳...</div><script>
const LEAGUES={"eng.1":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي","esp.1":"🇪🇸 إسباني","ita.1":"🇮🇹 إيطالي","ger.1":"🇩🇪 ألماني","fra.1":"🇫🇷 فرنسي","tur.1":"🇹🇷 تركي","sau.1":"🇸🇦 سعودي","egy.1":"🇪🇬 مصري","uae.1":"🇦🇪 إماراتي","qat.1":"🇶🇦 قطري","uefa.champions":"🏆 أبطال أوروبا","uefa.europa":"🏆 أوروبا","por.1":"🇵🇹 برتغالي","ned.1":"🇳🇱 هولندي","bel.1":"🇧🇪 بلجيكي","sco.1":"🏴󠁧󠁢󠁳󠁣󠁴󠁿 اسكتلندي","usa.1":"🇺🇸 أمريكي","bra.1":"🇧🇷 برازيلي","arg.1":"🇦🇷 أرجنتيني","mex.1":"🇲🇽 مكسيكي","fifa.friendly":"🌍 ودية","uefa.nations":"🏆 أمم","fifa.world.qual":"🌍 تصفيات"};
let grid=document.getElementById('grid');Object.entries(LEAGUES).forEach(([k,v])=>{grid.innerHTML+=`<div class="box" id="box-${k}"><b>${v}</b><br><small>${k}</small><br><span id="cnt-${k}">⏳</span></div>`;});
let allUp=[],allLive=[],allNat=[],done=0;
async function fetchLeague(lg){
try{
let r=await fetch('/api/league14/'+lg);let d=await r.json();
let total=d.up.length+d.live.length+d.nat.length;
document.getElementById('cnt-'+lg).innerText=total>0?total+' مباريات':'0 - توقف';
document.getElementById('box-'+lg).className=total>0?'box has':'box zero';
allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
document.getElementById('liveC').innerText=allLive.length;document.getElementById('upC').innerText=allUp.length;document.getElementById('natC').innerText=allNat.length;
let box=document.getElementById('matches');
let html='';
if(allLive.length>0) html+='<div style="background:#300;padding:5px;text-align:center;color:red">🔴 مباشر ('+allLive.length+')</div>'+allLive.map(m=>`<div class="card live">🔴 <b>${m.home} vs ${m.away}</b> <b style=color:#FFD700>${m.score}</b><br><small>${m.league}</small></div>`).join('');
html+=allUp.map(m=>`<div class=card>📅 <b>${m.home} vs ${m.away}</b><br><small>${m.date} | ${m.league} ✅ حقيقي</small></div>`).join('');
if(allNat.length>0) html+='<div style="background:#002233;padding:5px;text-align:center;color:#00bfff">🌍 منتخبات ('+allNat.length+')</div>'+allNat.map(m=>`<div class=card style="border-right-color:#00bfff">🌍 <b>${m.home} vs ${m.away}</b><br><small>${m.date} | ${m.league}</small></div>`).join('');
box
