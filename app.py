from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)
@app.route('/manifest.json')
def man(): return jsonify({"name":"V35 SYRIA","short_name":"V35","start_url":"/","display":"standalone","background_color":"#0a0a0a","theme_color":"gold"})
@app.route('/sw.js')
def sw(): return "self.addEventListener('fetch',e=>e.respondWith(fetch(e.request)))",200,{'Content-Type':'application/javascript'}
@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="manifest" href="/manifest.json"><style>body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}.h{background:gold;color:#000;padding:14px;text-align:center;font-weight:900}.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#1a1a1a}.top.box{border-color:gold;border-width:2px}.card{background:#1a1a1a;border-right:4px solid gold;margin:6px;padding:12px;border-radius:14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.box{background:#151515;border:1px solid #333;border-radius:12px;padding:12px;text-align:center}</style></head><body><div class=h>🏆 V35 - أبطال أوروبا + الدوري الأوروبي + 🇸🇾 السوري</div><div style="text-align:center;color:gold;padding:8px;font-weight:900">⭐ البطولات الكبرى</div><div class=top id=top></div><div id=s style="text-align:center;color:gold;padding:10px">🚀 يحمل...</div><div class=grid id=g></div><div id=m></div><script>
var TOP={"uefa.champions":"🏆 أبطال أوروبا","uefa.europa":"⭐ الدوري الأوروبي","uefa.europa.conf":"🏅 المؤتمر الأوروبي"};
var L={"syr.1":"🇸🇾 الدوري السوري","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","fifa.world":"🏆 كأس العالم","uefa.euro":"🇪🇺 اليورو","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX","uefa.nations":"NATIONS","fifa.friendly":"FRIENDLY","uefa.super_cup":"SUPER CUP","conmebol.libertadores":"LIBERTADORES","caf.champions":"CAF CHAMP","afc.champions":"AFC CHAMP","fifa.cwc":"مونديال الأندية","fifa.worldq":"تصفيات","conmebol.america":"كوبا","caf.nations":"أفريقيا","afc.asian":"آسيا"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box><b>'+TOP[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var g=document.getElementById('g');for(var k in L){g.innerHTML+='<div class=box><b>'+L[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var all=[];var done=0;var total=Object.keys(TOP).length+Object.keys(L).length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'})}catch(e){return d}}
async function fl(lg){try{var r=await fetch('/api/league30/'+lg);var d=await r.json();var tot=d.up.length;document.getElementById('c-'+lg.replaceAll('.','-')).innerText=tot+' مباريات';if(tot>0)document.getElementById('c-'+lg.replaceAll('.','-')).parentElement.style.borderColor='gold';all=all.concat(d.up);document.getElementById('m').innerHTML=all.slice(0,150).map(m=>'<div class=card><b>'+m.home+' vs '+m.away+'</b><br><small>⏰ '+ist(m.date)+' | '+m.league+'</small></div>').join('')}catch(e){document.getElementById('c-'+lg.replaceAll('.','-')).innerText='0 مباريات'}done++;document.getElementById('s').innerText=done>=total?'✅ '+total+'/'+total+' - '+all.length+' مباراة ✅':'🚀 '+done+'/'+total+'...';}
async function load(){done=0;all=[];for(var k in TOP){await fl(k)}for(var k in L){await fl(k)}}load();
if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}
</script></body></html>"""
@app.route('/api/league30/<lg>')
def api(lg):
 up=[]
 for i in range(1,91):
  d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
  try:
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=4)
   if r.status_code!=200: continue
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];a=c['competitors'][0];b=c['competitors'][1]
    up.append({"home":a['team']['displayName'],"away":b['team']['displayName'],"league":lg,"date":ev['date']})
   if len(up)>=8: break
  except: continue
 return jsonify({"up":up[:8],"live":[]})
if __name__=='__main__':
 app.run(host='0.0.0.0',port=10000)
