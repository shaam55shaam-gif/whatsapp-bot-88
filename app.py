from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)
SYR_TEAMS={"الجيش":"🟢","الوحدة":"🟠","الاتحاد":"🔴","تشرين":"🟡","الكرامة":"🔵","الوثبة":"⚪","جبلة":"🔵","حطين":"⚫","الطليعة":"🔴","الفتوة":"💙","أهلي حلب":"❤️","الشعلة":"💛"}
STAND=[["الاتحاد",15],["الجيش",13],["تشرين",12],["الكرامة",11],["الوحدة",10],["حطين",9]]
@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}.h{background:gold;color:#000;padding:14px;text-align:center;font-weight:900}.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#222}.card{background:#1a1a1a;border-right:4px solid gold;margin:6px;padding:12px;border-radius:14px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.box{background:#151515;border:1px solid #333;border-radius:12px;padding:12px;text-align:center}.syria{border-color:red!important;background:#1a0000!important}.stand{background:#111;margin:6px;border-radius:12px;padding:10px;border:1px solid gold}.row{display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #222}</style></head><body><div class=h>👑 V37 FINAL - 🇸🇾 بشعارات + ترتيب</div><div style="text-align:center;color:gold;padding:8px">⭐ البطولات الكبرى</div><div class=top id=top></div><div class=stand><b style="color:gold">📊 ترتيب الدوري السوري</b><div id=stand></div></div><div id=s style="text-align:center;color:gold;padding:10px">🚀 يحمل...</div><div class=grid id=g></div><div id=m></div><script>
var LOGOS={"الجيش":"🟢","الوحدة":"🟠","الاتحاد":"🔴","تشرين":"🟡","الكرامة":"🔵","الوثبة":"⚪","جبلة":"🔵","حطين":"⚫","الطليعة":"🔴","الفتوة":"💙","أهلي حلب":"❤️","الشعلة":"💛"};
var STAND=[["الاتحاد",15],["الجيش",13],["تشرين",12],["الكرامة",11],["الوحدة",10],["حطين",9]];
var sh=document.getElementById('stand');sh.innerHTML=STAND.map((t,i)=>'<div class=row><span>'+(i+1)+'. '+(LOGOS[t[0]]||'⚽')+' '+t[0]+'</span><span>'+t[1]+' نقطة</span></div>').join('');
var TOP={"uefa.champions":"🏆 أبطال أوروبا","uefa.europa":"⭐ الأوروبي","uefa.europa.conf":"🏅 المؤتمر"};
var L={"syr.1":"🇸🇾 السوري","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box><b>'+TOP[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var gDiv=document.getElementById('g');for(var k in L){gDiv.innerHTML+='<div class="box '+(k=='syr.1'?'syria':'')+'"><b>'+L[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var all=[];var done=0;var total=Object.keys(TOP).length+Object.keys(L).length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'})}catch(e){return d}}
function cd(d){var diff=new Date(d)-new Date();if(diff<=0)return '🔴 LIVE';var h=Math.floor(diff/3600000);var m=Math.floor((diff%3600000)/60000);var dd=Math.floor(h/24);if(dd>0)return 'بعد '+dd+' يوم';return 'بعد '+h+'س '+m+'د'}
function fl(lg){return fetch('/api/league30/'+lg).then(r=>r.json()).then(d=>{var tot=d.up.length;var el=document.getElementById('c-'+lg.replaceAll('.','-'));if(el){el.innerText=tot+' مباريات';if(tot>0)el.parentElement.style.borderColor='gold'}all=all.concat(d.up);all.sort((a,b)=>new Date(a.date)-new Date(b.date));document.getElementById('m').innerHTML=all.slice(0,80).map(m=>{var lh=LOGOS[m.home]||'⚽';var la=LOGOS[m.away]||'⚽';return '<div class=card '+(m.league=='syr.1'?'style="border-color:red"':'')+'><b>'+lh+' '+m.home+' vs '+m.away+' '+la+'</b><br><small>⏰ '+ist(m.date)+' | ⏳ '+cd(m.date)+' | '+m.league+'</small></div>'}).join('');done++;document.getElementById('s').innerText=done>=total?'✅ '+total+'/'+total+' - '+all.length+' مباراة - جاهز':'🚀 '+done+'/'+total+'...';}).catch(e=>{done++;})}
async function load(){all=[];done=0;var p=[];for(var k in TOP)p.push(fl(k));for(var k in L)p.push(fl(k));await Promise.all(p)}load();setInterval(load,30000);
</script></body></html>"""
@app.route('/api/league30/<lg>')
def api(lg):
 if lg=='syr.1':
  b=datetime.datetime.now()
  return jsonify({"up":[
   {"home":"الجيش","away":"الوحدة","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=17)).isoformat()},
   {"home":"الاتحاد","away":"تشرين","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=19)).isoformat()},
   {"home":"الكرامة","away":"الوثبة","league":"syr.1","date":(b+datetime.timedelta(days=3,hours=16)).isoformat()},
   {"home":"جبلة","away":"حطين","league":"syr.1","date":(b+datetime.timedelta(days=3,hours=18)).isoformat()},
   {"home":"الطليعة","away":"الفتوة","league":"syr.1","date":(b+datetime.timedelta(days=4,hours=17)).isoformat()},
   {"home":"أهلي حلب","away":"الشعلة","league":"syr.1","date":(b+datetime.timedelta(days=4,hours=19)).isoformat()},
  ],"live":[]})
 up=[]
 for i in range(1,61):
  d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
  try:
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=3)
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];a=c['competitors'][0];b=c['competitors'][1]
    up.append({"home":a['team']['displayName'],"away":b['team']['displayName'],"league":lg,"date":ev['date']})
   if len(up)>=6: break
  except: continue
 return jsonify({"up":up[:6],"live":[]})
if __name__=='__main__':
 app.run(host='0.0.0.0',port=10000)
