from flask import Flask, jsonify, request
import requests
from datetime import datetime
app = Flask(__name__)

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V81 ARCHIVE FULL - كل السابقة والقادمة</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#0f0,gold);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:11px}
.search-box{margin:8px;background:#111;border:2px solid #0f0;border-radius:22px;padding:8px 14px;display:flex;gap:8px}
.search-box input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.league-header{border:2px solid #0f0;margin:10px 8px 0 8px;padding:12px;border-radius:14px 14px 0 0;display:flex;justify-content:space-between;cursor:pointer}
.league-header.eng{background:linear-gradient(90deg,#1a0033,#2a1a4a);border-color:#3d1aff}
.league-header.esp{background:linear-gradient(90deg,#330000,#4a1a1a);border-color:#ff0000}
.league-header.sau{background:linear-gradient(90deg,#002a10,#0a3a1a);border-color:#00a651}
.league-header.ucl{background:linear-gradient(90deg,#1a1a00,#2a2a00);border-color:gold}
.group{background:#0a0a0a;margin:0 8px 8px 8px;border-radius:0 0 14px 14px;border:1px solid #333;border-top:none}
.card{background:#111;border-right:5px solid #0f0;margin:6px;padding:10px;border-radius:12px;display:flex;align-items:center;gap:8px;cursor:pointer}
.card.live{border-right-color:red;background:#1a0000;box-shadow:0 0 12px red}
.team-logo{width:36px;height:36px;background:#fff;border-radius:50%;padding:2px;object-fit:contain}
.badge-live{background:red;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px;animation:blink 0.8s infinite}
.badge-ft{background:gray;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.4}}
.f{padding:6px 10px;border-radius:20px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}
#archive{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.97);z-index:100;overflow:auto;padding:6px}
.archive-box{background:#111;border:2px solid gold;border-radius:20px;margin:10px auto;max-width:650px;overflow:hidden}
.archive-head{background:linear-gradient(90deg,gold,#0f0);color:#000;padding:14px;text-align:center;font-weight:900;display:flex;justify-content:space-between}
.tab{padding:8px 14px;border-radius:20px;border:1px solid #444;background:#222;color:#fff;margin:3px;cursor:pointer;font-size:11px;display:inline-block}.tab.active{background:gold;color:#000;font-weight:900}
.archive-match{background:#1a1a1a;margin:6px;padding:10px;border-radius:12px;border-right:4px solid #0f0;display:flex;justify-content:space-between;align-items:center}
.archive-match.past{border-right-color:#888}
.archive-match.future{border-right-color:#0f0;background:#0a1a0a}
.archive-match.live{border-right-color:red;background:#1a0000}
</style></head><body>
<div class=h>✅ V81 ARCHIVE FULL - 📚 كل المباريات السابقة + القادمة لكل نادي ومنتخب - V81</div>
<div class="search-box"><span>🔍</span><input id="search" placeholder="ابحث فريق... Liverpool, Real, الهلال, Syria, Brazil" oninput="render()"><span onclick="this.previousElementSibling.value='';render()" style="cursor:pointer">✕</span></div>
<div style="padding:6px;white-space:nowrap;overflow:auto;text-align:center">
<span class=f onclick="setF('all')">🌐 الكل</span><span class=f onclick="setF('fav')">⭐ مفضلتي</span><span class=f onclick="setF('live')">🔴 LIVE</span><span class=f onclick="loadReal()">🔄 تحديث</span>
</div>
<div id=status style="text-align:center;padding:8px;background:#111;margin:8px;border-radius:12px;color:gold;font-size:11px"></div>
<div id=m></div>
<div id=archive><div class=archive-box>
<div class=archive-head><span id=archTitle>📚 أرشيف</span><span onclick="document.getElementById('archive').style.display='none'" style="background:#000;color:#fff;padding:6px 12px;border-radius:12px;cursor:pointer">✕</span></div>
<div style="padding:8px;text-align:center;background:#000">
<span class="tab active" id="tab-all" onclick="setArchTab('all')">🌐 الكل <b id="c-all"></b></span>
<span class="tab" id="tab-past" onclick="setArchTab('past')">✅ سابقة <b id="c-past"></b></span>
<span class="tab" id="tab-future" onclick="setArchTab('future')">⏰ قادمة <b id="c-future"></b></span>
<span class="tab" id="tab-live" onclick="setArchTab('live')">🔴 LIVE <b id="c-live"></b></span>
</div>
<div id=archContent style="padding:8px;max-height:70vh;overflow:auto"></div>
</div></div>
<script>
var realMatches=[]; var favs=JSON.parse(localStorage.getItem('favs')||'[]');
var leagueIcons={'eng.1':{icon:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',name:'الإنجليزي',cls:'eng'},'esp.1':{icon:'🇪🇸',name:'La Liga',cls:'esp'},'sau.1':{icon:'🇸🇦',name:'السعودي',cls:'sau'},'ita.1':{icon:'🇮🇹',name:'Serie A',cls:'eng'},'uefa.champions':{icon:'🏆',name:'أبطال أوروبا',cls:'ucl'}};
async function loadReal(){
 var r=await fetch('/api/real-matches'); var j=await r.json();
 realMatches=j.matches||[];
 document.getElementById('status').innerHTML='✅ '+realMatches.length+' مباراة - 👆 اضغط شعار أي فريق لفتح أرشيفه الكامل<br>📚 V81 بيجيب كل المباريات السابقة (الموسم كامل) + كل القادمة من ESPN Schedule';
 render();
}
var curF='all'; var archTab='all'; var currentArchMatches=[]; var currentArchTeam='';
function setF(f){curF=f; render();}
function setArchTab(t){archTab=t; document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active')); document.getElementById('tab-'+t).classList.add('active'); renderArchive();}
function toggleFav(team){ var i=favs.indexOf(team); if(i>=0)favs.splice(i,1); else favs.push(team); localStorage.setItem('favs',JSON.stringify(favs)); render(); }
async function openArchive(team){
 currentArchTeam=team; archTab='all'; document.getElementById('archive').style.display='block';
 document.getElementById('archTitle').innerText='📚 أرشيف '+team;
 document.getElementById('archContent').innerHTML='<div style="text-align:center;padding:20px;color:gold">⏳ جاري جلب كل مباريات '+team+'<br><br>✅ السابقة (موسم كامل)<br>⏰ القادمة (موسم كامل)<br><small>من ESPN Team Schedule API</small><br><br><div style="border:2px solid #0f0;width:30px;height:30px;border-top-color:transparent;border-radius:50%;animation:spin 1s linear infinite;margin:auto"></div></div><style>@keyframes spin{to{transform:rotate(360deg)}}</style>';
 try{
  var r=await fetch('/api/team-archive?team='+encodeURIComponent(team));
  var j=await r.json();
  currentArchMatches=j.matches||[];
  document.getElementById('archTitle').innerText='📚 '+team+' - '+j.teamName+' - '+currentArchMatches.length+' مباراة';
  document.getElementById('c-all').innerText='('+currentArchMatches.length+')';
  document.getElementById('c-past').innerText='('+j.past+')';
  document.getElementById('c-future').innerText='('+j.future+')';
  document.getElementById('c-live').innerText='('+j.live+')';
  renderArchive();
 }catch(e){ document.getElementById('archContent').innerHTML='❌'; }
}
function renderArchive(){
 var filtered=currentArchMatches;
 if(archTab=='past') filtered=currentArchMatches.filter(m=>m.type=='past');
 if(archTab=='future') filtered=currentArchMatches.filter(m=>m.type=='future');
 if(archTab=='live') filtered=currentArchMatches.filter(m=>m.isLive);
 var html='';
 if(filtered.length==0) html+='<div style="text-align:center;padding:20px;color:gray">لا يوجد مباريات - جرب تاب ثاني</div>';
 else{
  filtered.forEach(m=>{
   html+='<div class="archive-match '+m.type+' '+(m.isLive?'live':'')+'"><div><b>'+m.home+' <span style="color:gold">'+m.score+'</span> '+m.away+'</b><br><small>🏆 '+m.competition+' - 📅 '+m.date+'</small><br><small>'+(m.type=='past'?'✅ منتهية - '+m.result:'⏰ قادمة - '+m.time)+'</small></div><div style="text-align:left"><span class="'+(m.isLive?'badge-live':'badge-ft')+'">'+(m.isLive?'🔴 LIVE':m.score)+'</span><br><small>'+m.date+'</small></div></div>';
  });
 }
 document.getElementById('archContent').innerHTML=html;
}
function render(){
 var q=document.getElementById('search').value.toLowerCase();
 var filtered=realMatches.filter(m=>{
  if(q &&!(m.home.toLowerCase().includes(q)||m.away.toLowerCase().includes(q))) return false;
  if(curF=='live'&&!m.isLive) return false;
  if(curF=='fav'&&!favs.some(f=>m.home.includes(f)||m.away.includes(f))) return false;
  return true;
 });
 var grouped={}; filtered.forEach(m=>{ if(!grouped[m.league])grouped[m.league]=[]; grouped[m.league].push(m); });
 var html=''; var order=['eng.1','esp.1','sau.1','uefa.champions','ita.1'];
 Object.keys(grouped).forEach(lg=>{ if(!order.includes(lg))order.push(lg); });
 order.forEach(lg=>{
  if(!grouped[lg]) return;
  var info=leagueIcons[lg]||{icon:'⚽',name:lg,cls:'eng'}; var matches=grouped[lg];
  html+='<div class="league-header '+info.cls+'" onclick="toggleLeague(\\''+lg+'\\')"><div><span style="font-size:20px">'+info.icon+'</span> <b>'+info.name+'</b> <span style="background:#0f0;color:#000;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:900">'+matches.length+'</span></div><span id="arr-'+lg+'">▶</span></div><div class="group" id="group-'+lg+'">';
  matches.forEach(m=>{
   var isFav=favs.includes(m.home)||favs.includes(m.away);
   html+='<div class="card '+(m.isLive?'live':'')+(isFav?' fav':'')+'"><img class="team-logo" src="'+m.homeLogo+'" onclick="openArchive(\\''+m.home+'\\')" onerror="this.src=\\'https://via.placeholder.com/36\\'"><div style="flex:1" onclick="openArchive(\\''+m.home+'\\')"><b>📚 '+m.home+' vs '+m.away+'</b> '+(m.isLive?'<span class=badge-live>🔴 LIVE '+m.score+'</span>':'<span class=badge-ft>✅ '+m.score+'</span>')+'<br><small style="color:gold">👆 اضغط لفتح أرشيف كامل: سابقة+قادمة</small></div><img class="team-logo" src="'+m.awayLogo+'" onclick="openArchive(\\''+m.away+'\\')" onerror="this.src=\\'https://via.placeholder.com/36\\'"><button onclick="toggleFav(\\''+m.home+'\\')" style="background:'+(isFav?'gold':'#222')+';color:'+(isFav?'#000':'gold')+';border:1px solid gold;border-radius:14px;padding:4px 8px">⭐</button></div>';
  });
  html+='</div>';
 });
 document.getElementById('m').innerHTML=html;
}
function toggleLeague(lg){ document.getElementById('group-'+lg).classList.toggle('hidden'); }
loadReal();
</script></body></html>
"""
@app.route('/')
def home(): return HTML

@app.route('/api/real-matches')
def real_matches():
    matches=[]
    for lg in ['eng.1','esp.1','sau.1','ita.1','ger.1','uefa.champions']:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=4)
            if r.status_code==200:
                for ev in r.json().get('events',[])[:10]:
                    comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                    if len(comps)>=2:
                        matches.append({"home":comps[0]['team']['displayName'],"away":comps[1]['team']['displayName'],"homeLogo":comps[0]['team'].get('logo',''),"awayLogo":comps[1]['team'].get('logo',''),"competition":ev.get('league',{}).get('name',lg),"score":f"{comps[0].get('score','-')} - {comps[1].get('score','-')}","date":ev.get('date','')[:10],"league":lg,"isLive":ev.get('status',{}).get('type',{}).get('state','pre')=='in'})
        except: continue
    return jsonify({"matches":matches})

@app.route('/api/team-archive')
def team_archive():
    team=request.args.get('team','')
    team_lower=team.lower().strip()
    matches=[]; team_id=None; team_name=team; found_league=None
    # 1- دور على ID الفريق من كل الدوريات
    for lg in ['eng.1','esp.1','sau.1','ita.1','ger.1','fra.1','uefa.champions','fifa.world','fifa.worldq']:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/teams",timeout=5)
            if r.status_code==200:
                data=r.json()
                for t in data.get('sports',[{}])[0].get('leagues',[{}])[0].get('teams',[]):
                    tm=t.get('team',{})
                    if team_lower in tm.get('displayName','').lower() or team_lower in tm.get('shortDisplayName','').lower() or team_lower in tm.get('abbreviation','').lower():
                        team_id=tm.get('id'); team_name=tm.get('displayName'); found_league=lg
                        break
                if team_id: break
        except: continue
    # 2- إذا لقينا ID - جيب الجدول الكامل موسم كامل
    if team_id and found_league:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{found_league}/teams/{team_id}/schedule",timeout=6)
            if r.status_code==200:
                data=r.json()
                for ev in data.get('events',[]):
                    comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                    if len(comps)>=2:
                        h=comps[0]['team']['displayName']; a=comps[1]['team']['displayName']
                        state=ev.get('status',{}).get('type',{}).get('state','post')
                        is_live=state=='in'; is_future=state=='pre'
                        score=f"{comps[0].get('score','-')} - {comps[1].get('score','-')}"
                        # نتيجة فوز/خسارة
                        result=""
                        if not is_future and not is_live:
                            try:
                                hs=int(comps[0].get('score',0)); aws=int(comps[1].get('score',0))
                                if team_lower in h.lower():
                                    result="فوز ✅" if hs>aws else "خسارة ❌" if hs<aws else "تعادل ➖"
                                else:
                                    result="فوز ✅" if aws>hs else "خسارة ❌" if aws<hs else "تعادل ➖"
                            except: result="منتهية"
                        matches.append({"home":h,"away":a,"competition":ev.get('league',{}).get('name',found_league),"score":score,"date":ev.get('date','')[:10],"time":ev.get('date','')[11:16],"type":'future' if is_future else 'past',"isLive":is_live,"result":result})
        except: pass
    # 3- إذا ما لقينا أو فشل - جيب من scoreboard كبديل + مولد مباريات قادمة واقعية
    if len(matches)==0:
        for lg in ['eng.1','esp.1','sau.1','ita.1','ger.1','uefa.champions']:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=3)
                if r.status_code==200:
                    for ev in r.json().get('events',[])[:30]:
                        comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                        if len(comps)>=2:
                            h=comps[0]['team']['displayName']; a=comps[1]['team']['displayName']
                            if team_lower in h.lower() or team_lower in a.lower():
                                state=ev.get('status',{}).get('type',{}).get('state','post')
                                matches.append({"home":h,"away":a,"competition":ev.get('league',{}).get('name',lg),"score":f"{comps[0].get('score','-')} - {comps[1].get('score','-')}","date":ev.get('date','')[:10],"time":ev.get('date','')[11:16],"type":'future' if state=='pre' else 'past',"isLive":state=='in',"result":""})
            except: continue
    matches_sorted=sorted(matches,key=lambda x:x['date'],reverse=True)
    past=len([m for m in matches_sorted if m['type']=='past'])
    future=len([m for m in matches_sorted if m['type']=='future'])
    live=len([m for m in matches_sorted if m['isLive']])
    return jsonify({"team":team,"teamName":team_name,"matches":matches_sorted,"past":past,"future":future,"live":live,"found":team_id is not None,"league":found_league})

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
