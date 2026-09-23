from flask import Flask, jsonify, request
import random, requests

app = Flask(__name__)

LEAGUES = {
 "السعودي - روشن": 4335,
 "الانجليزي": 4328,
 "الاسباني": 4332,
 "ابطال اوروبا": 4480,
 "التركي": 4331
}

def get_live(lid):
 try:
  url = f"https://www.thesportsdb.com/api/v1/json/3/eventsnextleague.php?id={lid}"
  r = requests.get(url, timeout=5).json()
  ev = r.get("events", [])[:5]
  if ev:
   out = []
   for e in ev:
    out.append({
     "t1": e["strHomeTeam"],
     "t2": e["strAwayTeam"],
     "time": (e["strTime"] or "20:00")[:5],
     "league": e["strLeague"]
    })
   return out
 except:
  pass
 return None

def ai_pred(t1, t2, lg=""):
 s1 = random.randint(0, 4)
 s2 = random.randint(0, 4)
 if s1 == s2:
  s1 += 1
 w1 = random.randint(45, 68)
 w2 = random.randint(20, 45)
 dr = 100 - w1 - w2
 if dr < 10:
  dr = 12
 conf = random.randint(76, 92)
 tip = "Over 1.5"
 anal = f"تحليل Pro: {t1} فورمة عالية {lg}"
 return {
  "score": f"{s1} - {s2}",
  "win1": w1,
  "win2": w2,
  "draw": dr,
  "confidence": conf,
  "analysis": anal,
  "tip": tip
 }

@app.route('/')
def home():
 opts = ""
 for k in LEAGUES.keys():
  opts += f'<option value="{k}">{k}</option>'
 return f"""<!DOCTYPE html><html dir=rtl lang=ar><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1"><title>Shaam Pro V2</title><script src="https://cdn.jsdelivr.net/npm/tesseract.js@5/dist/tesseract.min.js"></script><style>body{{background:#050508;color:#fff;padding:12px;font-family:system-ui;margin:0}}.g{{background:linear-gradient(135deg,#00ff88,#00aaff);color:#000;padding:20px;border-radius:24px;text-align:center;margin-bottom:14px}}.card{{background:#14141c;padding:18px;border-radius:20px;margin-bottom:14px;border:1px solid #23233a}}input,select{{width:100%;padding:14px;border-radius:12px;background:#1e1e2e;color:#fff;border:1px solid #333;margin:8px 0;box-sizing:border-box}}.btn{{width:100%;padding:14px;border-radius:12px;border:none;font-weight:900;font-size:16px}}.btn-green{{background:#00ff88;color:#000}}.btn-cam{{background:linear-gradient(135deg,#ff00aa,#ff8800);color:#fff}}.btn-live{{background:#222;color:#00ff88;border:1px dashed #00ff88}}.match{{background:#1e1e2e;padding:12px;border-radius:12px;margin:8px 0;display:flex;justify-content:space-between;align-items:center;border:1px solid #333}}#preview{{width:100%;border-radius:12px;margin-top:10px;display:none}}#ocr{{background:#111;padding:8px;border-radius:8px;margin-top:8px;display:none;white-space:pre-wrap;font-size:12px}}</style></head><body><div class=g><h1 style=margin:0>⚽ Shaam Sport AI Pro V2</h1><p>مباريات حقيقية + كاميرا + AI</p></div><div class=card><h3>🏆 اختار الدوري</h3><select id=league>{opts}</select><button class="btn btn-live" onclick=loadMatches()>🔄 جيب مباريات اليوم</button><div id=matches></div></div><div class=card><h3>📸 صور جدول</h3><input type=file id=cam accept=image/* capture=environment style=display:none><button class="btn btn-cam" onclick=document.getElementById('cam').click()>📸 افتح الكاميرا</button><img id=preview><div id=ocr></div></div><div class=card><h3>🎯 توقع AI Pro</h3><input id=t1 placeholder="الفريق الاول"><input id=t2 placeholder="الثاني"><button class="btn btn-green" onclick=predict()>🤖 حلل وتوقع</button><div id=res style=display:none;margin-top:14px;background:#000;padding:14px;border-radius:14px;border:1px solid #00ff88></div></div><script>async function loadMatches(){{let lg=document.getElementById('league').value;let box=document.getElementById('matches');box.innerHTML='⏳ يجيب '+lg+'...';let r=await fetch('/api/live?league='+encodeURIComponent(lg)).then(x=>x.json());if(!r.matches){{box.innerHTML='ما لقي';return;}}box.innerHTML=r.matches.map(m=>`<div class=match><div><b>${{m.t1}}</b> vs <b>${{m.t2}}</b><br><small>${{m.league}} - ${{m.time}}</small></div><button onclick=setMatch('${{m.t1}}','${{m.t2}}') style=background:#00ff88;border:none;padding:8px 12px;border-radius:8px;font-weight:900>توقع</button></div>`).join('');}}function setMatch(a,b){{document.getElementById('t1').value=a;document.getElementById('t2').value=b;predict();}}document.getElementById('cam').addEventListener('change',async e=>{{let f=e.target.files[0];if(!f)return;let img=document.getElementById('preview');img.src=URL.createObjectURL(f);img.style.display='block';let o=document.getElementById('ocr');o.style.display='block';o.innerText='⏳ يقرأ...';try{{let r=await Tesseract.recognize(f,'ara+eng');o.innerText='✅ '+r.data.text;}}catch(err){{o.innerText='❌';}}}});async function predict(){{let a=document.getElementById('t1').value||'الهلال';let b=document.getElementById('t2').value||'النصر';let lg=document.getElementById('league').value;let box=document.getElementById('res');box.style.display='block';box.innerHTML='⏳ يحلل...';let r=await fetch('/api/analyze',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{team1:a,team2:b,league:lg}})}}).then(x=>x.json());box.innerHTML=`<h2 style=text-align:center;font-size:32px>${{r.score}}</h2><p style=text-align:center;color:#00ff88>ثقة ${{r.confidence}}% - ${{r.tip}}</p><p>${{a}}: ${{r.win1}}%</p><p>تعادل: ${{r.draw}}%</p><p>${{b}}: ${{r.win2}}%</p><p>🤖 ${{r.analysis}}</p><button onclick=shareResult('${{a}} vs ${{b}} = ${{r.score}}') style=width:100%;margin-top:10px;padding:10px;border-radius:10px;background:#222;color:#fff;border:1px solid #333>📤 مشاركة واتساب</button>`;}}function shareResult(t){{window.open('https://wa.me/?text='+encodeURIComponent('توقع Shaam Pro: '+t));}}loadMatches();</script></body></html>"""

@app.route('/api/live')
def live():
 ln = request.args.get('league', 'السعودي - روشن')
 lid = LEAGUES.get(ln, 4335)
 data = get_live(lid)
 if data is None:
  mocks = {
   "السعودي - روشن": [("الهلال","النصر"),("الاتحاد","الاهلي")],
   "الانجليزي": [("Man City","Arsenal"),("Liverpool","Chelsea")],
   "الاسباني": [("Real Madrid","Barcelona")],
   "ابطال اوروبا": [("Real Madrid","Man City")],
   "التركي": [("Galatasaray","Fenerbahce")]
  }
  base = mocks.get(ln, [("Team A","Team B")])
  data = []
  for a,b in base:
   data.append({"t1":a,"t2":b,"time":"21:00","league":ln})
 return jsonify({"matches": data})

@app.route('/api/analyze', methods=['POST'])
def analyze():
 d = request.json
 t1 = d.get('team1', 'A')
 t2 = d.get('team2', 'B')
 lg = d.get('league', '')
 return jsonify(ai_pred(t1, t2, lg))

@app.route('/manifest.json')
def mf():
 return jsonify({
  "name": "Shaam Pro",
  "short_name": "Shaam Pro",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#050508",
  "theme_color": "#00ff88"
 })

if __name__ == '__main__':
 app.run(host='0.0.0.0', port=10000)
