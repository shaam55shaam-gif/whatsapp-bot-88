from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

HTML = """<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V17 ALL LEAGUES 🌍</title><style>body{background:#000;color:#fff;font-family:Arial;margin:0}.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:12px;text-align:center;font-weight:900;font-size:15px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}.leagueBox{background:#111;border:1px solid #333;border-radius:12px;padding:8px;text-align:center;font-size:11px}.leagueBox b{color:#FFD700}.card{background:#1a1a1a;border-right:4px solid #FFD700;border-radius:12px;margin:7px;padding:10px;font-size:12px}.live{border-right-color:red}.money{background:#111;border:1px solid #FFD700;padding:8px;border-radius:20px;margin:6px;text-align:center;font-weight:900;display:flex;justify-content:space-around;font-size:11px}</style></head><body><div class="h">🌍 Shaam V17 - كل دوريات العالم + المنتخبات ✅</div><div class="money"><span>🔴 <span id="liveC">..</span> مباشر</span><span>📅 <span id="upC">..</span> قادمة</span><span>🌍 <span id="natC">..</span> منتخبات</span></div><div style="padding:6px"><div class="grid" id="leaguesGrid"></div><h3 style="text-align:center;color:#FFD700;margin:10px 0">📅 مباريات الـ 7 أيام الجاية - كل الدوريات الحقيقية</h3><div id="allMatches">⏳ يحمّل 15 دوري حقيقي من ESPN...</div></div><script>
const LEAGUES_NAMES={"eng.1":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي","esp.1":"🇪🇸 إسباني","ita.1":"🇮🇹 إيطالي","ger.1":"🇩🇪 ألماني","fra.1":"🇫🇷 فرنسي","tur.1":"🇹🇷 تركي","sau.1":"🇸🇦 سعودي","uefa.champions":"🏆 أبطال","uefa.europa":"🏆 أوروبا","por.1":"🇵🇹 برتغالي","ned.1":"🇳🇱 هولندي","bel.1":"🇧🇪 بلجيكي","usa.1":"🇺🇸 أمريكي","bra.1":"🇧🇷 برازيلي","egy.1":"🇪🇬 مصري","fifa.friendly":"🌍 منتخبات ودية","uefa.nations":"🏆 دوري الأمم"};
let grid=document.getElementById('leaguesGrid');Object.entries(LEAGUES_NAMES).forEach(([k,v])=>{grid.innerHTML+=`<div class=leagueBox><b>${v}</b><br><small>${k}</small><br><span id="c-${k}">..</span></div>`;});
async function load(){try{let r=await fetch('/api/all');let d=await r.json();document.getElementById('liveC').innerText=d.live.length;document.getElementById('upC').innerText=d.upcoming.length;document.getElementById('natC').innerText=d.national.length;let box=document.getElementById('allMatches');if(d.live.length>0){box.innerHTML='<h4 style=color:red>🔴 مباشر الآن</h4>'+d.live.map(m=>`<div class="card live"><b>${m.home} vs ${m.away}</b> <b style=color:#FFD700>${m.score}</b><br><small>${LEAGUES_NAMES[m.league]||m.league} ${m.minute} ✅</small></div>`).join('')+'<hr>';}else{box.innerHTML='<div class=card>📭 لا يوجد مباشر الآن - يبدأ 19:00 بتوقيت إسطنبول<br><small>شوف القادمة تحت 👇</small></div>';}
box.innerHTML+=d.upcoming.map(m=>`<div class=card><b>${m.home} vs ${m.away}</b><br><small>📅 ${m.time} | ${LEAGUES_NAMES[m.league]||m.league} ✅ حقيقي</small></div>`).join('');
if(d.national.length>0){box.innerHTML+='<h4 style=color:#00bfff>🌍 المنتخبات</h4>'+d.national.map(m=>`<div class=card style="border-right-color:#00bfff"><b>🌍 ${m.home} vs ${m.away}</b><br><small>${m.league} ${m.time}</small></div>`).join('');}
Object.keys(LEAGUES_NAMES).forEach(k=>{let el=document.getElementById('c-'+k);if(el){let cnt=d.upcoming.filter(x=>x.league==k).length+d.live.filter(x=>x.league==k).length;el.innerText=cnt>0?cnt+' مباريات':'0';}});}catch(e){document.getElementById('allMatches').innerHTML='❌ خطأ - حدّث الصفحة';}}load();setInterval(load,60000);</script></body></html>"""

@app.route('/')
def home(): return HTML

@app.route('/api/all')
def api_all():
    live=[]
    up=[]
    nat=[]
    # مباشر - 12 دوري
    for lg in ["eng.1","esp.1","ita.1","ger.1","fra.1","tur.1","sau.1","uefa.champions","uefa.europa","por.1","ned.1","bel.1"]:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=2)
            for ev in r.json().get('events',[]):
                comp=ev['competitions'][0]
                if comp['status']['type']['state']=='in':
                    live.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":f"{comp['competitors'][0].get('score','0')}-{comp['competitors'][1].get('score','0')}","league":lg,"minute":comp['status'].get('displayClock','Live')})
        except: continue
    # قادمة 7 أيام - 15 دوري
    for i in range(1,8):
        date=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        for lg in ["eng.1","esp.1","ita.1","ger.1","fra.1","tur.1","sau.1","por.1","ned.1","bel.1","usa.1","bra.1","egy.1","mex.1","qat.1"]:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}",timeout=2)
                for ev in r.json().get('events',[]):
                    comp=ev['competitions'][0]
                    up.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"time":date,"league":lg})
                if len(up)>=50: break
            except: continue
        if len(up)>=50: break
    # منتخبات
    for i in range(0,7):
        date=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        for lg in ["fifa.friendly","uefa.nations","fifa.world.qual"]:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}",timeout=2)
                for ev in r.json().get('events',[]):
                    comp=ev['competitions'][0]
                    nat.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"time":date,"league":lg})
            except: continue
    return jsonify({"live":live,"upcoming":up[:50],"national":nat[:20]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
