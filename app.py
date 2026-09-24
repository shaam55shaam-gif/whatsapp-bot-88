from flask import Flask, jsonify, request
import requests
from datetime import datetime
app = Flask(__name__)

HEADERS = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V92 LIVE - مباشر بدون تخمين</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:#0f0;color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0}
.row{display:flex;justify-content:space-between;background:#1a1a1a;margin:4px 8px;padding:14px;border-radius:12px;border:1px solid #333}
.row.top{background:linear-gradient(90deg,gold,#0f0);color:#000;font-weight:900;border:2px solid gold}
.error{background:#330000;border:2px solid red;color:#ff6666;padding:14px;border-radius:12px;margin:8px;text-align:center}
.loading{background:#111;border:2px solid gold;color:gold;padding:20px;border-radius:12px;margin:8px;text-align:center}
</style></head><body>
<div class=h>🔴 V92 LIVE - نتائج مباشرة من ESPN - بدون تخمين - إذا فشل بيقلك فشل</div>
<div style="text-align:center;padding:8px">
<button onclick="loadTable()" style="background:#0f0;color:#000;padding:12px 24px;border-radius:20px;border:none;font-weight:900;font-size:14px">🔄 جلب الترتيب المباشر الآن</button>
<button onclick="loadMatches()" style="background:gold;color:#000;padding:12px 24px;border-radius:20px;border:none;font-weight:900;font-size:14px;margin:4px">⚽ جلب المباريات المباشرة</button>
</div>
<div id=status style="text-align:center;padding:8px;color:gold">اضغط زر لجلب مباشر من ESPN API</div>
<div id=m></div>
<script>
async function loadTable(){
 document.getElementById('status').innerHTML='⏳ جاري جلب ترتيب La Liga مباشر من ESPN...';
 document.getElementById('m').innerHTML='<div class=loading>⏳ جاري الاتصال بـ site.api.espn.com/apis/site/v2/sports/soccer/esp.1/standings...</div>';
 try{
  var r=await fetch('/api/live-table');
  var j=await r.json();
  if(j.error){ document.getElementById('m').innerHTML='<div class=error>❌ '+j.error+'<br><small>'+j.details+'</small></div>'; document.getElementById('status').innerHTML='❌ فشل - ما عم خمن'; return; }
  var html='<div style="background:gold;color:#000;padding:12px;border-radius:12px;margin:8px;text-align:center;font-weight:900">🏆 ترتيب مباشر - ESPN - '+j.league+' - '+new Date().toLocaleString('ar')+'</div>';
  html+='<div style="display:flex;justify-content:space-between;background:#333;padding:10px;border-radius:10px;margin:8px;color:gold;font-weight:900"><span># الفريق</span><span>لعب | نقاط</span></div>';
  j.table.forEach(row=>{
   var cls=row.pos==1?'row top':'row';
   html+='<div class="'+cls+'"><div><span style="background:gold;color:#000;padding:2px 8px;border-radius:10px;font-weight:900">'+row.pos+'</span> '+row.teamAr+'</div><div><b>'+row.played+' | '+row.wins+' فوز</b><br><span style="font-weight:900">'+row.points+' نقطة</span><br><small>له '+row.gf+' عليه '+row.ga+'</small></div></div>';
  });
  html+='<div style="text-align:center;padding:8px;color:gray;font-size:10px">✅ مباشر من '+j.source+' - '+j.count+' فريق - '+j.time+'</div>';
  document.getElementById('m').innerHTML=html;
  document.getElementById('status').innerHTML='✅ ترتيب مباشر - '+j.count+' فريق - من ESPN';
 }catch(e){ document.getElementById('m').innerHTML='<div class=error>❌ خطأ شبكة: '+e.message+'</div>'; }
}
async function loadMatches(){
 document.getElementById('status').innerHTML='⏳ جاري جلب مباريات اليوم مباشر...';
 document.getElementById('m').innerHTML='<div class=loading>⏳ جاري جلب scoreboard مباشر...</div>';
 try{
  var r=await fetch('/api/live-matches'); var j=await r.json();
  if(j.error){ document.getElementById('m').innerHTML='<div class=error>❌ '+j.error+'</div>'; return; }
  var html='<div style="background:#0f0;color:#000;padding:12px;border-radius:12px;margin:8px;text-align:center;font-weight:900">⚽ مباريات مباشرة - '+j.count+' مباراة - '+new Date().toLocaleString('ar')+'</div>';
  j.matches.forEach(m=>{
   html+='<div class=row><div><b>'+m.homeAr+' ضد '+m.awayAr+'</b><br><small>'+m.league+' - '+m.date+'</small></div><div><b style="color:gold">'+m.score+'</b><br><small>'+m.status+'</small></div></div>';
  });
  document.getElementById('m').innerHTML=html;
  document.getElementById('status').innerHTML='✅ مباريات مباشرة - '+j.count;
 }catch(e){ document.getElementById('m').innerHTML='<div class=error>❌ '+e.message+'</div>'; }
}
</script></body></html>
"""

@app.route('/')
def home(): return HTML

@app.route('/api/live-table')
def live_table():
    # جلب مباشر - بدون تخمين
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/standings?season=2025"
        r = requests.get(url, headers=HEADERS, timeout=10)
        if r.status_code!= 200:
            return jsonify({"error":f"ESPN رجع {r.status_code}","details":r.text[:200],"source":url}), 500

        data = r.json()
        table = []
        children = data.get('children', [])
        if not children:
            return jsonify({"error":"ESPN ما رجع children","details":str(data)[:500],"source":url}), 500

        entries = children[0].get('standings',{}).get('entries', [])
        if len(entries)==0 and 'children' in children[0]:
            entries = children[0]['children'][0].get('standings',{}).get('entries', [])

        if len(entries)==0:
            return jsonify({"error":"ESPN رجع 0 فريق","details":"entries فاضي","source":url}), 500

        for idx, entry in enumerate(entries):
            team = entry.get('team',{}).get('displayName','?')
            stats = entry.get('stats', [])
            # استخراج نقاط
            pts = 0; wins=0; played=0; gf=0; ga=0
            for s in stats:
                if s.get('name')=='points': pts = s.get('value',0)
                if s.get('name')=='wins': wins = s.get('value',0)
                if s.get('name')=='gamesPlayed': played = s.get('value',0)
                if s.get('name')=='pointsFor': gf = s.get('value',0)
                if s.get('name')=='pointsAgainst': ga = s.get('value',0)

            table.append({
                "pos": idx+1,
                "team": team,
                "teamAr": team, # نخلي الإنجليزي مباشر بدون ترجمة وهمية
                "played": played,
                "wins": wins,
                "points": pts,
                "gf": gf,
                "ga": ga
            })

        return jsonify({
            "table": table,
            "count": len(table),
            "league": "La Liga esp.1 2025/26",
            "source": url,
            "time": datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({"error":"فشل الاتصال بـ ESPN","details":str(e),"source":url}), 500

@app.route('/api/live-matches')
def live_matches():
    try:
        url = "https://site.api.espn.com/apis/site/v2/sports/soccer/esp.1/scoreboard"
        r = requests.get(url, headers=HEADERS, timeout=8)
        data = r.json()
        matches=[]
        for ev in data.get('events',[]):
            comp = ev.get('competitions',[{}])[0]
            comps = comp.get('competitors',[])
            if len(comps)>=2:
                h = comps[0]['team']['displayName']
                a = comps[1]['team']['displayName']
                hs = comps[0].get('score','-')
                aws = comps[1].get('score','-')
                matches.append({
                    "home":h,"away":a,"homeAr":h,"awayAr":a,
                    "score":f"{hs} - {aws}",
                    "status":ev.get('status',{}).get('type',{}).get('description',''),
                    "date":ev.get('date','')[:10],
                    "league":"esp.1"
                })
        return jsonify({"matches":matches,"count":len(matches),"source":url})
    except Exception as e:
        return jsonify({"error":str(e)}), 500

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
