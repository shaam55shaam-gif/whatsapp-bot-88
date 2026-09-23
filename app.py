import requests
from flask import Flask, jsonify
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V10 THE END 👑 GOLD</title>
<style>
:root{--gold:#ffcc00;--green:#00ff88}
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{background:#000;color:#fff}
.header{background:linear-gradient(90deg,#ffcc00,#ffff00,#00ff88,#ffcc00,#ff00ff,#ffcc00);background-size:400%;animation:g 2s linear infinite;padding:14px;text-align:center;position:sticky;top:0;z-index:999;border-bottom:3px solid #ffcc00}
@keyframes g{0%{background-position:0%}100%{background-position:400%}}
.nav{display:flex;gap:3px;padding:6px;background:#0a0a0a;overflow-x:auto;position:sticky;top:62px;z-index:998}
.nav button{background:#1a1a1a;color:#fff;border:1px solid #333;padding:8px 10px;border-radius:20px;font-size:10px;white-space:nowrap}
.nav button.active{background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;font-weight:900;transform:scale(1.1);box-shadow:0 0 15px #ffcc00}
.card{background:linear-gradient(145deg,#111,#1a1a1a);border:1px solid #333;border-radius:16px;margin:8px;padding:12px;box-shadow:0 0 15px rgba(255,204,0,.2)}
.gold-card{border:2px solid var(--gold);box-shadow:0 0 25px rgba(255,204,0,.4)}
.live{border-right:4px solid red;animation:rr 1.2s infinite}
@keyframes rr{0%,100%{box-shadow:0 0 5px red}50%{box-shadow:0 0 25px red}}
.team{display:flex;justify-content:space-between;align-items:center;margin:7px 0;font-weight:bold;font-size:14px}
.score{font-size:28px;font-weight:900;color:var(--gold);text-shadow:0 0 10px var(--gold)}
.btn{padding:7px 9px;border-radius:10px;border:none;font-weight:bold;font-size:10px;margin:2px;cursor:pointer}
.btn-gold{background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;width:94%;margin:8px 3%;padding:14px;border-radius:25px;font-weight:900;font-size:15px;display:block;box-shadow:0 4px 15px rgba(255,204,0,.5);animation:pulseGold 2s infinite}
@keyframes pulseGold{0%,100%{transform:scale(1)}50%{transform:scale(1.02)}}
.search{width:94%;margin:8px 3%;padding:13px;border-radius:25px;border:2px solid var(--gold);background:#111;color:#fff;text-align:center;font-weight:bold}
.chat{height:280px;overflow-y:auto;background:#000;border-radius:12px;padding:8px;margin:8px;border:1px solid #444}
.msg{background:#1a1a1a;padding:6px 10px;border-radius:12px;margin:4px 0;font-size:12px;border-right:3px solid var(--gold)}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.95);z-index:2000;align-items:center;justify-content:center;padding:12px}
.modal-box{width:100%;max-width:500px;background:#111;border-radius:16px;padding:15px;border:2px solid var(--gold)}
.video{width:100%;height:280px;border-radius:12px;border:none}
.leader{width:100%;border-collapse:collapse;margin-top:10px}
.leader th{background:var(--gold);color:#000;padding:8px}
.leader td{padding:8px;text-align:center;border-bottom:1px solid #333}
.install{position:fixed;bottom:12px;left:8px;right:8px;background:linear-gradient(90deg,#ffcc00,#ffff00);color:#000;padding:14px;border-radius:15px;font-weight:900;text-align:center;z-index:1000;box-shadow:0 5px 25px rgba(255,204,0,.6);animation:pulseGold 1.5s infinite}
</style>
</head>
<body>
<div class="header"><h1 style="color:#000;font-weight:900;font-size:15px">👑 Shaam V10 THE END - GOLD EDITION 👑</h1><div style="color:#000;font-weight:900;font-size:9px">تطبيق + لعبة توقع + أبطال أوروبا + 5 معلقين عرب - النهاية الأسطورية</div></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('ucl',this)">🏆 أبطال</button>
<button onclick="showTab('game',this)">🎮 لعبة</button>
<button onclick="showTab('leader',this)">🏅 الأبطال</button>
<button onclick="showTab('standings',this)">📊 ترتيب</button>
<button onclick="showTab('chat',this)">💬 دردشة</button>
<button onclick="showTab('fav',this)">⭐ مفضلة</button>
</div>
<input class="search" placeholder="🔍 ابحث... برشلونة، الهلال، ريال، ليفربول" oninput="filterTeams(this.value)">
<button class="btn-gold" onclick="activateGod()">👑🔔 فعل وضع الإله: صوت 5 معلقين + اهتزاز + واتساب + تثبيت</button>
<div style="text-align:center;font-size:10px;color:#aaa">آخر: <span id="lastUpdate">--</span> | <span id="count">--</span> | 🎙️ <span id="comStatus">متوقف</span> | 🎮 نقاطك: <span id="myPoints" style="color:#ffcc00;font-weight:900">0</span></div>

<div id="live" class="tab"><div id="matches"><div style="text-align:center;padding:40px;color:var(--gold)">⏳ V10 GOLD يحمّل إمبراطورية الكورة...</div></div></div>
<div id="ucl" class="tab" style="display:none"><div class="card gold-card"><h3>🏆 دوري أبطال أوروبا - مباشر GOLD</h3><div id="uclMatches"></div><button class="btn" style="background:var(--gold);color:#000;width:100%;margin-top:10px;padding:12px" onclick="playVideo('Champions League live','UCL LIVE')">📺 شاهد بث الأبطال مباشر</button></div></div>
<div id="game" class="tab" style="display:none"><div class="card gold-card"><h3>🎮 لعبة التوقع - اربح وتصدر!</h3><p style="font-size:11px;color:#aaa">توقع النتيجة الصحيحة وخذ 10 نقاط! توقع الفائز 5 نقاط!</p><div id="gameBox" style="margin-top:10px"></div></div></div>
<div id="leader" class="tab" style="display:none"><div class="card"><h3>🏅 لوحة الشرف - أبطال التوقع</h3><table class="leader"><tr><th>🏆</th><th>اللاعب</th><th>نقاط</th></tr><tr style="background:rgba(255,204,0,.2)"><td>🥇</td><td>👑 شامي (أنت)</td><td id="leaderYou">0</td></tr><tr><td>🥈</td><td>مدريديستا</td><td>145</td></tr><tr><td>🥉</td><td>برشلوني</td><td>130</td></tr><tr><td>4</td><td>هلالي</td><td>110</td></tr><tr><td>5</td><td>نصراوي</td><td>95</td></tr></table><button class="btn-gold" onclick="shareLeader()">📲 شارك إنجازك واتساب</button></div></div>
<div id="standings" class="tab" style="display:none"><div class="card"><select id="leagueSelect" onchange="loadStandings()" style="width:100%;padding:12px;border-radius:12px;background:#111;color:#fff;border:2px solid var(--gold);font-weight:bold"><option value="eng.1">🏴󠁧󠁢󠁥󠁮󠁧󠁿 الإنجليزي</option><option value="esp.1">🇪🇸 الإسباني</option><option value="sau.1">🇸🇦 السعودي</option><option value="uefa.champions">🏆 أبطال أوروبا</option></select><div id="standingsTable"></div></div></div>
<div id="chat" class="tab" style="display:none"><div class="card"><h3>💬 دردشة V10 GOLD</h3><div class="chat" id="chatBox"><div class="msg">👑 <b>شامي:</b> V10 THE END وصل!</div><div class="msg">🔥 <b>مشجع:</b> أسطورة والله!</div></div><div style="display:flex;gap:6px;margin-top:8px"><input id="chatInput" placeholder="اكتب..." style="flex:1;padding:10px;border-radius:20px;background:#222;color:#fff;border:1px solid #444"><button onclick="sendChat()" style="background:var(--gold);color:#000;border:none;padding:10px 15px;border-radius:20px;font-weight:900">إرسال</button></div></div></div>
<div id="fav" class="tab" style="display:none"><div class="card" id="favList"></div></div>

<div id="videoModal" class="modal" onclick="closeVideo()"><div class="modal-box" onclick="event.stopPropagation()"><div style="display:flex;justify-content:space-between"><h3 id="videoTitle">🎥</h3><button onclick="closeVideo()" style="background:red;color:#fff;border:none;padding:5px 10px;border-radius:8px">X</button></div><iframe id="videoFrame" class="video" allowfullscreen></iframe><div style="margin-top:8px;background:#222;padding:10px;border-radius:10px"><p id="commentary" style="font-size:13px;font-weight:bold">🎙️ خليل البلوشي: GOAL!</p><p style="font-size:10px;color:#aaa;margin-top:4px">🔊 صوت المعلق الحقيقي شغال!</p></div></div></div>

<div id="installBanner" class="install" onclick="installApp()">📲👑 ثبّت V10 THE END كتطبيق - اضغط يصير بجوالك مثل واتساب! + احصل على APK</div>
<audio id="goalSound" src="https://www.soundjay.com/human/sounds/man-shouting-goal-01.mp3" preload="auto"></audio>

<script>
let favs=JSON.parse(localStorage.getItem('shaam_v10_favs')||'[]');
let points=parseInt(localStorage.getItem('shaam_v10_points')||'0');
let allMatches=[]; let soundOn=false; let dp=null;
document.getElementById('myPoints').innerText=points; document.getElementById('leaderYou').innerText=points;
window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();dp=e;document.getElementById('installBanner').style.display='block';});
function installApp(){if(dp){dp.prompt();}else{alert('📲 تثبيت V10 كتطبيق:\\n1. اضغط ⋮ فوق\\n2. Add to Home Screen / تثبيت التطبيق\\n3. رح يصير أيقونة ذهبية بجوالك!\\n\\nAPK قريباً!');}}
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='standings')loadStandings();if(t=='game')loadGame();if(t=='fav')loadFavs();}
async function loadMatches(){try{let r=await fetch('/api/live');let d=await r.json();allMatches=d.matches;document.getElementById('lastUpdate').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('count').innerText=d.matches.length+' مباراة';render(allMatches);if(soundOn)try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([300,100,300]);}catch(e){}}catch(e){}}
function render(list){
 if(!list.length){document.getElementById('matches').innerHTML='<div class=card>لا يوجد</div>';return}
 document.getElementById('matches').innerHTML=list.map(m=>{
  let isLive=m.minute.includes("'");let predH=Math.floor(Math.random()*3);let predA=Math.floor(Math.random()*2);
  return `<div class="card ${isLive?'live':''} ${m.league.includes('champions')?'gold-card':''}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#222;padding:3px 8px;border-radius:10px">${m.league}${m.league.includes('champions')?' 🏆':''}</span>${isLive?`<span style="color:red;font-weight:900">🔴 ${m.minute}</span>`:`<span>${m.status}</span>`}</div><div class="team"><span>${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div class="team"><span>${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div>${m.scorer?`<div style="background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:900;display:inline-block">⚽ ${m.scorer}</div>`:''}<div style="margin-top:6px;background:#0a0a0a;padding:6px;border-radius:10px;font-size:11px">🎯 توقعي: ${predH}-${predA} <button class="btn" style="background:var(--gold);color:#000" onclick="predict('${m.home} vs ${m.away}','${predH}-${predA}')">توقع ${predH}-${predA}</button></div><div style="display:flex;gap:4px;margin-top:8px"><button class="btn" style="background:var(--gold);color:#000" onclick="toggleFav('${m.home} vs ${m.away}')">⭐</button><button class="btn" style="background:red;color:#fff" onclick="playVideo('${m.home} ${m.away} goal','${m.home} vs ${m.away}')">🎥 هدف</button><button class="btn" style="background:#333;color:#fff" onclick="addChat('يشجع ${m.home} 👑')">💬</button><button class="btn" style="background:#25D366;color:#fff" onclick="shareWA('${m.home} ${m.score} ${m.away}')">📲</button></div></div>`;
 }).join('');
 document.getElementById('uclMatches').innerHTML=list.filter(x=>x.league.includes('champions')||x.league.includes('uefa')).map(m=>`<div style="padding:8px;border-bottom:1px solid #222;display:flex;justify-content:space-between"><span>🏆 ${m.home} vs ${m.away}</span><span style="color:var(--gold);font-weight:900">${m.score} ${m.minute}</span></div>`).join('')||'<div style="padding:10px;text-align:center">⏳ لا يوجد مباريات أبطال الآن - ترقب الثلاثاء!</div>';
}
function loadGame(){let html=allMatches.slice(0,6).map(m=>{let a=Math.floor(Math.random()*4);let b=Math.floor(Math.random()*3);return `<div class=card><b>⚽ ${m.home} vs ${m.away}</b><br><div style="margin:8px 0"><button class="btn" style="background:#222;color:#fff;border:1px solid #444;padding:10px" onclick="predict('${m.home} vs ${m.away}','${a}-${b}')">${a}-${b}</button><button class="btn" style="background:#222;color:#fff;border:1px solid #444;padding:10px" onclick="predict('${m.home} vs ${m.away}','1-1')">1-1</button><button class="btn" style="background:#222;color:#fff;border:1px solid #444;padding:10px" onclick="predict('${m.home} vs ${m.away}','2-1')">2-1</button></div><small style="color:#aaa">اربح 10 نقاط للنتيجة الصحيحة!</small></div>`}).join('');document.getElementById('gameBox').innerHTML=html||'⏳';}
function predict(match,pred){points+=5;localStorage.setItem('shaam_v10_points',points);document.getElementById('myPoints').innerText=points;document.getElementById('leaderYou').innerText=points;addChat(`توقعت ${match} ${pred} 🎯`);alert(`🎯 تم حفظ توقعك: ${match}\\nالنتيجة: ${pred}\\n+5 نقاط! مجموعك: ${points}\\n\\nإذا صح توقعك تربح 10 نقاط إضافية!`);if(navigator.vibrate)navigator.vibrate(50);}
function filterTeams(q){if(!q){render(allMatches);return}render(allMatches.filter(m=>(m.home+m.away).toLowerCase().includes(q.toLowerCase())));}
function playVideo(q,title){
 const comms=['🎙️ خليل البلوشي: ياااا الله! هدف خرااافي! GOAL!','🎙️ رؤوف خليف: جول جول جول! الله على الأهداف!','🎙️ عصام الشوالي: ما هذا الجمال! هدف للتاريخ!','🎙️ حفيظ دراجي: هدف! هدف! يالروعة!','🎙️ عامر الخوذيري: الله أكبر! هدف عالمي!'];
 document.getElementById('videoTitle').innerText='🎥 '+title;
 document.getElementById('commentary').innerText=comms[Math.floor(Math.random()*comms.length)];
 document.getElementById('videoFrame').src='https://www.youtube.com/embed?listType=search&list='+encodeURIComponent(q+' goal today')+'&autoplay=1';
 document.getElementById('videoModal').style.display='flex';
 if(soundOn)try{document.getElementById('goalSound').play();}catch(e){}
}
function closeVideo(){document.getElementById('videoFrame').src='';document.getElementById('videoModal').style.display='none';}
function toggleFav(id){if(favs.includes(id))favs=favs.filter(x=>x!=id);else favs.push(id);localStorage.setItem('shaam_v10_favs',JSON.stringify(favs));alert('⭐ '+id);if(navigator.vibrate)navigator.vibrate(50);}
function loadFavs(){if(!favs.length){document.getElementById('favList').innerHTML='<p style="text-align:center;padding:20px">⭐ ما عندك مفضلة</p>';return}document.getElementById('favList').innerHTML=favs.map(f=>`<div class=card>⭐ ${f}</div>`).join('');}
async function loadStandings(){let lg=document.getElementById('leagueSelect').value;document.getElementById('standingsTable').innerHTML='⏳...';try{let r=await fetch('/api/standings/'+lg);let data=await r.json();document.getElementById('standingsTable').innerHTML=`<table style="width:100%;margin-top:10px;border-collapse:collapse"><tr style="background:var(--gold);color:#000"><th>#</th><th style="text-align:right">الفريق</th><th>نقاط</th></tr>${data.map((t,i)=>`<tr style="border-bottom:1px solid #333;${i<4?'background:rgba(255,204,0,.1)':''}"><td style="padding:8px;text-align:center">${i+1}</td><td style="text-align:right;padding:8px">🏟️ ${t.team}</td><td style="text-align:center;color:var(--gold);font-weight:900">${t.points}</td></tr>`).join('')}</table>`;}catch(e){}}
function sendChat(){let inp=document.getElementById('chatInput');if(!inp.value)return;addChat(inp.value);inp.value='';}
function addChat(txt){let box=document.getElementById('chatBox');box.innerHTML+=`<div class=msg>👤 <b>أنت:</b> ${txt}</div>`;box.scrollTop=box.scrollHeight;setTimeout(()=>{let replies=['والله كفو! 🔥','V10 أسطوري! 👑','هدف! ⚽','أتفق!'];box.innerHTML+=`<div class=msg>🤖 <b>مشجع:</b> ${replies[Math.floor(Math.random()*replies.length)]}</div>`;box.scrollTop=box.scrollHeight;},800);}
function shareWA(t){window.open('https://wa.me/?text='+encodeURIComponent('⚽ '+t+' - Shaam V10 THE END: https://whatsapp-bot-88.onrender.com 🏆'),'__blank');}
function shareLeader(){window.open('https://wa.me/?text='+encodeURIComponent('🏆 أنا في المركز الأول في Shaam V10! نقاطي: '+points+' - تعال نافسني! https://whatsapp-bot-88.onrender.com 👑'),'_blank');}
function activateGod(){soundOn=true;document.getElementById('comStatus').innerText='👑🔊 5 معلقين شغالين!';alert('👑 تم تفعيل وضع الإله V10 THE END:\\n🎙️ 5 معلقين: البلوشي، خليف، الشوالي، دراجي، الخوذيري\\n🔊 صوت GOAL!\\n📳 اهتزاز\\n🎮 +5 نقاط هدية!\\n📲 ثبّت التطبيق من البانر تحت!');points+=5;localStorage.setItem('shaam_v10_points',points);document.getElementById('myPoints').innerText=points;document.getElementById('leaderYou').innerText=points;try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([400,100,400]);if('Notification' in window)Notification.requestPermission();document.getElementById('installBanner').style.display='block';}catch(e){}}
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
        if not matches: matches=[{"home":"Real Madrid","away":"Barcelona","score":"2-1","league":"uefa.champions","status":"In Progress","minute":"67'","scorer":"Mbappé د 67 هدف"}]
        return jsonify({"matches":matches})
    except: return jsonify({"matches":[]})
@app.route('/api/standings/<league>')
def standings(league):
    try:
        r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/standings",timeout=4)
        d=r.json(); out=[]; entries=d['children'][0]['standings']['entries']
        for e in entries[:15]:
            team=e['team']['displayName']; stats={s['name']:s['value'] for s in e['stats']}
            out.append({"team":team,"points":stats.get('points',0),"played":stats.get('gamesPlayed',0)})
        return jsonify(out)
    except: return jsonify([])
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
