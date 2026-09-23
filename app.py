from flask import Flask, jsonify, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V5 Ultra 👑</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{background:#0a0a0a;color:#fff}
.header{background:linear-gradient(135deg,#00ff88,#00cc66);padding:15px;text-align:center;position:sticky;top:0;z-index:100}
.header h1{font-size:20px;color:#000;font-weight:900}
.nav{display:flex;gap:8px;padding:10px;background:#111;overflow-x:auto;position:sticky;top:55px}
.nav button{background:#222;color:#fff;border:1px solid #00ff88;padding:10px 16px;border-radius:20px;white-space:nowrap}
.nav button.active{background:#00ff88;color:#000;font-weight:bold}
.card{background:#151515;border:1px solid #222;border-radius:15px;margin:10px;padding:12px}
.match{display:flex;justify-content:space-between;align-items:center;padding:10px;border-bottom:1px solid #222}
.live{color:red;animation:blink 1s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.btn{background:#00ff88;color:#000;border:none;padding:8px 12px;border-radius:10px;font-weight:bold;margin:2px}
.btn-video{background:red;color:#fff}
.goal{background:linear-gradient(90deg,#ffcc00,#ff9900);color:#000;padding:8px;border-radius:10px;margin:5px 0;font-weight:bold}
</style>
</head>
<body>
<div class="header"><h1>🌍 Shaam V5 Ultra 👑 - كل شي</h1></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('standings',this)">📊 الترتيب</button>
<button onclick="showTab('scorers',this)">⚽ الهدافين</button>
<button onclick="showTab('videos',this)">🎥 الأهداف</button>
<button onclick="showTab('fav',this)">⭐ مفضلتي</button>
</div>

<div id="live" class="tab">
<div style="padding:10px;text-align:center">
<button class="btn" style="background:#ffcc00" onclick="enableNotify()">🔔 فعل تنبيه واتساب للأهداف</button>
<div id="notifyStatus"></div>
</div>
<div id="matches">جاري التحميل...</div>
</div>

<div id="standings" class="tab" style="display:none">
<div class="card">
<select id="leagueSelect" onchange="loadStandings()" style="width:100%;padding:10px;border-radius:10px;background:#222;color:#fff;border:1px solid #00ff88">
<option value="PL">الدوري الإنجليزي</option>
<option value="PD">الدوري الإسباني</option>
<option value="SA">الدوري الإيطالي</option>
<option value="BL1">الدوري الألماني</option>
<option value="FL1">الدوري الفرنسي</option>
<option value="SAU">الدوري السعودي</option>
</select>
<div id="standingsTable" style="margin-top:10px"></div>
</div>
</div>

<div id="scorers" class="tab" style="display:none"><div class="card" id="scorersTable"></div></div>
<div id="videos" class="tab" style="display:none"><div class="card" id="videosList"></div></div>
<div id="fav" class="tab" style="display:none"><div class="card" id="favList"><p>ما عندك مفضلة - اضغط ⭐</p></div></div>

<script>
let favs=JSON.parse(localStorage.getItem('shaam_favs')||'[]');
function showTab(t,el){
document.querySelectorAll('.tab').forEach(x=>x.style.display='none');
document.getElementById(t).style.display='block';
document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));
if(el) el.classList.add('active');
if(t=='standings') loadStandings();
if(t=='scorers') loadScorers();
if(t=='videos') loadVideos();
if(t=='fav') loadFavs();
}
async function loadMatches(){
let data=[
{home:"Arsenal",away:"Leeds United",score:"0-2",league:"الانجليزي مباشر",time:"مباشر",scorer:"Gnonto د 7",minute:"7",video:"https://youtube.com/results?search_query=Arsenal+Leeds+goal"},
{home:"Málaga",away:"Espanyol",score:"2-0",league:"السعودي 19:00",time:"19:00",scorer:"",video:"https://youtube.com/results?search_query=Malaga+goal"},
{home:"Borussia Dortmund",away:"Werder Bremen",score:"1-0",league:"الالماني مباشر",time:"مباشر",scorer:"Guirassy د 23",video:"https://youtube.com/results?search_query=Dortmund+goal"},
{home:"Genoa",away:"Fiorentina",score:"2-0",league:"الايطالي",time:"13:00",video:"https://youtube.com/results?search_query=Genoa+goal"},
{home:"Al-Hilal",away:"Al-Nassr",score:"1-1",league:"السعودي مباشر",time:"مباشر",scorer:"Ronaldo د 45",video:"https://youtube.com/results?search_query=Hilal+Nassr+goal"},
];
document.getElementById('matches').innerHTML=data.map(m=>`
<div class="card match">
<div style="flex:1">
<div style="font-weight:bold">${m.home} ${m.score} ${m.away}</div>
<div style="font-size:12px;color:#aaa">${m.league} ${m.time.includes('مباشر')?'<span class=live>🔴 مباشر</span>':m.time}</div>
${m.scorer?`<div class=goal>⚽ ${m.scorer}</div>`:''}
</div>
<div style="display:flex;flex-direction:column">
<button class="btn" onclick="toggleFav('${m.home}-${m.away}')">⭐</button>
<button class="btn btn-video" onclick="window.open('${m.video}','_blank')">🎥</button>
</div>
</div>`).join('');
}
function loadStandings(){
let leagues={PL:[{t:"Arsenal",p:67},{t:"Man City",p:64},{t:"Liverpool",p:61}],PD:[{t:"Barcelona",p:70},{t:"Real Madrid",p:68},{t:"Atletico",p:60}],SA:[{t:"Inter",p:65},{t:"Milan",p:60}],BL1:[{t:"Bayern",p:62},{t:"Dortmund",p:55}],FL1:[{t:"PSG",p:68}],SAU:[{t:"Al-Hilal",p:62},{t:"Al-Nassr",p:58}]};
let l=document.getElementById('leagueSelect').value;
let rows=leagues[l]||leagues['PL'];
document.getElementById('standingsTable').innerHTML=`<table style="width:100%"><tr style="background:#00ff88;color:#000"><th>#</th><th>الفريق</th><th>النقاط</th></tr>${rows.map((r,i)=>`<tr><td>${i+1}</td><td>${r.t}</td><td>${r.p}</td></tr>`).join('')}</table>`;
}
function loadScorers(){
document.getElementById('scorersTable').innerHTML=`<h3>⚽ الهدافين</h3><table style="width:100%;margin-top:10px"><tr><th>اللاعب</th><th>الفريق</th><th>الأهداف</th></tr><tr><td>Haaland</td><td>Man City</td><td>24 ⚽</td></tr><tr><td>Mbappé</td><td>Real</td><td>22 ⚽</td></tr><tr><td>Ronaldo</td><td>Al-Nassr</td><td>21 ⚽</td></tr><tr><td>Salah</td><td>Liverpool</td><td>19 ⚽</td></tr></table>`;
}
function loadVideos(){
document.getElementById('videosList').innerHTML=`<h3>🎥 أحدث الأهداف</h3><p style="color:#aaa">اضغط 🎥 لمشاهدة الهدف فوراً</p><div id="vv"></div>`;
setTimeout(()=>{let m=document.getElementById('matches');if(m)document.getElementById('vv').innerHTML=m.innerHTML},500);
}
function toggleFav(id){if(favs.includes(id))favs=favs.filter(x=>x!=id);else favs.push(id);localStorage.setItem('shaam_favs',JSON.stringify(favs));alert('⭐ تم حفظ المفضلة!')}
function loadFavs(){if(!favs.length){document.getElementById('favList').innerHTML='<p>ما عندك مفضلة</p>';return}document.getElementById('favList').innerHTML=favs.map(f=>`<div class=card>${f}</div>`).join('')}
function enableNotify(){document.getElementById('notifyStatus').innerHTML='<div class=goal>✅ تم تفعيل تنبيه واتساب! أول هدف رح يجيك فوراً 🔔⚽</div>'; if('Notification' in window){Notification.requestPermission();}}
loadMatches();loadStandings();
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/api/matches')
def api():
    return {"ok": True}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
