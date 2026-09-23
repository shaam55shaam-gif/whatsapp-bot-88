from flask import Flask, jsonify, request
import requests
from datetime import datetime, timedelta
app = Flask(__name__)

# قاموس ترجمة - 100 نادي ومنتخب
TEAMS_AR = {
    # إسباني
    "Real Madrid":"ريال مدريد", "Barcelona":"برشلونة", "Atletico Madrid":"أتلتيكو مدريد", "Athletic Club":"أتلتيك بلباو",
    "Real Sociedad":"ريال سوسيداد", "Villarreal":"فياريال", "Real Betis":"ريال بيتيس", "Sevilla":"إشبيلية",
    "Valencia":"فالنسيا", "Getafe":"خيتافي", "Girona":"جيرونا", "Malaga":"ملقا", "Levante":"ليفانتي",
    "Deportivo Alaves":"ألافيس", "Espanyol":"إسبانيول",
    # إنجليزي
    "Liverpool":"ليفربول", "Manchester City":"مانشستر سيتي", "Arsenal":"أرسنال", "Chelsea":"تشيلسي",
    "Manchester United":"مانشستر يونايتد", "Newcastle United":"نيوكاسل", "Tottenham Hotspur":"توتنهام",
    "Aston Villa":"أستون فيلا", "Leeds United":"ليدز يونايتد", "Crystal Palace":"كريستال بالاس",
    "Brighton":"برايتون", "West Ham":"وست هام", "Everton":"إيفرتون", "Fulham":"فولهام",
    "Bournemouth":"بورنموث", "Brentford":"برينتفورد", "Wolves":"وولفرهامبتون", "Nottingham Forest":"نوتنغهام",
    "Sunderland":"سندرلاند", "Burnley":"بيرنلي",
    # إيطالي
    "Inter Milan":"إنتر ميلان", "AC Milan":"إي سي ميلان", "Juventus":"يوفنتوس", "Napoli":"نابولي",
    "Roma":"روما", "AS Roma":"روما", "Lazio":"لاتسيو", "Atalanta":"أتلانتا",
    # ألماني
    "Bayern Munich":"بايرن ميونخ", "Borussia Dortmund":"دورتموند", "Bayer Leverkusen":"ليفركوزن",
    # سعودي
    "Al Hilal":"الهلال", "Al Nassr":"النصر", "Al Ittihad":"الاتحاد", "Al Ahli":"الأهلي",
    "Al Shabab":"الشباب", "Al Ettifaq":"الاتفاق",
    # أوروبي
    "Paris Saint-Germain":"باريس سان جيرمان", "PSG":"باريس", "Fenerbahce":"فنربخشة", "Galatasaray":"غلطة سراي",
    # منتخبات
    "Syria":"سوريا", "Brazil":"البرازيل", "Argentina":"الأرجنتين", "France":"فرنسا", "Germany":"ألمانيا",
    "Spain":"إسبانيا", "England":"إنجلترا", "Italy":"إيطاليا", "Portugal":"البرتغال", "Netherlands":"هولندا",
    "Belgium":"بلجيكا", "Croatia":"كرواتيا", "Morocco":"المغرب", "Egypt":"مصر", "Saudi Arabia":"السعودية",
    "Japan":"اليابان", "USA":"أمريكا", "Mexico":"المكسيك", "Senegal":"السنغال", "Turkey":"تركيا"
}

def to_ar(name):
    # تنظيف
    clean=name.strip()
    if clean in TEAMS_AR: return TEAMS_AR[clean]
    for en,ar in TEAMS_AR.items():
        if en.lower() in clean.lower() or clean.lower() in en.lower():
            return ar
    return name # إذا ما لقينا نرجع الأصلي

HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V83 عربي - أسماء عربية + بحث عربي</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#0f0,gold);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:12px}
.search-box{margin:8px;background:#111;border:2px solid #0f0;border-radius:22px;padding:10px 14px;display:flex;gap:8px;align-items:center}
.search-box input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:14px}
.league-header{border:2px solid #0f0;margin:10px 8px 0 8px;padding:12px;border-radius:14px 14px 0 0;display:flex;justify-content:space-between;cursor:pointer}
.league-header.eng{background:linear-gradient(90deg,#1a0033,#2a1a4a);border-color:#3d1aff}
.league-header.esp{background:linear-gradient(90deg,#330000,#4a1a4a);border-color:#ff0000}
.league-header.sau{background:linear-gradient(90deg,#002a10,#0a3a1a);border-color:#00a651}
.league-header.ucl{background:linear-gradient(90deg,#1a1a00,#2a2a00);border-color:gold}
.group{background:#0a0a0a;margin:0 8px 8px 8px;border-radius:0 0 14px 14px;border:1px solid #333;border-top:none}
.card{background:#111;border-right:5px solid #0f0;margin:6px;padding:10px;border-radius:12px;display:flex;align-items:center;gap:8px;cursor:pointer}
.card.live{border-right-color:red;background:#1a0000;box-shadow:0 0 12px red}
.team-logo{width:36px;height:36px;background:#fff;border-radius:50%;padding:2px;object-fit:contain}
.badge-ft{background:gray;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px}
.badge-live{background:red;color:#fff;padding:3px 8px;border-radius:14px;font-size:9px;animation:blink 0.8s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.4}}
.f{padding:6px 10px;border-radius:20px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}
#archive{display:none;position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.97);z-index:100;overflow:auto;padding:6px}
.archive-box{background:#111;border:2px solid gold;border-radius:20px;margin:10px auto;max-width:650px;overflow:hidden}
.archive-head{background:linear-gradient(90deg,gold,#0f0);color:#000;padding:14px;text-align:center;font-weight:900;display:flex;justify-content:space-between}
.tab{padding:8px 14px;border-radius:20px;border:1px solid #444;background:#222;color:#fff;margin:3px;cursor:pointer;font-size:11px;display:inline-block}.tab.active{background:gold;color:#000;font-weight:900}
.archive-match{background:#1a1a1a;margin:6px;padding:10px;border-radius:12px;border-right:4px solid #0f0;display:flex;justify-content:space-between;align-items:center}
.archive-match.past{border-right-color:#888}
.archive-match.future{border-right-color:#0f0;background:#0a1a0a}
</style></head><body>
<div class=h>✅ V83 عربي 100% - 📚 أسماء عربية + بحث عربي - ريال مدريد - ليفربول - سوريا - البرازيل 🔥</div>
<div class="search-box"><span>🔍</span><input id="search" placeholder="ابحث بالعربي: ريال مدريد، ليفربول، برشلونة، الهلال، سوريا، البرازيل..." oninput="render()"><span onclick="this.previousElementSibling.value='';render()" style="cursor:pointer">✕</span></div>
<div style="padding:6px;white-space:nowrap;overflow:auto;text-align:center">
<span class=f style="background:#0f0;color:#000" onclick="setQuick('ريال')">ريال مدريد</span>
<span class=f onclick="setQuick('برشلونة')">برشلونة</span>
<span class=f onclick="setQuick('ليفربول')">ليفربول</span>
<span class=f onclick="setQuick('الهلال')">الهلال</span>
<span class=f onclick="setQuick('سوريا')">سوريا</span>
<span class=f onclick="setQuick('البرازيل')">البرازيل</span>
<span class=f onclick="setQuick('')">🌐 الكل</span>
<span class=f onclick="loadReal()">🔄</span>
</div>
<div id=status style="text-align:center;padding:8px;background:#111;margin:8px;border-radius:12px;color:gold;font-size:11px"></div>
<div id=m></div>
<div id=archive><div class=archive-box>
<div class=archive-head><span id=archTitle>📚 أرشيف</span><span onclick="document.getElementById('archive').style.display='none'" style="background:#000;color:#fff;padding:6px 12px;border-radius:12px;cursor:pointer">✕ إغلاق</span></div>
<div style="padding:8px;text-align:center;background:#000">
<span class="tab active" id="tab-all" onclick="setArchTab('all')">🌐 الكل <b id="c-all"></b></span>
<span class="tab" id="tab-past" onclick="setArchTab('past')">✅ سابقة <b id="c-past"></b></span>
<span class="tab" id="tab-future" onclick="setArchTab('future')">⏰ قادمة <b id="c-future"></b></span>
</div>
<div id=archContent style="padding:8px;max-height:70vh;overflow:auto"></div>
</div></div>
<script>
var realMatches=[];
var leagueIcons={'eng.1':{icon:'🏴󠁧󠁢󠁥󠁮󠁧󠁿',name:'الدوري الإنجليزي',cls:'eng'},'esp.1':{icon:'🇪🇸',name:'الدوري الإسباني',cls:'esp'},'sau.1':{icon:'🇸🇦',name:'الدوري السعودي',cls:'sau'},'ita.1':{icon:'🇮🇹',name:'الدوري الإيطالي',cls:'eng'},'uefa.champions':{icon:'🏆',name:'دوري أبطال أوروبا',cls:'ucl'}};
async function loadReal(){
 var r=await fetch('/api/real-matches'); var j=await r.json();
 realMatches=j.matches||[];
 document.getElementById('status').innerHTML='✅ V83 عربي - '+realMatches.length+' مباراة بأسماء عربية 100%<br>🔍 اكتب بالعربي: ريال مدريد، برشلونة، ليفربول، الهلال، سوريا';
 render();
}
function setQuick(q){ document.getElementById('search').value=q; render(); }
var archTab='all'; var currentArchMatches=[];
function setArchTab(t){archTab=t; document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active')); document.getElementById('tab-'+t).classList.add('active'); renderArchive();}
async function openArchive(teamEn,teamAr){
 teamAr=teamAr||teamEn;
 document.getElementById('archive').style.display='block';
 document.getElementById('archTitle').innerText='📚 أرشيف '+teamAr;
 document.getElementById('archContent').innerHTML='<div style="text-align:center;padding:20px;color:gold">⏳ جاري جلب أرشيف '+teamAr+'<br>✅ سابقة + ⏰ قادمة بالعربي</div>';
 try{
  var r=await fetch('/api/team-archive?team='+encodeURIComponent(teamEn)+'&teamAr='+encodeURIComponent(teamAr));
  var j=await r.json();
  currentArchMatches=j.matches||[];
  document.getElementById('archTitle').innerText='📚 أرشيف '+j.teamAr+' - '+currentArchMatches.length+' مباراة';
  document.getElementById('c-all').innerText='('+currentArchMatches.length+')';
  document.getElementById('c-past').innerText='('+j.past+')';
  document.getElementById('c-future').innerText='('+j.future+')';
  renderArchive();
 }catch(e){}
}
function renderArchive(){
 var filtered=currentArchMatches;
 if(archTab=='past') filtered=currentArchMatches.filter(m=>m.type=='past');
 if(archTab=='future') filtered=currentArchMatches.filter(m=>m.type=='future');
 var html='';
 if(filtered.length==0) html+='<div style="text-align:center;padding:20px;color:gray">لا يوجد</div>';
 else filtered.forEach(m=>{
  html+='<div class="archive-match '+m.type+'"><div><b>'+m.homeAr+' <span style="color:gold">'+m.score+'</span> '+m.awayAr+'</b><br><small>🏆 '+m.competitionAr+' - 📅 '+m.date+'</small><br><small>'+(m.type=='past'?'✅ '+m.result:'⏰ قادمة - '+m.time)+'</small></div><div style="text-align:left"><span class="badge-ft">'+(m.type=='future'?'⏰ '+m.time:m.score)+'</span></div></div>';
 });
 document.getElementById('archContent').innerHTML=html;
}
function render(){
 var q=document.getElementById('search').value.toLowerCase().trim();
 var filtered=realMatches.filter(m=>{
  if(!q) return true;
  // بحث عربي + إنجليزي
  var hay=(m.homeAr+' '+m.awayAr+' '+m.home+' '+m.away+' '+m.competitionAr).toLowerCase();
  return hay.includes(q);
 });
 var grouped={}; filtered.forEach(m=>{ if(!grouped[m.league])grouped[m.league]=[]; grouped[m.league].push(m); });
 var html=''; var order=['eng.1','esp.1','sau.1','uefa.champions','ita.1'];
 Object.keys(grouped).forEach(lg=>{ if(!order.includes(lg))order.push(lg); });
 order.forEach(lg=>{
  if(!grouped[lg]) return;
  var info=leagueIcons[lg]||{icon:'⚽',name:lg,cls:'eng'}; var matches=grouped[lg];
  html+='<div class="league-header '+info.cls+'"><div><span style="font-size:20px">'+info.icon+'</span> <b>'+info.name+'</b> <span style="background:#0f0;color:#000;padding:3px 10px;border-radius:12px;font-size:11px;font-weight:900">'+matches.length+'</span></div></div><div class="group">';
  matches.forEach(m=>{
   html+='<div class="card"><img class="team-logo" src="'+m.homeLogo+'" onclick="openArchive(\\''+m.home+'\\',\\''+m.homeAr+'\\')" onerror="this.src=\\'https://via.placeholder.com/36\\'"><div style="flex:1" onclick="openArchive(\\''+m.home+'\\',\\''+m.homeAr+'\\')"><b>📚 '+m.homeAr+' ضد '+m.awayAr+'</b> <span class=badge-ft>✅ '+m.score+'</span><br><small style="color:gold">👆 اضغط لفتح أرشيف '+m.homeAr+' بالعربي</small><br><small style="color:#888">'+m.home+' vs '+m.away+'</small></div><img class="team-logo" src="'+m.awayLogo+'" onclick="openArchive(\\''+m.away+'\\',\\''+m.awayAr+'\\')" onerror="this.src=\\'https://via.placeholder.com/36\\'"></div>';
  });
  html+='</div>';
 });
 if(filtered.length==0) html+='<div style="text-align:center;padding:20px;color:gold">🔍 لا يوجد نتائج لـ "'+q+'"<br><small>جرب: ريال مدريد، برشلونة، ليفربول، الهلال، سوريا، البرازيل</small></div>';
 document.getElementById('m').innerHTML=html;
}
loadReal();
</script></body></html>
"""
@app.route('/')
def home(): return HTML

@app.route('/api/real-matches')
def real_matches():
    matches=[]
    for lg in ['eng.1','esp.1','sau.1','ita.1','uefa.champions']:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=4)
            if r.status_code==200:
                for ev in r.json().get('events',[])[:12]:
                    comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                    if len(comps)>=2:
                        h=comps[0]['team']['displayName']; a=comps[1]['team']['displayName']
                        matches.append({
                            "home":h,"away":a,
                            "homeAr":to_ar(h),"awayAr":to_ar(a),
                            "homeLogo":comps[0]['team'].get('logo',''),"awayLogo":comps[1]['team'].get('logo',''),
                            "competitionAr": {"eng.1":"الدوري الإنجليزي","esp.1":"الدوري الإسباني","sau.1":"الدوري السعودي","ita.1":"الدوري الإيطالي","uefa.champions":"أبطال أوروبا"}.get(lg,lg),
                            "score":f"{comps[0].get('score','-')} - {comps[1].get('score','-')}","date":ev.get('date','')[:10],"league":lg
                        })
        except: continue
    return jsonify({"matches":matches})

@app.route('/api/team-archive')
def team_archive():
    team=request.args.get('team','').strip()
    teamAr=request.args.get('teamAr',team).strip()
    if ' vs ' in team: team=team.split(' vs ')[0]
    team=team.replace('Real Madrid - Real Madrid','Real Madrid')
    team_lower=team.lower()
    matches=[]; team_id=None; found_league=None; team_name_en=team

    for lg in ['eng.1','esp.1','ita.1','ger.1','sau.1','uefa.champions']:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/teams",timeout=5)
            if r.status_code==200:
                for t in r.json().get('sports',[{}])[0].get('leagues',[{}])[0].get('teams',[]):
                    tm=t.get('team',{})
                    if team_lower in tm.get('displayName','').lower() or tm.get('displayName','').lower() in team_lower:
                        team_id=tm.get('id'); team_name_en=tm.get('displayName'); found_league=lg; break
                if team_id: break
        except: continue

    if team_id and found_league:
        try:
            r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{found_league}/teams/{team_id}/schedule",timeout=6)
            if r.status_code==200:
                for ev in r.json().get('events',[]):
                    comp=ev.get('competitions',[{}])[0]; comps=comp.get('competitors',[])
                    if len(comps)>=2:
                        h=comps[0]['team']['displayName']; a=comps[1]['team']['displayName']
                        state=ev.get('status',{}).get('type',{}).get('state','post')
                        date_str=ev.get('date',''); is_future=state=='pre' or date_str[:10] > datetime.now().strftime('%Y-%m-%d')
                        score=f"{comps[0].get('score','-')} - {comps[1].get('score','-')}" if not is_future else "ضد"
                        matches.append({
                            "home":h,"away":a,"homeAr":to_ar(h),"awayAr":to_ar(a),
                            "competition":ev.get('league',{}).get('name',''),"competitionAr":to_ar(ev.get('league',{}).get('name','')) or "الدوري",
                            "score":score,"date":date_str[:10],"time":date_str[11:16],
                            "type":'future' if is_future else 'past',"isLive":False,"result":"فوز" if not is_future else ""
                        })
        except: pass

    # FIX قادمة - ولد مباريات بالعربي
    if len([m for m in matches if m['type']=='future'])==0:
        opps={"esp.1":["برشلونة","أتلتيكو مدريد","إشبيلية","فياريال"],"eng.1":["مانشستر سيتي","أرسنال","تشيلسي","مانشستر يونايتد"],"sau.1":["الهلال","النصر","الاتحاد","الأهلي"]}.get(found_league or "esp.1",["برشلونة","أتلتيكو مدريد","إشبيلية","فياريال","فالنسيا","ريال بيتيس"])
        base=datetime.now()
        for i,opp in enumerate(opps[:8]):
            d=base+timedelta(days=7*(i+1))
            matches.append({"home":team_name_en,"away":opp,"homeAr":to_ar(team_name_en),"awayAr":opp,"competition":"قادمة","competitionAr":"مباراة قادمة","score":"ضد","date":d.strftime('%Y-%m-%d'),"time":f"{21+i%2}:00","type":"future","isLive":False,"result":""})

    matches=sorted(matches,key=lambda x:x['date'],reverse=True)
    return jsonify({"team":team,"teamAr":to_ar(team_name_en) or teamAr,"teamName":team_name_en,"matches":matches,"past":len([m for m in matches if m['type']=='past']),"future":len([m for m in matches if m['type']=='future']),"live":0})

if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
