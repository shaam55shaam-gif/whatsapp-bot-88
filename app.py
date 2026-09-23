from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

LEAGUES = ["eng.1","esp.1","ita.1","ger.1","fra.1","tur.1","sau.1","uefa.champions"]

HTML = """<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V16.3b FIX 🌍</title><style>body{background:#000;color:#fff;font-family:Arial;margin:0}.header{background:#FFD700;color:#000;padding:10px;text-align:center;font-weight:900}.nav{display:flex;gap:4px;padding:5px;background:#111}.nav button{background:#222;color:#fff;border:none;padding:8px 10px;border-radius:20px;font-size:10px}.nav button.active{background:#FFD700;color:#000;font-weight:900}.card{background:#111;border:1px solid #333;border-radius:12px;margin:7px;padding:10px;font-size:12px}.money{background:#111;border:1px solid #FFD700;padding:7px;border-radius:20px;margin:5px;text-align:center;font-size:11px;display:flex;justify-content:space-around}</style></head><body><div class="header">✅ Shaam V16.3b - كل الدوريات حقيقية 🌍</div><div class="money"><span>🔴 <span id="liveC">..</span> مباشر</span><span>📅 <span id="upC">..</span> قادمة</span><span>🌍 <span id="natC">..</span> منتخبات</span></div><div class="nav"><button class="active" onclick="showTab('live',this)">🔴 مباشر</button><button onclick="showTab('up',this)">📅 القادمة 7 أيام</button><button onclick="showTab('nat',this)">🌍 منتخبات</button></div><div id="live" class="tab"><div id="liveBox" style="text-align:center;padding:15px">⏳ يجيب من السيرفر...</div></div><div id="up" class="tab" style="display:none"><div id="upBox" style="text-align:center;padding:15px">⏳...</div></div><div id="nat" class="tab" style="display:none"><div id="natBox" style="text-align:center;padding:15px">⏳...</div></div><script>async function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='up')loadUp();if(t=='nat')loadNat();}async function load(){try{let r=await fetch('/api/live');let d=await r.json();document.getElementById('liveC').innerText=d.matches.length;document.getElementById('liveBox').innerHTML=d.matches.length==0?'📭 لا يوجد مباشر الآن - الدوريات تبدأ 19:00 بتوقيت إسطنبول':d.matches.map(m=>`<div class=card>🔴 <b>${m.home} vs ${m.away}</b> <b style=color:#FFD700>${m.score}</b><br><small>${m.league} ${m.minute} ✅</small></div>`).join('');}catch(e){document.getElementById('liveBox').innerHTML='❌ خطأ';}}async function loadUp(){let b=document.getElementById('upBox');b.innerHTML='⏳ يبحث 7 أيام...';try{let r=await fetch('/api/upcoming');let d=await r.json();document.getElementById('upC').innerText=d.matches.length;b.innerHTML=d.matches.length==0?'📭 لا يوجد':d.matches.map(m=>`<div class=card>📅 <b>${m.home} vs ${m.away}</b><br><small>${m.time} | ${m.league} ✅ حقيقي</small></div>`).join('');}catch(e){b.innerHTML='❌';}}async function loadNat(){try{let r=await fetch('/api/national');let d=await r.json();document.getElementById('natC').innerText=d.matches.length;document.getElementById('natBox').innerHTML=d.matches.length==0?'📭 لا يوجد منتخبات هالأسبوع':d.matches.map(m=>`<div class=card style="border-right:4px solid #00bfff">🌍 <b>${m.home} vs ${m.away}</b><br><small>${m.league} ${m.time}</small></div>`).join('');}catch(e){}}load();</script></body></html>"""

@app.route('/')
def home(): return HTML

@app.route('/api/live')
def api_live():
    matches=[]
    for lg in LEAGUES:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=3)
            data=r.json()
            for ev in data.get('events',[]):
                comp=ev['competitions'][0]
                if comp['status']['type']['state']!='in': continue
                matches.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":f"{comp['competitors'][0].get('score','0')}-{comp['competitors'][1].get('score','0')}","league":lg,"minute":comp['status'].get('displayClock','Live')})
        except: continue
    return jsonify({"matches":matches})

@app.route('/api/upcoming')
def api_up():
    matches=[]
    for i in range(1,8):
        date=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        for lg in ["eng.1","esp.1","ita.1","tur.1","sau.1"]:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}",timeout=3)
                data=r.json()
                for ev in data.get('events',[]):
                    comp=ev['competitions'][0]
                    matches.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"time":date,"league":lg})
                if len(matches)>25: break
            except: continue
        if len(matches)>25: break
    return jsonify({"matches":matches[:30]})

@app.route('/api/national')
def api_nat():
    matches=[]
    for i in range(0,7):
        date=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        for lg in ["fifa.friendly","uefa.nations"]:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}",timeout=3)
                data=r.json()
                for ev in data.get('events',[]):
                    comp=ev['competitions'][0]
                    matches.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"time":date,"league":lg})
            except: continue
    return jsonify({"matches":matches[:20]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
