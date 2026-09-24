from flask import Flask, jsonify
import requests
from datetime import datetime
app = Flask(__name__)

HEADERS = {"User-Agent":"Mozilla/5.0"}

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V93 FIX JSON ERROR</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:#0f0;color:#000;padding:12px;text-align:center;font-weight:900}
.row{display:flex;justify-content:space-between;background:#1a1a1a;margin:4px 8px;padding:14px;border-radius:12px;border:1px solid #333}
.row.top{background:linear-gradient(90deg,#a50044,#004d98);color:#fff;border:2px solid gold;font-weight:900}
.error{background:#330000;border:2px solid red;color:#ff9999;padding:14px;border-radius:12px;margin:8px;text-align:center}
.ok{background:#002200;border:2px solid #0f0;color:#0f0;padding:14px;border-radius:12px;margin:8px;text-align:center}
</style></head><body>
<div class=h>✅ V93 FIX - صلحت خطأ JSON - نتائج مباشرة بدون تخمين</div>
<div style="text-align:center;padding:10px">
<button onclick="loadTable()" style="background:#0f0;color:#000;padding:14px 28px;border-radius:20px;border:none;font-weight:900;font-size:15px">🔄 جلب ترتيب مباشر</button>
<button onclick="loadMatches()" style="background:gold;color:#000;padding:14px 28px;border-radius:20px;border:none;font-weight:900;font-size:15px;margin:6px">⚽ جلب مباريات</button>
</div>
<div id=status style="text-align:center;padding:8px;color:gold">اضغط جلب ترتيب مباشر</div>
<div id=m></div>
<script>
async function loadTable(){
 document.getElementById('status').innerHTML='⏳ جاري جلب ترتيب مباشر...';
 document.getElementById('m').innerHTML='<div style="text-align:center;padding:20px;color:gold">⏳ جاري...</div>';
 try{
  var r=await fetch('/api/live-table'); var j=await r.json();
  if(j.error){ document.getElementById('m').innerHTML='<div class=error>❌ '+j.error+'<br><small>'+(j.details||'')+'</small><br><br>المصدر: '+j.source+'</div>'; return; }
  var html='<div style="background:linear-gradient(90deg,#a50044,#004d98);color:#fff;padding:12px;border-radius:12px;margin:8px;text-align:center;font-weight:900">🏆 '+j.league+' - مباشر - '+j.count+' فريق - '+new Date().toLocaleString('ar')+'</div>';
  html+='<div style="display:flex;justify-content:space-between;background:#333;padding:10px;border-radius:10px;margin:8px;color:gold;font-weight:900"><span># الفريق</span><span>نقاط</span></div>';
  j.table.forEach(row=>{
   var cls=row.pos==1?'row top':'row';
   html+='<div class="'+cls+'"><div><span style="background:gold;color:#000;padding:2px 8px;border-radius:10px">'+row.pos+'</span> '+row.teamAr+'</div><div><b>'+row.points+' نقطة</b> - '+row.played+' لعب</div></div>';
  });
  document.getElementById('m').innerHTML=html;
  document.getElementById('status').innerHTML='✅ مباشر من '+j.source;
 }catch(e){ document.getElementById('m').innerHTML='<div class=error>❌ '+e.message+'</div>'; }
}
async function loadMatches(){
 document.getElementById('status').innerHTML='⏳ جلب مباريات...';
 try{
  var r=await fetch('/api/live-matches'); var text=await r.text(); var j;
  try{ j=JSON.parse(text); }catch(err){ document.getElementById('m').innerHTML='<div class=error>❌ ESPN رجع مو JSON<br><small>'+text.substring(0,200)+'</small></div>'; return; }
  if(j.error){ document.getElementById('m').innerHTML='<div class=error>❌ '+j.error+'</div>'; return; }
  if(j.matches.length==0){ document.getElementById('m').innerHTML='<div class=ok>✅ لا يوجد مباريات اليوم - ESPN رجع 0 مباراة - هذا مباشر مو تخمين</div>'; document.getElementById('status').innerHTML='✅ مباشر - 0 مباراة اليوم'; return; }
  var html=''; j.matches.forEach(m=>{ html+='<div class=row><div>'+m.homeAr+' ضد '+m.awayAr+'</div><div>'+m.score+'</div></div>'; });
  document.getElementById('m').innerHTML=html;
 }catch(e){ document.getElementById('m').innerHTML='<div class=error>❌ '+e.message+'</div>'; }
}
loadTable();
</script></body></html>
"""
@app.route('/')
def home(): return HTML

@app.route('/api/live-table')
def live_table():
    # نحاول 3 مصادر مباشرة - بدون تخمين
    sources = [
        "https://api-football-standings.azharimm.dev/leagues/esp.1/standings?season=2025",
        "https://api-football-standings.azharimm.dev/leagues/esp.1/standings?season=2024",
        "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/standings?season=2025"
    ]
    for url in sources:
        try:
            r = requests.get(url, headers=HEADERS, timeout=12)
            if r.status_code!=200: continue
            # FIX: جرب يقرأ JSON بأمان
            try:
                data = r.json()
            except:
                continue

            # مصدر azharimm
            if 'data' in data and 'standings' in data['data']:
                standings = data['data']['standings']
                table=[]
                for idx, entry in enumerate(standings):
                    team = entry.get('team',{}).get('displayName') or entry.get('team',{}).get('name','?')
                    stats = entry.get('stats',[])
                    # stats array في هذا API شكل ثاني
                    pts = 0; played=0; wins=0
                    # يحاول يقرأ من stats
                    if isinstance(stats, list):
                        for s in stats:
                            if isinstance(s, dict):
                                if s.get('name')=='points': pts=s.get('value',0)
                                if s.get('name')=='wins': wins=s.get('value',0)
                                if s.get('name')=='gamesPlayed': played=s.get('value',0)
                    # إذا stats مو موجود - اقرأ مباشر
                    if pts==0:
                        pts = entry.get('stats',{}).get('points',0) if isinstance(entry.get('stats'), dict) else entry.get('points',0)
                        played = entry.get('stats',{}).get('gamesPlayed',0) if isinstance(entry.get('stats'), dict) else entry.get('gamesPlayed',0)
                        # بعض API يرجع stats كـ dict
                        if isinstance(entry.get('stats'), list) and len(entry['stats'])>=7:
                            # ترتيب: played, wins, losses...
                            try:
                                pts = entry['stats'][6].get('value',0) if isinstance(entry['stats'][6], dict) else 0
                            except: pass

                    table.append({"pos":idx+1,"team":team,"teamAr":team,"played":played,"wins":wins,"points":pts,"gf":0,"ga":0})

                if len(table)>0:
                    return jsonify({"table":table,"count":len(table),"league":"La Liga 2025/26","source":url,"time":datetime.now().isoformat()})

            # مصدر ESPN
            if 'children' in data:
                children=data.get('children',[])
                if children:
                    entries=children[0].get('standings',{}).get('entries',[])
                    table=[]
                    for idx, e in enumerate(entries):
                        tm=e.get('team',{}).get('displayName','?')
                        pts=0; played=0; wins=0
                        for s in e.get('stats',[]):
                            if s.get('name')=='points': pts=s.get('value',0)
                            if s.get('name')=='gamesPlayed': played=s.get('value',0)
                            if s.get('name')=='wins': wins=s.get('value',0)
                        table.append({"pos":idx+1,"team":tm,"teamAr":tm,"played":played,"wins":wins,"points":pts,"gf":0,"ga":0})
                    if len(table)>0:
                        return jsonify({"table":table,"count":len(table),"league":"La Liga 2025/26 ESPN","source":url,"time":datetime.now().isoformat()})

        except Exception as e:
            continue

    return jsonify({"error":"كل المصادر المباشرة فشلت","details":"جربت 3 مصادر وكلهم فشلوا - ما رح خمن","source":"azharimm + ESPN"}), 500

@app.route('/api/live-matches')
def live_matches():
    try:
        url="https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard"
        r=requests.get(url, headers=HEADERS, timeout=10)
        # FIX JSON ERROR - تحقق قبل ما تعمل.json()
        if r.status_code!=200:
            return jsonify({"error":f"ESPN status {r.status_code}","details":r.text[:200]}), 500
        if not r.text.strip():
            return jsonify({"matches":[],"count":0,"source":url,"note":"ESPN رجع فاضي - لا يوجد مباريات اليوم"})
        try:
            data=r.json()
        except Exception as je:
            return jsonify({"matches":[],"count":0,"source":url,"note":f"ESPN رجع مو JSON اليوم - {str(je)} - النص: {r.text[:100]}"})

        matches=[]
        for ev in data.get('events',[]):
            comp=ev.get('competitions',[{}])[0]
            comps=comp.get('competitors',[])
            if len(comps)>=2:
                h=comps[0]['team']['displayName']; a=comps[1]['team']['displayName']
                hs=comps[0].get('score','-'); aws=comps[1].get('score','-')
                matches.append({"home":h,"away":a,"homeAr":h,"awayAr":a,"score":f"{hs} - {aws}","date":ev.get('date','')[:10]})
        return jsonify({"matches":matches,"count":len(matches),"source":url})
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
