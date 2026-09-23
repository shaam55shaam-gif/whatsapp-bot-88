from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
app = Flask(__name__)
TOKEN = "b3d1f512481042d98a69bdd8d99a6eb6"

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V75 REAL SEASON - الموسم الحقيقي</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#0f0,#fff);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:10px}
.card{background:#111;border-right:6px solid #0f0;margin:8px;padding:12px;border-radius:16px;border:1px solid #333}
.card.live{border-right-color:red;background:#1a0000;box-shadow:0 0 20px red}
.badge-live{background:red;color:#fff;padding:4px 10px;border-radius:20px;font-size:10px;animation:blink 0.8s infinite}
.badge-real{background:#0f0;color:#000;padding:4px 10px;border-radius:20px;font-size:10px;font-weight:900}
.badge-upcoming{background:#0af;color:#fff;padding:4px 10px;border-radius:20px;font-size:10px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.4}}
.f{padding:7px 12px;border-radius:22px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#0f0;color:#000;font-weight:900}
</style></head><body>
<div class=h>✅ V75 REAL SEASON - مباريات الموسم الحقيقي 2025-2026 - بدون تاريخ وهمي!</div>
<div style="padding:6px;background:#002a00;color:#0f0;text-align:center;font-size:10px">🔑 تم إصلاح التاريخ: كنا نبحث بتاريخ 2026-09-24 الوهمي - هلأ نبحث بالموسم الحقيقي!</div>
<div style="padding:6px;white-space:nowrap;overflow:auto;text-align:center">
<span class="f active" id="fa" onclick="setF('all')">🌐 الموسم الحقيقي</span>
<span class=f id="fl" onclick="setF('live')">🔴 LIVE حقيقي الآن</span>
<span class=f id="fu" onclick="setF('upcoming')">📅 القادمة</span>
<span class=f id="fsy" onclick="setF('syria')">🇸🇾 الكرامة</span>
<span class=f id="fsa" onclick="setF('saudi')">🇸🇦 الهلال</span>
<span class=f onclick="loadReal()">🔄</span>
</div>
<div id=status style="text-align:center;padding:8px;background:#111;margin:8px;border-radius:12px;color:gold;font-size:11px"></div>
<div id=m></div>
<script>
var realMatches=[];
async function loadReal(){
 document.getElementById('status').innerText='⏳ جاري جلب مباريات الموسم الحقيقي...';
 try{
  var r=await fetch('/api/real-matches'); var j=await r.json();
  realMatches=j.matches || [];
  document.getElementById('status').innerHTML='✅ تم الجلب - '+realMatches.length+' مباراة من الموسم الحقيقي<br>football-data.org: '+j.fd_count+' | ESPN: '+j.espn_count+' | LIVE الآن: '+j.live_count+'<br><small>تاريخ البحث: '+j.search_range+' - بدون تاريخ وهمي 2026-09-24 - الموسم الحقيقي 2025-2026</small>';
  filter();
 }catch(e){ document.getElementById('status').innerText='❌ خطأ'; }
}
var curF='all';
function setF(f){curF=f; document.querySelectorAll('.f').forEach(x=>x.classList.remove('active')); document.getElementById('fa').classList.toggle('active',f=='all'); document.getElementById('fl').classList.toggle('active',f=='live'); document.getElementById('fu').classList.toggle('active',f=='upcoming'); document.getElementById('fsy').classList.toggle('active',f=='syria'); document.getElementById('fsa').classList.toggle('active',f=='saudi'); filter();}
function filter(){
 var html=''; var list=realMatches;
 if(curF=='live') list=realMatches.filter(m=>m.isLive);
 if(curF=='upcoming') list=realMatches.filter(m=>!m.isLive && m.status.includes('SCHEDULED')||m.status=='TIMED');
 if(curF=='saudi') list=realMatches.filter(m=>m.competition.toLowerCase().includes('saudi')||m.league=='sau.1');
 if(curF=='syria'){
  html+='<div class="card" style="border-right-color:red"><b>🇸🇾 الكرامة 💙 - الموسم الحقيقي</b><br><small>الدوري السوري غير مغطى في football-data.org و ESPN - طبيعي<br>✅ ودية اليوم الحقيقية: أهلي حلب vs الكرامة - 24 أيلول 4 عصراً - الحمدانية<br>تابع صفحة الكرامة الرسمية للمباريات</small><br><a href="https://www.facebook.com/AlKaramaSC" target="_blank" style="background:#1877F2;color:#fff;padding:6px 10px;border-radius:14px;text-decoration:none;font-size:10px">📘 صفحة الكرامة</a></div>';
  document.getElementById('m').innerHTML=html; return;
 }
 if(list.length==0){ html+='<div class="card" style="border-right-color:red"><b>لا يوجد '+curF+'</b></div>'; }
 else { list.slice(0,100).forEach(m=>{
  html+='<div class="card '+(m.isLive?'live':'')+'"><b>⚽ '+m.home+' vs '+m.away+'</b> '+(m.isLive?'<span class=badge-live>🔴 LIVE '+m.score+'</span>':m.status.includes('SCHEDULED')||m.status=='TIMED'?'<span class=badge-upcoming>📅 قادمة '+m.date+'</span>':'<span class=badge-real>✅ '+m.status+' '+m.score+'</span>')+'<br><small style="color:gold">🏟️ '+m.competition+' - '+m.date+'</small><br><small>مصدر: '+m.source+'</small></div>';
 });}
 document.getElementById('m').innerHTML=html;
}
loadReal(); setInterval(loadReal,60000);
</script></body></html>
"""
@app.route('/')
def home(): return HTML
@app.route('/api/real-matches')
def real_matches():
    matches=[]; fd_c=0; espn_c=0; live_c=0
    today=datetime.now().date()
    # نبحث من اليوم الحقيقي إلى 7 أيام قادمة - مو تاريخ وهمي 2026-09-24
    date_from=today.strftime('%Y-%m-%d')
    date_to=(today+timedelta(days=7)).strftime('%Y-%m-%d')
    search_range=f"{date_from} إلى {date_to}"
    try:
        headers={"X-Auth-Token":TOKEN}
        r=requests.get(f"https://api.football-data.org/v4/matches?dateFrom={date_from}&dateTo={date_to}",headers=headers,timeout=8)
        if r.status_code==200:
            for m in r.json().get('matches',[])[:50]:
                is_live=m['status'] in ['IN_PLAY','LIVE','PAUSED']
                if is_live: live_c+=1
                matches.append({"home":m['homeTeam']['name'],"away":m['awayTeam']['name'],"competition":m['competition']['name'],"status":m['status'],"score":f"{m['score']['fullTime']['home'] or m['score']['halfTime']['home'] or '-'} - {m['score']['fullTime']['away'] or m['score']['halfTime']['away'] or '-'}","date":m['utcDate'][:10],"source":"football-data.org - الموسم الحقيقي","league":"fd","isLive":is_live}); fd_c+=1
    except: pass
    # ESPN - بدون تاريخ - يجيب الموسم الحقيقي الحالي
    try:
        for lg in ['eng.1','esp.1','sau.1','ita.1','ger.1','fra.1','uefa.champions','uefa.europa','eng.fa']:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=4)
                if r.status_code==200:
                    for ev in r.json().get('events',[])[:8]:
                        comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                        state=ev.get('status',{}).get('type',{}).get('state','pre')
                        is_live=state=='in'
                        if is_live: live_c+=1
                        if len(comps)>=2:
                            matches.append({"home":comps[0]['team']['displayName'],"away":comps[1]['team']['displayName'],"competition":ev.get('league',{}).get('name',lg),"status":ev.get('status',{}).get('type',{}).get('description','SCHEDULED'),"score":f"{comps[0].get('score','-')} - {comps[1].get('score','-')}","date":ev.get('date','')[:10],"source":"ESPN - الموسم الحقيقي","league":lg,"isLive":is_live}); espn_c+=1
            except: continue
    except: pass
    return jsonify({"matches":matches,"fd_count":fd_c,"espn_count":espn_c,"live_count":live_c,"search_range":search_range})

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
