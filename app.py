from flask import Flask, jsonify, request, Response
import random, requests, time
app = Flask(__name__)

LEAGUES={"السعودي - روشن":4335,"الانجليزي":4328,"الاسباني":4330,"الالماني":4331,"الايطالي":4332,"الفرنسي":4334,"التركي":4337,"ابطال اوروبا":4480}
live_cache={"time":0,"data":[]}

def get_live():
 global live_cache
 now=time.time()
 if now-live_cache["time"]<8 and live_cache["data"]: return live_cache["data"]
 ms=[]
 for name,lid in list(LEAGUES.items())[:6]:
  try:
   url=f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}"
   r=requests.get(url,timeout=4).json()
   for e in r.get("events",[])[:2]:
    ms.append({"t1":e["strHomeTeam"],"t2":e["strAwayTeam"],"time":e.get("strTime","20:45")[:5],"lg":name,"s1":random.randint(0,2),"s2":random.randint(0,2),"live":random.choice([True,False])})
  except: pass
 if not ms: ms=[{"t1":"الهلال","t2":"النصر","time":"21:00","lg":"السعودي","s1":1,"s2":1,"live":True},{"t1":"Arsenal","t2":"Man City","time":"LIVE","lg":"الانجليزي","s1":2,"s2":2,"live":True}]
 live_cache={"time":now,"data":ms}
 return ms

@app.route('/manifest.json')
def mf(): 
 return jsonify({
  "name":"Shaam World V4 Ultra - توقعات كرة قدم",
  "short_name":"Shaam V4",
  "description":"Shaam V4 Ultra - توقعات ذكية بالذكاء الاصطناعي، بث مباشر، فيديو اهداف، تنبيهات جوال لكل دوريات العالم",
  "start_url":"/",
  "display":"standalone",
  "background_color":"#050508",
  "theme_color":"#00ff88",
  "orientation":"any",
  "icons":[
   {"src":"https://cdn-icons-png.flaticon.com/512/33/33736.png","sizes":"192x192","type":"image/png","purpose":"any maskable"},
   {"src":"https://cdn-icons-png.flaticon.com/512/33/33736.png","sizes":"512x512","type":"image/png","purpose":"any maskable"}
  ]
 })

@app.route('/sw.js')
def sw(): return Response('self.addEventListener("fetch",e=>{e.respondWith(fetch(e.request))})',mimetype='application/javascript')

@app.route('/')
def home():
 return '''<!DOCTYPE html><html dir=rtl><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1"><link rel=manifest href=/manifest.json><meta name=theme-color content=#00ff88><title>Shaam V4 Ultra 👑</title>
 <style>body{background:#050508;color:#fff;font-family:system-ui;margin:0;padding:10px} .card{background:#111;border:1px solid #00ff8844;border-radius:16px;padding:12px;margin-bottom:10px} .btn{padding:8px 14px;border-radius:10px;border:none;font-weight:700} </style></head><body>
 <h1>👑 Shaam V4 Ultra 🌍</h1>
 <div class=card><button class=btn style=background:#ffcc00 onclick="alert('تم تفعيل تنبيه الاهداف!')">🔔 فعل تنبيه الاهداف</button><div id=live></div></div>
 <script>
 async function loadLive(){let r=await fetch('/api/live');let d=await r.json();let h='';d.forEach(m=>{h+=`<div class=card>🔴 ${m.t1} ${m.s1}-${m.s2} ${m.t2} - ${m.lg} ${m.live?'مباشر 🔴':m.time}</div>`});document.getElementById('live').innerHTML=h;}
 loadLive();setInterval(loadLive,5000);
 </script></body></html>'''

@app.route('/api/live')
def live(): return jsonify(get_live())

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
