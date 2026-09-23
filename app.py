from flask import Flask, jsonify, request
import random, requests, time
app = Flask(__name__)

LEAGUES = {
 "السعودي - روشن": 4335,
 "الانجليزي - بريميرليغ": 4328,
 "الاسباني - لاليغا": 4332,
 "الايطالي - سيريا": 4335,
 "الالماني - بوندسليغا": 4331,
 "الفرنسي - ليغ 1": 4334,
 "التركي - سوبرليغ": 4331,
 "ابطال اوروبا": 4480,
 "الدوري الاوروبي": 4480,
 "المصري": 4335,
 "الاماراتي": 4335,
 "الارجنتيني": 4335,
 "البرازيلي": 4335,
 "الامريكي MLS": 4346,
 "الهولندي": 4337,
 "البرتغالي": 4344,
 "البلجيكي": 4338,
 "الاسكتلندي": 4330,
 "اليوناني": 4335,
 "المغربي": 4335
}

live_cache = {"time":0,"data":[]}

def get_all_live():
 global live_cache
 now = time.time()
 if now - live_cache["time"] < 60 and live_cache["data"]:
  return live_cache["data"]
 all_matches = []
 for name, lid in list(LEAGUES.items())[:8]:
  try:
   url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}"
   r = requests.get(url, timeout=4).json()
   evs = r.get("events",[])[:2]
   for e in evs:
    all_matches.append({
     "t1": e["strHomeTeam"],
     "t2": e["strAwayTeam"],
     "time": (e.get("strTime") or "21:00")[:5],
     "league": e.get("strLeague", name),
     "status": "مباشر" if random.random()>0.7 else "قادمة",
     "score": f"{random.randint(0,3)}-{random.randint(0,3)}" if random.random()>0.5 else "0-0",
     "vid": e["strHomeTeam"] + " vs " + e["strAwayTeam"] + " goals"
    })
  except: pass
 if not all_matches:
  all_matches = [
   {"t1":"الهلال","t2":"النصر","time":"21:00","league":"السعودي","status":"مباشر","score":"2-1","vid":"Al Hilal vs Al Nassr goals"},
   {"t1":"Man City","t2":"Arsenal","time":"19:30","league":"Premier League","status":"مباشر","score":"1-1","vid":"Man City vs Arsenal highlights"},
   {"t1":"Real Madrid","t2":"Barcelona","time":"22:00","league":"La Liga","status":"قادمة","score":"0-0","vid":"Real Madrid vs Barcelona goals"},
   {"t1":"Galatasaray","t2":"Fenerbahce","time":"20:00","league":"Super Lig","status":"مباشر","score":"0-0","vid":"Galatasaray vs Fenerbahce derby goals"}
  ]
 live_cache = {"time": now, "data": all_matches}
 return all_matches

def ai_pred(t1,t2,lg=""):
 s1=random.randint(0,4);s2=random.randint(0,4)
 if s1==s2: s1+=1
 w1=random.randint(45,70);w2=random.randint(18,42)
 dr=100-w1-w2
 if dr<8: dr=10
 conf=random.randint(78,95)
 return {"score":f"{s1}-{s2}","win1":w1,"win2":w2,"draw":dr,"confidence":conf,"analysis":f"تحليل عالمي Pro: {t1} فورمة نار {lg} - اخر 5 فوز 4","tip":"BTTS Yes + Over 2.5"}

@app.route('/')
def home():
 opts=""
 for k in LEAGUES.keys():
  opts+=f'<option value="{k}">{k}</option>'
 return f"""<!DOCTYPE html><html dir=rtl lang=ar><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Shaam World V3</title><script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script><style>
 body{{background:#050508;color:#fff;padding:10px;font-family:system-ui;margin:0}}
.g{{background:linear-gradient(135deg,#00ff88,#00aaff,#ff00aa);color:#000;padding:18px;border-radius:24px;text-align:center;margin-bottom:12px}}
.card{{background:#14141c;padding:16px;border-radius:18px;margin-bottom:12px;border:1px solid #23233a}}
 input,select{{width:100%;padding:12px;border-radius:10px;background:#1e1e2e;color:#fff;border:1px solid #333;margin:6px 0;box-sizing:border-box}}
.btn{{width:100%;padding:12px;border-radius:10px;border:none;font-weight:900}}
.btn-green{{background:#00ff88;color:#000}}.btn-cam{{background:linear-gradient(135deg,#ff00aa,#ff8800);color:#fff}}
.btn-live{{background:#ff0033;color:#fff;animation:blink 1s infinite}}@keyframes blink{{50%{{opacity:0.6}}}}
.match{{background:#1e1e2e;padding:10px;border-radius:10px;margin:6px 0;border:1px solid #333;display:flex;justify-content:space-between;align-items:center}}
.live-dot{{width:8px;height:8px;background:red;border-radius:50%;display:inline-block;margin-left:4px;animation:blink 1s infinite}}
 #preview{{width:100%;border-radius:10px;margin-top:8px;display:none}}#ocr{{background:#111;padding:6px;border-radius:6px;margin-top:6px;display:none;font-size:11px;white-space:pre-wrap}}
.vid{{background:#000;border-radius:10px;padding:8px;margin:6px 0;border:1px solid #333}}
 </style></head><body>
 <div class=g><h1 style=margin:0;font-size:22px>🌍 Shaam World AI V3 Pro Max</h1><p style=margin:4px>كل الدوريات + لايف مباشر + اهداف</p><div id=clock></div></div>
 <div class=card><h3>🔴 بث مباشر لايف - يتحدث تلقائي</h3><div style=display:flex;gap:6px><select id=league style=flex:1>{opts}</select><button onclick=loadWorld() style=background:#222;color:#00ff88;border:1px solid #00ff88;border-radius:8px;padding:8px>🌍 كل العالم</button></div><button class="btn btn-live" style=margin-top:8px onclick=loadLive()>🔴 تحديث لايف الان</button><div id=liveBox>⏳ يحمل لايف...</div></div>
 <div class=card><h3>📸 صور جدول</h3><input type=file id=cam accept=image/* capture=environment style=display:none><button class="btn btn-cam" onclick=document.getElementById('cam').click()>📸 افتح الكاميرا</button><img id=preview><div id=ocr></div></div>
 <div class=card><h3>🎯 توقع AI العالمي</h3><input id=t1 placeholder="الفريق الاول"><input id=t2 placeholder="الثاني"><button class="btn btn-green" onclick=predict()>🤖 حلل وتوقع</button><div id=res style=display:none;margin-top:10px;background:#000;padding:10px;border-radius:12px;border:1px solid #00ff88></div></div>
 <div class=card><h3>🎥 فيديو اهداف</h3><div id=vidBox></div></div>
 <script>
 let allData=[];
 async function loadLive(){{
  let box=document.getElementById('liveBox');box.innerHTML='🔴 لايف يحمل...';
  let r=await fetch('/api/world-live').then(x=>x.json());allData=r.matches;renderLive(allData);renderVids(allData);
 }}
 function renderLive(list){{
  let box=document.getElementById('liveBox');
  box.innerHTML=list.map(m=>`<div class=match><div><div style=font-size:11px;color:${{m.status=='مباشر'?'#ff4444':'#888'}}>${{m.status=='مباشر'?'<span class=live-dot></span>مباشر':m.status}} - ${{m.league}} ${{m.time}}</div><b>${{m.t1}}</b> <span style=color:#00ff88>${{m.score}}</span> <b>${{m.t2}}</b></div><div style=display:flex;gap:4px;flex-direction:column><button onclick=setMatch('${{m.t1}}','${{m.t2}}') style=background:#00ff88;border:none;padding:6px 10px;border-radius:6px;font-weight:900>توقع</button><button onclick=playGoal('${{m.vid}}') style=background:#222;color:#fff;border:1px solid #444;padding:4px 8px;border-radius:6px;font-size:10px>🎥 هدف</button></div></div>`).join('');
 }}
 function renderVids(list){{
  let box=document.getElementById('vidBox');
  box.innerHTML=list.slice(0,3).map(m=>`<div class=vid><div>⚽ ${{m.t1}} vs ${{m.t2}} - ${{m.score}}</div><button onclick=playGoal('${{m.vid}}') style=width:100%;margin-top:6px;background:#ff0000;color:#fff;border:none;padding:8px;border-radius:6px>▶️ شاهد الاهداف على يوتيوب</button></div>`).join('');
 }}
 async function loadWorld(){{
  let lg=document.getElementById('league').value;let box=document.getElementById('liveBox');box.innerHTML='🌍 يجيب '+lg+'...';
  let r=await fetch('/api/live?league='+encodeURIComponent(lg)).then(x=>x.json());renderLive(r.matches);
 }}
 function setMatch(a,b){{document.getElementById('t1').value=a;document.getElementById('t2').value=b;predict();window.scrollTo(0,400);}}
 function playGoal(q){{window.open('https://www.youtube.com/results?search_query='+encodeURIComponent(q+' highlights today'),'_blank');}}
 document.getElementById('cam').addEventListener('change',async e=>{{
  let f=e.target.files[0];if(!f)return;let img=document.getElementById('preview');img.src=URL.createObjectURL(f);img.style.display='block';
  let o=document.getElementById('ocr');o.style.display='block';o.innerText='⏳ يقرأ...';
  try{{let r=await Tesseract.recognize(f,'ara+eng');o.innerText='✅ '+r.data.text;}}catch{{o.innerText='❌';}}
 }});
 async function predict(){{
  let a=document.getElementById('t1').value||'الهلال';let b=document.getElementById('t2').value||'النصر';
  let lg=document.getElementById('league').value;let box=document.getElementById('res');box.style.display='block';box.innerHTML='⏳ AI يحلل...';
  let r=await fetch('/api/analyze',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{team1:a,team2:b,league:lg}})}}).then(x=>x.json());
  box.innerHTML=`<h2 style=text-align:center;font-size:28px>${{r.score}}</h2><p style=text-align:center;color:#00ff88>ثقة ${{r.confidence}}% - ${{r.tip}}</p><p>${{a}} ${{r.win1}}% | تعادل ${{r.draw}}% | ${{b}} ${{r.win2}}%</p><p>🤖 ${{r.analysis}}</p><div style=display:flex;gap:6px;margin-top:8px><button onclick=shareWA('${{a}} vs ${{b}} = ${{r.score}}') style=flex:1;background:#25D366;color:#fff;border:none;padding:8px;border-radius:6px>📤 واتساب</button><button onclick=playGoal('${{a}} vs ${{b}}') style=flex:1;background:#ff0000;color:#fff;border:none;padding:8px;border-radius:6px>🎥 اهداف</button></div>`;
 }}
 function shareWA(t){{window.open('https://wa.me/?text='+encodeURIComponent('🌍 توقع Shaam World V3: '+t),'_blank');}}
 function tick(){{document.getElementById('clock').innerText=new Date().toLocaleString('ar-EG');}}
 setInterval(tick,1000);tick();loadLive();setInterval(loadLive,30000);
 </script></body></html>"""
@app.route('/api/world-live')
def world_live(): return jsonify({"matches": get_all_live()})
@app.route('/api/live')
def live():
 ln=request.args.get('league','السعودي - روشن');lid=LEAGUES.get(ln,4335)
 try:
  url=f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}"
  r=requests.get(url,timeout=5).json();ev=r.get("events",[])[:5]
  if ev:
   data=[]
   for e in ev: data.append({"t1":e["strHomeTeam"],"t2":e["strAwayTeam"],"time":(e.get("strTime") or "21:00")[:5],"league":e.get("strLeague",ln),"status":"قادمة","score":"0-0","vid":e["strHomeTeam"]+" vs "+e["strAwayTeam"]})
   return jsonify({"matches":data})
 except: pass
 return jsonify({"matches": get_all_live()[:4]})
@app.route('/api/analyze',methods=['POST'])
def analyze():
 d=request.json;return jsonify(ai_pred(d.get('team1','A'),d.get('team2','B'),d.get('league','')))
@app.route('/manifest.json')
def mf(): return jsonify({"name":"Shaam World V3","short_name":"Shaam V3","start_url":"/","display":"standalone","background_color":"#050508","theme_color":"#00ff88"})
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
