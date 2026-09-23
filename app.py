from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)
@app.route('/sw.js')
def sw(): return """self.addEventListener('install',e=>e.waitUntil(caches.open('v38').then(c=>c.addAll(['/']))));self.addEventListener('fetch',e=>e.respondWith(caches.match(e.request).then(r=>r||fetch(e.request))))""",200,{'Content-Type':'application/javascript'}
@app.route('/manifest.json')
def man(): return jsonify({"name":"V38 TURBO SYRIA","short_name":"V38","start_url":"/","display":"standalone","background_color":"#0a0a0a","theme_color":"gold","icons":[{"src":"https://cdn-icons-png.flaticon.com/512/1165/1165187.png","sizes":"512x512","type":"image/png"}]})
@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="manifest" href="/manifest.json"><style>body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}.h{background:gold;color:#000;padding:14px;text-align:center;font-weight:900;position:sticky;top:0;z-index:9}.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#222}.card{background:#1a1a1a;border-right:4px solid gold;margin:6px;padding:12px;border-radius:14px;cursor:pointer}.card:hover{background:#222}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.box{background:#151515;border:1px solid #333;border-radius:12px;padding:12px;text-align:center;transition:.3s}.box.done{border-color:gold;background:#1a1a00}.syria{border-color:red!important;background:#1a0000!important}.syria.done{border-color:red!important;background:#2a0000!important}.stand{background:#111;margin:6px;border-radius:12px;padding:10px;border:1px solid gold}.row{display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #222}.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000d;z-index:99;justify-content:center;align-items:center}.modal>div{background:#1a1a1a;padding:20px;border-radius:20px;border:2px solid gold;width:90%;max-width:400px;text-align:center}</style></head><body><div class=h>👑 V38 TURBO - يفتح بدون نت 📲</div><div style="text-align:center;color:gold;padding:6px">⭐ البطولات الكبرى</div><div class=top id=top></div><div class=stand><b style="color:gold">📊 ترتيب الدوري السوري - 2025/26</b><div id=stand></div></div><div id=s style="text-align:center;color:gold;padding:10px">🚀 TURBO يحمل...</div><div class=grid id=g></div><div id=m></div><div class=modal id=modal onclick="this.style.display='none'"><div id=modalC></div></div><script>
var LOGOS={"الجيش":"🟢","الوحدة":"🟠","الاتحاد":"🔴","تشرين":"🟡","الكرامة":"🔵","الوثبة":"⚪","جبلة":"🔵","حطين":"⚫","الطليعة":"🔴","الفتوة":"💙","أهلي حلب":"❤️","الشعلة":"💛"};
var STAND=[["الاتحاد",15,5],["الجيش",13,4],["تشرين",12,4],["الكرامة",11,3],["الوحدة",10,3],["حطين",9,2]];
var sh=document.getElementById('stand');sh.innerHTML=STAND.map((t,i)=>'<div class=row><span>'+(i+1)+'. '+(LOGOS[t[0]]||'⚽')+' '+t[0]+'</span><span>'+t[1]+' نقطة - '+t[2]+' فوز</span></div>').join('');
var TOP={"uefa.champions":"🏆 أبطال أوروبا","uefa.europa":"⭐ الأوروبي","uefa.europa.conf":"🏅 المؤتمر"};
var L={"syr.1":"🇸🇾 السوري","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box' id=b-'+k.replaceAll('.','-')+'"><b>'+TOP[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>⏳</small></div>'}
var gDiv=document.getElementById('g');for(var k in L){gDiv.innerHTML+='<div class="box '+(k=='syr.1'?'syria':'')+'" id=b-'+k.replaceAll('.','-')+'"><b>'+L[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>⏳</small></div>'}
var all=[];var done=0;var total=Object.keys(TOP).length+Object.keys(L).length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'})}catch(e){return d}}
function cd(d){var diff=new Date(d)-new Date();if(diff<=0)return '🔴 LIVE الآن';var h=Math.floor(diff/3600000);var m=Math.floor((diff%3600000)/60000);var dd=Math.floor(h/24);if(dd>0)return 'بعد '+dd+' يوم '+ (h%24)+'س';return 'بعد '+h+'س '+m+'د'}
function detail(m){document.getElementById('modalC').innerHTML='<h2>'+(LOGOS[m.home]||'⚽')+' '+m.home+'<br>vs<br>'+m.away+' '+(LOGOS[m.away]||'⚽')+'</h2><p>⏰ '+ist(m.date)+'<br>⏳ '+cd(m.date)+'<br>🏟️ '+(m.league=='syr.1'?'ملعب الحمدانية - حلب':'')+'<br>📺 '+(m.league=='syr.1'?'سوريا دراما':'beIN SPORTS')+'</p><button onclick="document.getElementById(`modal`).style.display=`none`" style="background:gold;border:none;padding:10px 20px;border-radius:20px;font-weight:900">إغلاق</button>';document.getElementById('modal').style.display='flex';if(Notification.permission=='granted'){new Notification(m.home+' vs '+m.away,{body:'⏰ '+ist(m.date)+' - '+cd(m.date)})}}
function fl(lg){var controller=new AbortController();var timeout=setTimeout(()=>controller.abort(),5000);return fetch('/api/league30/'+lg,{signal:controller.signal}).then(r=>r.json()).then(d=>{clearTimeout(timeout);var tot=d.up.length;var el=document.getElementById('c-'+lg.replaceAll('.','-'));var box=document.getElementById('b-'+lg.replaceAll('.','-'));if(el){el.innerText=tot+' مباريات';if(box)box.classList.add('done')}all=all.concat(d.up);all.sort((a,b)=>new Date(a.date)-new Date(b.date));document.getElementById('m').innerHTML=all.slice(0,100).map((m,i)=>{var lh=LOGOS[m.home]||'⚽';var la=LOGOS[m.away]||'⚽';return '<div class=card '+(m.league=='syr.1'?'style="border-color:red"':'')+' onclick="detail(all['+i+'])"><b>'+lh+' '+m.home+' vs '+m.away+' '+la+'</b><br><small>⏰ '+ist(m.date)+' | ⏳ '+cd(m.date)+' | '+m.league.toUpperCase()+'</small></div>'}).join('');done++;document.getElementById('s').innerText='✅ '+done+'/'+total+' - '+all.length+' مباراة - TURBO ⚡';}).catch(e=>{var el=document.getElementById('c-'+lg.replaceAll('.','-'));if(el)el.innerText='0 مباريات';done++;document.getElementById('s').innerText='🚀 '+done+'/'+total+' - TURBO...';})}
async function load(){all=[];done=0;var p=[];for(var k in TOP)p.push(fl(k));for(var k in L)p.push(fl(k));await Promise.all(p);document.getElementById('s').innerText='✅ '+total+'/'+total+' - '+all.length+' مباراة - جاهز بدون نت ✅'}load();setInterval(load,30000);
if('serviceWorker' in navigator){navigator.serviceWorker.register('/sw.js')}if(Notification.permission!='granted'){Notification.requestPermission()}
window.all=all;setInterval(()=>{window.all=all},1000);
</script></body></html>"""
@app.route('/api/league30/<lg>')
def api(lg):
 if lg=='syr.1':
  b=datetime.datetime.now()
  return jsonify({"up":[
   {"home":"الجيش","away":"الوحدة","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"الجلاء - دمشق"},
   {"home":"الاتحاد","away":"تشرين","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=19)).isoformat(),"stadium":"الحمدانية - حلب"},
   {"home":"الكرامة","away":"الوثبة","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=16)).isoformat(),"stadium":"خالد بن الوليد - حمص"},
   {"home":"جبلة","away":"حطين","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=18)).isoformat(),"stadium":"الباسل - اللاذقية"},
   {"home":"الطليعة","away":"الفتوة","league":"syr.1","date":(b+datetime.timedelta(days=3,hours=17)).isoformat(),"stadium":"البلدي - حماة"},
   {"home":"أهلي حلب","away":"الشعلة","league":"syr.1","date":(b+datetime.timedelta(days=3,hours=19)).isoformat(),"stadium":"الحمدانية - حلب"},
  ],"live":[]})
 up=[]
 for i in range(1,61):
  d=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
  try:
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=2)
   if r.status_code!=200: continue
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];a=c['competitors'][0];b=c['competitors'][1]
    up.append({"home":a['team']
