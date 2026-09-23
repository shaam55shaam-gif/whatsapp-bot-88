from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

ALL_LEAGUES = {
"eng.1":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي","esp.1":"🇪🇸 إسباني","ita.1":"🇮🇹 إيطالي","ger.1":"🇩🇪 ألماني","fra.1":"🇫🇷 فرنسي",
"tur.1":"🇹🇷 تركي","sau.1":"🇸🇦 سعودي","egy.1":"🇪🇬 مصري","uae.1":"🇦🇪 إماراتي","qat.1":"🇶🇦 قطري",
"uefa.champions":"🏆 أبطال أوروبا","uefa.europa":"🏆 الدوري الأوروبي","uefa.europa.conf":"🏆 المؤتمر",
"por.1":"🇵🇹 برتغالي","ned.1":"🇳🇱 هولندي","bel.1":"🇧🇪 بلجيكي","sco.1":"🏴󠁧󠁢󠁳󠁣󠁴󠁿 اسكتلندي","usa.1":"🇺🇸 أمريكي",
"bra.1":"🇧🇷 برازيلي","arg.1":"🇦🇷 أرجنتيني","mex.1":"🇲🇽 مكسيكي","jpn.1":"🇯🇵 ياباني","aus.1":"🇦🇺 أسترالي",
"ned.2":"🇳🇱 هولندي 2","eng.2":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي 2","esp.2":"🇪🇸 إسباني 2",
"fifa.friendly":"🌍 ودية منتخبات","uefa.nations":"🏆 دوري الأمم","fifa.world.qual":"🌍 تصفيات كأس العالم","fifa.world":"🏆 كأس العالم",
"caf.champions":"🏆 أبطال أفريقيا","afc.champions":"🏆 أبطال آسيا","conmebol.libertadores":"🏆 ليبرتادوريس"
}

HTML = """<!DOCTYPE html><html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Shaam V18 ALL 35 🌍</title><style>body{background:#000;color:#fff;font-family:Arial;margin:0}.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:12px;text-align:center;font-weight:900}.money{background:#111;border:2px solid #FFD700;padding:10px;border-radius:20px;margin:6px;text-align:center;font-weight:900;display:flex;justify-content:space-around}.grid{display:grid;grid-template-columns:1fr 1fr;gap:5px;padding:5px}.box{background:#111;border:1px solid #333;border-radius:10px;padding:8px;text-align:center;font-size:10px;min-height:45px}.box.has{background:#1a2e1a;border-color:#00ff00}.card{background:#1a1a1a;border-right:4px solid #FFD700;border-radius:12px;margin:6px;padding:9px;font-size:12px}.live{border-right-color:red}</style></head><body><div class="h">🌍 Shaam V18 - كل الدوريات الـ 35 حقيقية ✅</div><div class="money"><span>🔴 <span id="liveC">0</span> مباشر</span><span>📅 <span id="upC">0</span> قادمة</span><span>🌍 <span id="natC">0</span> منتخبات</span><span>⏳ <span id="done">0</span>/35</span></div><div id="status" style="text-align:center;color:#FFD700;font-size:11px;padding:4px">⏳ يجيب كل الدوريات واحد واحد...</div><div class="grid" id="grid"></div><h3 style="text-align:center;color:#FFD700;margin:8px 0">📅 كل المباريات الحقيقية</h3><div id="matches">⏳ بانتظار الدوريات...</div><script>
const LEAGUES={"eng.1":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 إنجليزي","esp.1":"🇪🇸 إسباني","ita.1":"🇮🇹 إيطالي","ger.1":"🇩🇪 ألماني","fra.1":"🇫🇷 فرنسي","tur.1":"🇹🇷 تركي","sau.1":"🇸🇦 سعودي","egy.1":"🇪🇬 مصري","uae.1":"🇦🇪 إماراتي","qat.1":"🇶🇦 قطري","uefa.champions":"🏆 أبطال أوروبا","uefa.europa":"🏆 أوروبا","uefa.europa.conf":"🏆 المؤتمر","por.1":"🇵🇹 برتغالي","ned.1":"🇳🇱 هولندي","bel.1":"🇧🇪 بلجيكي","sco.1":"🏴󠁧󠁢󠁳󠁣󠁴󠁿 اسكتلندي","usa.1":"🇺🇸 أمريكي","bra.1":"🇧🇷 برازيلي","arg.1":"🇦🇷 أرجنتيني","mex.1":"🇲🇽 مكسيكي","jpn.1":"🇯🇵 ياباني","aus.1":"🇦🇺 أسترالي","ned.2":"🇳🇱 2","eng.2":"🏴󠁧󠁢󠁥󠁮󠁧󠁿 2","esp.2":"🇪🇸 2","fifa.friendly":"🌍 ودية","uefa.nations":"🏆 أمم","fifa.world.qual":"🌍 تصفيات","fifa.world":"🏆 كأس العالم","caf.champions":"🏆 أفريقيا","afc.champions":"🏆 آسيا","conmebol.libertadores":"🏆 ليبرتادوريس"};
let grid=document.getElementById('grid');Object.entries(LEAGUES).forEach(([k,v])=>{grid.innerHTML+=`<div class="box" id="box-${k}"><b>${v}</b><br><small>${k}</small><br><span id="cnt-${k}">⏳</span></div>`;});
let allUp=[],allLive=[],allNat=[],done=0;
async function fetchLeague(lg){
try{
let r=await fetch('/api/league/'+lg);let d=await r.json();
document.getElementById('cnt-'+lg).innerText=d.up.length+d.live.length>0?d.up.length+d.live.length+' مباريات':'0';
if(d.up.length+d.live.length>0) document.getElementById('box-'+lg).classList.add('has');
allUp=allUp.concat(d.up);allLive=allLive.concat(d.live);allNat=allNat.concat(d.nat);
document.getElementById('liveC').innerText=allLive.length;document.getElementById('upC').innerText=allUp.length;document.getElementById('natC').innerText=allNat.length;
let box=document.getElementById('matches');
let html='';
if(allLive.length>0) html+='<div style="background:#300;padding:5px;text-align:center;color:red">🔴 مباشر الآن ('+allLive.length+')</div>'+allLive.map(m=>`<div class="card live">🔴 <b>${m.home} vs ${m.away}</b> <b style=color:#FFD700>${m.score}</b><br><small>${m.league}</small></div>`).join('');
html+=allUp.map(m=>`<div class=card>📅 <b>${m.home} vs ${m.away}</b><br><small>${m.date} | ${m.league} ✅</small></div>`).join('');
if(allNat.length>0) html+='<div style="background:#002233;padding:5px;text-align:center;color:#00bfff">🌍 منتخبات</div>'+allNat.map(m=>`<div class=card style="border-right-color:#00bfff">🌍 <b>${m.home} vs ${m.away}</b><br><small>${m.league}</small></div>`).join('');
box.innerHTML=html||'📭 لا يوجد مباريات بالأيام الجاية - توقف دولي';
}catch(e){document.getElementById('cnt-'+lg).innerText='خطأ';}
done++;document.getElementById('done').innerText=done;document.getElementById('status').innerText=`✅ جاب ${done}/35 دوري - ${allUp.length+allLive.length} مباراة حقيقية`;
if(done==Object.keys(LEAGUES).length) document.getElementById('status').innerText=`✅ خلص! جاب كل الـ 35 دوري - ${allUp.length+allLive.length} مباراة حقيقية من ESPN`;
}
async function loadAll(){for(let lg of Object.keys(LEAGUES)){await fetchLeague(lg);}}
loadAll();
</script></body></html>"""

@app.route('/')
def home(): return HTML

@app.route('/api/league/<lg>')
def api_league(lg):
    live=[]
    up=[]
    nat=[]
    try:
        r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=4)
        for ev in r.json().get('events',[]):
            comp=ev['competitions'][0]
            if comp['status']['type']['state']=='in':
                live.append({"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"score":f"{comp['competitors'][0].get('score','0')}-{comp['competitors'][1].get('score','0')}","league":lg})
    except: pass
    # قادمة 3 أيام فقط لكل دوري (عشان السرعة)
    for i in range(1,4):
        date=(datetime.datetime.now()+datetime.timedelta(days=i)).strftime("%Y%m%d")
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard?dates={date}",timeout=4)
            for ev in r.json().get('events',[]):
                comp=ev['competitions'][0]
                item={"home":comp['competitors'][0]['team']['displayName'],"away":comp['competitors'][1]['team']['displayName'],"date":date,"league":lg}
                if lg.startswith("fifa") or lg.startswith("uefa.nations"):
                    nat.append(item)
                else:
                    up.append(item)
            if len(up)>=5: break
        except: continue
    return jsonify({"live":live,"up":up[:5],"nat":nat[:5]})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
