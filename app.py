import requests
from flask import Flask, jsonify
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V12 INFINITY GOD ♾️💰</title>
<meta name="theme-color" content="#ff00ff">
<link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiU2hhYW0gVjEyIElORklOSVRZIiwic2hvcnRfbmFtZSI6IlNoYWFtIFYxMiIsInN0YXJ0X3VybCI6Ii8iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsImJhY2tncm91bmRfY29sb3IiOiIjMDAwMDAwIiwidGhlbWVfY29sb3IiOiIjZmYwMGZmIn0=">
<style>
:root{--inf:#ff00ff;--dia:#00ffff;--gold:#ffcc00}
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{background:#000;color:#fff}
.header{background:linear-gradient(90deg,#ff00ff,#00ffff,#ffcc00,#00ff88,#ff00ff,#ff00ff);background-size:600%;animation:g 1s linear infinite;padding:16px;text-align:center;position:sticky;top:0;z-index:999;border-bottom:4px solid #ff00ff;box-shadow:0 0 40px #ff00ff}
@keyframes g{0%{background-position:0%}100%{background-position:600%}}
.nav{display:flex;gap:3px;padding:6px;background:#050505;overflow-x:auto;position:sticky;top:68px;z-index:998}
.nav button{background:#111;color:#fff;border:1px solid #333;padding:8px 9px;border-radius:20px;font-size:8px;white-space:nowrap}
.nav button.active{background:linear-gradient(90deg,#ff00ff,#00ffff);color:#fff;font-weight:900;transform:scale(1.12);box-shadow:0 0 20px #ff00ff}
.card{background:linear-gradient(145deg,#080808,#1a1a1a);border:1px solid #222;border-radius:20px;margin:8px;padding:12px;box-shadow:0 0 25px rgba(255,0,255,.2)}
.infinity{border:2px solid #ff00ff;box-shadow:0 0 35px rgba(255,0,255,.6),0 0 60px rgba(0,255,255,.3);background:linear-gradient(145deg,#110011,#001111)}
.live{border-right:6px solid #ff0000;animation:rr 0.8s infinite}
@keyframes rr{0%,100%{box-shadow:0 0 15px red,0 0 30px #ff00ff}50%{box-shadow:0 0 40px red,0 0 80px #ff00ff}}
.team{display:flex;justify-content:space-between;align-items:center;margin:9px 0;font-weight:900;font-size:16px}
.score{font-size:36px;font-weight:900;background:linear-gradient(90deg,#ff00ff,#00ffff,#ffcc00);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-shadow:0 0 20px #ff00ff}
.btn{padding:7px 8px;border-radius:11px;border:none;font-weight:900;font-size:8px;margin:2px;cursor:pointer}
.btn-inf{background:linear-gradient(90deg,#ff00ff,#00ffff,#ffcc00);color:#000;width:94%;margin:8px 3%;padding:16px;border-radius:30px;font-weight:900;font-size:15px;display:block;box-shadow:0 0 35px #ff00ff;animation:pd 1.5s infinite}
@keyframes pd{0%,100%{transform:scale(1)}50%{transform:scale(1.04)}}
.search{width:94%;margin:8px 3%;padding:15px;border-radius:30px;border:2px solid #ff00ff;background:#111;color:#fff;text-align:center;font-weight:bold;box-shadow:0 0 20px rgba(255,0,255,.4)}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.97);z-index:3000;align-items:center;justify-content:center;padding:10px}
.modal-box{width:100%;max-width:580px;background:#0a0a0a;border-radius:20px;padding:15px;border:3px solid #ff00ff;box-shadow:0 0 50px #ff00ff}
.video{width:100%;height:320px;border-radius:16px;border:none}
.money{position:fixed;top:72px;left:8px;background:linear-gradient(90deg,#ff00ff,#00ffff,#ffcc00);color:#000;padding:7px 14px;border-radius:25px;font-weight:900;font-size:11px;z-index:1000;box-shadow:0 0 20px #ff00ff;animation:pd 2s infinite}
.install{position:fixed;bottom:10px;left:8px;right:8px;background:linear-gradient(90deg,#ff00ff,#00ffff,#ffcc00,#ff00ff);background-size:400%;animation:g 1.5s linear infinite;color:#fff;padding:16px;border-radius:18px;font-weight:900;text-align:center;z-index:1000;box-shadow:0 0 40px #ff00ff;text-shadow:0 0 10px #000}
.ad{margin:8px;background:linear-gradient(90deg,#111,#222);border:1px dashed #ff00ff;border-radius:12px;padding:10px;text-align:center;font-size:11px;color:#aaa}
</style>
</head>
<body>
<div class="header"><h1 style="color:#fff;font-weight:900;font-size:16px;text-shadow:0 0 15px #000">♾️ Shaam V12 INFINITY GOD - MONEY UNIVERSE ♾️</h1><div style="color:#fff;font-weight:900;font-size:9px">AdMob + PayPal + 6 قنوات + VIP + سحب يومي 1000$ + 10 معلقين + AI</div></div>
<div class="money" id="moneyBar">💰 <span id="myMoney">1000</span>$ | 🎯 <span id="myPoints">0</span> | 👑 <span id="myVip">عادي</span></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('tv',this)">📺 بث 6</button>
<button onclick="showTab('game',this)">🎮 لعبة💰</button>
<button onclick="showTab('store',this)">🛒 متجر PayPal</button>
<button onclick="showTab('ai',this)">🤖 AI</button>
<button onclick="showTab('leader',this)">🏆 سحب</button>
<button onclick="showTab('chat',this)">💬 دردشة</button>
</div>
<input class="search" placeholder="♾️ ابحث... برشلونة، الهلال، ريال، رونالدو، ميسي" oninput="filterTeams(this.value)">
<button class="btn-inf" onclick="activateInfinity()">♾️🔔 فعل وضع INFINITY: 10 معلقين + 1000$ + VIP مجاني + تثبيت + سحب</button>
<div style="text-align:center;font-size:10px;color:#aaa">آخر: <span id="lastUpdate">--</span> | <span id="count">--</span> | 🎙️ <span id="comStatus">متوقف</span> | 💰 إعلانات: <span id="adStatus">نشطة</span></div>
<div class="ad">📢 إعلان AdMob - كل مشاهدة +0.10$ لك! 💰 [مساحة إعلانية - اربط AdMob لاحقاً]</div>

<div id="live" class="tab"><div id="matches"><div style="text-align:center;padding:60px;color:#ff00ff">♾️ V12 INFINITY يحمّل الكون والمال...</div></div></div>

<div id="tv" class="tab" style="display:none">
<div class="card infinity"><h3>📺 بث INFINITY - 6 قنوات + راديو</h3>
<div style="display:flex;gap:5px;overflow-x:auto;padding:6px 0">
<div class="ch active" style="padding:8px 12px;background:#111;border:2px solid #ff00ff;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(0,this)">🏴󠁧󠁢󠁥󠁮󠁧󠁿 BeIN 1</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(1,this)">🇪🇸 BeIN 2</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(2,this)">🏆 UCL HD</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(3,this)">🇸🇦 SSC</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(4,this)">📻 راديو</div>
<div class="ch" style="padding:8px 12px;background:#111;border:1px solid #333;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer" onclick="switchChannel(5,this)">🎙️ تحليل</div>
</div>
<iframe id="tvFrame" class="video" style="height:340px;margin-top:10px" src="https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0" allowfullscreen></iframe>
</div>
</div>

<div id="game" class="tab" style="display:none">
<div class="card infinity"><h3>🎮 لعبة التوقع - اربح فلوس حقيقية!</h3>
<p style="font-size:11px;color:#aaa">توقع صحيح = 100$ + 20 نقطة | سحب يومي على 1000$!</p>
<div id="gameBox"></div>
<div style="margin-top:10px;background:#000;padding:10px;border-radius:12px;border:1px solid #ff00ff"><b>🎰 سحب اليوم:</b> <span id="jackpot">1000$</span> - <span id="players">234</span> لاعب مشارك<br><button class="btn" style="background:linear-gradient(90deg,#ff00ff,#ffcc00);color:#000;width:100%;padding:12px;margin-top:6px" onclick="joinJackpot()">🎰 ادخل السحب مجاناً - 1000$!</button></div>
</div>
</div>

<div id="store" class="tab" style="display:none">
<div class="card infinity"><h3>🛒 متجر INFINITY - PayPal + VIP</h3>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px">
<button class="btn" style="background:#222;color:#ff00ff;border:2px solid #ff00ff;padding:14px" onclick="buyShop('VIP شهر',500)">👑 VIP شهر<br>500$<br><small>بدون إعلانات + شارة</small></button>
<button class="btn" style="background:#222;color:#00ffff;border:2px solid #00ffff;padding:14px" onclick="buyShop('ألماس',1000)">💎 شارة INFINITY<br>1000$<br><small>شارة أبدية</small></button>
<button class="btn" style="background:#222;color:#ffcc00;border:2px solid #ffcc00;padding:14px" onclick="buyShop('PayPal 10$',10000)">💰 PayPal 10$<br>10000$ لعبة<br><small>اسحب فلوس حقيقية!</small></button>
<button class="btn" style="background:#222;color:#00ff88;border:2px solid #00ff88;padding:14px" onclick="buyShop('إزالة إعلانات',300)">🚫 إزالة إعلانات<br>300$<br><small>للأبد</small></button>
</div>
<p style="font-size:10px;color:#aaa;margin-top:10px">* الفلوس داخل اللعبة - لربط PayPal الحقيقي تواصل معي بعد V12</p>
</div>
</div>

<div id="ai" class="tab" style="display:none"><div class="card infinity"><h3>🤖 AI INFINITY يعلق + يترجم</h3><div id="aiBox" style="background:#000;padding:12px;border-radius:12px;border:1px solid #ff00ff;height:300px;overflow-y:auto">⏳ AI يحلل...</div><button class="btn" style="background:#ff00ff;color:#fff;width:100%;padding:12px;margin-top:8px" onclick="startAI()">🤖 شغّل AI + ترجمة</button></div></div>

<div id="leader" class="tab" style="display:none"><div class="card"><h3>🏆 سحب INFINITY - 1000$ يومياً</h3><div id="leaderBoard"></div><button class="btn" style="background:linear-gradient(90deg,#ff00ff,#00ffff);color:#fff;width:100%;padding:14px;margin-top:10px" onclick="shareLeader()">📲 شارك وادخل السحب مرتين!</button></div></div>
<div id="chat" class="tab" style="display:none"><div class="card"><h3>💬 دردشة INFINITY</h3><div id="chatBox" style="height:320px;overflow-y:auto;background:#000;border-radius:12px;padding:8px;border:1px solid #ff00ff"><div style="background:#111;padding:6px 10px;border-radius:12px;margin:4px 0;font-size:12px;border-right:3px solid #ff00ff">♾️ <b>شامي INFINITY:</b> V12 وصل!</div></div><div style="display:flex;gap:6px;margin-top:8px"><input id="chatInput" placeholder="اكتب..." style="flex:1;padding:10px;border-radius:20px;background:#222;color:#fff;border:1px solid #444"><button onclick="sendChat()" style="background:#ff00ff;color:#fff;border:none;padding:10px 15px;border-radius:20px;font-weight:900">إرسال</button></div></div></div>

<div id="videoModal" class="modal" onclick="closeVideo()"><div class="modal-box" onclick="event.stopPropagation()"><div style="display:flex;justify-content:space-between"><h3 id="videoTitle" style="color:#ff00ff">♾️</h3><button onclick="closeVideo()" style="background:red;color:#fff;border:none;padding:6px 12px;border-radius:10px">X</button></div><iframe id="videoFrame" class="video" allowfullscreen></iframe><div style="margin-top:10px;background:#000;padding:12px;border-radius:12px;border:1px solid #ff00ff"><p id="commentary" style="font-weight:900;color:#ff00ff">🎙️</p><p id="aiLive" style="font-size:11px;color:#aaa;margin-top:6px">🤖 AI...</p><div class="ad" style="margin-top:8px">📢 إعلان - +0.10$ بعد المشاهدة 💰</div></div></div></div>

<div id="installBanner" class="install" onclick="showAPK()">♾️📲 ثبّت V12 INFINITY - يصير تطبيق + اصنع APK + اربح 1000$ يومياً!</div>
<audio id="goalSound" src="https://www.soundjay.com/human/sounds/man-shouting-goal-01.mp3" preload="auto"></audio>

<script>
let points=parseInt(localStorage.getItem('shaam_v12_points')||'0');
let money=parseInt(localStorage.getItem('shaam_v12_money')||'1000');
let vip=localStorage.getItem('shaam_v12_vip')||'عادي';
let allMatches=[]; let soundOn=false;
document.getElementById('myPoints').innerText=points; document.getElementById('myMoney').innerText=money; document.getElementById('myVip').innerText=vip;
let channels=["https://www.youtube.com/embed/jfKfPfyJRdk","https://www.youtube.com/embed/XqZsoesa55w","https://www.youtube.com/embed/dQw4w9WgXcQ","https://www.youtube.com/embed/9bZkp7q19f0","https://www.youtube.com/embed/5qap5aO4i9A","https://www.youtube.com/embed/jfKfPfyJRdk"];
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='game')loadGame();if(t=='leader')loadLeader();}
function switchChannel(i,el){document.getElementById('tvFrame').src=channels[i];document.querySelectorAll('.ch').forEach(c=>{c.style.border='1px solid #333';c.style.background='#111';});el.style.border='2px solid #ff00ff';el.style.background='rgba(255,0,255,.2)';}
async function loadMatches(){try{let r=await fetch('/api/live');let d=await r.json();allMatches=d.matches;document.getElementById('lastUpdate').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('count').innerText=d.matches.length+' مباراة';render(allMatches);if(soundOn)try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([500,100,500]);money+=10;localStorage.setItem('shaam_v12_money',money);document.getElementById('myMoney').innerText=money;}catch(e){}}catch(e){}}
function render(list){
 document.getElementById('matches').innerHTML=list.map(m=>{
  let isLive=m.minute.includes("'");let p1=Math.floor(Math.random()*3);let p2=Math.floor(Math.random()*2);
  return `<div class="card ${isLive?'live':''} ${m.league.includes('champions')?'infinity':''}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#111;padding:4px 10px;border-radius:12px;border:1px solid #ff00ff">${m.league}${m.league.includes('champions')?' 🏆':''}</span>${isLive?`<span style="color:red;font-weight:900">🔴 ${m.minute} ♾️</span>`:`<span>${m.status}</span>`}</div><div class="team"><span>♾️ ${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div class="team"><span>♾️ ${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div>${m.scorer?`<div style="background:linear-gradient(90deg,#ff00ff,#00ffff);color:#fff;padding:5px 12px;border-radius:20px;font-size:11px;font-weight:900;display:inline-block;margin:4px 0">⚽ ${m.scorer} | 🤖 AI: هدف!</div>`:''}<div style="background:#050505;padding:8px;border-radius:12px;margin:6px 0;border:1px dashed #ff00ff;font-size:11px">🎯 AI: ${p1}-${p2} (${Math.floor(Math.random()*40+60)}%) <button class="btn" style="background:linear-gradient(90deg,#ff00ff,#00ffff);color:#fff" onclick="predict('${m.home} vs ${m.away}','${p1}-${p2}')">توقع +100$</button></div><div class="ad" style="margin:4px 0;padding:6px">📢 إعلان +0.10$</div><div style="display:flex;gap:3px;flex-wrap:wrap"><button class="btn" style="background:#ff00ff;color:#fff" onclick="toggleFav('${m.home}')">⭐</button><button class="btn" style="background:red;color:#fff" onclick="playVideo('${m.home} ${m.away} goal','${m.home} vs ${m.away}')">🎥 هدف</button><button class="btn" style="background:#ffcc00;color:#000" onclick="showTab('tv',document.querySelectorAll('.nav button')[1])">📺 بث</button><button class="btn" style="background:#333;color:#fff" onclick="addChat('يشجع ${m.home} ♾️')">💬</button><button class="btn" style="background:#25D366;color:#fff" onclick="shareWA('${m.home} ${m.score} ${m.away}')">📲</button></div></div>`;
 }).join('');
}
function loadGame(){let html=allMatches.slice(0,5).map(m=>{let a=Math.floor(Math.random()*4);let b=Math.floor(Math.random()*3);return `<div class=card><b>♾️ ${m.home} vs ${m.away}</b><br><div style="margin:8px 0;display:flex;gap:6px"><button class="btn" style="background:#111;color:#ff00ff;border:2px solid #ff00ff;padding:10px;flex:1" onclick="predict('${m.home} vs ${m.away}','${a}-${b}')">${a}-${b} +100$</button><button class="btn" style="background:#111;color:#00ffff;border:1px solid #00ffff;padding:10px;flex:1" onclick="predict('${m.home} vs ${m.away}','1-1')">1-1 +50$</button></div></div>`}).join('');document.getElementById('gameBox').innerHTML=html||'⏳';}
function loadLeader(){document.getElementById('leaderBoard').innerHTML=`<table style="width:100%;border-collapse:collapse"><tr style="background:linear-gradient(90deg,#ff00ff,#00ffff)"><th style="color:#fff;padding:8px">#</th><th style="color:#fff">اللاعب</th><th style="color:#fff">💰</th><th style="color:#fff">فرص سحب</th></tr><tr style="background:rgba(255,0,255,.2)"><td style="padding:8px;text-align:center">🥇</td><td>♾️ شامي INFINITY (أنت)</td><td>${money}$</td><td>${Math.floor(points/10)+1}</td></tr><tr><td style="text-align:center">🥈</td><td>مدريدي</td><td>5000$</td><td>12</td></tr><tr><td style="text-align:center">🥉</td><td>هلالي</td><td>3200$</td><td>8</td></tr></table><div style="margin-top:10px;background:#000;padding:10px;border-radius:12px;border:1px solid #ff00ff;text-align:center"><b>🎰 السحب اليوم الساعة 10 مساءً على 1000$ حقيقي!</b><br><small>كل 10 نقاط = فرصة سحب إضافية</small></div>`;}
function predict(match,pred){money+=100;points+=20;localStorage.setItem('shaam_v12_money',money);localStorage.setItem('shaam_v12_points',points);document.getElementById('myMoney').innerText=money;document.getElementById('myPoints').innerText=points;addChat(`توقعت ${match} ${pred} ♾️ +100$`);alert(`♾️ توقعك: ${match} ${pred}\\n+100$! +20 نقطة!\\n💰 رصيدك: ${money}$\\n🎰 فرصة سحب إضافية!`);if(navigator.vibrate)navigator.vibrate(100);}
function buyShop(item,price){if(money<price){alert('❌ رصيدك '+money+'$ ما يكفي! اجمع من التوقعات!');return}money-=price;if(item.includes('VIP')){vip='VIP 👑';localStorage.setItem('shaam_v12_vip','VIP 👑');document.getElementById('myVip').innerText=vip;}localStorage.setItem('shaam_v12_money',money);document.getElementById('myMoney').innerText=money;alert(`✅ اشتريت ${item} ♾️!\\nرصيدك: ${money}$`);}
function joinJackpot(){alert('🎰 تم دخولك سحب 1000$ اليوم! ♾️\\nفرصك: '+(Math.floor(points/10)+1)+'\\nالسحب 10 مساءً! شارك الرابط لفرصة إضافية!');points+=5;localStorage.setItem('shaam_v12_points',points);document.getElementById('myPoints').innerText=points;}
function filterTeams(q){if(!q){render(allMatches);return}render(allMatches.filter(m=>(m.home+m.away).toLowerCase().includes(q.toLowerCase())));}
function playVideo(q,title){
 const comms=['♾️ خليل البلوشي: ياااا الله! هدف INFINITY!','♾️ رؤوف خليف: جول تاريخي!','♾️ عصام الشوالي: الله الله!','♾️ حفيظ دراجي: خرافي!','♾️ عامر الخوذيري: عالمي!','♾️ فهد العتيبي: هدف!','♾️ علي الكعبي: جووول!','🇬🇧 Peter Drury: WHAT A GOAL!','🇬🇧 Martin Tyler: AND IT IS A GOAL!','🇪🇸 Español: GOOOOLAZO!'];
 document.getElementById('videoTitle').innerText='♾️ '+title;
 document.getElementById('commentary').innerText=comms[Math.floor(Math.random()*comms.length)];
 document.getElementById('aiLive').innerText='🤖 AI: تسديدة 102km/h، زاوية 12°، نسبة الهدف 8% فقط! هدف مستحيل! ترجمة: Incredible goal! + إعلان 0.10$';
 document.getElementById('videoFrame').src='https://www.youtube.com/embed?listType=search&list='+encodeURIComponent(q+' goal today')+'&autoplay=1';
 document.getElementById('videoModal').style.display='flex';
 money+=1;localStorage.setItem('shaam_v12_money',money);document.getElementById('myMoney').innerText=money;
 if(soundOn)try{document.getElementById('goalSound').play();}catch(e){}
}
function closeVideo(){document.getElementById('videoFrame').src='';document.getElementById('videoModal').style.display='none';}
function toggleFav(id){alert('♾️ ⭐ '+id+' ألماسي!');}
function sendChat(){let inp=document.getElementById('chatInput');if(!inp.value)return;addChat(inp.value);inp.value='';}
function addChat(txt){let box=document.getElementById('chatBox');box.innerHTML+=`<div style="background:#111;padding:6px 10px;border-radius:12px;margin:4px 0;font-size:12px;border-right:3px solid #ff00ff">👤 <b>أنت ♾️:</b> ${txt}</div>`;box.scrollTop=box.scrollHeight;}
function shareWA(t){window.open('https://wa.me/?text='+encodeURIComponent('♾️ '+t+' - Shaam V12 INFINITY: https://whatsapp-bot-88.onrender.com ♾️💰'),'_blank');}
function shareLeader(){window.open('https://wa.me/?text='+encodeURIComponent('♾️ أنا مشارك في سحب 1000$ يومياً في Shaam V12 INFINITY! رصيدي: '+money+'$ - تعال نافسني! https://whatsapp-bot-88.onrender.com 🎰'),'_blank');}
function activateInfinity(){soundOn=true;money+=1000;points+=100;localStorage.setItem('shaam_v12_money',money);localStorage.setItem('shaam_v12_points',points);localStorage.setItem('shaam_v12_vip','VIP 👑');document.getElementById('myMoney').innerText=money;document.getElementById('myPoints').innerText=points;document.getElementById('myVip').innerText='VIP 👑';document.getElementById('comStatus').innerText='♾️ 10 معلقين!';document.getElementById('adStatus').innerText='💰 1000$ هدية!';alert('♾️👑 INFINITY GOD تفعّل!\\n🎙️ 10 معلقين\\n💰 +1000$ هدية! رصيدك: '+money+'$\\n👑 VIP مجاني للأبد!\\n📺 6 قنوات\\n🎰 سحب 1000$ يومياً\\n📲 ثبّت التطبيق!');try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([600,100,600]);if('Notification' in window)Notification.requestPermission();}catch(e){}}
function showAPK(){alert('♾️📲 تثبيت V12 INFINITY:\\n\\n1. اضغط ⋮ فوق\\n2. Add to Home Screen / تثبيت\\n3. يصير أيقونة ♾️ بجوالك!\\n\\nلصنع APK حقيقي:\\n- روح appsgeyser.com\\n- حط رابطك: https://whatsapp-bot-88.onrender.com\\n- حمّل APK وبيعه!\\n\\nلربح فلوس حقيقية:\\n- اربط AdMob في الكود\\n- كل مشاهدة إعلان = 0.10$ لك!');}
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
        leagues=["eng.1","esp.1","ita.1","ger.1","fra.1","sau.1","uefa.champions","uefa.europa"]
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
        if not matches: matches=[{"home":"Real Madrid","away":"Man City","score":"4-3","league":"uefa.champions","status":"In Progress","minute":"90+3'","scorer":"Vinicius د 93 هدف INFINITY"}]
        return jsonify({"matches":matches})
    except: return jsonify({"matches":[]})
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
