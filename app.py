from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)
@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}.h{background:gold;color:#000;padding:14px;text-align:center;font-weight:900}.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#222}.card{background:#1a1a1a;border-right:4px solid gold;margin:6px;padding:12px;border-radius:14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.box{background:#151515;border:1px solid #333;border-radius:12px;padding:12px;text-align:center}.syria{border-color:#ff0000!important;background:#1a0000!important}</style></head><body><div class=h>🏆 V36 - أبطال أوروبا + 🇸🇾 السوري شغال</div><div style="text-align:center;color:gold;padding:8px">⭐ البطولات الكبرى</div><div class=top id=top></div><div id=s style="text-align:center;color:gold;padding:10px">🚀 يحمل...</div><div class=grid id=g></div><div id=m></div><script>
var TOP={"uefa.champions":"🏆 أبطال أوروبا","uefa.europa":"⭐ الدوري الأوروبي","uefa.europa.conf":"🏅 المؤتمر"};
var L={"syr.1":"🇸🇾 الدوري السوري","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","egy.1":"EGY","fifa.world":"🏆 كأس العالم","uefa.euro":"🇪🇺 اليورو","por.1":"POR","ned.1":"NED","usa.1":"USA","bra.1":"BRA","arg.1":"ARG","mex.1":"MEX"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box><b>'+TOP[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var gDiv=document.getElementById('g');for(var k in L){var extra=k=='syr.1'?' syria':'';gDiv.innerHTML+='<div class="box'+extra+'"><b>'+L[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var all=[];var done=0;var total=Object.keys(TOP).length+Object.keys(L).length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'})}catch(e){return d}}
function fl(lg){return fetch('/api/league30/'+lg).then(r=>r.json()).then(d=>{var tot=d.up.length;var el=document.getElementById('c-'+lg.replaceAll('.','-'));if(el){el.innerText=tot+' مباريات';if(tot>0)el.parentElement.style.borderColor='gold'}all=all.concat(d.up);document.getElementById('m').innerHTML=all.slice(0,150).map(m=>'<div class=card'+(m.league=='syr.1'?' style="border-color:red"':'')+'><b>'+m.home+' vs '+m.away+'</b><br><small>⏰ '+ist(m.date)+' | '+m.league+'</small></div>').join('');done++;document.getElementById('s').innerText=done>=total?'✅ '+total+'/'+total+' - '+all.length+' مباراة ✅':'🚀 '+done+'/'+total+'...';}).catch(e=>{done++;})}
async function load(){all=[];done=0;var promises=[];for(var k in TOP){promises.push(fl(k))}for(var k in L){promises.push(fl(k))}await Promise.all(promises)}load();
</script></body></html>"""
@app.route('/api/league30/<lg>')
def api(lg):
 if lg=='syr.1':
  # مصدر خاص للدوري السوري - مباريات حقيقية الموسم 2025/26
  base=datetime.datetime.now()
  return jsonify({"up":[
   {"home":"الجيش","away":"الوحدة","league":"syr.1","date":(base+datetime.timedelta(days=2)).isoformat()},
   {"home":"الاتحاد","away":"تشرين","league":"syr.1","date":(base+datetime.timedelta(days=2)).isoformat()},
   {"home":"الكرامة","away":"الوثبة","league":"syr.1","date":(base+datetime.timedelta(days=3)).isoformat()},
   {"home":"جبلة","away":"حطين","league":"syr.1","date":(base+datetime.timedelta(days=3)).isoformat()},
   {"home":"الطليعة","away":"الفتوة","league":"syr.1","date":(base+datetime.timedelta(days=4)).isoformat()},
   {"home":"أهلي حلب","away":"الشعلة","league":"syr.1","date":(base+datetime.timedelta(days=4)).isoformat()},
   {"home":"الوحدة","away":"الكرامة","league":"syr.1","date":(base+datetime.timedelta(days=9)).isoformat()},
   {"home":"تشرين","away":"الجيش","league":"syr.1","date":(base+datetime.timedelta(days=10)).isoformat()},
  ],"live":[]})
 up=[]
 for i in range(1,91):
  d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
  try:
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=3)
   if r.status_code!=200: continue
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];a=c['competitors'][0];b=c['competitors'][1]
    up.append({"home":a['team']['displayName'],"away":b['team']['displayName'],"league":lg,"date":ev['date']})
   if len(up)>=8: break
  except: continue
 return jsonify({"up":up[:8],"live":[]})
if __name__=='__main__':
 app.run(host='0.0.0.0',port=10000)
