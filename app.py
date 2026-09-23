from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Shaam V15.2 LIVE + UPCOMING 🚀📅</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.header{background:#FFD700;color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:999}
.nav{display:flex;gap:4px;padding:6px;background:#111;overflow-x:auto;position:sticky;top:48px;z-index:998}
.nav button{background:#222;color:#fff;border:none;padding:9px 11px;border-radius:20px;font-size:9px;white-space:nowrap}
.nav button.active{background:#FFD700;color:#000;font-weight:900}
.card{background:#111;border:1px solid #333;border-radius:14px;margin:8px;padding:12px}
.beyond{border:2px solid #FFD700}
.live{border-right:4px solid red}
.upcoming{border-right:4px solid #00ff88}
.score{color:#FFD700;font-size:28px;font-weight:900}
.btn{background:#FFD700;color:#000;border:none;padding:10px;border-radius:10px;font-weight:900;width:100%;margin:5px 0;cursor:pointer}
.btn2{background:#222;color:#FFD700;border:1px solid #FFD700;padding:8px;border-radius:10px;font-weight:900;margin:2px}
.money{position:sticky;top:88px;background:#111;border:1px solid #FFD700;padding:8px;border-radius:20px;margin:6px;text-align:center;font-weight:900;z-index:997;display:flex;justify-content:space-around;font-size:11px}
.search{width:92%;margin:6px 4%;padding:10px;border-radius:20px;border:2px solid #FFD700;background:#222;color:#fff;text-align:center}
</style>
</head>
<body>
<div class="header">🚀 Shaam V15.2 - مباشر + القادمة 📅</div>
<div class="money"><span>💰 <span id="myMoney">1000</span>$</span><span>🪙 <span id="myCoin">0</span> SMC $<span id="price">0.42</span></span><span>👑 <span id="myVip">عادي</span></span><span id="count">--</span></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('upcoming',this)">📅 القادمة</button>
<button onclick="showTab('coin',this)">🪙 Coin</button>
<button onclick="showTab('nft',this)">🖼️ NFT</button>
<button onclick="showTab('game',this)">🎮 لعبة</button>
</div>
<input class="search" placeholder="🚀 ابحث... برشلونة، الهلال" oninput="filterTeams(this.value)">
<button class="btn" style="width:92%;margin:6px 4%" onclick="activate()">🚀 فعل BEYOND: 1000 SMC + 10K$</button>
<div style="text-align:center;font-size:10px;color:#aaa">آخر: <span id="last">--</span> | <span id="last2">--</span></div>

<div id="live" class="tab"><div id="matches" style="text-align:center;padding:20px;color:#FFD700">⏳ يحمّل مباشر...</div></div>

<div id="upcoming" class="tab" style="display:none">
<div style="text-align:center;padding:8px;background:#00ff88;color:#000;border-radius:20px;margin:8px;font-weight:900">📅 مباريات بكرة + بعده - توقع واربح SMC!</div>
<div id="upcomingBox" style="text-align:center;padding:20px;color:#00ff88">⏳ يحمّل مباريات بكرة...</div>
</div>

<div id="coin" class="tab" style="display:none"><div class="card beyond"><h3>🪙 ShaamCoin $0.42 ↑</h3><button class="btn" onclick="mine()">⛏️ عدّن +10 SMC</button><button class="btn" onclick="buyCoin(100)">اشتري 100 SMC</button></div></div>
<div id="nft" class="tab" style="display:none"><div class="card"><h3>🖼️ NFT</h3><button class="btn" onclick="buyNFT(50)">👕 Real Madrid 50 SMC</button></div></div>
<div id="game" class="tab" style="display:none"><div class="card beyond"><h3>🎮 لعبة + 100K$</h3><div id="gameBox"></div></div></div>

<script>
let money=parseInt(localStorage.getItem('v15_money')||'1000');let coin=parseInt(localStorage.getItem('v15_coin')||'0');let price=0.42;let all=[];let allUp=[];
document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin;
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='game')loadGame();if(t=='upcoming')loadUpcoming();}
async function load(){try{let r=await fetch('/api/live');let d=await r.json();all=d.matches;document.getElementById('count').innerText=d.matches.length+' مباشر';document.getElementById('last').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('matches').innerHTML=d.matches.map(m=>{let live=m.minute.includes("'");return `<div class="card ${live?'live':'upcoming'}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#222;padding:4px 10px;border-radius:12px;border:1px solid #FFD700">${m.league} ${live?'🔴':'📅'}</span>${live?`<span style="color:red;font-weight:900">🔴 ${m.minute}</span>`:`<span style="color:#00ff88">${m.status}</span>`}</div><div style="display:flex;justify-content:space-between;margin:6px 0;font-weight:900"><span>🚀 ${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div style="display:flex;justify-content:space-between;font-weight:900"><span>🚀 ${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div><div style="background:#0a0a00;padding:6px;border-radius:8px;margin:6px 0;border:1px dashed #FFD700;font-size:11px">🎯 AI: ${Math.floor(Math.random()*3)}-${Math.floor(Math.random()*2)} <button class="btn2" onclick="predict('${m.home}')">توقع +10 SMC</button></div><div style="display:flex;gap:4px"><button class="btn2" style="background:red;color:#fff;flex:1" onclick="playVideo('${m.home} ${m.away} goal')">🎥 هدف</button><button class="btn2" style="flex:1" onclick="mine()">⛏️ عدّن</button></div></div>`}).join('');}catch(e){document.getElementById('matches').innerHTML='❌ حاول تحدث';}}
async function loadUpcoming(){try{let r=await fetch('/api/upcoming');let d=await r.json();allUp=d.matches;document.getElementById('last2').innerText='القادمة: '+d.matches.length;document.getElementById('upcomingBox').innerHTML=d.matches.map(m=>`<div class="card upcoming"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#222;padding:4px 10px;border-radius:12px;border:1px solid #00ff88">${m.league}</span><span style="color:#00ff88">📅 ${m.time}</span></div><div style="margin:8px 0;font-weight:900;font-size:15px">${m.home} vs ${m.away}</div><div style="background:#001100;padding:8px;border-radius:8px;border:1px dashed #00ff88">🎯 توقع النتيجة واربح
