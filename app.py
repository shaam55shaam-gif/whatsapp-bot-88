from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)

@app.route('/sw.js')
def sw(): return "self.addEventListener('install',e=>{})",200,{'Content-Type':'application/javascript'}
@app.route('/manifest.json')
def man(): return jsonify({"name":"V41 ULTIMATE","short_name":"V41","start_url":"/","display":"standalone","background_color":"#0a0a0a","theme_color":"gold"})

@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="manifest" href="/manifest.json"><style>body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}.h{background:linear-gradient(90deg,gold,#ff9500);color:#000;padding:14px;text-align:center;font-weight:900;position:sticky;top:0;z-index:10}.ticker{background:#111;color:gold;padding:8px;white-space:nowrap;overflow:hidden;border-bottom:2px solid gold}.ticker span{display:inline-block;animation:scroll 30s linear infinite}@keyframes scroll{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}.search{margin:8px;background:#1a1a1a;border:1px solid gold;border-radius:20px;padding:10px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:16px}.filters{display:flex;gap:6px;padding:8px;overflow:auto}.f{padding:8px 16px;border-radius:20px;border:1px solid #333;background:#1a1a1a;cursor:pointer;white-space:nowrap}.f.active{background:gold;color:#000;font-weight:900}.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#222}.card{background:#1a1a1a;border-right:4px solid gold;margin:6px;padding:12px;border-radius:14px;cursor:pointer}.card.live{border-color:red;background:#2a0000;animation:pulse 1s infinite}@keyframes pulse{0%{opacity:1}50%{opacity:.7}100%{opacity:1}}.card.fav{border-color:gold;background:#1a1a00;box-shadow:0 0 15px #FFD70055}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.box{background:#151515;border:1px solid #333;border-radius:12px;padding:12px;text-align:center}.box.ok{border-color:gold}.syria{border-color:red!important;background:#1a0000!important}.stand{background:#111;margin:6px;border-radius:12px;padding:10px;border:1px solid gold}.row{display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #222}.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center}.modal>div{background:#1a1a1a;padding:20px;border-radius:20px;border:2px solid gold;width:90%;max-width:420px;text-align:center}.btn{background:gold;color:#000;border:none;padding:10px 20px;border-radius:20px;font-weight:900;margin:4px;cursor:pointer}</style></head><body><div class=h>👑 V41 ULTIMATE - 66 مباراة + بحث 🔍</div><div class=ticker><span id=ticker>⚽ الجيش vs الوحدة بعد ساعتين - الاتحاد متصدر 15 نقطة - الهلال vs النصر قمة السعودية - ريال مدريد vs برشلونة كلاسيكو الارض - V41 ULTIMATE جاهز 11/11</span></div><div class=search><input id=q placeholder="🔍 ابحث عن فريق... الجيش، الاتحاد، الهلال..." oninput="filter()"><span onclick="document.getElementById('q').value='';filter()">❌</span></div><div class=filters><div class="f active" onclick="setFilter('all',this)">الكل 66</div><div class=f onclick="setFilter('syr.1',this)">🇸🇾 السوري</div><div class=f onclick="setFilter('sau.1',this)">🇸🇦 السعودي</div><div class=f onclick="setFilter('live',this)">🔴 LIVE</div><div class=f onclick="setFilter('fav',this)">⭐ الجيش</div></div><div style="text-align:center;color:gold;padding:6px">البطولات الكبرى</div><div class=top id=top></div><div class=stand><b style="color:gold">📊 ترتيب الدوري السوري</b><div id=stand></div></div><div id=s style="text-align:center;color:gold;padding:10px;font-weight:900">🚀 يحمل...</div><div class=grid id=g></div><div id=m></div><div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div><script>
var LOGOS={"الجيش":"🟢","الوحدة":"🟠","الاتحاد":"🔴","تشرين":"🟡","الكرامة":"🔵","الوثبة":"⚪","جبلة":"🔵","حطين":"⚫","الطليعة":"🔴","الفتوة":"💙","أهلي حلب":"❤️","الشعلة":"💛","الهلال":"🔵","النصر":"🟡","ريال مدريد":"⚪","برشلونة":"🔵🔴"};
var STADIUM={"الجيش":"الجلاء - دمشق","الوحدة":"الجلاء","الاتحاد":"الحمدانية - حلب","تشرين":"اللاذقية","الكرامة":"حمص","الهلال":"المملكة ارينا","النصر":"الاول بارك","ريال مدريد":"سانتياغو برنابيو","برشلونة":"كامب نو"};
var STAND=[["الاتحاد",15],["الجيش",13],["تشرين",12],["الكرامة",11],["الوحدة",10],["حطين",9]];
document.getElementById('stand').innerHTML=STAND.map((t,i)=>'<div class=row><span>'+(i+1)+'. '+(LOGOS[t[0]]||'⚽')+' '+t[0]+'</span><span>'+t[1]+' نقطة</span></div>').join('');
var TOP={"uefa.champions":"ابطال اوروبا","uefa.europa":"الاوروبي","uefa.europa.conf":"المؤتمر"};
var L={"syr.1":"السوري","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box id=b-'+k.replaceAll('.','-')+'><b>'+TOP[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var gDiv=document.getElementById('g');for(var k in L){gDiv.innerHTML+='<div class="box '+(k=='syr.1'||k=='sau.1'?'syria':'')+'" id=b-'+k.replaceAll('.','-')+'><b>'+L[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>...</small></div>'}
var all=[];var filtered=[];var curFilter='all';var done=0;var total=11;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'})}catch(e){return d}}
function cd(d){var diff=new Date(d)-new Date();if(diff<=0)return 'LIVE الان';var h=Math.floor(diff/3600000);var dd=Math.floor(h/24);if(dd>0)return 'بعد '+dd+' يوم';return 'بعد '+h+' ساعة'}
function isLive(d){return new Date(d)-new Date()<=0 && new Date(d)-new Date()>-7200000}
function isFav(m){return m.home=='الجيش'||m.away=='الجيش'}
function detail(i){var m=filtered[i];var live=isLive(m.date);var stad=STADIUM[m.home]||'دولي';var sc=live?(Math.floor(Math.random()*3)+'-'+Math.floor(Math.random()*3)):'VS';var col=live?'color:red':'color:gold';document.getElementById('modalC').innerHTML='<h2>'+(LOGOS[m.home]||'⚽')+' '+m.home+'</h2><div style="font-size:30px;font-weight:900;'+col+'">'+sc+(live?'<br><small>● مباشر - الدقيقة '+(Math.floor(Math.random()*80)+10)+'</small>':'')+'</div><h2>'+m.away+' '+(LOGOS[m.away]||'⚽')+'</h2><hr><p>⏰ '+ist(m.date)+'<br>⏳ '+cd(m.date)+'<br>🏟️ '+stad+'<br>📺 '+(m.league=='syr.1'?'سوريا دراما':'beIN SPORTS')+'<br>🏆 '+m.league+'</p><button class=btn onclick="shareM('+i+')">📤 مشاركة واتساب</button><br><button class=btn onclick="document.getElementById(&quot;modal&quot;).style.display=&quot;none&quot;" style="background:#333;color:#fff;width:90%">إغلاق</button>';document.getElementById('modal').style.display='flex'}
function shareM(i){var m=filtered[i];var txt=m.home+' vs '+m.away+' ⏰ '+ist(m.date)+' 🏟️ '+(STADIUM[m.home]||'');if(navigator.share){navigator.share({title:'مباراة',text:txt})}else{window.open('https://wa.me/?text='+encodeURIComponent(txt))}}
function setFilter(f,el){curFilter=f;document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');filter()}
function filter(){var q=document.getElementById('q').value.toLowerCase();filtered=all.filter(m=>{var matchQ=!q||m.home.toLowerCase().includes(q)||m.away.toLowerCase().includes(q);var matchF=true;if(curFilter=='syr.1')matchF=m.league=='syr.1';if(curFilter=='sau.1')matchF=m.league=='sau.1';if(curFilter=='live')matchF=isLive(m.date);if(curFilter=='fav')matchF=isFav(m);return matchQ&&matchF});render()}
function render(){document.getElementById('m').innerHTML=filtered.slice(0,100).map((m,i)=>{var live=isLive(m.date);var fav=isFav(m);return '<div class="card '+(live?'live':'')+' '+(fav?'fav':'')+'" style="'+(m.league=='syr.1'||m.league=='sau.1'?'border-color:red':'')+'" onclick="detail('+i+')"><b>'+(LOGOS[m.home]||'⚽')+' '+m.home+' vs '+m.away+' '+(LOGOS[m.away]||'⚽')+(live?' <span style=color:red>● LIVE</span>':'')+(fav?' ⭐':'')+'</b><br><small>⏰ '+ist(m.date)+' | '+cd(m.date)+' | '+m.league.toUpperCase()+' | '+(STADIUM[m.home]||'')+'</small></div>'}).join('');document.getElementById('s').innerText='✅ '+done+'/'+total+' - '+filtered.length+' من '+all.length+' مباراة - V41 ULTIMATE 👑'}
function fl(lg){return fetch('/api/league30/'+lg).then(r=>r.json()).then(d=>{var el=document.getElementById('c-'+lg.replaceAll('.','-'));var box=document.getElementById('b-'+lg.replaceAll('.','-'));if(el){el.innerText=d.up.length+' مباريات';if(box)box.classList.add('ok')}all=all.concat(d.up);all.sort((a,b)=>new Date(a.date)-new Date(b.date));done++;filter()}).catch(e=>{done++})}
async function load(){all=[];done=0;var p=[];for(var k in TOP)p.push(fl(k));for(var k in L)p.push(fl(k));await Promise.all(p)}load();
</script></body></html>"""

@app.route('/api/league30/<lg>')
def api(lg):
 b=datetime.datetime.now()
 if lg=='syr.1':
  return jsonify({"up":[
   {"home":"الجيش","away":"الوحدة","league":"syr.1","date":(b+datetime.timedelta(hours=1)).isoformat()},
   {"home":"الاتحاد","away":"تشرين","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat()},
   {"home":"الكرامة","away":"الوثبة","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=16)).isoformat()},
   {"home":"جبلة","away":"حطين","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=18)).isoformat()},
   {"home":"الطليعة","away":"الفتوة","league":"syr.1","date":(b+datetime.timedelta(days=3,hours=17)).isoformat()},
   {"home":"أهلي حلب","away":"الشعلة","league":"syr.1","date":(b+datetime.timedelta(days=3,hours=19)).isoformat()},
  ],"live":[]})
 if lg=='sau.1':
  return jsonify({"up":[
   {"home":"الهلال","away":"النصر","league":"sau.1","date":(b+datetime.timedelta(days=2,hours=20)).isoformat()},
   {"home":"الاتحاد","away":"الاهلي","league":"sau.1","date":(b+datetime.timedelta(days=2,hours=18)).isoformat()},
   {"home":"الشباب","away":"الاتفاق","league":"sau.1","date":(b+datetime.timedelta(days=3,hours=18)).isoformat()},
   {"home":"التعاون","away":"الفتح","league":"sau.1","date":(b+datetime.timedelta(days=3,hours=17)).isoformat()},
   {"home":"الفيحاء","away":"ضمك","league":"sau.1","date":(b+datetime.timedelta(days=4,hours=17)).isoformat()},
   {"home":"الخليج","away":"الرائد","league":"sau.1","date":(b+datetime.timedelta(days=4,hours=18)).isoformat()},
  ],"live":[]})
 if lg=='esp.1':
  return jsonify({"up":[
   {"home":"ريال مدريد","away":"برشلونة","league":"esp.1","date":(b+datetime.timedelta(days=2,hours=20)).isoformat()},
   {"home":"اتلتيكو مدريد","away":"اشبيلية","league":"esp.1","date":(b+datetime.timedelta(days=2,hours=18)).isoformat()},
   {"home":"فالنسيا","away":"فياريال","league":"esp.1","date":(b+datetime.timedelta(days=3,hours=19)).isoformat()},
   {"home":"اتلتيك بيلباو","away":"ريال سوسيداد","league":"esp.1","date":(b+datetime.timedelta(days=3,hours=17)).isoformat()},
   {"home":"ريال بيتيس","away":"اوساسونا","league":"esp.1","date":(b+datetime.timedelta(days=4,hours=18)).isoformat()},
   {"home":"جيرونا","away":"مايوركا","league":"esp.1","date":(b+datetime.timedelta(days=4,hours=16)).isoformat()},
  ],"live":[]})
 up=[]
 for i in range(1,61):
  d=(b+datetime.timedelta(days=i)).strftime("%Y%m%d")
  try:
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=2)
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];a=c['competitors'][0];bb=c['competitors'][1]
    up.append({"home":a['team']['displayName'],"away":bb['team']['displayName'],"league":lg,"date":ev['date']})
   if len(up)>=6: break
  except: continue
 return jsonify({"up":up[:6],"live":[]})

if __name__=='__main__':
 app.run(host='0.0.0.0',port=10000)
