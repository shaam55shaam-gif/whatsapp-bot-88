import requests
from flask import Flask, jsonify
app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V9 ULTRA GOD 👑</title>
<link rel="manifest" href="data:application/json;base64,eyJuYW1lIjoiU2hhYW0gVjkiLCJzaG9ydF9uYW1lIjoiU2hhYW0iLCJkaXNwbGF5Ijoic3RhbmRhbG9uZSIsInN0YXJ0X3VybCI6Ii8ifQ==">
<style>
:root{--green:#00ff88;--gold:#ffcc00;--bg:#050505;--card:#111;--text:#fff}
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{background:var(--bg);color:var(--text)}
.header{background:linear-gradient(90deg,#00ff88,#ffff00,#00ffaa,#00ff88,#ff00ff,#00ff88);background-size:400%;animation:grad 2s linear infinite;padding:12px;text-align:center;position:sticky;top:0;z-index:999}
@keyframes grad{0%{background-position:0%}100%{background-position:400%}}
.nav{display:flex;gap:4px;padding:6px;background:#0a0a0a;overflow-x:auto;position:sticky;top:52px;z-index:998}
.nav button{background:#1a1a1a;color:#fff;border:1px solid #333;padding:8px 11px;border-radius:20px;font-size:11px;white-space:nowrap}
.nav button.active{background:var(--green);color:#000;font-weight:900;transform:scale(1.08)}
.card{background:linear-gradient(145deg,#111,#1a1a1a);border:1px solid #222;border-radius:16px;margin:8px;padding:12px;box-shadow:0 0 15px rgba(0,255,136,.2)}
.live-card{border-right:4px solid red;animation:glowRed 1.5s infinite}
@keyframes glowRed{0%,100%{box-shadow:0 0 5px red}50%{box-shadow:0 0 25px red}}
.team{display:flex;align-items:center;gap:8px;margin:6px 0;font-weight:bold}
.score{font-size:26px;font-weight:900;color:var(--green);text-shadow:0 0 10px var(--green)}
.btn{padding:7px 10px;border-radius:10px;border:none;font-weight:bold;font-size:11px;margin:2px;cursor:pointer}
.btn-gold{background:linear-gradient(90deg,var(--gold),#ff9900);color:#000;width:94%;margin:8px 3%;padding:13px;border-radius:25px;font-weight:900;font-size:14px;display:block}
.search{width:94%;margin:8px 3%;padding:13px;border-radius:25px;border:2px solid var(--green);background:#111;color:#fff;text-align:center;font-weight:bold}
.chat-box{height:300px;overflow-y:auto;background:#000;border-radius:12px;padding:8px;margin:8px;border:1px solid #333}
.msg{background:#1a1a1a;padding:6px 10px;border-radius:12px;margin:4px 0;font-size:12px;border-right:3px solid var(--green)}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.93);z-index:2000;align-items:center;justify-content:center;padding:12px}
.modal-box{width:100%;max-width:500px;background:#111;border-radius:16px;padding:15px;border:2px solid var(--green)}
.video-frame{width:100%;height:280px;border-radius:12px;border:none}
.install{position:fixed;bottom:15px;left:10px;right:10px;background:linear-gradient(90deg,#00ff88,#00ffaa);color:#000;padding:12px;border-radius:15px;font-weight:900;text-align:center;z-index:1000;display:none;box-shadow:0 4px 20px rgba(0,255,136,.5)}
</style>
</head>
<body>
<div class="header"><h1 style="color:#000;font-weight:900;font-size:14px">👑 Shaam V9 ULTRA GOD 🌍 FINAL FINAL | مع دردشة + تعليق عربي 🎙️</h1><div style="font-size:9px;color:#000;font-weight:bold">تثبيت كتطبيق + توقعات ذكاء اصطناعي + دوري الأبطال</div></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('ucl',this)">🏆 أبطال</button>
<button onclick="showTab('standings',this)">📊 ترتيب</button>
<button onclick="showTab('chat',this)">💬 دردشة</button>
<button onclick="showTab('pred',this)">🎯 توقع</button>
<button onclick="showTab('fav',this)">⭐ مفضلة</button>
</div>
<input class="search" placeholder="🔍 ابحث... برشلونة، الهلال، ريال مدريد، ليفربول" oninput="filterTeams(this.value)">
<button class="btn-gold" onclick="activateAll()">🔔🎙️ فعل كل شي: صوت المعلق + تنبيه واتساب + اهتزاز - اضغط هنا</button>
<div style="text-align:center;font-size:10px;color:#888">آخر تحديث: <span id="lastUpdate">--</span> | <span id="count">--</span> | 🎙️ <span id="comStatus">متوقف</span></div>

<div id="live" class="tab"><div id="matches"><div style="text-align:center;padding:40px;color:var(--green)">⏳ V9 يحمّل 22 مباراة حية...</div></div></div>
<div id="ucl" class="tab" style="display:none"><div class="card"><h3>🏆 دوري أبطال أوروبا مباشر</h3><div id="uclMatches"></div></div></div>
<div id="standings" class="tab" style="display:none"><div class="card"><select id="leagueSelect" onchange="loadStandings()" style="width:100%;padding:12px;border-radius:12px;background:#111;color:#fff;border:2px solid var(--green);font-weight:bold"><option value="eng.1">🏴󠁧󠁢󠁥󠁮󠁧󠁿 الإنجليزي</option><option value="esp.1">🇪🇸 الإسباني</option><option value="ita.1">🇮🇹 الإيطالي</option><option value="sau.1">🇸🇦 السعودي</option><option value="uefa.champions">🏆 أبطال أوروبا</option></select><div id="standingsTable"></div></div></div>

<div id="chat" class="tab" style="display:none">
<div class="card">
<h3>💬 دردشة المشجعين الحية</h3>
<div class="chat-box" id="chatBox">
<div class="msg">👑 <b>شامي:</b> V9 أسطوري والله!</div>
<div class="msg" style="border-color:red">🔴 <b>مدريدي:</b> هلا مدريد 2-1</div>
<div class="msg" style="border-color:#ffcc00">🟡 <b>نصراوي:</b> رونالدو هدف!</div>
<div class="msg">💙 <b>هلالي:</b> الهلال 3-0</div>
</div>
<div style="display:flex;gap:6px;margin-top:8px"><input id="chatInput" placeholder="اكتب تشجيعك..." style="flex:1;padding:10px;border-radius:20px;background:#222;color:#fff;border:1px solid #444"><button onclick="sendChat()" style="background:var(--green);color:#000;border:none;padding:10px 15px;border-radius:20px;font-weight:bold">إرسال</button></div>
</div>
</div>

<div id="pred" class="tab" style="display:none"><div class="card" id="predBox"><h3>🎯 توقعات الذكاء الاصطناعي</h3><div style="margin-top:10px">⏳ يحسب...</div></div></div>
<div id="fav" class="tab" style="display:none"><div class="card" id="favList"></div></div>

<div id="videoModal" class="modal" onclick="closeVideo()"><div class="modal-box" onclick="event.stopPropagation()"><div style="display:flex;justify-content:space-between"><h3 id="videoTitle">🎥 هدف</h3><button onclick="closeVideo()" style="background:red;color:#fff;border:none;padding:5px 10px;border-radius:8px">X</button></div><iframe id="videoFrame" class="video-frame" allowfullscreen></iframe><div style="margin-top:10px"><p id="commentary" style="background:#222;padding:8px;border-radius:10px;font-size:12px">🎙️ خليل البلوشي: ياااااا الله! هدف خرافي!</p></div></div></div>

<div id="installBanner" class="install" onclick="installApp()">📲 ثبّت Shaam V9 كتطبيق على جوالك - اضغط هنا!</div>
<audio id="goalSound" src="https://www.soundjay.com/human/sounds/man-shouting-goal-01.mp3" preload="auto"></audio>

<script>
let favs=JSON.parse(localStorage.getItem('shaam_v9_favs')||'[]');
let allMatches=[]; let soundOn=false; let deferredPrompt=null;

window.addEventListener('beforeinstallprompt',e=>{e.preventDefault();deferredPrompt=e;document.getElementById('installBanner').style.display='block';});
function installApp(){if(deferredPrompt){deferredPrompt.prompt();}else{alert('📲 لتثبيت التطبيق:\\n1. اضغط ⋮ فوق بالمتصفح\\n2. اختر Add to Home Screen\\n3. رح يصير تطبيق مثل الواتساب!');}}
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='standings')loadStandings();if(t=='chat'){}if(t=='pred')loadPred();if(t=='fav')loadFavs();if(t=='ucl')loadUCL();}
async function loadMatches(){try{let r=await fetch('/api/live');let d=await r.json();allMatches=d.matches;document.getElementById('lastUpdate').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('count').innerText=d.matches.length+' مباراة';render(d.matches);if(soundOn){try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([300,100,300]);}catch(e){}}}catch(e){}}
function render(list){if(!list.length){document.getElementById('matches').innerHTML='<div class=card>لا يوجد</div>';return}document.getElementById('matches').innerHTML=list.map(m=>{let isLive=m.minute.includes("'");return `<div class="card ${isLive?'live-card':''}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#222;padding:3px 8px;border-radius:10px">${m.league}</span>${isLive?`<span style="color:red;font-weight:900">🔴 مباشر ${m.minute}</span>`:`<span>${m.status}</span>`}</div><div class="team"><span style="flex:1">${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div class="team"><span style="flex:1">${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div>${m.scorer?`<div style="background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;padding:4px 10px;border-radius:20px;font-size:11px;font-weight:bold;display:inline-block">⚽ ${m.scorer}</div>`:''}<div style="display:flex;gap:4px;margin-top:8px"><button class="btn" style="background:var(--green);color:#000" onclick="toggleFav('${m.home} vs ${m.away}')">⭐</button><button class="btn" style="background:red;color:#fff" onclick="playVideo('${m.home} ${m.away} goal','${m.home} vs ${m.away}')">🎥 هدف</button><button class="btn" style="background:#333;color:#fff" onclick="addChat('يشجع ${m.home} 🔥')">💬</button><button class="btn" style="background:#25D366;color:#fff" onclick="shareWA('${m.home} ${m.score} ${m.away}')">📲</button></div></div>`}).join('');document.getElementById('uclMatches').innerHTML=list.filter(x=>x.league.includes('champions')||x.league.includes('uefa')).map(m=>`<div style="padding:8px;border-bottom:1px solid #222">${m.home} ${m.score} ${m.away} - ${m.minute}</div>`).join('')||'لا يوجد مباريات أبطال الآن';}
function filterTeams(q){if(!q){render(allMatches);return}render(allMatches.filter(m=>(m.home+m.away).toLowerCase().includes(q.toLowerCase())));}
function playVideo(q,title){document.getElementById('videoTitle').innerText='🎥 '+title;let comms=['خليل البلوشي: ياااا الله! هدف خرافي!','رؤوف خليف: جول جول جول!','عصام الشوالي: الله على الأهداف!'];document.getElementById('commentary').innerText='🎙️ '+comms[Math.floor(Math.random()*comms.length)];document.getElementById('videoFrame').src='https://www.youtube.com/embed?listType=search&list='+encodeURIComponent(q+' goal today')+'&autoplay=1';document.getElementById('videoModal').style.display='flex';if(soundOn)try{document.getElementById('goalSound').play();}catch(e){}}
function closeVideo(){document.getElementById('videoFrame').src='';document.getElementById('videoModal').style.display='none';}
function toggleFav(id){if(favs.includes(id))favs=favs.filter(x=>x!=id);else favs.push(id);localStorage.setItem('shaam_v9_favs',JSON.stringify(favs));alert('⭐ '+id);if(navigator.vibrate)navigator.vibrate(50);}
function loadFavs(){if(!favs.length){document.getElementById('favList').innerHTML='<p style="text-align:center;padding:20px">⭐ ما عندك مفضلة</p>';return}document.getElementById('favList').innerHTML=favs.map(f=>`<div class=card>⭐ ${f}</div>`).join('');}
async function loadStandings(){let lg=document.getElementById('leagueSelect').value;document.getElementById('standingsTable').innerHTML='⏳...';try{let r=await fetch('/api/standings/'+lg);let data=await r.json();document.getElementById('standingsTable').innerHTML=`<table style="width:100%;margin-top:10px;border-collapse:collapse"><tr style="background:var(--green);color:#000"><th>#</th><th style="text-align:right">الفريق</th><th>نقاط</th></tr>${data.map((t,i)=>`<tr style="border-bottom:1px solid #333;${i<4?'background:rgba(0,255,136,.1)':''}"><td style="padding:8px;text-align:center">${i+1}</td><td style="text-align:right;padding:8px">🏟️ ${t.team}</td><td style="text-align:center;color:var(--green);font-weight:900">${t.points}</td></tr>`).join('')}</table>`;}catch(e){}}
function loadUCL(){render(allMatches);}
function loadPred(){let preds=allMatches.slice(0,5).map(m=>{let p=Math.floor(Math.random()*60+20);return `<div class=card><b>${m.home} vs ${m.away}</b><br>🤖 توقع الذكاء: فوز ${m.home} بنسبة ${p}%<br>⚽ توقع النتيجة: ${Math.floor(Math.random()*3+1)}-${Math.floor(Math.random()*2)}<br><button class="btn" style="background:var(--green);color:#000;margin-top:6px" onclick="addChat('أتوقع ${m.home} يفوز! 🔥')">💬 أتوقع</button></div>`}).join('');document.getElementById('predBox').innerHTML='<h3>🎯 توقعات الذكاء الاصطناعي</h3>'+preds;}
function sendChat(){let inp=document.getElementById('chatInput');if(!inp.value)return;addChat(inp.value);inp.value='';}
function addChat(txt){let box=document.getElementById('chatBox');box.innerHTML+=`<div class=msg>👤 <b>أنت:</b> ${txt}</div>`;box.scrollTop=box.scrollHeight;setTimeout(()=>{let replies=['والله كفو! 🔥','هدف! ⚽','مباراة نار!','أتفق 100%'];box.innerHTML+=`<div class=msg>🤖 <b>مشجع:</b> ${replies[Math.floor(Math.random()*replies.length)]}</div>`;box.scrollTop=box.scrollHeight;},1000);}
function shareWA(t){window.open('https://wa.me/?text='+encodeURIComponent('⚽ '+t+' - Shaam V9: https://whatsapp-bot-88.onrender.com'),'_blank');}
function activateAll(){soundOn=true;document.getElementById('comStatus').innerText='🔊🎙️ شغال!';alert('✅ تم تفعيل V9 ULTRA:\\n🔊 صوت المعلق خليل البلوشي\\n📳 اهتزاز عند الهدف\\n🔔 تنبيه\\n💬 دردشة\\n🎯 توقعات');try{document.getElementById('goalSound').play();if(navigator.vibrate)navigator.vibrate([300,100,300]);if('Notification' in window)Notification.requestPermission();}catch(e){}}
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
        if not matches: matches=[{"home":"Real Madrid","away":"Barcelona","score":"2-1","league":"esp.1","status":"In Progress","minute":"67'","scorer":"Mbappé د 67"}]
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
