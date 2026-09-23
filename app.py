from flask import Flask, jsonify
import requests
app = Flask(__name__)

HTML = """<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V15.3 FIXED 🚀</title><style>body{background:#000;color:#fff;font-family:Arial;margin:0}.header{background:#FFD700;color:#000;padding:12px;text-align:center;font-weight:900}.nav{display:flex;gap:4px;padding:6px;background:#111;overflow-x:auto}.nav button{background:#222;color:#fff;border:none;padding:9px 11px;border-radius:20px;font-size:9px;white-space:nowrap}.nav button.active{background:#FFD700;color:#000;font-weight:900}.card{background:#111;border:1px solid #333;border-radius:14px;margin:8px;padding:12px}.live{border-right:4px solid red}.upcoming{border-right:4px solid #00ff88}.score{color:#FFD700;font-size:26px;font-weight:900}.btn{background:#FFD700;color:#000;border:none;padding:10px;border-radius:10px;font-weight:900;width:100%;margin:5px 0}.money{background:#111;border:1px solid #FFD700;padding:8px;border-radius:20px;margin:6px;text-align:center;font-weight:900;display:flex;justify-content:space-around}</style></head><body><div class="header">🚀 Shaam V15.3 FIXED - مباشر + القادمة 📅✅</div><div class="money"><span>💰 <span id="myMoney">1000</span>$</span><span>🪙 <span id="myCoin">0</span> SMC</span><span id="count">--</span></div><div class="nav"><button class="active" onclick="showTab('live',this)">🔴 مباشر</button><button onclick="showTab('upcoming',this)">📅 القادمة</button><button onclick="showTab('coin',this)">🪙 Coin</button></div><button class="btn" style="width:92%;margin:6px 4%" onclick="activate()">🚀 فعل 1000 SMC + 10K$</button><div id="live" class="tab"><div id="matches" style="text-align:center;padding:20px">⏳ يحمّل مباشر...</div></div><div id="upcoming" class="tab" style="display:none"><div id="upcomingBox" style="text-align:center;padding:20px">⏳ يحمّل القادمة...</div></div><div id="coin" class="tab" style="display:none"><div class="card"><h3>🪙 ShaamCoin $0.42</h3><button class="btn" onclick="mine()">⛏️ عدّن +10 SMC</button></div></div><script>let money=1000,coin=0,all=[];function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='upcoming')loadUp();}async function load(){try{let r=await fetch('/api/live');let d=await r.json();all=d.matches;document.getElementById('count').innerText=d.matches.length+' مباراة';document.getElementById('matches').innerHTML=d.matches.map(m=>`<div class=card><b>${m.home} vs ${m.away}</b> <span class=score>${m.score}</span><br><small>${m.league} ${m.minute}</small><br><button class=btn onclick="predict()">توقع +10 SMC</button></div>`).join('');}catch(e){}}async function loadUp(){try{let r=await fetch('/api/upcoming');let d=await r.json();document.getElementById('upcomingBox').innerHTML=d.matches.map(m=>`<div class=card><b>${m.home} vs ${m.away}</b><br><small>${m.time} ${m.league}</small><br><button class=btn onclick="predictUp()">توقع +20 SMC</button></div>`).join('')||'لا يوجد غدا';}catch(e){}}function predict(){money+=200;coin+=10;alert('+200$ +10 SMC');}function predictUp(){money+=300;coin+=20;alert('+300$ +20 SMC قادمة');}function mine(){coin+=10;alert('+10 SMC');}function activate(){money+=10000;coin+=1000;alert('+10K$ +1000 SMC!');}load();</script></body></html>"""

@app.route('/')
def home(): return HTML

@app.route('/api/live')
def live():
    matches=[]
    try:
        for lg in ["eng.1","esp.1","sau.1"]:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=3)
            d=r.json()
            for ev in d.get('events',[])[:5]:
                comp=ev['competitions'][0]
                h=comp['competitors'][0]; a=comp['competitors'][1]
                matches.append({"home":h['team']['displayName'],"away":a['team']['displayName'],"score":"0-0","league":lg,"minute":"FT"})
    except: pass
    if not matches: matches=[{"home":"Real Madrid","away":"Barcelona","score":"2-1","league":"LaLiga","minute":"90'"}]
    return jsonify({"matches":matches})

@app.route('/api/upcoming')
def upcoming():
    matches=[]
    try:
        r=requests.get("https://site.api.espn.com/apis/site/v2/sports/soccer/eng.1/scoreboard?dates=20260924",timeout=3)
        d=r.json()
        for ev in d.get('events',[])[:10]:
            comp=ev['competitions'][0]
            h=comp['competitors'][0]; a=comp['competitors'][1]
            matches.append({"home":h['team']['displayName'],"away":a['team']['displayName'],"time":"Tomorrow 20:00","league":"eng.1"})
    except: pass
    if not matches: matches=[{"home":"Man City","away":"Arsenal","time":"Tomorrow 21:00","league":"PL"},{"home":"Al Hilal","away":"Al Nassr","time":"Tomorrow 20:00","league":"Saudi"}]
    return jsonify({"matches":matches})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
