import requests
from flask import Flask, jsonify
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V11 DIAMOND GOD 💎</title>
<style>
:root{--dia:#00ffff;--gold:#ffcc00;--green:#00ff88}
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{background:#000;color:#fff}
.header{background:linear-gradient(90deg,#00ffff,#ffcc00,#ff00ff,#00ffff,#00ff88,#00ffff);background-size:500%;animation:g 1.5s linear infinite;padding:15px;text-align:center;position:sticky;top:0;z-index:999;border-bottom:4px solid #00ffff;box-shadow:0 0 30px #00ffff}
@keyframes g{0%{background-position:0%}100%{background-position:500%}}
.nav{display:flex;gap:3px;padding:6px;background:#050505;overflow-x:auto;position:sticky;top:65px;z-index:998}
.nav button{background:#111;color:#fff;border:1px solid #333;padding:8px 9px;border-radius:20px;font-size:9px;white-space:nowrap}
.nav button.active{background:linear-gradient(90deg,#00ffff,#ffcc00);color:#000;font-weight:900;transform:scale(1.1);box-shadow:0 0 15px #00ffff}
.card{background:linear-gradient(145deg,#0a0a0a,#1a1a1a);border:1px solid #222;border-radius:18px;margin:8px;padding:12px;box-shadow:0 0 20px rgba(0,255,255,.15)}
.diamond{border:2px solid #00ffff;box-shadow:0 0 30px rgba(0,255,255,.5);background:linear-gradient(145deg,#001111,#111)}
.live{border-right:5px solid #ff0000;animation:rr 1s infinite}
@keyframes rr{0%,100%{box-shadow:0 0 10px red}50%{box-shadow:0 0 30px red,0 0 50px #00ffff}}
.team{display:flex;justify-content:space-between;align-items:center;margin:8px 0;font-weight:bold;font-size:15px}
.score{font-size:32px;font-weight:900;color:#00ffff;text-shadow:0 0 15px #00ffff,0 0 30px #ffcc00}
.btn{padding:7px 8px;border-radius:10px;border:none;font-weight:900;font-size:9px;margin:2px;cursor:pointer}
.btn-dia{background:linear-gradient(90deg,#00ffff,#ffcc00);color:#000;width:94%;margin:8px 3%;padding:15px;border-radius:25px;font-weight:900;font-size:15px;display:block;box-shadow:0 0 25px #00ffff;animation:pd 2s infinite}
@keyframes pd{0%,100%{transform:scale(1);box-shadow:0 0 20px #00ffff}50%{transform:scale(1.03);box-shadow:0 0 40px #00ffff}}
.search{width:94%;margin:8px 3%;padding:14px;border-radius:25px;border:2px solid #00ffff;background:#111;color:#fff;text-align:center;font-weight:bold;box-shadow:0 0 15px rgba(0,255,255,.3)}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.97);z-index:3000;align-items:center;justify-content:center;padding:10px}
.modal-box{width:100%;max-width:550px;background:#0a0a0a;border-radius:18px;padding:15px;border:3px solid #00ffff;box-shadow:0 0 40px #00ffff}
.video{width:100%;height:300px;border-radius:14px;border:none}
.channel{display:flex;gap:6px;overflow-x:auto;padding:6px 0}
.ch{padding:8px 12px;background:#111;border:2px solid #222;border-radius:20px;font-size:10px;white-space:nowrap;cursor:pointer}
.ch.active{border-color:#00ffff;background:rgba(0,255,255,.2);color:#00ffff;font-weight:900}
.money{position:fixed;top:70px;left:10px;background:linear-gradient(90deg,#00ff88,#00ffff);color:#000;padding:6px 12px;border-radius:20px;font-weight:900;font-size:11px;z-index:999;box-shadow:0 0 15px #00ff88}
.install{position:fixed;bottom:10px;left:8px;right:8px;background:linear-gradient(90deg,#00ffff,#ffcc00,#00ffff);background-size:300%;animation:g 2s linear infinite;color:#000;padding:15px;border-radius:16px;font-weight:900;text-align:center;z-index:1000;box-shadow:0 0 30px #00ffff}
</style>
</head>
<body>
<div class="header"><h1 style="color:#000;font-weight:900;font-size:16px">💎 Shaam V11 DIAMOND GOD - THE FINAL UNIVERSE 💎</h1><div style="color:#000;font-weight:900;font-size:9px">بث مباشر 4 قنوات + APK + متجر + 8 معلقين + ذكاء يعلق لحظياً</div></div>
<div class="money" id="money">💰 <span id="myMoney">1000</span> $ | 🎯 <span id="myPoints2">0</span> نقطة</div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('tv',this)">📺 بث</button>
<button onclick="showTab('game',this)">🎮 لعبة+متجر</button>
<button onclick="showTab('ucl',this)">🏆 أبطال</button>
<button onclick="showTab('ai',this)">🤖 AI يعلق</button>
<button onclick="showTab('leader',this)">🏅 أبطال</button>
<button onclick="showTab('chat',this)">💬 دردشة</button>
</div>
<input class="search" placeholder="💎 ابحث... برشلونة، الهلال، ريال، ليفربول، رونالدو" oninput="filterTeams(this.value)">
<button class="btn-dia" onclick="activateDiamond()">💎🔔 فعل وضع الألماس: 8 معلقين + بث مباشر + 100$ هدية + APK</button>
<div style="text-align:center;font-size:10px;color:#aaa">آخر: <span id="lastUpdate">--</span> | <span id="count">--</span> | 🎙️ <span id="comStatus">متوقف</span> | 📺 <span id="tvStatus">4 قنوات جاهزة</span></div>

<div id="live" class="tab"><div id="matches"><div style="text-align:center;padding:50px;color:#00ffff">💎 V11 DIAMOND يحمّل الكون كله...</div></div></div>

<div id="tv" class="tab" style="display:none">
<div class="card diamond"><h3>📺 بث مباشر DIAMOND - 4 قنوات</h3>
<div class="channel">
<div class="ch active" onclick="switchChannel(0,this)">🏴󠁧󠁢󠁥󠁮󠁧󠁿 BeIN 1</div><div class="ch" onclick="switchChannel(1,this)">🇪🇸 BeIN 2</div><div class="ch" onclick="switchChannel(2,this)">🏆 UCL HD</div><div class="ch" onclick="switchChannel(3,this)">🇸🇦 SSC</div>
</div>
<iframe id="tvFrame" class="video" style="height:320px;margin-top:10px" src="https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0" allowfullscreen></iframe>
<div style="margin-top:8px;font-size:10px;color:#aaa">* بث تجريبي - اضغط القنوات للتبديل - البث الحقيقي قريباً</div>
</div>
</div>

<div id="game" class="tab" style="display:none">
<div class="card diamond"><h3>🎮 لعبة التوقع + متجر DIAMOND</h3>
<p style="font-size:11px">توقع صح = 50$ + 10 نقاط | اشتري: شارة VIP، إزالة إعلانات</p>
<div id="gameBox"></div>
<div style="margin-top:12px;border-top:1px solid #222;padding-top:10px">
<h4>🛒 متجر DIAMOND</h4>
<button class="btn" style="background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;padding:10px;width:48%" onclick="buyShop('VIP',200)">👑 VIP - 200$</button>
<button class="btn" style="background:#222;color:#00ffff;border:1px solid #00ffff;padding:10px;width:48%" onclick="buyShop('شارة ألماس',500)">💎 شارة ألماس - 500$</button>
</div>
</div>
</div>

<div id="ucl" class="tab" style="display:none"><div class="card diamond"><h3>🏆 دوري الأبطال DIAMOND</h3><div id="uclMatches"></div></div></div>

<div id="ai" class="tab" style="display:none"><div class="card diamond"><h3>🤖 AI يعلق لحظياً - معلق ذكي</h3><div id="aiCommentary" style="background:#000;padding:12px;border-radius:12px;border:1px solid #00ffff;font-size:13px;line-height:1.6">⏳ الذكاء يحلل المباريات...</div><button class="btn" style="background:#00ffff;color:#000;width:100%;margin-top:8px;padding:12px" onclick="startAI()">🤖 شغّل تعليق AI مباشر</button></div></div>

<div id="leader" class="tab" style="display:none"><div class="card"><h3>🏅 لوحة الشرف DIAMOND</h3><table style="width:100%;border-collapse:collapse;margin-top:10px"><tr style="background:linear-gradient(90deg,#00ffff,#ffcc00)"><th style="color:#000;padding:8px">#</th><th style="color:#000">اللاعب</th><th style="color:#000">💰</th><th style="color:#000">نقاط</th></tr><tr style="background:rgba(0,255,255,.2)"><td style="padding:8px;text-align:center">🥇</td><td>💎 شامي DIAMOND (أنت)</td><td id="leaderMoney">1000$</td><td id="leaderPoints">0</td></tr><tr><td style="text-align:center">🥈</td><td>مدريدي</td><td>850$</td><td>210</td></tr><tr><td style="text-align:center">🥉</td><td>برشلوني</td><td>720$</td><td>180</td></tr></table></div></div>

<div id="chat" class="tab" style="display:none"><div class="card"><h3>💬 دردشة DIAMOND</h3><div id="chatBox" style="height:300px;overflow-y:auto;background:#000;border-radius:12px;padding:8px;border:1px solid #00ffff"><div style="background:#111;padding:6px 10px;border-radius:12px;margin:4px 0;font-size:12px;border-right:3px solid #00ffff">💎 <b>شامي:</b> V11 DIAMOND وصل!</div></div><div style="display:flex;gap:6px;margin-top:8px"><input id="chatInput" placeholder="اكتب..." style="flex:1;padding:10px;border-radius:20px;background:#222;color:#fff;border:1px solid #444"><button onclick="sendChat()" style="background:#00ffff;color:#000;border:none;padding:10px 15px;border-radius:20px;font-weight:900">إرسال</button></div></div></div>

<div id="videoModal" class="modal" onclick="closeVideo()"><div class="modal-box" onclick="event.stopPropagation()"><div style="display:flex;justify-content:space-between"><h3 id="videoTitle" style="color:#00ffff">🎥</h3><button onclick="closeVideo()" style="background:red;color:#fff;border:none;padding:6px 12px;border-radius:10px">X</button></div><iframe id="videoFrame" class="video" allowfullscreen></iframe><div style="margin-top:10px;background:#000;padding:12px;border-radius:12px;border:1px solid #00ffff"><p id="commentary" style="font-weight:900;color:#00ffff">🎙️</p><p id="aiLive" style="font-size:11px;color:#aaa;margin-top:6px">🤖 AI: يحلل الهدف...</p></div></div></div>

<div id="apkModal" class="modal" onclick="this.style.display='none'"><div class="modal-box" onclick="event.stopPropagation()"><h3 style="color:#00ffff">📲 تحويل لـ APK</h3><p style="margin:10px 0;font-size:13px">موقعك صار جاهز كتطبيق!</p><div style="background:#000;padding:10px;border-radius:10px;font-size:11px;border:1px dashed #00ffff">1. اضغط ⋮ فوق<br>2. Add to Home Screen<br>3. رح تصير أيقونة 💎 بجوالك!<br><br>APK الحقيقي: استخدم موقع<br><b>appsgeyser.com</b><br>وحط رابطك:<br>https://whatsapp-bot-88.onrender.com</div><button onclick="this.parentElement.parentElement.style.display='none'" style="width:100%;margin-top:10px;background:#00ffff;color:#000;padding:12px;border:none;border-radius:12px;font-weight:900">فهمت! 💎</button></div></div>

<div id="installBanner" class="install" onclick="showAPK()">💎📲 ثبّت V11 DIAMOND - يصير تطبيق ألماسي! + اصنع APK الآن!</div>
<audio id="goalSound" src="https://www.soundjay.com/human/sounds/man-shouting-goal-01.mp3" preload="auto"></audio>

<script>
let points=parseInt(localStorage.getItem('shaam_v11_points')||'0');
let money=parseInt(localStorage.getItem('shaam_v11_money')||'1000');
let allMatches=[]; let soundOn=false; let aiInterval=null;
document.getElementById('myPoints2').innerText=points; document.getElementById('myMoney').innerText=money;
document.getElementById('leaderPoints').innerText=points; document.getElementById('leaderMoney').innerText=money+'$';
let channels=["https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=0","https://www.youtube.com/embed/XqZsoesa55w?autoplay=0","https://www.youtube.com/embed/dQw4w9WgXcQ?autoplay=0","https://www.youtube.com/embed/9bZkp7q19f0?autoplay=0"];
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='game')loadGame();}
function switchChannel(i,el){document.getElementById('tvFrame').src=channels[i];document.querySelectorAll('.ch').forEach(c=>c.classList.remove('active'));el.classList.add('active');document.getElementById('tvStatus').innerText='📺 قناة '+(i+1)+' شغالة';}
async function loadMatches(){try{let r=await fetch('/api/live');let d=await r.json();allMatches=d.matches;document.getElementById('lastUpdate').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('count').innerText=d.matches.length+' مباراة';render(allMatches);if(soundOn)try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([400,100,400]);}catch(e){}}catch(e){}}
function render(list){
 document.getElementById('matches').innerHTML=list.map(m=>{
  let isLive=m.minute.includes("'");let p1=Math.floor(Math.random()*3);let p2=Math.floor(Math.random()*2);
  return `<div class="card ${isLive?'live':''} ${m.league.includes('champions')?'diamond':''}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#111;padding:4px 10px;border-radius:12px;border:1px solid #00ffff">${m.league}${m.league.includes('champions')?' 🏆':''}</span>${isLive?`<span style="color:red;font-weight:900;animation:blink 1s infinite">🔴 ${m.minute}</span>`:`<span>${m.status}</span>`}</div><div class="team"><span>💎 ${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div class="team"><span>💎 ${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div>${m.scorer?`<div style="background:linear-gradient(90deg,#00ffff,#ffcc00);color:#000;padding:5px 12px;border-radius:20px;font-size:11px;font-weight:900;display:inline-block;margin:4px 0">⚽ ${m.scorer} | 🤖 AI: هدف متوقع!</div>`:''}<div style="background:#050505;padding:8px;border-radius:12px;margin:6px 0;border:1px dashed #00ffff;font-size:11px">🎯 توقع AI: ${p1}-${p2} (${Math.floor(Math.random()*50+50)}%) <button class="btn" style="background:#00ffff;color:#000" onclick="predict('${m.home} vs ${m.away}','${p1}-${p2}')">توقع +50$</button></div><div style="display:flex;gap:3px;flex-wrap:wrap"><button class="btn" style="background:#00ffff;color:#000" onclick="toggleFav('${m.home}')">⭐</button><button class="btn" style="background:red;color:#fff" onclick="playVideo('${m.home} ${m.away} goal','${m.home} vs ${m.away}')">🎥 هدف</button><button class="btn" style="background:#ffcc00;color:#000" onclick="switchTabToTV()">📺 بث</button><button class="btn" style="background:#333;color:#fff" onclick="addChat('يشجع ${m.home} 💎')">💬</button><button class="btn" style="background:#25D366;color:#fff" onclick="shareWA('${m.home} ${m.score} ${m.away}')">📲</button></div></div>`;
 }).join('');
 document.getElementById('uclMatches').innerHTML=list.filter(x=>x.league.includes('champions')).map(m=>`<div style="padding:10px;border-bottom:1px solid #222;display:flex;justify-content:space-between"><span>🏆 ${m.home} vs ${m.away}</span><span style="color:#00ffff;font-weight:900">${m.score} ${m.minute}</span></div>`).join('')||'لا يوجد أبطال الآن';
}
function loadGame(){let html=allMatches.slice(0,5).map(m=>{let a=Math.floor(Math.random()*4);let b=Math.floor(Math.random()*3);return `<div class=card><b>💎 ${m.home} vs ${m.away}</b><br><div style="margin:8px 0;display:flex;gap:6px"><button class="btn" style="background:#111;color:#00ffff;border:1px solid #00ffff;padding:10px;flex:1" onclick="predict('${m.home} vs ${m.away}','${a}-${b}')">${a}-${b} +50$</button><button class="btn" style="background:#111;color:#ffcc00;border:1px solid #ffcc00;padding:10px;flex:1" onclick="predict('${m.home} vs ${m.away}','1-1')">1-1 +30$</button></div></div>`}).join('');document.getElementById('gameBox').innerHTML=html||'⏳';}
function predict(match,pred){money+=50;points+=10;localStorage.setItem('shaam_v11_money',money);localStorage.setItem('shaam_v11_points',points);document.getElementById('myMoney').innerText=money;document.getElementById('myPoints2').innerText=points;document.getElementById('leaderMoney').innerText=money+'$';document.getElementById('leaderPoints').innerText=points;addChat(`توقعت ${match} ${pred} 💎 +50$`);alert(`💎 توقعك: ${match} ${pred}\\n+50$! +10 نقاط!\\n💰 رصيدك: ${money}$`);if(navigator.vibrate)navigator.vibrate(100);}
function buyShop(item,price){if(money<price){alert('❌ ما عندك فلوس كفاية! رصيدك '+money+'$');return}money-=price;localStorage.setItem('shaam_v11_money',money);document.getElementById('myMoney').innerText=money;document.getElementById('leaderMoney').innerText=money+'$';alert(`✅ اشتريت ${item}! 💎\\nرصيدك الآن: ${money}$`);}
function filterTeams(q){if(!q){render(allMatches);return}render(allMatches.filter(m=>(m.home+m.away).toLowerCase().includes(q.toLowerCase())));}
function playVideo(q,title){
 const comms=['💎 خليل البلوشي: ياااااا الله! هدف ألماسي!','💎 رؤوف خليف: جول جول جول! تاريخي!','💎 عصام الشوالي: الله الله الله على الأهداف!','💎 حفيظ دراجي: هدف خرافي يا ناس!','💎 عامر الخوذيري: يا سلام! هدف عالمي!','💎 فهد العتيبي: هدف! هدف! هدف!','💎 علي سعيد الكعبي: جووووول!','🇬🇧 Peter Drury: OHHH WHAT A GOAL! UNBELIEVABLE!'];
 document.getElementById('videoTitle').innerText='💎 '+title;
 document.getElementById('commentary').innerText=comms[Math.floor(Math.random()*comms.length)];
 document.getElementById('aiLive').innerText='🤖 AI يحلل: تسديدة قوية 98km/h، زاوية مستحيلة! نسبة الهدف 12% فقط! هدف خرافي!';
 document.getElementById('videoFrame').src='https://www.youtube.com/embed?listType=search&list='+encodeURIComponent(q+' goal today')+'&autoplay=1';
 document.getElementById('videoModal').style.display='flex';
 if(soundOn)try{document.getElementById('goalSound').play();}catch(e){}
}
function closeVideo(){document.getElementById('videoFrame').src='';document.getElementById('videoModal').style.display='none';}
function toggleFav(id){alert('💎 ⭐ '+id+' أضيف للمفضلة الألماسية!');if(navigator.vibrate)navigator.vibrate(50);}
function switchTabToTV(){showTab('tv',document.querySelectorAll('.nav button')[1]);document.getElementById('tvFrame').scrollIntoView();}
function startAI(){
 let msgs=['⚽ هجمة خطيرة!','🔥 تسديدة قوية!','😱 فرصة ضائعة!','⚡ مرتدة سريعة!','🎯 ركنية خطيرة!','💎 مهارة خرافية!','🔴 كرت أصفر!','⚽ GOAL! هدف!'];
 let box=document.getElementById('aiCommentary');box.innerHTML='🤖 AI بدأ التعليق المباشر...<br><br>';
 aiInterval=setInterval(()=>{let m=msgs[Math.floor(Math.random()*msgs.length)];let time=new Date().toLocaleTimeString('ar-EG');box.innerHTML+=`[${time}] ${m}<br>`;box.scrollTop=box.scrollHeight;},2500);
 alert('🤖 AI بدأ يعلق لحظياً على كل المباريات! ادخل تبويب AI!');
}
function sendChat(){let inp=document.getElementById('chatInput');if(!inp.value)return;addChat(inp.value);inp.value='';}
function addChat(txt){let box=document.getElementById('chatBox');box.innerHTML+=`<div style="background:#111;padding:6px 10px;border-radius:12px;margin:4px 0;font-size:12px;border-right:3px solid #00ffff">👤 <b>أنت 💎:</b> ${txt}</div>`;box.scrollTop=box.scrollHeight;}
function shareWA(t){window.open('https://wa.me/?text='+encodeURIComponent('💎 '+t+' - Shaam V11 DIAMOND: https://whatsapp-bot-88.onrender.com 💎'),'_blank');}
function activateDiamond(){soundOn=true;money+=100;localStorage.setItem('shaam_v11_money',money);document.getElementById('myMoney').innerText=money;document.getElementById('leaderMoney').innerText=money+'$';document.getElementById('comStatus').innerText='💎 8 معلقين شغالين!';alert('💎👑 تم تفعيل وضع الألماس V11 DIAMOND GOD:\\n🎙️ 8 معلقين عرب + انجليزي\\n📺 4 قنوات بث\\n💰 +100$ هدية! رصيدك: '+money+'$\\n🤖 AI يعلق\\n📲 اصنع APK من البانر تحت!');try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([500,100,500]);if('Notification' in window)Notification.requestPermission();}catch(e){}}
function showAPK(){document.getElementById('apkModal').style.display='flex';}
loadMatches();setInterval(loadMatches,30000);
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
                for ev in d.get('events',[])[:5]:
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
        if not matches: matches=[{"home":"Real Madrid","away":"Man City","score":"3-2","league":"uefa.champions","status":"In Progress","minute":"89'","scorer":"Bellingham د 89 هدف قاتل"}]
        return jsonify({"matches":matches})
    except: return jsonify({"matches":[]})
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
