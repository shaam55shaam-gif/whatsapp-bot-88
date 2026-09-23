from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

# كل دوريات العالم الحقيقية من ESPN
LEAGUES = [
"eng.1","eng.2","eng.3","esp.1","esp.2","ita.1","ger.1","fra.1","ned.1","por.1","tur.1","bel.1",
"sau.1","qat.1","uae.1","egy.1",
"uefa.champions","uefa.europa","uefa.europa.conf","uefa.nations","uefa.champions.qual",
"fifa.world","fifa.world.qual","fifa.friendly","fifa.womens.world",
"conmebol.libertadores","conmebol.sudamericana",
"usa.1","mex.1","bra.1","arg.1",
"jpn.1","chn.1","aus.1"
]

HTML = """<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V16 WORLD 🌍</title><style>body{background:#000;color:#fff;font-family:Arial;margin:0}.header{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:12px;text-align:center;font-weight:900}.nav{display:flex;gap:4px;padding:6px;background:#111;overflow-x:auto}.nav button{background:#222;color:#fff;border:none;padding:9px 11px;border-radius:20px;font-size:9px;white-space:nowrap}.nav button.active{background:#FFD700;color:#000;font-weight:900}.card{background:#111;border:1px solid #333;border-radius:14px;margin:8px;padding:10px;font-size:12px}.live{border-right:4px solid red}.nat{border-right:4px solid #00bfff}.score{color:#FFD700;font-weight:900}.btn{background:#FFD700;color:#000;border:none;padding:8px;border-radius:10px;font-weight:900;width:100%;margin:4px 0}.money{background:#111;border:1px solid #FFD700;padding:8px;border-radius:20px;margin:6px;text-align:center;font-weight:900;display:flex;justify-content:space-around;font-size:11px}select{background:#222;color:#fff;border:1px solid #FFD700;padding:6px;border-radius:10px;width:92%;margin:6px 4%}</style></head><body><div class="header">🌍 Shaam V16 WORLD - كل دوريات العالم + منتخبات ✅</div><div class="money"><span>🔴 <span id="liveCount">0</span> مباشر</span><span>📅 <span id="upCount">0</span> قادمة</span><span>🌍 35 دوري</span></div><select id="leagueFilter" onchange="filterLeague()"><option value="all">🌍 كل الدوريات + المنتخبات</option><option value="eng.1">🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League</option><option value="esp.1">🇪🇸 LaLiga</option><option value="sau.1">🇸🇦 Saudi</option><option value="tur.1">🇹🇷 Turkey</option><option value="uefa.champions">🏆 Champions</option><option value="fifa.world">🌍 منتخبات - World Cup</option><option value="fifa.friendly">🤝 منتخبات ودية</option><option value="uefa.nations">🏆 Nations League</option></select><div class="nav"><button class="active" onclick="showTab('live',this)">🔴 مباشر العالم</button><button onclick="showTab('upcoming',this)">📅 القادمة - كل الدوريات</button><button onclick="showTab('national',this)">🌍 المنتخبات</button></div><div id="live" class="tab"><div id="matches" style="text-align:center;padding:20px">⏳ يحمّل 35 دوري من ESPN...</div></div><div id="upcoming" class="tab" style="display:none"><div id="upcomingBox" style="text-align:center;padding:20px">⏳ يحمّل القادمة...</div></div><div id="national" class="tab" style="display:none"><div id="nationalBox" style="text-align:center;padding:20px">⏳ يحمّل المنتخبات...</div></div><script>let allLive=[],allUp=[],allNat=[];async function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='upcoming')loadUp();if(t=='national')loadNat();}function filterLeague(){let v=document.getElementById('leagueFilter').value;renderLive(v);renderUp(v);}function renderLive(f){let box=document.getElementById('matches');let list=f=='all'?allLive:allLive.filter(m=>m.league==f);if(list.length==0){box.innerHTML='<div class=card>📭 لا يوجد مباشر الآن بهالدوري - جرب كل الدوريات<br>الوقت الحالي بإسطنبول: مباريات أوروبا تبدأ 19:00-23:00</div>';return}box.innerHTML=list.map(m=>`<div class="card live"><b>${m.home} vs ${m.away}</b> <span class=score>${m.score}</span><br><small>${m.league} ${m.minute} ${m.type}</small></div>`).join('');}function renderUp(f){let box=document.getElementById('upcomingBox');let list=f=='all'?allUp:allUp.filter(m=>m.league==f);if(list.length==0){box.innerHTML='<div class=card>📭 لا يوجد قادمة بهالدوري بالـ 5 أيام الجاية</div>';return}box.innerHTML=list.map(m=>`<div class=card><b>${m.home} vs ${m.away}</b><br><small>📅 ${m.time} | ${m.league}</small></div>`).join('');}async function load(){try{let r=await fetch('/api/live');let d=await r.json();allLive=d.matches;document.getElementById('liveCount').innerText=allLive.length;renderLive(document.getElementById('leagueFilter').value);}catch(e){}}async function loadUp(){try{let r=await fetch('/api/upcoming');let d=await r.json();allUp=d.matches;document.getElementById('upCount').innerText=allUp.length;renderUp(document.getElementById('leagueFilter').value);}catch(e){}}async function loadNat(){try{let r=await fetch('/api/national');let d=await r.json();allNat=d.matches;document.getElementById('nationalBox').innerHTML=d.matches.length==0?'<div class=card>📭 لا يوجد مباريات منتخبات بالـ 7 أيام الجاية</div>':d.matches.map(m=>`<div class="card nat"><b>🌍 ${m.home} vs ${m.away}</b> <span class=score>${m.score}</span><br><small>${m.league} ${m.time}</small></div>`).join('');}catch(e){}}load();setInterval(load,30000);</script></body></html>"""

@app.route('/')
def home(): return HTML

@app.route('/api/live')
def live():
    matches=[]
    for lg in LEAGUES:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=3)
            d=r.json()
            for ev in d.get('events',[]):
                comp=ev['competitions'][0]
                if comp['status']['type']['state']!='in': continue
                h=comp['competitors'][0]['team']['displayName']
                a=comp['competitors'][1]['team']['displayName']
                hs=comp['competitors'][0].get('score','0')
                as_=comp['competitors'][1].get('score','0')
                typ="🌍 منتخب" if "fifa" in lg or "uefa.nations" in lg else "🏆 نادي"
                matches.append({"home":h,"away":a,"score":f"{hs}-{as_}","league":lg,"minute":comp['status'].get('displayClock','Live'),"type":typ})
        except: continue
    return jsonify({"matches":matches})

@app.route('/api/upcoming')
def upcoming():
    matches=[]
    for i in range(1,6):
        date = (datetime.datetime.now() + datetime.timedelta(days=i)).strftime("%Y%m%d")
        for lg in LEAGUES[:20]:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}",timeout=3)
                d=r.json()
                for
