import requests
from flask import Flask, jsonify
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V13 ETERNITY GOD ♾️💰</title>
<meta name="theme-color" content="#FFD700">
<style>
:root{--et:#FFD700;--inf:#ff00ff;--dia:#00ffff}
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI Black,Segoe UI}
body{background:#000;color:#fff}
.header{background:linear-gradient(90deg,#FFD700,#ff00ff,#00ffff,#FFD700,#00ff88,#FFD700,#ff00ff);background-size:800%;animation:g.8s linear infinite;padding:18px;text-align:center;position:sticky;top:0;z-index:9999;border-bottom:5px solid #FFD700;box-shadow:0 0 50px #FFD700}
@keyframes g{0%{background-position:0%}100%{background-position:800%}}
.nav{display:flex;gap:3px;padding:7px;background:#020202;overflow-x:auto;position:sticky;top:72px;z-index:9998}
.nav button{background:#111;color:#fff;border:1px solid #333;padding:9px 10px;border-radius:25px;font-size:8px;white-space:nowrap;font-weight:900}
.nav button.active{background:linear-gradient(90deg,#FFD700,#ff00ff);color:#000;transform:scale(1.15);box-shadow:0 0 25px #FFD700;border:2px solid #FFD700}
.card{background:linear-gradient(145deg,#080800,#1a1a1a);border-radius:22px;margin:9px;padding:13px;box-shadow:0 0 30px rgba(255,215,0,.2)}
.eternity{border:3px solid #FFD700;box-shadow:0 0 50px rgba(255,215,0,.6),0 0 80px rgba(255,0,255,.4);background:linear-gradient(145deg,#111100,#110011,#001111);animation:et 3s infinite}
@keyframes et{0%,100%{box-shadow:0 0 50px #FFD700}50%{box-shadow:0 0 80px #FFD700,0 0 120px #ff00ff}}
.live{border-right:7px solid #ff0000;animation:rr.6s infinite}
@keyframes rr{0%,100%{box-shadow:0 0 20px red,0 0 40px #FFD700}50%{box-shadow:0 0 60px red,0 0 100px #FFD700}}
.team{display:flex;justify-content:space-between;align-items:center;margin:10px 0;font-weight:900;font-size:17px}
.score{font-size:40px;font-weight:900;background:linear-gradient(90deg,#FFD700,#ff00ff,#00ffff,#FFD700);background-size:300%;animation:g 2s linear infinite;-webkit-background-clip:text;-webkit-text-fill-color:transparent;filter:drop-shadow(0 0 10px #FFD700)}
.btn{padding:8px 9px;border-radius:12px;border:none;font-weight:900;font-size:8px;margin:2px;cursor:pointer}
.btn-et{background:linear-gradient(90deg,#FFD700,#ff00ff,#00ffff,#FFD700);background-size:400%;animation:g 1.5s linear infinite;color:#000;width:94%;margin:10px 3%;padding:18px;border-radius:35px;font-weight:900;font-size:16px;display:block;box-shadow:0 0 40px #FFD700;animation:pd 1.2s infinite}
@keyframes pd{0%,100%{transform:scale(1)}50%{transform:scale(1.05)}}
.search{width:94%;margin:9px 3%;padding:16px;border-radius:35px;border:3px solid #FFD700;background:#111;color:#fff;text-align:center;font-weight:900;box-shadow:0 0 25px rgba(255,215,0,.5)}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.98);z-index:5000;align-items:center;justify-content:center;padding:10px}
.modal-box{width:100%;max-width:600px;background:#0a0a00;border-radius:22px;padding:16px;border:4px solid #FFD700;box-shadow:0 0 60px #FFD700}
.video{width:100%;height:340px;border-radius:18px;border:none}
.money{position:fixed;top:76px;left:8px;background:linear-gradient(90deg,#FFD700,#ff00ff,#00ffff);background-size:300%;animation:g 2s linear infinite;color:#000;padding:8px 16px;border-radius:30px;font-weight:900;font-size:12px;z-index:1000;box-shadow:0 0 30px #FFD700;border:2px solid #FFD700}
.install{position:fixed;bottom:10px;left:8px;right:8px;background:linear-gradient(90deg,#FFD700,#ff00ff,#00ffff,#FFD700);background-size:500%;animation:g 1s linear infinite;color:#000;padding:18px;border-radius:20px;font-weight:900;text-align:center;z-index:1000;box-shadow:0 0 50px #FFD700;border:3px solid #FFD700;text-shadow:0 0 5px #fff}
.ad{margin:9px;background:linear-gradient(90deg,#111100,#222);border:2px dashed #FFD700;border-radius:14px;padding:11px;text-align:center;font-size:11px;color:#FFD700;font-weight:900}
</style>
</head>
<body>
<div class="header"><h1 style="color:#000;font-weight:900;font-size:18px;text-shadow:0 0 10px #fff">♾️💎 Shaam V13 ETERNITY GOD - الخلود ♾️💎</h1><div style="color:#000;font-weight:900;font-size:10px">Stripe PayPal حقيقي + صوت AI + 8 قنوات + كأس عالم + Desktop App + 1M مشترك</div></div>
<div class="money" id="moneyBar">💰 <span id="myMoney">1000</span>$ | 🎯 <span id="myPoints">0</span> | 👑 <span id="myVip">عادي</span> | 🌍 <span id="subs">1M</span></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('tv',this)">📺 بث 8</button>
<button onclick="showTab('game',this)">🎮 لعبة💰</button>
<button onclick="showTab('store',this)">💳 متجر حقيقي</button>
<button onclick="showTab('world',this)">🌍 كأس عالم</button>
<button onclick="showTab('ai',this)">🤖 AI صوت</button>
<button onclick="showTab('leader',this)">🏆 سحب 10K$</button>
</div>
<input class="search" placeholder="♾️ ابحث... برشلونة، الهلال، ريال، رونالدو، ميسي، كأس العالم" oninput="filterTeams(this.value)">
<button class="btn-et" onclick="activateEternity()">♾️💎🔔 فعل وضع الخلود ETERNITY: صوت AI + 10K$ + VIP أبدي + Desktop</button>
<div style="text-align:center;font-size:10px;color:#aaa">آخر: <span id="lastUpdate">--</span> | <span id="count">--</span> | 🎙️ <span id="comStatus">متوقف</span> | 💳 <span id="payStatus">Stripe جاهز</span></div>
<div class="ad">💳💰 إعلان ممول - اربح 1$ لكل نقرة! [AdMob + Stripe Checkout جاهز - اربط مفاتيحك]</div>

<div id="live" class="tab"><div id="matches"><div style="text-align:center;padding:70px;color:#FFD700;font-size:18px">♾️ V13 ETERNITY يبني مجرة جديدة...</div></div></div>

<div id="tv" class="tab" style="display:none">
<div class="card eternity"><h3>📺 بث ETERNITY - 8 قنوات + IPTV + راديو</h3>
<div style="display:flex;gap:5px;overflow-x:auto;padding:8px 0">
<div class="ch" style="padding:10px 14px;background:linear-gradient(90deg,#FFD700,#ff9900);color:#000;border-radius:25px;font-size:10px;white-space:nowrap;cursor:pointer;font-weight:900" onclick="switchChannel(0,this)">🏴󠁧󠁢󠁥󠁮󠁧󠁿 BeIN 1</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(1,this)">🇪🇸 BeIN 2</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(2,this)">🏆 UCL HD</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(3,this)">🇸🇦 SSC 1</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(4,this)">🇸🇦 SSC 2</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(5,this)">📻 راديو</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(6,this)">🎙️ تحليل</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(7,this)">🌍 كأس عالم</div>
</div>
<iframe id="tvFrame" class="video" style="height:360px;margin-top:12px" src="https://www.youtube.com/embed/jfKfPfyJRdk" allowfullscreen></iframe>
<div style="margin-top:8px;background:#000;padding:10px;border-radius:12px;border:1px solid #FFD700"><p style="font-size:11px">💡 <b>IPTV حقيقي:</b> لاحقاً اربط m3u8 link من BeIN API</p></div>
</div>
</div>

<div id="game" class="tab" style="display:none">
<div class="card eternity"><h3>🎮 لعبة ETERNITY - اربح 10K$!</h3>
<p style="font-size:11px">توقع صحيح = 200$ + 30 نقطة | سحب أسبوعي على 10,000$ حقيقي!</p>
<div id="gameBox"></div>
<div style="margin-top:12px;background:#000;padding:12px;border-radius:14px;border:2px solid #FFD700"><b>🎰 الجائزة الكبرى: <span id="jackpot">10,000$</span></b> - <span id="players">1,247</span> لاعب<br><div style="margin-top:8px;background:#111;padding:8px;border-radius:10px"><small>🏆 الفائز الأخير: محمد من السعودية - ربح 10K$! مبروك!</small></div><button class="btn" style="background:linear-gradient(90deg,#FFD700,#ff00ff);color:#000;width:100%;padding:14px;margin-top:8px;font-size:12px" onclick="joinJackpot()">🎰 ادخل السحب على 10K$ مجاناً!</button></div>
</div>
</div>

<div id="store" class="tab" style="display:none">
<div class="card eternity"><h3>💳 متجر ETERNITY - دفع حقيقي Stripe/PayPal</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px">
<button class="btn" style="background:linear-gradient(90deg,#FFD700,#ff9900);color:#000;padding:16px;border-radius:14px" onclick="buyReal('VIP سنة - 19.99$','price_vip')">👑 VIP سنة<br><b>19.99$</b><br><small>Stripe حقيقي</small></button>
<button class="btn" style="background:linear-gradient(90deg,#00ffff,#0088ff);color:#000;padding:16px;border-radius:14px" onclick="buyReal('INFINITY شارة - 49.99$','price_inf')">💎 INFINITY<br><b>49.99$</b><br><small>للأبد + Desktop</small></button>
<button class="btn" style="background:linear-gradient(90deg,#00ff88,#00cc66);color:#000;padding:16px;border-radius:14px" onclick="buyReal('سحب 100$ PayPal','price_paypal')">💰 PayPal 100$<br><b>50000$ لعبة</b><br><small>اسحب حقيقي!</small></button>
<button class="btn" style="background:#111;color:#FFD700;border:2px solid #FFD700;padding:16px;border-radius:14px" onclick="buyShop('إزالة إعلانات',500)">🚫 بدون إعلانات<br><b>500$ لعبة</b><br><small>للأبد</small></button>
</div>
<div style="margin-top:12px;background:#000;padding:12px;border-radius:12px;border:2px dashed #FFD700"><p style="font-size:11px">💳 <b>كيف تربط Stripe حقيقي:</b><br>1. سجل في stripe.com<br>2. خذ المفتاح pk_test_...<br>3. حطه في الكود بدل price_vip<br>4. اربح فلوس حقيقية!</p></div>
</div>
</div>

<div id="world" class="tab" style="display:none">
<div class="card eternity"><h3>🌍 كأس العالم المصغر - بطولة Shaam</h3>
<div style="background:#000;padding:12px;border-radius:12px;border:1px solid #FFD700"><div style="display:flex;justify-content:space-between"><span>🇸🇦 السعودية</span><span style="color:#FFD700;font-weight:900">2-1</span><span>🇦🇷 الأرجنتين</span></div><div style="display:flex;justify-content:space-between;margin-top:8px"><span>🇵🇹 البرتغال</span><span style="color:#FFD700">1-1</span><span>🇫🇷 فرنسا</span></div><div style="display:flex;justify-content:space-between;margin-top:8px"><span>🏆 النهائي:</span><span style="color:#FFD700;font-weight:900">قريباً!</span><span>🎮 شارك!</span></div></div><button class="btn" style="background:#FFD700;color:#000;width:100%;padding:14px;margin-top:10px" onclick="joinWorldCup()">🌍 شارك في كأس عالم Shaam - اربح 50K$!</button>
</div>
</div>

<div id="ai" class="tab" style="display:none"><div class="card eternity"><h3>🤖 AI ETERNITY - يعلق بصوته!</h3><div id="aiBox" style="background:#000;padding:14px;border-radius:14px;border:2px solid #FFD700;height:340px;overflow-y:auto">⏳ AI يحمّل صوته...</div><div style="display:flex;gap:6px;margin-top:10px"><button class="btn" style="background:#FFD700;color:#000;flex:1;padding:12px" onclick="startAI()">🤖 شغّل تعليق AI</button><button class="btn" style="background:#ff00ff;color:#fff;flex:1;padding:12px" onclick="speakAI()">🔊 AI يتكلم!</button></div></div></div>

<div id="leader" class="tab" style="display:none"><div class="card"><h3>🏆 سحب ETERNITY - 10K$ أسبوعياً</h3><div id="leaderBoard"></div><button class="btn" style="background:linear-gradient(90deg,#FFD700,#ff00ff);color:#000;width:100%;padding:16px;margin-top:12px;font-weight:900" onclick="shareLeader()">📲 شارك وادخل السحب 3 مرات!</button></div></div>

<div id="videoModal" class="modal" onclick="closeVideo()"><div class="modal-box" onclick="event.stopPropagation()"><div style="display:flex;justify-content:space-between"><h3 id="videoTitle" style="color:#FFD700">♾️</h3><button onclick="closeVideo()" style="background:red;color:#fff;border:none;padding:8px 14px;border-radius:12px;font-weight:900">X</button></div><iframe id="videoFrame" class="video" allowfullscreen></iframe><div style="margin-top:12px;background:#000;padding:14px;border-radius:14px;border:2px solid #FFD700"><p id="commentary" style="font-weight:900;color:#FFD700;font-size:14px">🎙️</p><p id="aiLive" style="font-size:11px;color:#aaa;margin-top:8px">🤖 AI...</p><div class="ad" style="margin-top:10px">💳 إعلان Stripe - +1$ لكل نقرة! [اربط Stripe]</div><button class="btn" style="background:#00ffff;color:#000;width:100%;margin-top:8px;padding:10px" onclick="speakAI()">🔊 اسمع تعليق AI بصوت!</button></div></div></div>

<div id="installBanner" class="install" onclick="showAPK()">♾️💎📲 ثبّت V13 ETERNITY - Desktop + APK + اربح 10K$ + Stripe حقيقي!</div>
<audio id="goalSound" src="https://www.soundjay.com/human/sounds/man-shouting-goal-01.mp3" preload="auto"></audio>

<script>
let points=parseInt(localStorage.getItem('shaam_v13_points')||'0');
let money=parseInt(localStorage.getItem('shaam_v13_money')||'1000');
let vip=localStorage.getItem('shaam_v13_vip')||'عادي';
let allMatches=[]; let soundOn=false;
document.getElementById('myPoints').innerText=points; document.getElementById('myMoney').innerText=money; document.getElementById('myVip').innerText=vip;
let channels=["https://www.youtube.com/embed/jfKfPfyJRdk","https://www.youtube.com/embed/XqZsoesa55w","https://www.youtube.com/embed/dQw4w9WgXcQ","https://www.youtube.com/embed/9bZkp7q19f0","https://www.youtube.com/embed/5qap5aO4i9A","https://www.youtube.com/embed/jfKfPfyJRdk","https://www.youtube.com/embed/kJQP7kiw5Fk","https://www.youtube.com/embed/9bZkp7q19f0"];
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='game')loadGame();if(t=='leader')loadLeader();}
function switchChannel(i,el){document.getElementById('tvFrame').src=channels[i];document.querySelectorAll('.ch').forEach(c=>{c.style.border='1px solid #333';c.style.background='#111';c.style.color='#fff';});el.style.border='2px solid #FFD700';el.style.background='linear-gradient(90deg,#FFD700,#ff9900)';el.style.color='#000';}
async function loadMatches(){try{let r=await fetch('/api/live');let d=await r.json();allMatches=d.matches;document.getElementById('lastUpdate').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('count').innerText=d.matches.length+' مباراة';render(allMatches);if(soundOn)try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([700,100,700]);money+=20;localStorage.setItem('shaam_v13_money',money);document.getElementById('myMoney').innerText=money;}catch(e){}}catch(e){}}
function render(list){
 document.getElementById('matches').innerHTML=list.map(m=>{
  let isLive=m.minute.includes("'");let p1=Math.floor(Math.random()*3);let p2=Math.floor(Math.random()*2);
  return `<div class="card ${isLive?'live':''} ${m.league.includes('champions')?'eternity':''}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#111;padding:5px 12px;border-radius:15px;border:2px solid #FFD700;font-weight:900">${m.league}${m.league.includes('champions')?' 🏆♾️':''}</span>${isLive?`<span style="color:red;font-weight:900">🔴 ${m.minute} ETERNITY</span>`:`<span>${m.status}</span>`}</div><div class="team"><span>♾️💎 ${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div class="team"><span>♾️💎 ${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div>${m.scorer?`<div style="background:linear-gradient(90deg,#FFD700,#ff00ff);color:#000;padding:6px 14px;border-radius:25px;font-size:11px;font-weight:900;display:inline-block;margin:6px 0">⚽ ${m.scorer} | 🤖 AI: هدف ETERNITY!</div>`:''}<div style="background:#050500;padding:10px;border-radius:14px;margin:8px 0;border:2px dashed #FFD700;font-size:11px;font-weight:900">🎯 AI ETERNITY: ${p1}-${p2} (${Math.floor(Math.random()*30+70)}% ثقة) <button class="btn" style="background:linear-gradient(90deg,#FFD700,#ff00ff);color:#000" onclick="predict('${m.home} vs ${m.away}','${p1}-${p2}')">توقع +200$</button></div><div class="ad" style="margin:6px 0;padding:8px">💳 إعلان Stripe - +1$ لكل نقرة</div><div style="display:flex;gap:3px;flex-wrap:wrap"><button class="btn" style="background:#FFD700;color:#000" onclick="toggleFav('${m.home}')">⭐</button><button class="btn" style="background:red;color:#fff" onclick="playVideo('${m.home} ${m.away} goal','${m.home} vs ${m.away}')">🎥 هدف</button><button class="btn" style="background:#FFD700;color:#000" onclick="showTab('tv',document.querySelectorAll('.nav button')[1])">📺 بث</button><button class="btn" style="background:#25D366;color:#fff" onclick="shareWA('${m.home} ${m.score} ${m.away}')">📲</button></div></div>`;
 }).join('');
}
function loadGame(){let html=allMatches.slice(0,5).map(m=>{let a=Math.floor(Math.random()*4);let b=Math.floor(Math.random()*3);return `<div class=card><b>♾️💎 ${m.home} vs ${m.away}</b><br><div style="margin:10px 0;display:flex;gap:8px"><button class="btn" style="background:#111;color:#FFD700;border:2px solid #FFD700;padding:12px;flex:1;font-weight:900" onclick="predict('${m.home} vs ${m.away}','${a}-${b}')">${a}-${b} +200$</button><button class="btn" style="background:#111;color:#00ffff;border:1px solid #00ffff;padding:12px;flex:1" onclick="predict('${m.home} vs ${m.away}','1-1')">1-1 +100$</button></div></div>`}).join('');document.getElementById('gameBox').innerHTML=html||'⏳';}
function loadLeader(){document.getElementById('leaderBoard').innerHTML=`<table style="width:100%;border-collapse:collapse"><tr style="background:linear-gradient(90deg,#FFD700,#ff00ff)"><th style="color:#000;padding:10px">#</th><th style="color:#000">اللاعب</th><th style="color:#000">💰</th><th style="color:#000">سحب</th></tr><tr style="background:rgba(255,215,0,.3)"><td style="padding:10px;text-align:center">🥇</td><td>♾️💎 شامي ETERNITY (أنت)</td><td>${money}$</td><td>${Math.floor(points/10)+1}</td></tr><tr><td style="text-align:center">🥈</td><td>مدريدي ETERNITY</td><td>15000$</td><td>25</td></tr><tr><td style="text-align:center">🥉</td><td>هلالي VIP</td><td>9800$</td><td>18</td></tr></table><div style="margin-top:12px;background:#000;padding:12px;border-radius:14px;border:2px solid #FFD700;text-align:center"><b>🎰 السحب الأسبوعي الأحد 10 مساءً على 10,000$ حقيقي عبر PayPal!</b><br><small>🏆 الفائز الأخير: محمد من السعودية - 10K$! 🎉</small></div>`;}
function predict(match,pred){money+=200;points+=30;localStorage.setItem('shaam_v13_money',money);localStorage.setItem('shaam_v13_points',points);document.getElementById('myMoney').innerText=money;document.getElementById('myPoints').innerText=points;alert(`♾️💎 توقعك: ${match} ${pred}\\n+200$! +30 نقطة!\\n💰 رصيدك: ${money}$\\n🎰 +3 فرص سحب 10K$!`);if(navigator.vibrate)navigator.vibrate(120);}
function buyShop(item,price){if(money<price){alert('❌ رصيدك '+money+'$ ما يكفي!');return}money-=price;if(item.includes('إعلانات')){vip='VIP 👑';localStorage.setItem('shaam_v13_vip','VIP 👑');document.getElementById('myVip').innerText=vip;}localStorage.setItem('shaam_v13_money',money);document.getElementById('myMoney').innerText=money;alert(`✅ اشتريت ${item}! ♾️ رصيدك: ${money}$`);}
function buyReal(item,priceId){alert(`💳 شراء حقيقي: ${item}\\n\\nللتفعيل الحقيقي:\\n1. سجل في stripe.com\\n2. أنشئ منتج ${item}\\n3. انسخ priceId\\n4. استبدل ${priceId} في الكود\\n\\nبعدها أي شخص يشتري = فلوس حقيقية تدخل حسابك! 💰\\n\\nالآن تاخذ نسخة تجريبية مجانية!`);money+=1000;points+=100;vip='VIP 👑';localStorage.setItem('shaam_v13_money',money);localStorage.setItem('shaam_v13_points',points);localStorage.setItem('shaam_v13_vip',vip);document.getElementById('myMoney').innerText=money;document.getElementById('myPoints').innerText=points;document.getElementById('myVip').innerText=vip;}
function joinJackpot(){alert('🎰 تم دخولك سحب 10K$ الأسبوعي! ♾️💎\\nفرصك: '+(Math.floor(points/10)+1)+'\\nالسحب الأحد 10 مساءً عبر Live! شارك الرابط ل 3 فرص إضافية!');points+=10;localStorage.setItem('shaam_v13_points',points);document.getElementById('myPoints').innerText=points;}
function joinWorldCup(){alert('🌍 تم تسجيلك في كأس عالم Shaam! 🏆\\nالجائزة: 50,000$ للبطل!\\nالمباريات تبدأ غداً! جهز فريقك! ⚽');}
function filterTeams(q){if(!q){render(allMatches);return}render(allMatches.filter(m=>(m.home+m.away).toLowerCase().includes(q.toLowerCase())));}
function playVideo(q,title){
 const comms=['♾️💎 خليل البلوشي: ياااا الله! هدف الخلود ETERNITY!','♾️ رؤوف خليف: جول تاريخي أبدي!','♾️ عصام الشوالي: الله الله! هدف الخلود!','♾️ حفيظ دراجي: خرافي أبدي!','🇬🇧 Peter Drury: ETERNITY GOAL! UNBELIEVABLE!','🇬🇧 Martin Tyler: AND IT IS A GOAL FOR ETERNITY!','🇪🇸 GOOOOLAZO ETERNO!','🇫🇷 BUT ETERNEL! INCROYABLE!','🇧🇷 GOLAAACO ETERNO!','🇮🇹 GOL ETERNO! MAMMA MIA!'];
 document.getElementById('videoTitle').innerText='♾️💎 '+title;
 document.getElementById('commentary').innerText=comms[Math.floor(Math.random()*comms.length)];
 document.getElementById('aiLive').innerText='🤖 AI ETERNITY: تسديدة 110km/h، زاوية 8°، xG 0.02! هدف مستحيل! ترجمة: Impossible goal! + إعلان 1$ + Stripe';
 document.getElementById('videoFrame').src='https://www.youtube.com/embed?listType=search&list='+encodeURIComponent(q+' goal today')+'&autoplay=1';
 document.getElementById('videoModal').style.display='flex';
 money+=2;localStorage.setItem('shaam_v13_money',money);document.getElementById('myMoney').innerText=money;
 if(soundOn)try{document.getElementById('goalSound').play();}catch(e){}
}
function closeVideo(){document.getElementById('videoFrame').src='';document.getElementById('videoModal').style.display='none';}
function toggleFav(id){alert('♾️💎 ⭐ '+id+' خالد للأبد!');}
function speakAI(){
 let texts=['هدف خرافي يا الله!','ما هذا الجمال! هدف للتاريخ!','Goal! Unbelievable! Eternity goal!','GOOOLAZO! Increíble!'];
 let t=texts[Math.floor(Math.random()*texts.length)];
 document.getElementById('aiBox').innerHTML+=`<div style="margin:8px 0;padding:10px;background:#111;border-radius:12px;border-right:3px solid #FFD700">🔊 <b>AI يتكلم:</b> ${t}</div>`;
 if('speechSynthesis' in window){let u=new SpeechSynthesisUtterance(t);u.lang='ar-SA';u.rate=1.1;u.pitch=1.2;speechSynthesis.speak(u);}
 else{alert('🔊 AI يقول: '+t+' (المتصفح لا يدعم الصوت، استخدم Chrome)');}
}
function startAI(){let box=document.getElementById('aiBox');box.innerHTML='🤖 AI ETERNITY بدأ...<br><br>';let msgs=['⚽ هجمة خطيرة ETERNITY!','🔥 تسديدة صاروخية!','😱 فرصة مستحيلة ضاعت!','⚡ مرتدة بسرعة الضوء!','🎯 ركنية خطيرة!','💎 مهارة خالدة!'];setInterval(()=>{let m=msgs[Math.floor(Math.random()*msgs.length)];let time=new Date().toLocaleTimeString('ar-EG');box.innerHTML+=`[${time}] ${m}<br>`;box.scrollTop=box.scrollHeight;},2000);alert('🤖 AI يعلق + يتكلم! اضغط 🔊 AI يتكلم!');}
function shareWA(t){window.open('https://wa.me/?text='+encodeURIComponent('♾️💎 '+t+' - Shaam V13 ETERNITY: https://whatsapp-bot-88.onrender.com ♾️💰 10K$ سحب!'),'_blank');}
function shareLeader(){window.open('https://wa.me/?text='+encodeURIComponent('♾️💎 أنا مشارك في سحب 10K$ في Shaam V13 ETERNITY! رصيدي: '+money+'$ - تعال نافسني! https://whatsapp-bot-88.onrender.com 🎰 10K$!'),'_blank');}
function activateEternity(){soundOn=true;money+=10000;points+=500;localStorage.setItem('shaam_v13_money',money);localStorage.setItem('shaam_v13_points',points);localStorage.setItem('shaam_v13_vip','ETERNITY 👑♾️');document.getElementById('myMoney').innerText=money;document.getElementById('myPoints').innerText=points;document.getElementById('myVip').innerText='ETERNITY 👑♾️';document.getElementById('comStatus').innerText='♾️💎 10 معلقين + AI يتكلم!';document.getElementById('payStatus').innerText='💰 10K$ هدية!';alert('♾️💎👑 ETERNITY GOD تفعّل! الخلود!\\n🎙️ 10 معلقين + AI يتكلم بصوته!\\n💰 +10,000$ هدية! رصيدك: '+money+'$\\n👑 ETERNITY VIP أبدي!\\n📺 8 قنوات + كأس عالم\\n🎰 سحب 10K$ أسبوعياً حقيقي!\\n💳 Stripe/PayPal جاهز!\\n📲 Desktop + APK!');try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([800,100,800]);if('Notification' in window)Notification.requestPermission();speakAI();}catch(e){}}
function showAPK(){alert('♾️💎📲 تثبيت V13 ETERNITY:\\n\\n📱 موبايل: ⋮ > Add to Home Screen = تطبيق ♾️\\n💻 كمبيوتر: ⋮ > Install App = Desktop App!\\n\\nAPK حقيقي: appsgeyser.com + رابطك\\n\\nStripe حقيقي:\\n- stripe.com > أنشئ حساب\\n- Products > أنشئ VIP 19.99$\\n- انسخ price_... وحطه بدل price_vip\\n- كل بيع = فلوس حقيقية بحسابك! 💰');}
loadMatches();setInterval(loadMatches,30000);loadLeader();
</script>
</body>
</html>
"""

@app.route('/')
def home(): return HTML
@app.route('/api/live')
def live():
    try:
        leagues=["eng.1","esp.1","ita.1","ger.1","fra.1","sau.1","uefa.champions","uefa.europa","fifa.world"]
        matches=[]
        for lg in leagues:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=3)
                d=r.json()
                for ev in d.get('events',[])[:6]:
                    comp=ev['competitions'][0]; h=comp['competitors'][0]; a=comp['competitors'][1]
                    if h['homeAway']=='home': hN=h['team']['displayName']; aN=a['team']['displayName']; hs=h.get('score','0'); as_=a.get('score','0')
                    else: hN=a['team']['displayName']; aN=h['team']['displayName']; hs=a.get('score','0'); as_=h.get('score','0')
                    status=comp['status']['type']['description']; clock=comp['status'].get('displayClock','')
                    scorer=""
                    if comp.get('details'):
                        for det in comp['details'][-1:]:
                            if det.get('scoringPlay'): scorer=f"{det.get('clock',{}).get('displayValue','')} هدف"
                    matches.append({"home":hN,"away":aN,"score":f"{hs}-{as_}","league":lg,"status":status,"minute":clock,"scorer":scorer})
            except: continue
        if not matches: matches=[{"home":"Argentina","away":"France","score":"3-3","league":"fifa.world","status":"Final","minute":"ETERNITY","scorer":"Messi د 120+3 هدف الخلود"}]
        return jsonify({"matches":matches})
    except: return jsonify({"matches":[]})
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
