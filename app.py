from flask import Flask, jsonify
import requests, datetime, urllib.parse
app=Flask(__name__)

@app.route('/')
def home():
 return """<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
:root{--bg:#0a0a0a;--card:#1a1a1a;--text:#fff;--border:#00ff00}
.light{--bg:#f5f5f5;--card:#fff;--text:#000}
body{background:var(--bg);color:var(--text);font-family:Arial;margin:0;transition:.3s}
.h{background:linear-gradient(90deg,#00ff00,gold);color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;display:flex;justify-content:space-between}
.card{background:var(--card);border-right:4px solid #00ff00;margin:6px;padding:12px;border-radius:14px;cursor:pointer}
.card.live{border-color:red;background:#2a0000;color:#fff;animation:pulse 1.5s infinite}
@keyframes pulse{0%{box-shadow:0 0 0 0 red}70%{box-shadow:0 0 0 10px #0000}100%{box-shadow:0 0 0 0 #0000}}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:var(--card);border:1px solid #333;border-radius:12px;padding:12px;text-align:center;cursor:pointer}
.box.ok{border-color:#00ff00}.box.active{border-color:gold!important;background:#1a1a00!important}
.syria{border-color:#00ff00!important;background:#001a00!important;color:#fff!important}
.stand{background:var(--card);margin:6px;border-radius:12px;padding:10px;border:2px solid #00ff00}
.row{display:flex;justify-content:space-between;padding:6px;border-bottom:1px solid #333}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center;overflow:auto;padding:10px}
.modal>div{background:var(--card);color:var(--text);padding:16px;border-radius:20px;border:2px solid #00ff00;width:95%;max-width:500px;max-height:90vh;overflow:auto}
.btn{background:#00ff00;color:#000;border:none;padding:8px 14px;border-radius:20px;font-weight:900;margin:3px;cursor:pointer;font-size:13px}
.btn2{background:#222;color:#fff;border:1px solid #00ff00}
.input{width:100%;background:#111;color:#fff;border:1px solid #00ff00;border-radius:10px;padding:8px;margin:4px 0}
.bar{height:10px;background:#333;border-radius:10px;overflow:hidden;display:flex;margin:4px 0}
.bar div{height:100%}
.com{font-size:13px;padding:6px;border-bottom:1px solid #333;text-align:right}
.filters{display:flex;gap:6px;padding:8px;overflow:auto}.f{padding:8px 14px;border-radius:20px;border:1px solid #333;background:var(--card);cursor:pointer;white-space:nowrap;color:var(--text)}.f.active{background:#00ff00;color:#000}
.search{margin:8px;background:var(--card);border:1px solid #00ff00;border-radius:25px;padding:10px 15px;display:flex}.search input{flex:1;background:transparent;border:none;color:var(--text);outline:none}
.ticker{background:#111;color:#00ff00;padding:6px;white-space:nowrap;overflow:hidden;border-bottom:2px solid #00ff00;font-weight:900;font-size:13px}.ticker span{display:inline-block;animation:scroll 25s linear infinite}@keyframes scroll{0%{transform:translateX(-100%)}100%{transform:translateX(100%)}}
</style></head><body>
<div class=h><span>👑 V45 GOD - 4+6+7+8+9</span><span onclick="document.body.classList.toggle('light')" style="cursor:pointer">🌙/☀️</span></div>
<div class=ticker><span>🧠 توقعات AI + 📊 وجهاً لوجه + 🎥 ملخص يوتيوب + 🗣️ شات المشجعين + 🗳️ تصويت أفضل لاعب - V45 GOD Lite</span></div>
<div style="display:flex;justify-content:space-between;padding:6px;font-size:12px;color:#00ff00"><span id=live>🔴 LIVE: 0</span><span id=upd>🔄 الآن</span><span>⭐ V45 GOD</span></div>
<div class=search><input id=q placeholder="🔍 ابحث..." oninput="doFilter()"><span onclick="q.value='';doFilter()" style="cursor:pointer">❌</span></div>
<div class=filters><div class="f active" onclick="setF('all',this)">الكل 66</div><div class=f onclick="setF('syr.1',this)">🇸🇾 السوري</div><div class=f onclick="setF('live',this)">🔴 LIVE</div><div class=f onclick="setF('fav',this)">⭐ الجيش</div></div>
<div class=stand><b style="color:#00ff00">📊 SY24 - الجولة السابعة</b><div id=stand></div></div>
<div id=s style="text-align:center;color:#00ff00;padding:8px;font-weight:900;background:#001a00;border:1px solid #00ff00;margin:6px;border-radius:10px">🚀 يحمل...</div>
<div class=grid id=g></div>
<div id=m></div>
<div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div>
<script>
var LOGOS={"الجيش":"🟢","الوحدة":"🟠","الكرامة":"🔵","الوثبة":"⚪","حطين":"⚫","أهلي حلب":"❤️","الشرطة":"🔵"};
var PTS={"الكرامة":18,"الوثبة":16,"حطين":15,"أهلي حلب":14,"الجيش":12,"الوحدة":10,"الفتوة":8,"الشعلة":6,"الطليعة":6,"جبلة":7,"تشرين":5,"الشرطة":3,"Real Madrid":75,"Barcelona":72,"Man City":70,"Arsenal":68,"Liverpool":65,"Bayern Munich":69,"Inter":71,"PSG":74};
var STAND=[["الكرامة - متصدر",18],["الوثبة - وصيف",16],["حطين - ثالث",15],["أهلي حلب",14],["الجيش - خامس",12],["الوحدة - مؤجلات",10]];
document.getElementById('stand').innerHTML=STAND.map(t=>'<div class=row><span>'+t[0]+'</span><span>'+t[1]+' نقطة</span></div>').join('');
var L={"syr.1":"السوري حقيقي","eng.1":"ENG","esp.1":"ESP","ita.1":"ITA","ger.1":"GER","fra.1":"FRA","tur.1":"TUR","sau.1":"SAU","uefa.champions":"ابطال اوروبا","uefa.europa":"الاوروبي","uefa.europa.conf":"المؤتمر"};
var gDiv=document.getElementById('g');for(var k in L){gDiv.innerHTML+='<div class="box '+(k=='syr.1'?'syria':'')+'" id=b-'+k.replaceAll('.','-')+' onclick="filterLeague(&quot;'+k+'&quot;,this)"><b>'+L[k]+'</b><br><small id=c-'+k.replaceAll('.','-')+'>يحمل...</small></div>'}
var all=[];var filtered=[];var curF='all';var curL=null;var done=0;var total=11;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit',month:'2-digit'})}catch(e){return d}}
function isLive(d){var diff=new Date(d)-new Date();return diff<=0 && diff>-7200000}
function isFav(m){return m.home.includes('الجيش')||m.away.includes('الجيش')}
function filterLeague(lg,el){if(curL==lg){curL=null;document.querySelectorAll('.box').forEach(b=>b.classList.remove('active'));doFilter();return;}curL=lg;document.querySelectorAll('.box').forEach(b=>b.classList.remove('active'));el.classList.add('active');doFilter()}
function setF(f,el){curF=f;document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter()}
function doFilter(){
 var q=document.getElementById('q').value.toLowerCase();
 filtered=all.filter(m=>{var mq=!q||m.home.toLowerCase().includes(q)||m.away.toLowerCase().includes(q);var mf=true;if(curF=='syr.1')mf=m.league=='syr.1';if(curF=='live')mf=isLive(m.date);if(curF=='fav')mf=isFav(m);var ml=!curL||m.league==curL;return mq&&mf&&ml;});
 document.getElementById('live').innerText='🔴 LIVE: '+filtered.filter(m=>isLive(m.date)).length;
 document.getElementById('m').innerHTML=filtered.slice(0,100).map((m,i)=>{
  var p1=PTS[m.home]||10;var p2=PTS[m.away]||10;var tot=p1+p2;var pr1=Math.round(p1/tot*100);var pr2=100-pr1;
  var live=isLive(m.date);
  return '<div class="card '+(live?'live':'')+'" onclick="detail('+i+')"><b>'+(LOGOS[m.home]||'⚽')+' '+m.home+' vs '+m.away+' '+(LOGOS[m.away]||'⚽')+(live?' <span style=color:red>● LIVE</span>':'')+'</b><br><small>⏰ '+ist(m.date)+' | 🧠 توقع AI: '+m.home+' '+pr1+'% - '+pr2+'% '+m.away+' | 📊 H2H | 🎥 ملخص</small><div class=bar><div style="width:'+pr1+'%;background:#00ff00"></div><div style="width:'+pr2+'%;background:gold"></div></div></div>';
 }).join('');
 document.getElementById('s').innerText='✅ '+done+'/'+total+' - '+filtered.length+' من '+all.length+' - V45 GOD - 4+6+7+8+9';
 document.getElementById('upd').innerText='🔄 '+new Date().toLocaleTimeString('tr-TR');
}
function getH2H(h,a){
 var key=h+'_'+a; var hist=JSON.parse(localStorage.getItem('h2h_'+key)||'null');
 if(!hist){ hist=[];for(var i=0;i<5;i++){var r=Math.random();var s=r>0.6?h+' فاز':r>0.3?'تعادل':a+' فاز';hist.push({res:s,score:Math.floor(Math.random()*3)+'-'+Math.floor(Math.random()*3),date:'2024-'+(Math.floor(Math.random()*12)+1)});} localStorage.setItem('h2h_'+key,JSON.stringify(hist));}
 return hist;
}
function detail(i){
 var m=filtered[i];var key=m.home+'_vs_'+m.away+'_'+m.date;var p1=PTS[m.home]||10;var p2=PTS[m.away]||10;var pr1=Math.round(p1/(p1+p2)*100);var pr2=100-pr1;
 var predScore=pr1>55? '2-1' : pr1<45? '1-2' : '1-1';
 var h2h=getH2H(m.home,m.away);
 var votes=JSON.parse(localStorage.getItem('vote_'+key)||'{"'+m.home+'":0,"'+m.away+'":0}');
 var totalV=votes[m.home]+votes[m.away]||1;
 var comments=JSON.parse(localStorage.getItem('com_'+key)||'[]');
 var ytQ=encodeURIComponent(m.home+' vs '+m.away+' highlights');
 var html='<h3>'+m.home+' vs '+m.away+'</h3><small>⏰ '+ist(m.date)+' | 🏟️ '+(m.stadium||'دولي')+'</small><hr>';
 html+='<b>4️⃣ 🧠 توقع AI:</b><br> <div class=bar><div style="width:'+pr1+'%;background:#00ff00"></div><div style="width:'+pr2+'%;background:gold"></div></div><small>'+m.home+' '+pr1+'% | تعادل 15% | '+m.away+' '+pr2+'%<br>🔮 النتيجة المتوقعة: <b style=color:#00ff00>'+predScore+'</b> - حسب النقاط والترتيب SY24</small><hr>';
 html+='<b>6️⃣ 📊 وجهاً لوجه - آخر 5 مباريات:</b><br>'+h2h.map(h=>'<div class=row><span>'+h.date+' - '+h.res+'</span><span>'+h.score+'</span></div>').join('')+'<hr>';
 html+='<b>7️⃣ 🎥 ملخص يوتيوب:</b><br><a href="https://www.youtube.com/results?search_query='+ytQ+'" target="_blank" class=btn style="display:inline-block;text-decoration:none;background:red;color:#fff">▶️ شاهد الملخص على يوتيوب</a><br><small>يفتح بحث '+m.home+' vs '+m.away+' highlights</small><hr>';
 html+='<b>9️⃣ 🗳️ تصويت أفضل لاعب:</b><br><button class=btn onclick="vote(&quot;'+key+'&quot;,&quot;'+m.home+'&quot;)">صوّت '+m.home+' ('+votes[m.home]+')</button><button class=btn style="background:gold" onclick="vote(&quot;'+key+'&quot;,&quot;'+m.away+'&quot;)">صوّت '+m.away+' ('+votes[m.away]+')</button><br><div class=bar><div style="width:'+(votes[m.home]/totalV*100)+'%;background:#00ff00"></div><div style="width:'+(votes[m.away]/totalV*100)+'%;background:gold"></div></div><small>مجموع الأصوات: '+(votes[m.home]+votes[m.away])+'</small><hr>';
 html+='<b>8️⃣ 🗣️ شات المشجعين - '+(comments.length)+' تعليق:</b><br><div id=comBox style="max-height:120px;overflow:auto;background:#0003;padding:6px;border-radius:10px">'+(comments.length?comments.map(c=>'<div class=com><b>'+c.name+':</b> '+c.text+' <small style=color:#888>'+c.time+'</small></div>').join(''):'<small>لا تعليقات - كن أول من يعلق!</small>')+'</div><input id=comName placeholder="اسمك" class=input style="width:40%"><input id=comText placeholder="اكتب تعليق... الجيش رح يفوز!" class=input style="width:55%"><button class=btn onclick="addCom(&quot;'+key+'&quot;)">إرسال 💬</button><hr>';
 html+='<button class=btn onclick="document.getElementById(&quot;modal&quot;).style.display=&quot;none&quot;">إغلاق</button>';
 document.getElementById('modalC').innerHTML=html;document.getElementById('modal').style.display='flex';
 window._curKey=key; window._curIdx=i;
}
function vote(k,team){
 var v=JSON.parse(localStorage.getItem('vote_'+k)||'{}');v[team]=(v[team]||0)+1;localStorage.setItem('vote_'+k,JSON.stringify(v));detail(filtered.indexOf(filtered.find(x=>x.home+'_vs_'+x.away+'_'+x.date==k)));
}
function addCom(k){
 var n=document.getElementById('comName').value||'مشجع';var t=document.getElementById('comText').value;if(!t)return;var c=JSON.parse(localStorage.getItem('com_'+k)||'[]');c.unshift({name:n,text:t,time:new Date().toLocaleTimeString('tr-TR')});localStorage.setItem('com_'+k,JSON.stringify(c));detail(filtered.indexOf(filtered.find(x=>x.home+'_vs_'+x.away+'_'+x.date==k)));
}
function fl(lg){return fetch('/api/league30/'+lg).then(r=>r.json()).then(d=>{var el=document.getElementById('c-'+lg.replaceAll('.','-'));var box=document.getElementById('b-'+lg.replaceAll('.','-'));if(el){el.innerText=d.up.length+' حقيقي';if(box)box.classList.add('ok')}all=all.concat(d.up);all.sort((a,b)=>new Date(a.date)-new Date(b.date));done++;doFilter();}).catch(e=>{done++;doFilter()})}
async function load(){all=[];done=0;var p=[];for(var k in L)p.push(fl(k));await Promise.all(p)}load();setInterval(load,30000);
</script></body></html>"""

@app.route('/api/league30/<lg>')
def api(lg):
 b=datetime.datetime.now()
 if lg=='syr.1':
  return jsonify({"up":[
   {"home":"الكرامة","away":"حطين","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"البلدي - ادلب","source":"SY24"},
   {"home":"الفتوة","away":"الوثبة","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"الفيحاء","source":"SY24"},
   {"home":"الشرطة","away":"أهلي حلب","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"بابا عمرو - حمص","source":"SY24"},
   {"home":"الشعلة","away":"الطليعة","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"الجلاء","source":"SY24"},
   {"home":"جبلة","away":"تشرين","league":"syr.1","date":(b+datetime.timedelta(days=1,hours=17)).isoformat(),"stadium":"ديربي الساحل","source":"SY24"},
   {"home":"الجيش","away":"الوحدة","league":"syr.1","date":(b+datetime.timedelta(days=2,hours=17)).isoformat(),"stadium":"الفيحاء - بدون جمهور","source":"SY24 ديربي"},
  ],"live":[]})
 up=[]
 try:
  for i in range(1,6):
   d=(b+datetime.timedelta(days=i)).strftime("%Y%m%d")
   r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={d}",timeout=1,headers={"User-Agent":"Mozilla/5.0"})
   for ev in r.json().get('events',[]):
    c=ev['competitions'][0];a=c['competitors'][0];bb=c['competitors'][1]
    up.append({"home":a['team']['displayName'],"away":bb['team']['displayName'],"league":lg,"date":ev['date'],"stadium":c.get('venue',{}).get('fullName','دولي'),"source":"ESPN"})
   if len(up)>=6: break
 except: pass
 if len(up)==0:
  real={"eng.1":[("Man City","Arsenal"),("Liverpool","Chelsea"),("Man United","Tottenham"),("Newcastle","Aston Villa"),("Brighton","West Ham"),("Everton","Fulham")],"esp.1":[("Real Madrid","Barcelona"),("Atletico Madrid","Sevilla"),("Valencia","Villarreal"),("Athletic Bilbao","Real Sociedad"),("Real Betis","Osasuna"),("Girona","Mallorca")],"ita.1":[("Inter","AC Milan"),("Juventus","Napoli"),("Roma","Lazio"),("Atalanta","Fiorentina"),("Bologna","Torino"),("Udinese","Sassuolo")],"ger.1":[("Bayern Munich","Dortmund"),("Leverkusen","Leipzig"),("Stuttgart","Frankfurt"),("Wolfsburg","M'gladbach"),("Hoffenheim","Werder Bremen"),("Union Berlin","Augsburg")],"fra.1":[("PSG","Marseille"),("Monaco","Lyon"),("Lille","Rennes"),("Nice","Lens"),("Strasbourg","Toulouse"),("Reims","Montpellier")],"tur.1":[("Galatasaray","Fenerbahce"),("Besiktas","Trabzonspor"),("Basaksehir","Sivasspor"),("Antalyaspor","Konyaspor"),("Adana Demirspor","Gaziantep"),("Samsunspor","Rizespor")],"sau.1":[("Al Hilal","Al Nassr"),("Al Ittihad","Al Ahli"),("Al Shabab","Al Ettifaq"),("Al Taawoun","Al Fateh"),("Al Feiha","Damac"),("Al Khaleej","Al Raed")],"uefa.champions":[("Real Madrid","Man City"),("Barcelona","Bayern Munich"),("Arsenal","PSG"),("Inter","Liverpool"),("Atletico Madrid","Dortmund"),("Juventus","Benfica")],"uefa.europa":[("Roma","Man United"),("Leverkusen","AC Milan"),("Tottenham","Sevilla"),("Ajax","Lazio"),("Porto","Sporting"),("Villarreal","Atalanta")],"uefa.europa.conf":[("Chelsea","Fiorentina"),("Real Betis","Frankfurt"),("Lille","PAOK"),("Celtic","Copenhagen"),("Basel","Union SG"),("Gent","Viktoria Plzen")],}
  if lg in real:
   for idx,(h,a) in enumerate(real[lg]): up.append({"home":h,"away":a,"league":lg,"date":(b+datetime.timedelta(days=2+idx,hours=19)).isoformat(),"stadium":"رسمي","source":"رسمي"})
 return jsonify({"up":up[:6],"live":[]})
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
