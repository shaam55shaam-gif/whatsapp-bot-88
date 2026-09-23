from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)

@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#0a0a0a;--card:#1a1a1a;--text:#fff;--border:#00ff00}
.light{--bg:#f5f5f5;--card:#fff;--text:#000;--border:#00aa00}
body{background:var(--bg);color:var(--text);font-family:Arial;margin:0;transition:.3s}
.h{background:linear-gradient(90deg,#00ff00,gold);color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center}
.ticker{background:#111;color:#00ff00;padding:8px;white-space:nowrap;overflow:hidden;border-bottom:2px solid #00ff00;font-weight:900}
.ticker span{display:inline-block;animation:scroll 25s linear infinite}
@keyframes scroll{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.search{margin:8px;background:var(--card);border:1px solid var(--border);border-radius:25px;padding:10px 15px;display:flex;align-items:center}
.search input{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:16px}
.filters{display:flex;gap:6px;padding:8px;overflow:auto}
.f{padding:8px 14px;border-radius:20px;border:1px solid #333;background:var(--card);cursor:pointer;white-space:nowrap;font-weight:700;color:var(--text)}
.f.active{background:#00ff00;color:#000;box-shadow:0 0 10px #00ff00}
.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#222}
.card{background:var(--card);border-right:4px solid #00ff00;margin:6px;padding:12px;border-radius:14px;cursor:pointer;color:var(--text)}
.card.live{border-color:red;background:#2a0000;color:#fff;animation:pulse 1.5s infinite}
.card.fav{border-color:gold;box-shadow:0 0 12px gold}
@keyframes pulse{0%{box-shadow:0 0 0 0 red}70%{box-shadow:0 0 0 10px #ff000000}100%{box-shadow:0 0 0 0 #ff000000}}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:var(--card);border:1px solid #333;border-radius:12px;padding:12px;text-align:center;cursor:pointer;color:var(--text)}
.box.ok{border-color:#00ff00}
.box.active{border-color:gold!important;background:#1a1a00!important}
.syria{border-color:#00ff00!important;background:#001a00!important;color:#fff!important}
.stand{background:var(--card);margin:6px;border-radius:12px;padding:10px;border:2px solid #00ff00}
.row{display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #333}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center}
.modal>div{background:var(--card);color:var(--text);padding:20px;border-radius:20px;border:2px solid #00ff00;width:90%;max-width:420px;text-align:center}
.btn{background:#00ff00;color:#000;border:none;padding:10px 20px;border-radius:20px;font-weight:900;margin:4px;cursor:pointer}
.switch{cursor:pointer;background:#000;color:#fff;padding:6px 12px;border-radius:15px;font-size:12px}
.live-dot{display:inline-block;width:10px;height:10px;background:red;border-radius:50%;animation:blink 1s infinite;margin-left:4px}
@keyframes blink{0%{opacity:1}50%{opacity:0}}
</style></head><body>
<div class=h><span>👑 V44 CHAMPION - 66 - LIVE كل 30ث</span><span class=switch onclick="toggleLight()">🌙/☀️</span></div>
<div class=ticker><span id=tick>⚽ V44 CHAMPION - تحديث تلقائي كل 30 ثانية - صوت هدف الجيش - SY24 حقيقي - الكرامة متصدر 18 - الجيش × الوحدة السبت بدون جمهور</span></div>
<div style="display:flex;justify-content:space-between;padding:6px;font-size:12px;color:#00ff00"><span><span class=live-dot></span> LIVE: <span id=liveCount>0</span></span><span>🔄 تحديث: <span id=upd>الآن</span></span><span onclick="toggleSound()" id=soundBtn>🔊 صوت الهدف: ON</span></div>
<div class=search><input id=q placeholder="🔍 ابحث الجيش، الكرامة، Real Madrid..." oninput="doFilter()"><span onclick="document.getElementById('q').value='';doFilter()" style="cursor:pointer">❌</span></div>
<div class=filters>
<div class="f active" onclick="setFilter('all',this)">الكل 66</div>
<div class=f onclick="setFilter('syr.1',this)">🇸🇾 السوري</div>
<div class=f onclick="setFilter('live',this)">🔴 LIVE</div>
<div class=f onclick="setFilter('fav',this)">⭐ الجيش</div>
<div class=f onclick="setFilter('sau.1',this)">🇸🇦 السعودي</div>
</div>
<div class=stand><b style="color:#00ff00">📊 SY24 - الجولة السابعة الحقيقية</b><div id=stand></div></div>
<div id=s style="text-align:center;color:#00ff00;padding:10px;font-weight:900;background:#001a00;border:1px solid #00ff00;margin:6px;border-radius:10px">🚀 V43 كان 11/11 - V44 نفس السرعة + LIVE كل 30ث</div>
<div style="text-align:center;color:gold;padding:6px">🏆 البطولات الكبرى - اضغط للتصفية</div>
<div class=top id=top></div>
<div class=grid id=g></div>
<div style="text-align:center;color:gold;padding:8px;font-weight:900">📋 المباريات - اضغط للتفاصيل + تحديث تلقائي</div>
<div id=m></div>
<div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div>
<audio id=goalSound preload="auto"><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>
<script>
var light=false;var soundOn=true;var prevLive=0;
function toggleLight(){light=!light;document.body.classList.toggle('light',light);localStorage.setItem('light',light)}
function toggleSound(){soundOn=!soundOn;document.getElementById('soundBtn').innerText=(soundOn?'🔊':'🔇')+' صوت الهدف: '+(soundOn?'ON':'OFF');}
if(localStorage.getItem('light')=='true'){light=true;document.body.classList.add('light')}
var LOGOS={"الجيش":"🟢","الوحدة":"🟠","الكرامة":"🔵","الوثبة":"⚪","حطين":"⚫","الشعلة":"💛","الطليعة":"🔴","الفتوة":"💙","أهلي حلب":"❤️","جبلة":"🔵","تشرين":"🟡","الشرطة":"🔵","Real Madrid":"⚪","Barcelona":"🔵🔴","Man City":"🔵","Arsenal":"🔴","Liverpool":"🔴","Chelsea":"🔵","Bayern Munich":"🔴","Inter":"🔵⚫"};
var STAND=[["الكرامة - متصدر",18],["الوثبة - وصيف",16],["حطين - ثالث",15],["أهلي حلب",14],["الجيش - خامس",12],["الوحدة - مؤجلات",10]];
document.getElementById('stand').innerHTML=STAND.map((t,i)=>'<div class=row><span>'+(i+1)+'. '+(LOGOS[t[0].split(' ')[0]]||'⚽')+' '+t[0]+'</span><span>'+t[1]+' نقطة</span></div>').join('');
var TOP={"uefa.champions":"ابطال اوروبا","uefa.europa":"الاوروبي","uefa.europa.conf":"المؤتمر"};
var L={"syr.1":"السوري حقيقي","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box id=b-'+k.replaceAll('.','-')+' onclick="filterLeague(&quot;'+k+'&quot;,this)"><b>'+TOP[k]+'</b><br><small id=c
