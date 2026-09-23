from flask import Flask, jsonify
import requests
app = Flask(__name__)

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V79 ULTRA PRO - بحث + مفضلة + LIVE</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0;padding-bottom:80px}
.h{background:linear-gradient(90deg,#0f0,gold);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:11px}
.search-box{margin:8px;background:#111;border:2px solid #0f0;border-radius:22px;padding:8px 14px;display:flex;align-items:center;gap:8px}
.search-box input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.league-header{background:linear-gradient(90deg,#111,#222);border:2px solid #0f0;margin:10px 8px 0 8px;padding:12px;border-radius:14px 14px 0 0;display:flex;justify-content:space-between;align-items:center;cursor:pointer}
.league-header.eng{border-color:#3d1aff;background:linear-gradient(90deg,#1a0033,#2a1a4a)}
.league-header.esp{border-color:#ff0000;background:linear-gradient(90deg,#330000,#4a1a4a)}
.league-header.sau{border-color:#00a651;background:linear-gradient(90deg,#002a10,#0a3a1a)}
.league-header.ita{border-color:#008C45;background:linear-gradient(90deg,#001a0a,#0a2a1a)}
.league-header.ucl{border-color:gold;background:linear-gradient(90deg,#1a1a00,#2a2a00)}
.group{background:#0a0a0a;margin:0 8px 8px 8px;border-radius:0 0 14px 14px;border:1px solid #333;border-top:none;overflow:hidden;transition:all 0.3s}
.group.hidden{max-height:0;opacity:0;margin:0 8px}
.card{background:#111;border-right:5px solid #0f0;margin:6px;padding:10px;border-radius:12px;border:1px solid #333;display:flex;align-items:center;gap:8px;cursor:pointer}
.card.live{border-right-color:red;background:#1a0000;box-shadow:0 0 15px red;animation:pulse 1s infinite}
.card.fav{border-right-color:gold;background:#1a1a00;box-shadow:0 0 12px gold}
@keyframes pulse{0%,100%{box-shadow:0 0 10px red}50%{box-shadow:0 0 20px red}}
.team-logo{width:36px;height:36px;background:#fff;border-radius:50%;padding:2px;object-fit:contain}
.badge-live{background:red;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px;animation:blink 0.8s infinite}
.badge-ft{background:gray;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px}
.badge-fav{background:gold;color:#000;padding:3px 6px;border-radius:14px;font-size:10px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.4}}
.f{padding:6px 10px;border-radius:20px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#0f0;color:#000;font-weight:900}
.league-count{background:#0f0;color:#000;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:900}
#stadium{display:none;background:radial-gradient(#0a4a0a,#000);margin:8px;border-radius:20px;padding:10px;border:2px solid #0f0;position:sticky;top:50px;z-index:25}
canvas{width:100%;height:180px;border-radius:14px;background:#0a4a0a;display:block}
.fav-btn{background:#222;border:1px solid gold;color:gold;padding:4px 8px;border-radius:14px;cursor:pointer;font-size:12px}
.fav-btn.active{background:gold;color:#000}
</style></head><body>
<div class=h>✅ V79 ULTRA PRO - 🔍 بحث + ⭐ مفضلة + 🔔 تنبيه LIVE + 🏴󐁧󐁢󐁥󐁮󐁧󐁿 🇪🇸 🇸🇦 🏆</div>
<div class="search-box"><span>🔍</span><input id="search" placeholder="ابحث فريق... مثل Real, Liverpool, الهلال" oninput="render()"><span onclick="document.getElementById('search').value='';render()" style="cursor:pointer">✕</span></div>
<div style="padding:6px;white-space:nowrap;overflow:auto;text-align:center">
<span class="f active" id="fa" onclick="setF('all')">🌐 الكل 36 مرتب</span>
<span class=f onclick="setF('fav')">⭐ مفضلتي</span>
<span class=f id="fl" onclick="setF('live')">🔴 LIVE</span>
<span class=f onclick="toggleAll()">📂 طي/فتح</span>
<span class=f onclick="loadReal()">🔄</span>
</div>
<div id=status style="text-align:center;padding:8px;background:#111;margin:8px;border-radius:12px;color:gold;font-size:11px">⏳ جاري الجلب...</div>
<div id=stadium><div style="display:flex;justify-content:space-between;color:#0f0;font-weight:900;font-size:11px"><span id=sTitle>🏟️ ملعب 3D</span><span style="background:red;color:#fff;padding:2px 8px;border-radius:10px">● LIVE</span><span onclick="document.getElementById('stadium').style.display='none'" style="cursor:pointer;background:#333;padding:2px 8px;border-radius:8px">✕</span></div><canvas id=c></canvas><div id=comment style="background:#000;color:#0f0;padding:6px;border-radius:8px;margin-top:6px;text-align:center;font-weight:900;font-size:12px">⚽ هجمة خطيرة!</div></div>
<div id=m></div>
<script>
var realMatches=[]; var favs=JSON.parse(localStorage.getItem('favs')||'[]');
var leagueIcons={
 'eng.1':{icon:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',name:'الدوري الإنجليزي',flag:'🇬🇧',cls:'eng'},
 'esp.1':{icon:'🇪🇸',name:'La Liga - الإسباني',flag:'🇪🇸',cls:'esp'},
 'sau.1':{icon:'🇸🇦',name:'الدوري السعودي روشن',flag:'🇸🇦',cls:'sau'},
 'ita.1':{icon:'🇮🇹',name:'Serie A',flag:'🇮🇹',cls:'ita'},
 'ger.1':{icon:'🇩🇪',name:'Bundesliga',flag:'🇩🇪',cls:'eng'},
 'uefa.champions':{icon:'🏆',name:'دوري أبطال أوروبا',flag:'⭐',cls:'ucl'},
 'uefa.europa':{icon:'🏆',name:'الدوري الأوروبي',flag:'🏆',cls:'ucl'},
 'eng.fa':{icon:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',name:'كأس إنجلترا',flag:'🏆',cls:'eng'}
};
async function loadReal(){
 try{
  var r=await fetch('/api/real-matches'); var j=await r.json();
  realMatches=j.matches || [];
  var liveCount=realMatches.filter(m=>m.isLive).length;
  document.getElementById('status').innerHTML='✅ '+realMatches.length+' مباراة - 🔍 بحث + ⭐ مفضلتي ('+favs.length+') + 🔴 LIVE حقيقي: '+liveCount+'<br><small>🔍 اكتب Real يطلع ريال مدريد - ⭐ اضغط نجمة لحفظ فريقك - 🔔 إذا في LIVE بيعمل اهتزاز</small>';
  if(liveCount>0){ if(navigator.vibrate) navigator.vibrate([200,100,200]); document.getElementById('status').style.background='#330000'; }
  render();
 }catch(e){}
}
var curF='all';
function setF(f){curF=f; document.querySelectorAll('.f').forEach(x=>x.classList.remove('active')); render();}
function toggleFav(team){
 var i=favs.indexOf(team);
 if(i>=0) favs.splice(i,1); else favs.push(team);
 localStorage.setItem('favs',JSON.stringify(favs));
 render();
}
function render(){
 var q=document.getElementById('search').value.toLowerCase();
 var filtered=realMatches.filter(m=>{
  if(q &&!(m.home.toLowerCase().includes(q) || m.away.toLowerCase().includes(q) || m.competition.toLowerCase().includes(q))) return false;
  if(curF=='live' &&!m.isLive) return false;
  if(curF=='fav' &&!favs.some(f=>m.home.includes(f)||m.away.includes(f))) return false;
  return true;
 });
 var grouped={};
 filtered.forEach(m=>{ if(!grouped[m.league]) grouped[m.league]=[]; grouped[m.league].push(m); });
 var html='';
 var order=['eng.1','esp.1','sau.1','uefa.champions','ita.1','ger.1','fra.1'];
 Object.keys(grouped).forEach(lg=>{ if(!order.includes(lg)) order.push(lg); });
 // مفضلة فوق
 if(curF!='fav') {
  var favMatches=realMatches.filter(m=>favs.some(f=>m.home.includes(f)||m.away.includes(f)));
  if(favMatches.length>0 && q==''){
   html+='<div class="league-header" style="border-color:gold;background:linear-gradient(90deg,#2a2a00,#3a3a00)"><div><span style="font-size:20px">⭐</span> <b>⭐ مفضلتي - '+favMatches.length+'</b></div><span class="league-count" style="background:gold">'+favMatches.length+'</span></div><div class="group">';
   favMatches.slice(0,10).forEach(m=>{
    html+='<div class="card fav"><img class="team-logo" src="'+m.homeLogo+'" onerror="this.src=\\'https://via.placeholder.com/36\\'"><div style="flex:1"><b>⭐ '+m.home+' vs '+m.away+'</b> '+(m.isLive?'<span class=badge-live>🔴 LIVE '+m.score+'</span>':'<span class=badge-ft>✅ '+m.score+'</span>')+'<br><small>🏆 '+m.competition+'</small></div><img class="team-logo" src="'+m.awayLogo+'"></div>';
   });
   html+='</div>';
  }
 }
 order.forEach(lg=>{
  if(!grouped[lg]) return;
  var info=leagueIcons[lg]||{icon:'⚽',name:lg,flag:'⚽',cls:'eng'};
  var matches=grouped[lg];
  html+='<div class="league-header '+info.cls+'" onclick="toggleLeague(\\''+lg+'\\')"><div><span style="font-size:20px">'+info.icon+'</span> <b>'+info.flag+' '+info.name+'</b> <span class="league-count">'+matches.length+'</span></div><span id="arr-'+lg+'">▶</span></div>';
  html+='<div class="group" id="group-'+lg+'">';
  matches.forEach(m=>{
   var isFav=favs.includes(m.home)||favs.includes(m.away);
   html+='<div class="card '+(m.isLive?'live':'')+(isFav?' fav':'')+'"><img class="team-logo" src="'+m.homeLogo+'" onerror="this.src=\\'https://via.placeholder.com/36\\'"><div style="flex:1" onclick="openStadium(\\''+m.home+' vs '+m.away+'\\',\\''+m.home+'\\',\\''+m.away+'\\')"><b>'+m.home+' vs '+m.away+'</b> '+(m.isLive?'<span class=badge-live>🔴 LIVE '+m.score+'</span>':'<span class=badge-ft>✅ '+m.score+' FT</span>')+(isFav?'<span class=badge-fav> ⭐</span>':'')+'<br><small style="color:gold">📅 '+m.date+' - '+info.name+'</small></div><button class="fav-btn '+(isFav?'active':'')+'" onclick="toggleFav(\\''+m.home+'\\')">⭐</button><img class="team-logo" src="'+m.awayLogo+'" onerror="this.src=\\'https://via.placeholder.com/36\\'"></div>';
  });
  html+='</div>';
 });
 if(filtered.length==0) html+='<div style="text-align:center;padding:20px;color:gold"><b>🔍 لا يوجد نتائج لـ "'+q+'"</b><br><small>جرب Real, Liverpool, Barcelona, الهلال</small></div>';
 document.getElementById('m').innerHTML=html;
}
function toggleLeague(lg){ var g=document.getElementById('group-'+lg); g.classList.toggle('hidden'); }
function toggleAll(){ document.querySelectorAll('.group').forEach(g=>g.classList.toggle('hidden')); }
var bx=50,by=50,vx=2,vy=1.5;
function openStadium(title,h,a){
 document.getElementById('stadium').style.display='block';
 document.getElementById('sTitle').innerText='🏟️ '+title;
 var canvas=document.getElementById('c'); var ctx=canvas.getContext('2d');
 canvas.width=canvas.offsetWidth*2; canvas.height=180*2;
 var coms=["⚽ هجمة خطيرة لـ "+h+"!","🔥 تسديدة من "+a+"!","😱 كادت تدخل!","🎯 ركنية!","💥 تدخل قوي!"];
 var ci=0;
 (function loop(){ ctx.fillStyle='#0a4a0a'; ctx.fillRect(0,0,canvas.width,canvas.height); ctx.strokeStyle='#fff'; ctx.lineWidth=3; ctx.strokeRect(20,20,canvas.width-40,canvas.height-40); ctx.beginPath(); ctx.moveTo(20,canvas.height/2); ctx.lineTo(canvas.width-20,canvas.height/2); ctx.stroke(); ctx.beginPath(); ctx.arc(canvas.width/2,canvas.height/2,50,0,Math.PI*2); ctx.stroke(); ctx.fillStyle='#fff'; ctx.beginPath(); ctx.arc(bx/100*canvas.width,by/100*canvas.height,9,0,Math.PI*2); ctx.fill(); bx+=vx; by+=vy; if(bx<5||bx>95)vx*=-1; if(by<5||by>95)vy*=-1; requestAnimationFrame(loop); })();
 setInterval(()=>{ document.getElementById('comment').innerText=coms[ci%coms.length]; ci++; },2500);
 document.getElementById('stadium').scrollIntoView({behavior:'smooth'});
}
loadReal(); setInterval(loadReal,60000);
</script></body></html>
"""
@app.route('/')
def home(): return HTML
@app.route('/api/real-matches')
def real_matches():
    matches=[]
    try:
        for lg in ['eng.1','esp.1','sau.1','ita.1','ger.1','fra.1','uefa.champions','uefa.europa','eng.fa']:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=4)
                if r.status_code==200:
                    for ev in r.json().get('events',[])[:10]:
                        comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                        if len(comps)>=2:
                            matches.append({"home":comps[0]['team']['displayName'],"away":comps[1]['team']['displayName'],"homeLogo":comps[0]['team'].get('logo',''),"awayLogo":comps[1]['team'].get('logo',''),"competition":ev.get('league',{}).get('name',lg),"status":ev.get('status',{}).get('type',{}).get('description','FT'),"score":f"{comps[0].get('score','-')} - {comps[1].get('score','-')}","date":ev.get('date','')[:10],"league":lg,"isLive":ev.get('status',{}).get('type',{}).get('state','pre')=='in'})
            except: continue
    except: pass
    return jsonify({"matches":matches})

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
