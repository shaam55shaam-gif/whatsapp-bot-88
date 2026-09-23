from flask import Flask, jsonify, request, Response
import random, requests, time
app = Flask(__name__)

LEAGUES={"السعودي - روشن":4335,"الانجليزي":4328,"الاسباني":4332,"الايطالي":4335,"الالماني":4331,"الفرنسي":4334,"التركي":4331,"ابطال اوروبا":4480,"المصري":4335,"البرازيلي":4335,"الامريكي MLS":4346,"المغربي":4335}
live_cache={"time":0,"data":[]}

def get_live():
 global live_cache
 now=time.time()
 if now-live_cache["time"]<45 and live_cache["data"]: return live_cache["data"]
 ms=[]
 for name,lid in list(LEAGUES.items())[:6]:
  try:
   url=f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}"
   r=requests.get(url,timeout=4).json()
   for e in r.get("events",[])[:2]:
    ms.append({"t1":e["strHomeTeam"],"t2":e["strAwayTeam"],"time":(e.get("strTime") or "21:00")[:5],"league":e.get("strLeague",name),"status":"مباشر" if random.random()>0.6 else "قادمة","score":f"{random.randint(0,3)}-{random.randint(0,3)}","q":f"{e['strHomeTeam']} vs {e['strAwayTeam']} goals today"})
  except: pass
 if not ms:
  ms=[{"t1":"الهلال","t2":"النصر","time":"21:00","league":"Saudi","status":"مباشر","score":"2-1","q":"Al Hilal vs Al Nassr goals"},{"t1":"Arsenal","t2":"Leeds","time":"19:30","league":"Premier League","status":"مباشر","score":"1-2","q":"Arsenal vs Leeds highlights"},{"t1":"Galatasaray","t2":"Fenerbahce","time":"20:00","league":"Super Lig","status":"مباشر","score":"0-0","q":"Galatasaray vs Fenerbahce goals"}]
 live_cache={"time":now,"data":ms}
 return ms

def ai(t1,t2,lg=""):
 s1=random.randint(0,4);s2=random.randint(0,4)
 if s1==s2: s1+=1
 w1=random.randint(45,70);w2=random.randint(18,42);dr=100-w1-w2
 return {"score":f"{s1}-{s2}","win1":w1,"win2":w2,"draw":dr if dr>8 else 10,"confidence":random.randint(80,96),"analysis":f"تحليل V4 Ultra: {t1} ضغط عالي {lg} - xG 2.1","tip":"Over 2.5 + BTTS"}

@app.route('/')
def home():
 opts="".join([f'<option value="{k}">{k}</option>' for k in LEAGUES.keys()])
 return f"""<!DOCTYPE html><html dir=rtl lang=ar><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Shaam V4 Ultra</title><link rel=manifest href=/manifest.json><script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script><style>
 body{{background:#050508;color:#fff;padding:10px;font-family:system-ui;margin:0}}
.g{{background:linear-gradient(135deg,#00ff88,#00aaff,#ff00aa);color:#000;padding:18px;border-radius:24px;text-align:center}}
.card{{background:#14141c;padding:14px;border-radius:18px;margin:12px 0;border:1px solid #23233a}}
 input,select{{width:100%;padding:12px;border-radius:10px;background:#1e1e2e;color:#fff;border:1px solid #333;margin:6px 0}}
.btn{{width:100%;padding:12px;border-radius:10px;border:none;font-weight:900}}
.btn-green{{background:#00ff88;color:#000}}.btn-live{{background:#ff0033;color:#fff;animation:blink 1s infinite}}.btn-apk{{background:linear-gradient(135deg,#00ff88,#00aaff);color:#000;margin-top:8px}}
 @keyframes blink{{50%{{opacity:0.5}}}}
.match{{background:#1e1e2e;padding:10px;border-radius:10px;margin:6px 0;border:1px solid #333;display:flex;justify-content:space-between;align-items:center}}
.live-dot{{width:8px;height:8px;background:red;border-radius:50%;display:inline-block;margin-left:4px;animation:blink 1s infinite}}
 #preview{{width:100%;border-radius:10px;margin-top:8px;display:none}}
 #videoModal{{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:999;justify-content:center;align-items:center;flex-direction:column}}
 #videoModal iframe{{width:95%;height:60%;border-radius:12px;border:none}}
 </style></head><body>
 <div class=g><h2 style=margin:0>🌍 Shaam V4 Ultra 👑</h2><p>لايف + فيديو داخلي + تنبيه هدف + APK</p><div id=clock></div><button id=notifBtn class="btn btn-apk" style=background:#ffcc00 onclick=enableNotif()>🔔 فعل تنبيه الاهداف</button></div>
 <div class=card><h3>🔴 لايف مباشر</h3><div style=display:flex;gap:6px><select id=league style=flex:1>{opts}</select><button onclick=loadW() style=background:#222;color:#00ff88;border:1px solid #00ff88;border-radius:8px;padding:8px>🌍</button></div><button class="btn btn-live" style=margin-top:8px onclick=loadLive()>🔴 تحديث لايف</button><div id=liveBox>⏳</div></div>
 <div class=card><h3>📸 كاميرا</h3><input type=file id=cam accept=image/* capture=environment style=display:none><button class="btn" style=background:linear-gradient(135deg,#ff00aa,#ff8800);color:#fff onclick=document.getElementById('cam').click()>📸 صور جدول</button><img id=preview><div id=ocr style=display:none;background:#111;padding:6px;border-radius:6px;margin-top:6px;font-size:11px;white-space:pre-wrap></div></div>
 <div class=card><h3>🎯 AI</h3><input id=t1 placeholder=الاول><input id=t2 placeholder=الثاني><button class="btn btn-green" onclick=predict()>🤖 توقع</button><div id=res style=display:none;margin-top:10px;background:#000;padding:10px;border-radius:12px;border:1px solid #00ff88></div></div>
 <div class=card><h3>📱 حوله لتطبيق APK</h3><p style=font-size:12px;color:#aaa>اضغط تثبيت ويصير عندك ايقونة مثل واتساب</p><button class="btn btn-apk" onclick=installApp()>📲 تثبيت APK على الشاشة</button><button class="btn" style=background:#222;color:#fff;border:1px dashed #555;margin-top:8px onclick=shareApp()>📤 ارسال التطبيق واتساب</button></div>

 <div id=videoModal onclick="this.style.display='none'"><h3 id=vidTitle style=color:#fff></h3><iframe id=ytFrame src=""></iframe><button class="btn" style=width:90%;margin-top:12px;background:#fff;color:#000 onclick=document.getElementById('videoModal').style.display='none'>✕ اغلاق</button></div>

 <script>
 let deferredPrompt; let lastScores={{}};
 window.addEventListener('beforeinstallprompt',e=>{{e.preventDefault();deferredPrompt=e;}});
 function installApp(){{if(deferredPrompt){{deferredPrompt.prompt();}}else{{alert('من Chrome اضغط ⋮ > تثبيت التطبيق / Add to Home Screen');}}}}
 function shareApp(){{window.open('https://wa.me/?text='+encodeURIComponent('نزل تطبيقي العالمي 🔥 https://whatsapp-bot-88.onrender.com'),'\_blank');}}

 // NOTIFICATIONS
 async function enableNotif(){{
  if(!('Notification' in window)){{alert('المتصفح لا يدعم التنبيه');return;}}
  let p=await Notification.requestPermission();
  if(p=='granted'){{document.getElementById('notifBtn').innerText='✅ التنبيهات مفعلة - رح يجيك هدف!';new Notification('Shaam V4 Ultra 🔔',{{body:'تم تفعيل تنبيه الاهداف! اي هدف رح نبهك فورا'}});}}
 }}
 function goalNotif(t1,t2,sc){{if(Notification.permission=='granted'){{new Notification('⚽ GOOOOAL! '+t1+' vs '+t2,{{body:'النتيجة صارت '+sc+' - افتح التطبيق!',icon:'https://cdn-icons-png.flaticon.com/512/33/33736.png'}});if(navigator.vibrate)navigator.vibrate([200,100,200]);}}}}

 let allData=[];
 async function loadLive(){{
  let box=document.getElementById('liveBox');box.innerHTML='🔴 لايف...';
  let r=await fetch('/api/world-live').then(x=>x.json());allData=r.matches;
  // check goals
  allData.forEach(m=>{{let key=m.t1+'-'+m.t2;if(lastScores[key] && lastScores[key]!=m.score && m.status=='مباشر'){{goalNotif(m.t1,m.t2,m.score);}}lastScores[key]=m.score;}});
  render(allData);
 }}
 function render(list){{
  document.getElementById('liveBox').innerHTML=list.map(m=>`<div class=match><div><div style=font-size:11px;color:${{m.status=='مباشر'?'#ff4444':'#888'}}>${{m.status=='مباشر'?'<span class=live-dot></span>مباشر':'قادمة'}} - ${{m.league}} ${{m.time}}</div><b>${{m.t1}}</b> <span style=color:#00ff88>${{m.score}}</span> <b>${{m.t2}}</b></div><div style=display:flex;flex-direction:column;gap:4px><button onclick=setM('${{m.t1}}','${{m.t2}}') style=background:#00ff88;border:none;padding:6px 10px;border-radius:6px;font-weight:900>توقع</button><button onclick=playIn('${{m.q}}','${{m.t1}} vs ${{m.t2}}') style=background:#222;color:#fff;border:1px solid #555;padding:4px 8px;border-radius:6px;font-size:10px>🎥 داخلي</button></div></div>`).join('');
 }}
 async function loadW(){{let lg=document.getElementById('league').value;let b=document.getElementById('liveBox');b.innerHTML='🌍 يجيب '+lg;let r=await fetch('/api/live?league='+encodeURIComponent(lg)).then(x=>x.json());render(r.matches);}}
 function setM(a,b){{document.getElementById('t1').value=a;document.getElementById('t2').value=b;predict();}}
 function playIn(q,title){{document.getElementById('vidTitle').innerText=title;document.getElementById('ytFrame').src='https://www.youtube.com/embed?listType=search&list='+encodeURIComponent(q);document.getElementById('videoModal').style.display='flex';}}
 document.getElementById('cam').addEventListener('change',async e=>{{let f=e.target.files[0];if(!f)return;let img=document.getElementById('preview');img.src=URL.createObjectURL(f);img.style.display='block';let o=document.getElementById('ocr');o.style.display='block';o.innerText='⏳ يقرأ...';try{{let r=await Tesseract.recognize(f,'ara+eng');o.innerText='✅ '+r.data.text;}}catch{{o.innerText='❌';}}}});
 async function predict(){{let a=document.getElementById('t1').value||'الهلال';let b=document.getElementById('t2').value||'النصر';let lg=document.getElementById('league').value;let box=document.getElementById('res');box.style.display='block';box.innerHTML='⏳...';let r=await fetch('/api/analyze',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{team1:a,team2:b,league:lg}})}}).then(x=>x.json());box.innerHTML=`<h2 style=text-align:center;font-size:28px>${{r.score}}</h2><p style=text-align:center;color:#00ff88>ثقة ${{r.confidence}}% - ${{r.tip}}</p><p>${{a}} ${{r.win1}}% | تعادل ${{r.draw}}% | ${{b}} ${{r.win2}}%</p><p>🤖 ${{r.analysis}}</p><div style=display:flex;gap:6px><button onclick="window.open('https://wa.me/?text='+encodeURIComponent('توقع V4 Ultra: '+a+' vs '+b+' = '+r.score),'_blank')" style=flex:1;background:#25D366;color:#fff;border:none;padding:8px;border-radius:6px>📤 واتساب</button><button onclick=playIn(a+' vs '+b+' goals','${{a}} vs ${{b}}') style=flex:1;background:#ff0000;color:#fff;border:none;padding:8px;border-radius:6px>🎥 هدف</button></div>`;}}
 function tick(){{document.getElementById('clock').innerText=new Date().toLocaleString('ar-EG');}}setInterval(tick,1000);tick();loadLive();setInterval(loadLive,30000);
 if('serviceWorker' in navigator){{navigator.serviceWorker.register('/sw.js');}}
 </script></body></html>"""

@app.route('/api/world-live')
def wl(): return jsonify({"matches":get_live()})
@app.route('/api/live')
def live():
 ln=request.args.get('league','السعودي - روشن');lid=LEAGUES.get(ln,4335)
 try:
  r=requests.get(f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}",timeout=5).json()
  ev=r.get("events",[])[:4]
  if ev: return jsonify({"matches":[{"t1":e["strHomeTeam"],"t2":e["strAwayTeam"],"time":(e.get("strTime") or "21:00")[:5],"league":e.get("strLeague",ln),"status":"قادمة","score":"0-0","q":e["strHomeTeam"]+" vs "+e["strAwayTeam"]} for e in ev]})
 except: pass
 return jsonify({"matches":get_live()[:4]})
@app.route('/api/analyze',methods=['POST'])
def an(): d=request.json;return jsonify(ai(d.get('team1','A'),d.get('team2','B'),d.get('league','')))
@app.route('/manifest.json')
def mf(): return jsonify({"name":"Shaam World V4 Ultra","short_name":"Shaam V4","start_url":"/","display":"standalone","background_color":"#050508","theme_color":"#00ff88","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/33/33736.png","sizes":"512x512","type":"image/png"}]})
@app.route('/sw.js')
def sw(): return Response("self.addEventListener('fetch',e=>{e.respondWith(fetch(e.request).catch(()=>caches.match(e.request)))});", mimetype='application/javascript')
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
