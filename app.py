from flask import Flask, jsonify
import requests
from datetime import datetime
app = Flask(__name__)

HEADERS = {"User-Agent":"Mozilla/5.0"}

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>LIVE REAL - مثل باقي التطبيقات</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff88,gold);color:#000;padding:14px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20}
.row{display:flex;justify-content:space-between;background:#1a1a1a;margin:4px 8px;padding:14px;border-radius:12px;border:1px solid #333;align-items:center}
.row.top{background:linear-gradient(90deg,#a50044,#004d98);color:#fff;border:2px solid gold;font-weight:900;box-shadow:0 0 15px gold}
.loading{background:#111;border:2px solid gold;color:gold;padding:20px;border-radius:12px;margin:10px;text-align:center}
.error{background:#330000;border:2px solid red;color:#ff8888;padding:14px;border-radius:12px;margin:10px;text-align:center}
.ok{background:#002200;border:1px solid #0f0;color:#0f0;padding:10px;border-radius:10px;margin:8px;text-align:center;font-size:11px}
</style></head><body>
<div class=h>🔴 LIVE REAL - مثل باقي التطبيقات - نتائج مباشرة من TheSportsDB - بدون وهمي</div>
<div style="text-align:center;padding:10px">
<button onclick="loadLive()" style="background:#00ff88;color:#000;padding:14px 28px;border-radius:25px;border:none;font-weight:900;font-size:14px">🔄 جلب مباشر حي الآن - LIVE</button>
</div>
<div id=status style="text-align:center;padding:6px;color:gold;font-size:12px">اضغط الزر - جلب مباشر حي من TheSportsDB.com - نفس مصدر باقي التطبيقات</div>
<div id=m><div class=loading>⏳ اضغط زر الجلب المباشر الحي</div></div>
<script>
async function loadLive(){
 document.getElementById('status').innerHTML='⏳ جاري جلب مباشر حي من TheSportsDB...';
 document.getElementById('m').innerHTML='<div class=loading>🔴 LIVE - جاري الاتصال بـ thesportsdb.com/api/v1/json/3/lookuptable.php?l=4335 ...<br><small>نفس API اللي بتستخدمه تطبيقات La Liga</small></div>';
 try{
  var r=await fetch('/api/live-real'); 
  var text=await r.text();
  var j;
  try{ j=JSON.parse(text); }catch(e){ document.getElementById('m').innerHTML='<div class=error>❌ المصدر رجع مو JSON<br><small>'+text.substring(0,300)+'</small></div>'; return; }
  if(j.error){ document.getElementById('m').innerHTML='<div class=error>❌ '+j.error+'<br><small>'+(j.details||'')+'</small></div>'; return; }
  
  var html='<div class=ok>✅ 🔴 LIVE REAL - مباشر حي - '+j.source+' - '+j.count+' فريق - '+j.time+'<br>مصدر حي مو وهمي - مثل باقي التطبيقات</div>';
  html+='<div style="background:linear-gradient(90deg,#a50044,#004d98);color:#fff;padding:12px;border-radius:12px;margin:8px;text-align:center;font-weight:900">🏆 ترتيب مباشر حي - '+j.league+' - '+new Date().toLocaleString('ar')+'</div>';
  html+='<div style="display:flex;justify-content:space-between;background:#333;padding:10px;border-radius:10px;margin:8px;color:gold;font-weight:900;font-size:11px"><span># الفريق</span><span>لعب | نقاط | أهداف</span></div>';
  j.table.forEach(row=>{
   var cls=row.pos==1?'row top':'row';
   var crown=row.pos==1?'👑 ':'';
   html+='<div class="'+cls+'"><div><span style="background:gold;color:#000;padding:2px 8px;border-radius:10px;font-weight:900">'+row.pos+'</span> '+crown+row.teamAr+'</div><div style="text-align:left"><b>'+row.played+' لعب | '+row.wins+' فوز</b><br><span style="color:gold;font-weight:900;font-size:16px">'+row.points+' نقطة</span><br><small>⚽ '+row.gf+' له - '+row.ga+' عليه</small></div></div>';
  });
  html+='<div class=ok>🔴 هذا ترتيب مباشر حي من TheSportsDB.com - يتحدث كل يوم - مو وهمي أنا كاتبه<br>إذا برشلونة متصدر حي - بيطلع متصدر - إذا ريال متصدر - بيطلع متصدر</div>';
  document.getElementById('m').innerHTML=html;
  document.getElementById('status').innerHTML='✅ LIVE - '+j.count+' فريق - مباشر حي من '+j.source;
 }catch(e){
  document.getElementById('m').innerHTML='<div class=error>❌ خطأ شبكة: '+e.message+'</div>';
 }
}
loadLive();
</script></body></html>
"""
@app.route('/')
def home(): return HTML

@app.route('/api/live-real')
def live_real():
    # مصدر مباشر حي - نفس اللي بتستخدمه باقي التطبيقات - TheSportsDB
    url = "https://www.thesportsdb.com/api/v1/json/3/lookuptable.php?l=4335&s=2025-2026"
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        if r.status_code != 200:
            return jsonify({"error":f"TheSportsDB رجع {r.status_code}","details":r.text[:300],"source":url}), 500
        if not r.text.strip():
            return jsonify({"error":"TheSportsDB رجع فاضي","details":"لا يوجد بيانات اليوم","source":url}), 500
        
        try:
            data = r.json()
        except Exception as je:
            return jsonify({"error":"TheSportsDB رجع مو JSON","details":f"{str(je)} - النص: {r.text[:200]}","source":url}), 500

        if 'table' not in data or not data['table']:
            return jsonify({"error":"TheSportsDB رجع جدول فاضي","details":str(data)[:500],"source":url}), 500

        table=[]
        for idx, entry in enumerate(data['table']):
            try:
                team = entry.get('strTeam','?')
                played = int(entry.get('intPlayed',0) or 0)
                wins = int(entry.get('intWin',0) or 0)
                draws = int(entry.get('intDraw',0) or 0)
                losses = int(entry.get('intLoss',0) or 0)
                points = int(entry.get('intPoints',0) or 0)
                gf = int(entry.get('intGoalsFor',0) or 0)
                ga = int(entry.get('intGoalsAgainst',0) or 0)

                # ترجمة عربية
                ar_map = {
                    "Barcelona":"برشلونة","Real Madrid":"ريال مدريد","Atletico Madrid":"أتلتيكو مدريد",
                    "Real Betis":"ريال بيتيس","Sevilla":"إشبيلية","Villarreal":"فياريال",
                    "Athletic Bilbao":"أتلتيك بلباو","Real Sociedad":"ريال سوسيداد","Getafe":"خيتافي",
                    "Valencia":"فالنسيا","Alaves":"ألافيس","Espanyol":"إسبانيول","Celta Vigo":"سيلتا فيغو",
                    "Osasuna":"أوساسونا","Rayo Vallecano":"رايو فايكانو","Elche":"إلتشي",
                    "Levante":"ليفانتي","Malaga":"ملقا","Deportivo":"ديبورتيفو"
                }
                team_ar = ar_map.get(team, team)

                table.append({
                    "pos": int(entry.get('intRank', idx+1) or idx+1),
                    "team": team,
                    "teamAr": team_ar,
                    "played": played,
                    "wins": wins,
                    "draws": draws,
                    "losses": losses,
                    "points": points,
                    "gf": gf,
                    "ga": ga
                })
            except Exception as e:
                continue

        # رتب حسب نقاط مباشر - مثل باقي التطبيقات
        table = sorted(table, key=lambda x: (x['points'], x['gf']-x['ga']), reverse=True)
        for i, t in enumerate(table):
            t['pos'] = i+1

        return jsonify({
            "table": table,
            "count": len(table),
            "league": "La Liga 2025/26 - LIVE REAL",
            "source": "TheSportsDB.com - API حي مثل باقي التطبيقات",
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "isLive": True
        })

    except Exception as e:
        return jsonify({"error":"فشل جلب مباشر حي","details":str(e),"source":url}), 500

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
