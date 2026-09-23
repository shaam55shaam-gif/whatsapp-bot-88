from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)

@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold);color:#000;padding:14px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20}
.ticker{background:#111;color:#00ff00;padding:8px;white-space:nowrap;overflow:hidden;border-bottom:2px solid #00ff00;font-weight:900}
.ticker span{display:inline-block;animation:scroll 25s linear infinite}
@keyframes scroll{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.search{margin:8px;background:#1a1a1a;border:1px solid #00ff00;border-radius:25px;padding:10px 15px;display:flex;align-items:center}
.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:16px}
.filters{display:flex;gap:6px;padding:8px;overflow:auto;scrollbar-width:none}
.f{padding:8px 16px;border-radius:20px;border:1px solid #333;background:#1a1a1a;cursor:pointer;white-space:nowrap;font-weight:700}
.f.active{background:#00ff00;color:#000;box-shadow:0 0 10px #00ff00}
.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#222}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:12px;border-radius:14px;cursor:pointer;transition:.2s}
.card:hover{transform:scale(1.02);background:#222}
.card.live{border-color:red;background:#2a0000;animation:pulse 1.5s infinite}
.card.fav{border-color:gold;background:#1a1a00;box-shadow:0 0 12px gold}
@keyframes pulse{0%{box-shadow:0 0 0 0 red}70%{box-shadow:0 0 0 10px #ff000000}100%{box-shadow:0 0 0 0 #ff000000}}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:#151515;border:1px solid #333;border-radius:12px;padding:12px;text-align:center;cursor:pointer;transition:.3s}
.box.ok{border-color:#00ff00;box-shadow:0 0 8px #00ff0055}
.box.active{border-color:gold!important;background:#1a1a00!important;transform:scale(1.05)}
.syria{border-color:#00ff00!important;background:#001a00!important}
.stand{background:#111;margin:6px;border-radius:12px;padding:10px;border:2px solid #00ff00}
.row{display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #222}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center}
.modal>div{background:#1a1a1a;padding:20px;border-radius:20px;border:2px solid #00ff00;width:90%;max-width:420px;text-align:center}
.btn{background:#00ff00;color:#000;border:none;padding:10px 20px;border-radius:20px;font-weight:900;margin:4px;cursor:pointer}
</style></head><body>
<div class=h>👑 V43 ULTIMATE - 66 مباراة - بحث + LIVE + تفضيل + تفاصيل</div>
<div class=ticker><span id=tick>⚽ SY24 حقيقي - الكرامة متصدر 18 نقطة - الجيش × الوحدة السبت في الفيحاء بدون جمهور - Man City vs Arsenal - Real Madrid vs Barcelona - V43 ULTIMATE</span></div>
<div class=search><input id=q placeholder="🔍 ابحث عن فريق... الجيش، الكرامة، Real Madrid..." oninput="doFilter()"><span onclick="document.getElementById('q').value='';doFilter()" style="cursor:pointer">❌</span></div>
<div class=filters>
<div class="f active" onclick="setFilter('all',this)">الكل 66</div>
<div class=f onclick="setFilter('syr.1',this)">🇸🇾 السوري حقيقي</div>
<div class=f onclick="setFilter('sau.1',this)">🇸🇦 السعودي</div>
<div class=f onclick="setFilter('live',this)">🔴 LIVE</div>
<div class=f onclick="setFilter('fav',this)">⭐ الجيش</div>
</div>
<div class=stand><b style="color:#00ff00">📊 ترتيب الدوري السوري - الجولة السابعة الحقيقية SY24</b><div id=stand></div></div>
<div id=s style="text-align:center;color:#00ff00;padding:10px;font-weight:900;background:#001a00;border:1px solid #00ff00;margin:6px;border-radius:10px">🚀 V42 كان 11/11 - V43 نفس السرعة + كل الميزات</div>
<div style="text-align:center;color:gold;padding:6px">🏆 البطولات الكبرى - اضغط للتصفية</div>
<div class=top id=top></div>
<div style="text-align:center;color:#00ff00;padding:6px">🌍 كل الدوريات - اضغط لعرض المباريات</div>
<div class=grid id=g></div>
<div style="text-align:center;color:gold;padding:8px;font-weight:900">📋 المباريات - اضغط للتفاصيل</div>
<div id=m></div>
<div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div>
<script>
var LOGOS={"الجيش":"🟢","الوحدة":"🟠","الكرامة":"🔵","الوثبة":"⚪","حطين":"⚫","الشعلة":"💛","الطليعة":"🔴","الفتوة":"💙","أهلي حلب":"❤️","جبلة":"🔵","تشرين":"🟡","الشرطة":"🔵","Real Madrid":"⚪","Barcelona":"🔵🔴","Man City":"🔵","Arsenal":"🔴","Liverpool":"🔴","Chelsea":"🔵","Bayern Munich":"🔴","Inter":"🔵⚫"};
var STADIUM={"الجيش":"الجلاء - دمشق","الوحدة":"الجلاء","الكرامة":"خالد بن الوليد - حمص","الوثبة":"الباسل - حمص","حطين":"الباسل - اللاذقية","تشرين":"اللاذقية","جبلة":"البعث - جبلة","الشرطة":"الفيحاء - دمشق","أهلي حلب":"الحمدانية - حلب","Real Madrid":"برنابيو","Barcelona":"كامب نو","Man City":"الاتحاد","Arsenal":"الامارات","Liverpool":"انفيلد","Bayern Munich":"اليانز ارينا","Al Hilal":"المملكة ارينا","Al Nassr":"الاول بارك"};
var STAND=[["الكرامة - متصدر",18],["الوثبة - وصيف",16],["حطين - ثالث",15],["أهلي حلب",14],["الجيش - خامس",12],["الوحدة - مؤجلات",10]];
document.getElementById('stand').innerHTML=STAND.map((t,i)=>'<div class=row><span>'+(i+1)+'. '+(LOGOS[t[0].split(' ')[0]]||'⚽')+' '+t[0]+'</span><span>'+t[1]+' نقطة</span></div>').join('');
var TOP={"uefa.champions":"ابطال اوروبا","uefa.europa":"الاوروبي","uefa.europa.conf":"المؤتمر"};
var L={"syr.1":"السوري حقيقي","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box" id=b-'+k.replaceAll('.','-')+' onclick="filterLeague(&quot;'+k+'&quot;,this)"><b>'+TOP[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>يحمل...</small></div>'}
var gDiv=document.getElementById('g');for(var k in L){gDiv.innerHTML+='<div class="box '+(k=='syr.1'?'syria':'')+'" id=b-'+k.replaceAll('.','-')+' onclick="filterLeague(&quot;'+k+'&quot;,this)"><b>'+L
