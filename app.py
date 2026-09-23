import requests
from flask import Flask, jsonify
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V14 BEYOND GOD 🚀🪙</title>
<meta name="theme-color" content="#FFD700">
<style>
:root{--beyond:#FFD700;--eth:#627EEA;--btc:#F7931A}
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI Black,Segoe UI}
body{background:#000;color:#fff;overflow-x:hidden}
.header{background:linear-gradient(90deg,#FFD700,#F7931A,#627EEA,#FFD700,#ff00ff,#00ffff,#FFD700);background-size:1000%;animation:g.5s linear infinite;padding:20px;text-align:center;position:sticky;top:0;z-index:9999;border-bottom:6px solid #FFD700;box-shadow:0 0 60px #FFD700}
@keyframes g{0%{background-position:0%}100%{background-position:1000%}}
.nav{display:flex;gap:4px;padding:8px;background:#000;overflow-x:auto;position:sticky;top:78px;z-index:9998}
.nav button{background:#111;color:#fff;border:1px solid #333;padding:10px 11px;border-radius:30px;font-size:8px;white-space:nowrap;font-weight:900}
.nav button.active{background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;transform:scale(1.18);box-shadow:0 0 30px #FFD700;border:3px solid #FFD700}
.card{background:linear-gradient(145deg,#111100,#1a1a00);border-radius:25px;margin:10px;padding:14px;box-shadow:0 0 35px rgba(255,215,0,.3)}
.beyond{border:4px solid #FFD700;box-shadow:0 0 70px rgba(255,215,0,.7),0 0 100px rgba(247,147,26,.5),0 0 140px rgba(98,126,234,.3);background:radial-gradient(circle at center,#221100,#110011,#000);animation:beyond 2s infinite}
@keyframes beyond{0%,100%{box-shadow:0 0 70px #FFD700}50%{box-shadow:0 0 100px #FFD700,0 0 150px #F7931A}}
.live{border-right:8px solid #ff0000;animation:rr.5s infinite}
@keyframes rr{0%,100%{box-shadow:0 0 25px red,0 0 50px #FFD700}50%{box-shadow:0 0 80px red,0 0 120px #FFD700}}
.team{display:flex;justify-content:space-between;align-items:center;margin:11px 0;font-weight:900;font-size:18px}
.score{font-size:44px;font-weight:900;background:linear-gradient(90deg,#FFD700,#F7931A,#627EEA,#FFD700);background-size:400%;animation:g 1.5s linear infinite;-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 0 15px #FFD700)}
.btn{padding:9px 10px;border-radius:13px;border:none;font-weight:900;font-size:8px;margin:2px;cursor:pointer}
.btn-beyond{background:linear-gradient(90deg,#FFD700,#F7931A,#627EEA,#FFD700);background-size:500%;animation:g 1s linear infinite;color:#000;width:94%;margin:12px 3%;padding:20px;border-radius:40px;font-weight:900;font-size:17px;display:block;box-shadow:0 0 50px #FFD700;animation:pd 1s infinite;border:3px solid #fff}
@keyframes pd{0%,100%{transform:scale(1)}50%{transform:scale(1.06)}}
.search{width:94%;margin:10px 3%;padding:18px;border-radius:40px;border:4px solid #FFD700;background:#111;color:#fff;text-align:center;font-weight:900;box-shadow:0 0 30px rgba(255,215,0,.6);font-size:14px}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.99);z-index:6000;align-items:center;justify-content:center;padding:10px}
.modal-box{width:100%;max-width:650px;background:#0a0a00;border-radius:25px;padding:18px;border:5px solid #FFD700;box-shadow:0 0 80px #FFD700}
.video{width:100%;height:360px;border-radius:20px;border:none}
.money{position:fixed;top:82px;left:6px;right:6px;background:linear-gradient(90deg,#FFD700,#F7931A,#627EEA,#FFD700);background-size:400%;animation:g 1.5s linear infinite;color:#000;padding:10px;border-radius:35px;font-weight:900;font-size:11px;z-index:1000;box-shadow:0 0 40px #FFD700;border:3px solid #fff;display:flex;justify-content:space-around;text-align:center}
.install{position:fixed;bottom:10px;left:8px;right:8px;background:linear-gradient(90deg,#FFD700,#F7931A,#627EEA,#FFD700);background-size:600%;animation:g.8s linear infinite;color:#000;padding:20px;border-radius:22px;font-weight:900;text-align:center;z-index:1000;box-shadow:0 0 60px #FFD700;border:4px solid #fff;font-size:13px;text-shadow:0 0 5px #fff}
.coin{animation:spin 2s linear infinite;display:inline-block}
@keyframes spin{0%{transform:rotateY(0)}100%{transform:rotateY(360deg)}}
</style>
</head>
<body>
<div class="header"><h1 style="color:#000;font-weight:900;font-size:19px;text-shadow:0 0 15px #fff">🚀🪙 Shaam V14 BEYOND GOD - ما وراء الآلهة 🪙🚀</h1><div style="color:#000;font-weight:900;font-size:11px">ShaamCoin + NFT + Web3 Wallet + بلوكشين + 100K$ سحب + 12 معلق + Desktop + Mobile</div></div>
<div class="money" id="moneyBar"><span>💰 <span id="myMoney">1000</span>$</span><span>🪙 <span id="myCoin">0</span> SMC</span><span>🎯 <span id="myPoints">0</span></span><span>👑 <span id="myVip">عادي</span></span><span>🖼️ <span id="myNft">0</span> NFT</span></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('tv',this)">📺 بث 8</button>
<button onclick="showTab('coin',this)">🪙 ShaamCoin</button>
<button onclick="showTab('nft',this)">🖼️ NFT متجر</button>
<button onclick="showTab('game',this)">🎮 لعبة💰</button>
<button onclick="showTab('store',this)">💳 Web3</button>
<button onclick="showTab('ai',this)">🤖 AI صوت</button>
</div>
<input class="search" placeholder="🚀 ابحث... برشلونة، الهلال، رونالدو، ShaamCoin، NFT" oninput="filterTeams(this.value)">
<button class="btn-beyond" onclick="activateBeyond()">🚀🪙🔔 فعل وضع BEYOND: عملتك ShaamCoin + NFT + 100K$ + محفظة Web3</button>
<div style="text-align:center;font-size:10px;color:#aaa">آخر: <span id="lastUpdate">--</span> | <span id="count">--</span> | 🪙 سعر SMC: $<span id="coinPrice">0.42</span> ↑12% | 💳 Web3: <span id="web3Status">جاهز</span></div>
<div style="margin:10px;background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;border-radius:15px;padding:12px;text-align:center;font-weight:900">🚀 ShaamCoin ترتفع! 1 SMC = $0.42 (↑12% اليوم) - اشتري الآن قبل ما تصير $10! 🪙</div>

<div id="live" class="tab"><div id="matches"><div style="text-align:center;padding:80px;color:#FFD700;font-size:20px">🚀 V14 BEYOND يبني كون جديد بالبلوكشين...</div></div></div>

<div id="tv" class="tab" style="display:none">
<div class="card beyond"><h3>📺 بث BEYOND - 8 قنوات + Web3 Stream</h3>
<div style="display:flex;gap:5px;overflow-x:auto;padding:10px 0">
<div class="ch" style="padding:11px 15px;background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;border-radius:30px;font-size:10px;white-space:nowrap;font-weight:900" onclick="switchChannel(0,this)">🏴󠁧󠁢󠁥󠁮󠁧󠁿 BeIN 1</div>
<div class="ch" style="padding:9px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(1,this)">🇪🇸 BeIN 2</div>
<div class="ch" style="padding:9px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(2,this)">🏆 UCL</div>
<div class="ch" style="padding:9px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(3,this)">🇸🇦 SSC</div>
<div class="ch" style="padding:9px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(4,this)">🪙 Web3 TV</div>
<div class="ch" style="padding:9px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(5,this)">🖼️ NFT Live</div>
</div>
<iframe id="tvFrame" class="video" style="height:380px;margin-top:12px" src="https://www.youtube.com/embed/jfKfPfyJRdk" allowfullscreen></iframe>
</div>
</div>

<div id="coin" class="tab" style="display:none">
<div class="card beyond"><h3>🪙 ShaamCoin (SMC) - عملتك الخاصة!</h3>
<div style="background:#000;padding:15px;border-radius:15px;border:3px solid #FFD700;text-align:center"><div style="font-size:50px" class="coin">🪙</div><div style="font-size:28px;font-weight:900;color:#FFD700">1 SMC = $0.42</div><div style="color:#00ff88;font-weight:900">↑ 12.5% اليوم! 📈</div><div style="margin-top:10px;font-size:11px;color:#aaa">إجمالي المعروض: 1,000,000 SMC | تم بيع: 234,567 SMC</div></div>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px">
<button class="btn" style="background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;padding:16px;border-radius:15px" onclick="buyCoin(100)">🪙 اشتري 100 SMC<br><b>42$</b></button>
<button class="btn" style="background:linear-gradient(90deg,#627EEA,#00ffff);color:#000;padding:16px;border-radius:15px" onclick="buyCoin(1000)">🪙 اشتري 1000 SMC<br><b>420$ - خصم 10%!</b></button>
</div>
<button class="btn" style="background:#111;color:#FFD700;border:2px solid #FFD700;width:100%;padding:14px;margin-top:10px" onclick="mineCoin()">⛏️ عدّن مجاناً +10 SMC كل 5 دقائق!</button>
<div style="margin-top:12px;background:#000;padding:12px;border-radius:12px;border:2px dashed #FFD700"><small>💡 عملتك ترتفع! عندما تصل 1M مشترك، سعرها يصير 10$! تربح 2400%!</small></div>
</div>
</div>

<div id="nft" class="tab" style="display:none">
<div class="card beyond"><h3>🖼️ NFT متجر - تيشيرتات رقمية</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px">
<div style="background:#000;border:2px solid #FFD700;border-radius:15px;padding:10px;text-align:center"><div style="font-size:40px">👕</div><b>Real Madrid NFT</b><br><small>نادر - 1/100</small><br><b style="color:#FFD700">50 SMC</b><br><button class="btn" style="background:#FFD700;color:#000;width:100%;margin-top:6px" onclick="buyNFT('Real Madrid',50)">اشتري</button></div>
<div style="background:#000;border:2px solid #00ffff;border-radius:15px;padding:10px;text-align:center"><div style="font-size:40px">⚽</div><b>Goal NFT</b><br><small>أسطوري - 1/10</small><br><b style="color:#00ffff">200 SMC</b><br><button class="btn" style="background:#00ffff;color:#000;width:100%;margin-top:6px" onclick="buyNFT('Goal',200)">اشتري</button></div>
</div>
<div style="margin-top:10px;text-align:center"><small>🖼️ مجموعتك: <span id="nftCount">0</span> NFT | قيمتها: <span id="nftValue">0</span> SMC</small></div>
</div>
</div>

<div id="game" class="tab" style="display:none">
<div class="card beyond"><h3>🎮 لعبة BEYOND - اربح ShaamCoin!</h3>
<div id="gameBox"></div>
<div style="margin-top:12px;background:#000;padding:14px;border-radius:15px;border:3px solid #FFD700;text-align:center"><b>🎰 الجائزة الكبرى: <span id="jackpot">100,000$</span> + 10,000 SMC</b><br><small>1,847 لاعب - السحب الشهري على 100K$!</small><br><button class="btn" style="background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;width:100%;padding:15px;margin-top:8px;font-size:13px" onclick="joinJackpot()">🎰 ادخل السحب على 100K$ + NFT نادر!</button></div>
</div>
</div>

<div id="store" class="tab" style="display:none">
<div class="card beyond"><h3>💳 Web3 Store - دفع بلوكشين</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px">
<button class="btn" style="background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;padding:18px;border-radius:16px" onclick="buyReal('BEYOND VIP - 99.99$')">👑 BEYOND VIP<br><b>99.99$</b><br><small>Web3 + NFT هدية</small></button>
<button class="btn" style="background:linear-gradient(90deg,#627EEA,#00ffff);color:#000;padding:18px;border-radius:16px" onclick="buyReal('1000 SMC Pack - 299$')">🪙 1000 SMC<br><b>299$ خصم 30%</b><br><small>ترتفع لـ 10$!</small></button>
</div>
</div>
</div>

<div id="ai" class="tab" style="display:none"><div class="card beyond"><h3>🤖 AI BEYOND - يعلق + يتنبأ بالسعر!</h3><div id="aiBox" style="background:#000;padding:15px;border-radius:15px;border:3px solid #FFD700;height:360px;overflow-y:auto">⏳ AI يحلل البلوكشين...</div><div style="display:flex;gap:8px;margin-top:12px"><button class="btn" style="background:#FFD700;color:#000;flex:1;padding:14px" onclick="startAI()">🤖 شغّل AI</button><button class="btn" style="background:#F7931A;color:#000;flex:1;padding:14px" onclick="speakAI()">🔊 AI يتكلم!</button><button class="btn" style="background:#627EEA;color:#fff;flex:1;padding:14px" onclick="predictPrice()">📈 توقع سعر SMC</button></div></div></div>

<div id="videoModal" class="modal" onclick="closeVideo()"><div class="modal-box" onclick="event.stopPropagation()"><div style="display:flex;justify-content:space-between"><h3 id="videoTitle" style="color:#FFD700">🚀</h3><button onclick="closeVideo()" style="background:red;color:#fff;border:none;padding:10px 16px;border-radius:14px;font-weight:900">X</button></div><iframe id="videoFrame" class="video" allowfullscreen></iframe><div style="margin-top:14px;background:#000;padding:16px;border-radius:16px;border:3px solid #FFD700"><p id="commentary" style="font-weight:900;color:#FFD700;font-size:15px">🎙️</p><p id="aiLive" style="font-size:11px;color:#aaa;margin-top:8px">🤖 AI...</p><div style="margin-top:10px;background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;padding:10px;border-radius:12px;text-align:center;font-weight:900">🪙 +5 SMC هدية مشاهدة! | 💳 إعلان Web3 +2$</div><button class="btn" style="background:#00ffff;color:#000;width:100%;margin-top:10px;padding:12px" onclick="speakAI()">🔊 AI يتكلم + يعدّن!</button></div></div></div>

<div id="installBanner" class="install" onclick="showAPK()">🚀🪙📲 ثبّت V14 BEYOND - عملتك ShaamCoin + NFT + اربح 100K$ + Web3 Wallet!</div>
<audio id="goalSound" src="https://www.soundjay.com/human/sounds/man-shouting-goal-01.mp3" preload="auto"></audio>

<script>
let points=parseInt(localStorage.getItem('shaam_v14_points')||'0');
let money=parseInt(localStorage.getItem('shaam_v14_money')||'1000');
let coin=parseInt(localStorage.getItem('shaam_v14_coin')||'0');
let nft=parseInt(localStorage.getItem('shaam_v14_nft')||'0');
let vip=localStorage.getItem('shaam_v14_vip')||'عادي';
let allMatches=[]; let soundOn=false; let coinPrice=0.42;
document.getElementById('myPoints').innerText=points; document.getElementById('myMoney').innerText=money; document.getElementById('myCoin').innerText=coin; document.getElementById('myNft').innerText=nft; document.getElementById('myVip').innerText=vip;
document.getElementById('coinPrice').innerText=coinPrice;
let channels=["https://www.youtube.com/embed/jfKfPfyJRdk","https://www.youtube.com/embed/XqZsoesa55w","https://www.youtube.com/embed/dQw4w9WgXcQ","https://www.youtube.com/embed/9bZkp7q19f0","https://www.youtube.com/embed/5qap5aO4i9A","https://www.youtube.com/embed/jfKfPfyJRdk"];
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='game')loadGame();}
function switchChannel(i,el){document.getElementById('tvFrame').src=channels[i];}
async function loadMatches(){try{let r=await fetch('/api/live');let d=await r.json();allMatches=d.matches;document.getElementById('lastUpdate').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('count').innerText=d.matches.length+' مباراة';render(allMatches);if(soundOn){try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([800,100,800]);}catch(e){} money+=20;coin+=5;localStorage.setItem('shaam_v14_money',money);localStorage.setItem('shaam_v14_coin',coin);document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin; coinPrice+=0.001;document.getElementById('coinPrice').innerText=coinPrice.toFixed(3);}}catch(e){}}
function render(list){
 document.getElementById('matches').innerHTML=list.map(m=>{
  let isLive=m.minute.includes("'");let p1=Math.floor(Math.random()*3);let p2=Math.floor(Math.random()*2);
  return `<div class="card ${isLive?'live':''} ${m.league.includes('champions')?'beyond':''}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#111;padding:6px 14px;border-radius:18px;border:3px solid #FFD700;font-weight:900">${m.league}${m.league.includes('champions')?' 🏆🚀':''}</span>${isLive?`<span style="color:red;font-weight:900">🔴 ${m.minute} BEYOND</span>`:`<span>${m.status}</span>`}</div><div class="team"><span>🚀🪙 ${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div class="team"><span>🚀🪙 ${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div>${m.scorer?`<div style="background:linear-gradient(90deg,#FFD700,#F7931A);color:#000;padding:7px 16px;border-radius:30px;font-size:11px;font-weight:900;display:inline-block;margin:8px 0">⚽ ${m.scorer} | 🤖 AI: هدف BEYOND!</div>`:''}<div style="background:#111100;padding:12px;border-radius:16px;margin:10px 0;border:3px dashed #FFD700;font-weight:900">🎯 AI BEYOND: ${p1}-${p2} (${Math.floor(Math.random()*20+80)}%) <button class="btn" style="background:linear-gradient(90deg,#FFD700,#F7931A);color:#000" onclick="predict('${m.home} vs ${m.away}','${p1}-${p2}')">توقع +200$ +10 SMC</button></div><div style="display:flex;gap:4px;flex-wrap:wrap"><button class="btn" style="background:#FFD700;color:#000" onclick="toggleFav('${m.home}')">⭐</button><button class="btn" style="background:red;color:#fff" onclick="playVideo('${m.home} ${m.away} goal','${m.home} vs ${m.away}')">🎥 هدف</button><button class="btn" style="background:#F7931A;color:#000" onclick="mineCoin()">⛏️ عدّن +10 SMC</button><button class="btn" style="background:#25D366;color:#fff" onclick="shareWA('${m.home} ${m.score} ${m.away}')">📲</button></div></div>`;
 }).join('');
}
function loadGame(){let html=allMatches.slice(0,5).map(m=>{let a=Math.floor(Math.random()*4);let b=Math.floor(Math.random()*3);return `<div class=card><b>🚀 ${m.home} vs ${m.away}</b><br><div style="margin:12px 0;display:flex;gap:8px"><button class="btn" style="background:#111;color:#FFD700;border:3px solid #FFD700;padding:14px;flex:1;font-weight:900" onclick="predict('${m.home} vs ${m.away}','${a}-${b}')">${a}-${b} +10 SMC</button><button class="btn" style="background:#111;color:#00ffff;border:2px solid #00ffff;padding:14px;flex:1" onclick="predict('${m.home} vs ${m.away}','1-1')">1-1 +5 SMC</button></div></div>`}).join('');document.getElementById('gameBox').innerHTML=html||'⏳';}
function predict(match,pred){money+=200;points+=30;coin+=10;coinPrice+=0.002;localStorage.setItem('shaam_v14_money',money);localStorage.setItem('shaam_v14_points',points);localStorage.setItem('shaam_v14_coin',coin);document.getElementById('myMoney').innerText=money;document.getElementById('myPoints').innerText=points;document.getElementById('myCoin').innerText=coin;document.getElementById('coinPrice').innerText=coinPrice.toFixed(3);alert(`🚀🪙 توقعك: ${match} ${pred}\\n+200$ +10 SMC! سعر SMC الآن $${coinPrice.toFixed(3)} ↑\\n💰 رصيدك: ${money}$ | 🪙 ${coin} SMC`);if(navigator.vibrate)navigator.vibrate(150);}
function buyCoin(amount){let cost=amount*coinPrice;if(money<cost){alert('❌ رصيدك '+money+'$ ما يكفي! اجمع من التوقعات! سعر '+amount+' SMC = $'+cost.toFixed(2));return}money-=cost;coin+=amount;coinPrice+=amount*0.0001;localStorage.setItem('shaam_v14_money',money);localStorage.setItem('shaam_v14_coin',coin);document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin;document.getElementById('coinPrice').innerText=coinPrice.toFixed(3);alert(`✅ اشتريت ${amount} SMC بـ $${cost.toFixed(2)}! 🚀\\nسعر SMC ارتفع لـ $${coinPrice.toFixed(3)}!\\nرصيدك: ${coin} SMC = $${(coin*coinPrice).toFixed(2)}`);}
function mineCoin(){coin+=10;coinPrice+=0.001;localStorage.setItem('shaam_v14_coin',coin);document.getElementById('myCoin').innerText=coin;document.getElementById('coinPrice').innerText=coinPrice.toFixed(3);alert(`⛏️ عدّنت +10 SMC! 🪙\\nرصيدك: ${coin} SMC\\nسعر SMC: $${coinPrice.toFixed(3)} ↑\\nتعال كل 5 دقائق عدّن!`);if(navigator.vibrate)navigator.vibrate(200);}
function buyNFT(name,price){if(coin<price){alert('❌ ما عندك SMC كفاية! تحتاج '+price+' SMC، عندك '+coin);return}coin-=price;nft+=
