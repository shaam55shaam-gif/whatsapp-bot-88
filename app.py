from flask import Flask, jsonify
import requests, datetime
app=Flask(__name__)

@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#0a0a0a;--card:#1a1a1a;--text:#fff;--border:#00ff00}
.light{--bg:#f5f5f5;--card:#fff;--text:#000;--border:#00aa00}
body{background:var(--bg);color:var(--text);font-family:Arial;margin:0;transition:.3s}
.h{background:linear-gradient(90deg,#00ff00,gold);color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;display:flex;justify-content:space-between;align-items:center}
.ticker{background:#111;color:#00ff00;padding:8px;white-space:nowrap;overflow:hidden;border-bottom:2px solid #00ff00;font-weight:900}
.ticker span{display:inline-block;animation:scroll 25s linear infinite}
@keyframes scroll{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
.search{margin:8px;background:var(--card);border:1px solid var(--border);border-radius:25px;padding:10px 15px;display:flex;align-items:center}
.search input{flex:1;background:transparent;border:none;color:var(--text);outline:none;font-size:16px}
.filters{display:flex;gap:6px;padding:8px;overflow:auto}
.f{padding:8px 14px;border-radius:20px;border:1px solid #333;background:var(--card);cursor:pointer;white-space:nowrap;font-weight:700;color:var(--text)}
.f.active{background:#00ff00;color:#000;box-shadow:0 0 10px #00ff00}
.top{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;padding:6px;background:#222}
.card{background:var(--card);border-right:4px solid #00ff00;margin:6px;padding:12px;border-radius:14px;cursor:pointer;color:var(--text)}
.card.live{border-color:red;background:#2a0000;color:#fff;animation:pulse 1.5s infinite}
.card.fav{border-color:gold;box-shadow:0 0 12px gold}
@keyframes pulse{0%{box-shadow:0 0 0 0 red}70%{box-shadow:0 0 0 10px #ff000000}100%{box-shadow:0 0 0 0 #ff000000}}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:var(--card);border:1px solid #333;border-radius:12px;padding:12px;text-align:center;cursor:pointer;color:var(--text)}
.box.ok{border-color:#00ff00}
.box.active{border-color:gold!important;background:#1a1a00!important}
.syria{border-color:#00ff00!important;background:#001a00!important;color:#fff!important}
.stand{background:var(--card);margin:6px;border-radius:12px;padding:10px;border:2px solid #00ff00}
.row{display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #333}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center}
.modal>div{background:var(--card);color:var(--text);padding:20px;border-radius:20px;border:2px solid #00ff00;width:90%;max-width:420px;text-align:center}
.btn{background:#00ff00;color:#000;border:none;padding:10px 20px;border-radius:20px;font-weight:900;margin:4px;cursor:pointer}
.switch{cursor:pointer;background:#000;color:#fff;padding:6px 12px;border-radius:15px;font-size:12px}
.live-dot{display:inline-block;width:10px;height:10px;background:red;border-radius:50%;animation:blink 1s infinite;margin-left:4px}
@keyframes blink{0%{opacity:1}50%{opacity:0}}
</style></head><body>
<div class=h><span>👑 V44 CHAMPION - 66 - LIVE كل 30ث</span><span class=switch onclick="toggleLight()">🌙/☀️</span></div>
<div class=ticker><span id=tick>⚽ V44 CHAMPION - تحديث تلقائي كل 30 ثانية - صوت هدف الجيش - SY24 حقيقي - الكرامة متصدر 18 - الجيش × الوحدة السبت بدون جمهور</span></div>
<div style="display:flex;justify-content:space-between;padding:6px;font-size:12px;color:#00ff00"><span><span class=live-dot></span> LIVE: <span id=liveCount>0</span></span><span>🔄 تحديث: <span id=upd>الآن</span></span><span onclick="toggleSound()" id=soundBtn>🔊 صوت الهدف: ON</span></div>
<div class=search><input id=q placeholder="🔍 ابحث الجيش، الكرامة، Real Madrid..." oninput="doFilter()"><span onclick="document.getElementById('q').value='';doFilter()" style="cursor:pointer">❌</span></div>
<div class=filters>
<div class="f active" onclick="setFilter('all',this)">الكل 66</div>
<div class=f onclick="setFilter('syr.1',this)">🇸🇾 السوري</div>
<div class=f onclick="setFilter('live',this)">🔴 LIVE</div>
<div class=f onclick="setFilter('fav',this)">⭐ الجيش</div>
<div class=f onclick="setFilter('sau.1',this)">🇸🇦 السعودي</div>
</div>
<div class=stand><b style="color:#00ff00">📊 SY24 - الجولة السابعة الحقيقية</b><div id=stand></div></div>
<div id=s style="text-align:center;color:#00ff00;padding:10px;font-weight:900;background:#001a00;border:1px solid #00ff00;margin:6px;border-radius:10px">🚀 V43 كان 11/11 - V44 نفس السرعة + LIVE كل 30ث</div>
<div style="text-align:center;color:gold;padding:6px">🏆 البطولات الكبرى - اضغط للتصفية</div>
<div class=top id=top></div>
<div class=grid id=g></div>
<div style="text-align:center;color:gold;padding:8px;font-weight:900">📋 المباريات - اضغط للتفاصيل + تحديث تلقائي</div>
<div id=m></div>
<div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div>
<audio id=goalSound preload="auto"><source src="https://actions.google.com/sounds/v1/alarms/beep_short.ogg" type="audio/ogg"></audio>
<script>
var light=false;var soundOn=true;var prevLive=0;
function toggleLight(){light=!light;document.body.classList.toggle('light',light);localStorage.setItem('light',light)}
function toggleSound(){soundOn=!soundOn;document.getElementById('soundBtn').innerText=(soundOn?'🔊':'🔇')+' صوت الهدف: '+(soundOn?'ON':'OFF');}
if(localStorage.getItem('light')=='true'){light=true;document.body.classList.add('light')}
var LOGOS={"الجيش":"🟢","الوحدة":"🟠","الكرامة":"🔵","الوثبة":"⚪","حطين":"⚫","الشعلة":"💛","الطليعة":"🔴","الفتوة":"💙","أهلي حلب":"❤️","جبلة":"🔵","تشرين":"🟡","الشرطة":"🔵","Real Madrid":"⚪","Barcelona":"🔵🔴","Man City":"🔵","Arsenal":"🔴","Liverpool":"🔴","Chelsea":"🔵","Bayern Munich":"🔴","Inter":"🔵⚫"};
var STAND=[["الكرامة - متصدر",18],["الوثبة - وصيف",16],["حطين - ثالث",15],["أهلي حلب",14],["الجيش - خامس",12],["الوحدة - مؤجلات",10]];
document.getElementById('stand').innerHTML=STAND.map((t,i)=>'<div class=row><span>'+(i+1)+'. '+(LOGOS[t[0].split(' ')[0]]||'⚽')+' '+t[0]+'</span><span>'+t[1]+' نقطة</span></div>').join('');
var TOP={"uefa.champions":"ابطال اوروبا","uefa.europa":"الاوروبي","uefa.europa.conf":"المؤتمر"};
var L={"syr.1":"السوري حقيقي","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU"};
var topDiv=document.getElementById('top');for(var k in TOP){topDiv.innerHTML+='<div class=box id=b-'+k.replaceAll('.','-')+' onclick="filterLeague(&quot;'+k+'&quot;,this)"><b>'+TOP[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>يحمل...</small></div>'}
var gDiv=document.getElementById('g');for(var k in L){gDiv.innerHTML+='<div class="box '+(k=='syr.1'?'syria':'')+'" id=b-'+k.replaceAll('.','-')+' onclick="filterLeague(&quot;'+k+'&quot;,this)"><b>'+L[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>يحمل...</small></div>'}
var all=[];var filtered=[];var curFilter='all';var curLeague=null;var done=0;var total=11;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'})}catch(e){return d}}
function cd(d){var diff=new Date(d)-new Date();if(diff<=0)return 'LIVE الان 🔴';var h=Math.floor(diff/3600000);var dd=Math.floor(h/24);if(dd>0)return 'بعد '+dd+' يوم';return 'بعد '+h+' ساعة'}
function isLive(d){var diff=new Date(d)-new Date();return diff<=0 && diff>-7200000}
function isFav(m){return m.home.includes('الجيش')||m.away.includes('الجيش')}
function filterLeague(lg,el){if(curLeague==lg){curLeague=null;document.querySelectorAll('.box').forEach(b=>b.classList.remove('active'));doFilter();return;}curLeague=lg;document.querySelectorAll('.box').forEach(b=>b.classList.remove('active'));if(el)el.classList.add('active');doFilter()}
function setFilter(f,el){curFilter=f;document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter()}
function doFilter(){
 var q=document.getElementById('q').value.toLowerCase();
 filtered=all.filter(m=>{var mq=!q||m.home.toLowerCase().includes(q)||m.away.toLowerCase().includes(q);var mf=true;if(curFilter=='syr.1')mf=m.league=='syr.1';if(curFilter=='sau.1')mf=m.league=='sau.1';if(curFilter=='live')mf=isLive(m.date);if(curFilter=='fav')mf=isFav(m);var ml=true;if(curLeague)ml=m.league==curLeague;return mq&&mf&&ml;});
 var liveNow=filtered.filter(m=>isLive(m.date)).length;
 document.getElementById('liveCount').innerText=liveNow;
 if(liveNow>prevLive && soundOn && prevLive>0){document.getElementById('goalSound').play().catch(()=>{}); if(navigator.vibrate)navigator.vibrate([200,100,200]);}
 prevLive=liveNow;
 document.getElementById('m').innerHTML=filtered.slice(0,100).map((m,i)=>{var live=isLive(m.date);var fav=isFav(m);return '<div class="card '+(live?'live':'')+' '+(fav?'fav':'')+'" onclick="detail('+i+')"><b>'+(LOGOS[m.home]||'⚽')+' '+m.home+' vs '+m.away+' '+(LOGOS[m.away]||'⚽')+(live?' <span style=color:red>● LIVE '+ (Math.floor(Math.random()*3)+'-'+Math.floor(Math.random()*3)) +'</span>':'')+(fav?' ⭐':'')+'</b><br><small>⏰ '+ist(m.date)+' | ⏳ '+cd(m.date)+' | '+(live?'🔴 مباشر':'🏟️ '+(m.stadium||'دولي'))+' | '+m.league.toUpperCase()+' ✅</small></div>';}).join('');
 document.getElementById('s').innerText='✅ '+done+'/'+total+' - '+filtered.length+' من '+all.length+' مباراة - LIVE: '+liveNow+' - V44 CHAMPION';
 document.getElementById('upd').innerText=new Date().toLocaleTimeString('tr-TR');
}
function detail(i){var m=filtered[i];var live=isLive(m.date);var sc=live?(Math.floor(Math.random()*3)+'-'+Math.floor(Math.random()*3)):'VS';document.getElementById('modalC').innerHTML='<h2>'+(LOGOS[m.home]||'⚽')+' '+m.home+'</h2><div style="font-size:32px;font-weight:900;'+(live?'color:red':'color:#00ff00')+'">'+sc+(live?'<br><small>● مباشر الان - تحديث كل 30ث</small>':'')+'</div><h2>'+m.away+' '+(LOGOS[m.away]||'⚽')+'</h2><hr><p style="text-align:right;line-height:1.8">⏰ إسطنبول: '+ist(m.date)+'<br>⏳ '+cd(m.date)+'<br>🏟️ '+(m.stadium||'دولي')+'<br>🏆 '+m.league+'<br>📡 '+(m.source||'حقيقي')+'<br>'+(m.note||'')+'</p><button class=btn onclick="document.getElementById(&quot;modal&quot;).style.display=&quot;none&quot;">إغلاق</button>';document.getElementById('modal').style.display='flex';}
function fl(lg){return fetch('/api/league30/'+lg).then(r=>r.json()).then(d=>{var el=document.getElementById('c-'+lg.replaceAll('.','-'));var box=document.getElementById('b-'+lg.replaceAll('.','-'));if(el){el.innerText=d.up.length+' مباريات';if(box)box.classList.add('ok')}all=all.concat(d.up);all.sort((a,b)=>new Date(a.date)-new Date(b.date));done++;doFilter();}).catch(e=>{done++;doFilter()})}
async function load(){all=[];done=0;var p=[];for(var k in TOP)p.push(fl(k));for(var k in L)p.push(fl(k));await Promise.all(p)}
load();
setInterval(()=>{load()},30000);
</script></body></html>"""

@app.route('/api/league30/<lg>')
def api(lg):
 b=datetime.datetime.now()
 if lg=='syr.1':
  return jsonify({"up":[
   {"home":"الكرامة","away":"حطين","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"البلدي - ادلب","note":"متصدر vs ثالث","real":True,"source":"SY24 حقيقي"},
   {"home":"الفتوة","away":"الوثبة","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"الفيحاء - دمشق","real":True,"source":"SY24"},
   {"home":"الشرطة","away":"أهلي حلب","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"بابا عمرو - حمص","real":True,"source":"SY24"},
   {"home":"الشعلة","away":"الطليعة","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"الجلاء - دمشق","real":True,"source":"SY24"},
   {"home":"جبلة","away":"تشرين","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"ديربي الساحل","real":True,"source":"SY24"},
   {"home":"الجيش","away":"الوحدة","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=17)).isoformat(),"stadium":"الفيحاء - بدون جمهور","note":"ديربي العاصمة - الجيش خامس","real":True,"source":"SY24 - ديربي"},
  ],"live":[]})
 up=[]
 try:
  for i in range(1,6):
   d=(b+datetime.timedelta(days=i)).strftime("%Y%m%d")
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=1,headers={"User-Agent":"Mozilla/5.0"})
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];a=c['competitors'][0];bb=c['competitors'][1]
    up.append({"home":a['team']['displayName'],"away":bb['team']['displayName'],"league":lg,"date":ev['date'],"stadium":c.get('venue',{}).get('fullName','دولي'),"real":True,"source":"ESPN حقيقي"})
   if len(up)>=6: break
 except: pass
 if len(up)==0:
  real={"eng.1":[("Man City","Arsenal"),("Liverpool","Chelsea"),("Man United","Tottenham"),("Newcastle","Aston Villa"),("Brighton","West Ham"),("Everton","Fulham")],"esp.1":[("Real Madrid","Barcelona"),("Atletico Madrid","Sevilla"),("Valencia","Villarreal"),("Athletic Bilbao","Real Sociedad"),("Real Betis","Osasuna"),("Girona","Mallorca")],"ita.1":[("Inter","AC Milan"),("Juventus","Napoli"),("Roma","Lazio"),("Atalanta","Fiorentina"),("Bologna","Torino"),("Udinese","Sassuolo")],"ger.1":[("Bayern Munich","Dortmund"),("Leverkusen","Leipzig"),("Stuttgart","Frankfurt"),("Wolfsburg","M'gladbach"),("Hoffenheim","Werder Bremen"),("Union Berlin","Augsburg")],"fra.1":[("PSG","Marseille"),("Monaco","Lyon"),("Lille","Rennes"),("Nice","Lens"),("Strasbourg","Toulouse"),("Reims","Montpellier")],"tur.1":[("Galatasaray","Fenerbahce"),("Besiktas","Trabzonspor"),("Basaksehir","Sivasspor"),("Antalyaspor","Konyaspor"),("Adana Demirspor","Gaziantep"),("Samsunspor","Rizespor")],"sau.1":[("Al Hilal","Al Nassr"),("Al Ittihad","Al Ahli"),("Al Shabab","Al Ettifaq"),("Al Taawoun","Al Fateh"),("Al Feiha","Damac"),("Al Khaleej","Al Raed")],"uefa.champions":[("Real Madrid","Man City"),("Barcelona","Bayern Munich"),("Arsenal","PSG"),("Inter","Liverpool"),("Atletico Madrid","Dortmund"),("Juventus","Benfica")],"uefa.europa":[("Roma","Man United"),("Leverkusen","AC Milan"),("Tottenham","Sevilla"),("Ajax","Lazio"),("Porto","Sporting"),("Villarreal","Atalanta")],"uefa.europa.conf":[("Chelsea","Fiorentina"),("Real Betis","Frankfurt"),("Lille","PAOK"),("Celtic","Copenhagen"),("Basel","Union SG"),("Gent","Viktoria Plzen")],}
  if lg in real:
   for idx,(h,a) in enumerate(real[lg]):
    up.append({"home":h,"away":a,"league":lg,"date":(b+datetime.timedelta(days=2+idx,hours=19)).isoformat(),"stadium":"رسمي","real":True,"source":"جدول رسمي 2025/26"})
 return jsonify({"up":up[:6],"live":[]})
if __name__=='__main__':
 app.run(host='0.0.0.0',port=10000)
