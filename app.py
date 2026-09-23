from flask import Flask, jsonify
import requests
from datetime import datetime
app = Flask(__name__)
TOKEN = "b3d1f512481042d98a69bdd8d99a6eb6"

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V77 - مرتب حسب الدوري - أيقونة لكل بطولة</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#0f0,gold,#0f0);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:11px}
.league-header{background:linear-gradient(90deg,#111,#222);border:2px solid #0f0;margin:12px 8px 4px 8px;padding:10px;border-radius:14px;display:flex;justify-content:space-between;align-items:center;position:sticky;top:44px;z-index:20}
.league-header.eng{border-color:#3d1aff;background:linear-gradient(90deg,#1a0033,#2a1a4a)}
.league-header.esp{border-color:#ff0000;background:linear-gradient(90deg,#330000,#4a1a1a)}
.league-header.sau{border-color:#00a651;background:linear-gradient(90deg,#002a10,#0a3a1a)}
.league-header.ita{border-color:#008C45;background:linear-gradient(90deg,#001a0a,#0a2a1a)}
.league-header.ger{border-color:#ffcc00;background:linear-gradient(90deg,#2a2a00,#3a3a00);color:#fff}
.league-header.ucl{border-color:gold;background:linear-gradient(90deg,#1a1a00,#2a2a00)}
.card{background:#111;border-right:6px solid #0f0;margin:4px 8px 4px 16px;padding:10px;border-radius:12px;border:1px solid #333}
.card.live{border-right-color:red;background:#1a0000;box-shadow:0 0 15px red}
.badge-live{background:red;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px;animation:blink 0.8s infinite}
.badge-ft{background:gray;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.4}}
.f{padding:6px 10px;border-radius:20px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#0f0;color:#000;font-weight:900}
.league-count{background:#0f0;color:#000;padding:2px 8px;border-radius:12px;font-size:10px;font-weight:900}
</style></head><body>
<div class=h>✅ V77 - مرتب حسب الدوري - كل بطولة أيقونة مختلفة - 🏴󐁧󐁢󐁥󐁮󐁧󐁿 🇪🇸 🇸🇦 🇮🇹 🇩🇪 🏆</div>
<div style="padding:6px;white-space:nowrap;overflow:auto;text-align:center">
<span class="f active" id="fa" onclick="setF('all')">🌐 الكل مرتب حسب الدوري</span>
<span class=f id="fl" onclick="setF('live')">🔴 LIVE فقط</span>
<span class=f id="fe" onclick="setF('eng')">🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي</span>
<span class=f id="fs" onclick="setF('esp')">🇪🇸 إسباني</span>
<span class=f id="fsa" onclick="setF('sau')">🇸🇦 سعودي</span>
<span class=f onclick="loadReal()">🔄</span>
</div>
<div id=status style="text-align:center;padding:8px;background:#111;margin:8px;border-radius:12px;color:gold;font-size:11px"></div>
<div id=m></div>
<script>
var realMatches=[];
var leagueIcons={
 'eng.1':{icon:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',name:'الدوري الإنجليزي الممتاز',flag:'🇬🇧',cls:'eng',color:'#3d1aff'},
 'esp.1':{icon:'🇪🇸',name:'الدوري الإسباني - La Liga',flag:'🇪🇸',cls:'esp',color:'#ff0000'},
 'sau.1':{icon:'🇸🇦',name:'الدوري السعودي روشن',flag:'🇸🇦',cls:'sau',color:'#00a651'},
 'ita.1':{icon:'🇮🇹',name:'الدوري الإيطالي - Serie A',flag:'🇮🇹',cls:'ita',color:'#008C45'},
 'ger.1':{icon:'🇩🇪',name:'الدوري الألماني - Bundesliga',flag:'🇩🇪',cls:'ger',color:'#ffcc00'},
 'fra.1':{icon:'🇫🇷',name:'الدوري الفرنسي - Ligue 1',flag:'🇫🇷',cls:'eng',color:'#002395'},
 'uefa.champions':{icon:'🏆',name:'دوري أبطال أوروبا',flag:'⭐',cls:'ucl',color:'gold'},
 'uefa.europa':{icon:'🏆',name:'الدوري الأوروبي',flag:'🏆',cls:'ucl',color:'#ff6600'},
 'eng.fa':{icon:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',name:'كأس الاتحاد الإنجليزي',flag:'🏆',cls:'eng',color:'#ff0000'}
};
async function loadReal(){
 try{
  var r=await fetch('/api/real-matches'); var j=await r.json();
  realMatches=j.matches || [];
  document.getElementById('status').innerHTML='✅ تم الجلب - '+realMatches.length+' مباراة - مرتبة حسب الدوري<br>🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي: '+j.counts['eng.1']+' | 🇪🇸 إسباني: '+j.counts['esp.1']+' | 🇸🇦 سعودي: '+j.counts['sau.1']+' | 🏆 أبطال: '+j.counts['uefa.champions']+'<br><small>كل دوري أيقونة مختلفة + مرتب مع بعض</small>';
  render();
 }catch(e){ document.getElementById('status').innerText='❌'; }
}
var curF='all';
function setF(f){curF=f; document.querySelectorAll('.f').forEach(x=>x.classList.remove('active')); document.getElementById('fa').classList.toggle('active',f=='all'); document.getElementById('fl').classList.toggle('active',f=='live'); document.getElementById('fe').classList.toggle('active',f=='eng'); document.getElementById('fs').classList.toggle('active',f=='esp'); document.getElementById('fsa').classList.toggle('active',f=='sau'); render();}
function render(){
 var html='';
 var filtered=realMatches;
 if(curF=='live') filtered=realMatches.filter(m=>m.isLive);
 if(curF=='eng') filtered=realMatches.filter(m=>m.league=='eng.1');
 if(curF=='esp') filtered=realMatches.filter(m=>m.league=='esp.1');
 if(curF=='sau') filtered=realMatches.filter(m=>m.league=='sau.1');
 // ترتيب حسب الدوري
 var grouped={};
 filtered.forEach(m=>{
  if(!grouped[m.league]) grouped[m.league]=[];
  grouped[m.league].push(m);
 });
 // ترتيب الدوريات حسب الأهمية
 var order=['eng.1','esp.1','sau.1','uefa.champions','ita.1','ger.1','fra.1','uefa.europa','eng.fa'];
 Object.keys(grouped).forEach(lg=>{
  if(!order.includes(lg)) order.push(lg);
 });
 order.forEach(lg=>{
  if(!grouped[lg]) return;
  var info=leagueIcons[lg]||{icon:'⚽',name:lg,flag:'⚽',cls:'eng'};
  var matches=grouped[lg];
  html+='<div class="league-header '+info.cls+'"><div><span style="font-size:20px">'+info.icon+'</span> <b>'+info.flag+' '+info.name+'</b></div><span class="league-count">'+matches.length+' مباراة</span></div>';
  matches.forEach(m=>{
   html+='<div class="card '+(m.isLive?'live':'')+'"><div style="display:flex;justify-content:space-between;align-items:center"><b>'+info.icon+' '+m.home+' vs '+m.away+'</b> '+(m.isLive?'<span class=badge-live>🔴 LIVE '+m.score+'</span>':'<span class=badge-ft>✅ '+m.score+' FT</span>')+'</div><small style="color:gold">📅 '+m.date+' - '+info.name+'</small><br><small style="color:#aaa">مصدر: '+m.source+'</small></div>';
  });
 });
 if(filtered.length==0){
  if(curF=='live') html+='<div style="text-align:center;padding:20px;color:red"><b>🔴 لا يوجد LIVE الآن</b><br><small>اضغط "الكل مرتب حسب الدوري" لترى المباريات المنتهية مرتبة حسب الدوري</small></div>';
  else html+='<div style="text-align:center;padding:20px">لا يوجد</div>';
 }
 document.getElementById('m').innerHTML=html;
}
loadReal(); setInterval(loadReal,60000);
</script></body></html>
"""
@app.route('/')
def home(): return HTML
@app.route('/api/real-matches')
def real_matches():
    matches=[]; counts={}
    try:
        for lg in ['eng.1','esp.1','sau.1','ita.1','ger.1','fra.1','uefa.champions','uefa.europa','eng.fa']:
            counts[lg]=0
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=4)
                if r.status_code==200:
                    for ev in r.json().get('events',[])[:10]:
                        comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                        is_live=ev.get('status',{}).get('type',{}).get('state','pre')=='in'
                        if len(comps)>=2:
                            matches.append({"home":comps[0]['team']['displayName'],"away":comps[1]['team']['displayName'],"competition":ev.get('league',{}).get('name',lg),"status":ev.get('status',{}).get('type',{}).get('description','FT'),"score":f"{comps[0].get('score','-')} - {comps[1].get('score','-')}","date":ev.get('date','')[:10],"source":"ESPN","league":lg,"isLive":is_live}); counts[lg]+=1
            except: continue
    except: pass
    # ترتيب حسب الدوري
    matches.sort(key=lambda x: x['league'])
    return jsonify({"matches":matches,"counts":counts})

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
