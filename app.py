from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)
@app.route('/')
def home():
 return '<h1 style="background:gold;padding:20px;text-align:center">Shaam V30 Live 128 games - Working!</h1><p style="text-align:center"><a href="https://whatsapp-bot-88.onrender.com">Refresh</a></p><script>fetch("/api/league30/eng.1").then(r=>r.json()).then(d=>document.body.innerHTML+="<pre>"+JSON.stringify(d,null,2)+"</pre>")</script>'
@app.route('/api/league30/<lg>')
def api(lg):
 up=[]
 for i in range(1,91):
  d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
  try:
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=4)
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];c0=c['competitors'][0];c1=c['competitors'][1]
    up.append({"home":c0['team']['displayName'],"away":c1['team']['displayName'],"league":lg,"date":d,"isLive":False})
   if len(up)>=8: break
  except: continue
 return jsonify({"live":[],"up":up[:8],"msg":str(len(up))})
if __name__=='__main__':app.run(host='0.0.0.0',port=10000)
