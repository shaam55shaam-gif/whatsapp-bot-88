from flask import Flask, jsonify
import datetime
app = Flask(__name__)

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,#00aaff);color:#000;padding:9px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:10px;border-radius:12px}
.card.nat{border-right-color:gold;background:#1a1a00}.card.champ{border-right-color:#00aaff;background:#001a2a}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:6px;max-height:180px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:5px;text-align:center;font-size:9px}
.box.ok{border-color:#00ff00;background:#002a00}.box.ok2{border-color:gold;background:#2a2a00}.box.ok3{border-color:#00aaff;background:#001a2a}
.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:6px 10px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:6px;background:#333;border-radius:6px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,#00ff00,gold,#00aaff);transition:width.5s}
.sec{padding:6px 10px;font-weight:900;border-bottom:1px solid #333;margin-top:8px;font-size:11px}
</style></head><body>
<div class=h>V54.1 CHAMPIONS LIGHT - 200+10+12 = 222 بطولة AUTO - خفيف</div>
<div style="padding:5px;font-size:10px;color:#00ff00;display:flex;justify-content:space-between"><span id=cnt>0/0</span><span id=upd>يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: الهلال، Real Madrid، كأس العالم..." oninput="doFilter()"></div>
<div style="padding:6px;white-space:nowrap;overflow:auto"><span class="f active" onclick="setF('all',this)">الكل 222</span><span class=f onclick="setF('champ',this)">🏆 أبطال</span><span class=f onclick="setF('منتخبات',this)">🌍 منتخبات</span><span class=f onclick="setF('عرب',this)">🇸🇦 عرب</span></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">V54.1 LIGHT يحمل...</div>
<div class=sec style="color:#00aaff">🏆 أبطال - 10</div><div class=grid id=gC></div>
<div class=sec style="color:gold">🌍 منتخبات - 12</div><div class=grid id=gN></div>
<div class=sec style="color:#00ff00">🌍 أندية - 70 دولة</div><div class=grid id=g></div>
<div id=m></div>
<script>
var CHAMP=["ucl|أبطال أوروبا","uel|الدوري الأوروبي","afc_cl|أبطال آسيا","afc2|أبطال آسيا 2","caf_cl|أبطال أفريقيا","caf_conf|الكونفدرالية","arab_cl|أبطال العرب","gulf_cl|أبطال الخليج","club_world|كأس العالم أندية","libertadores|ليبرتادوريس"];
var NAT=["world_cup|كأس العالم","asia_cup|كأس آسيا","africa_cup|كأس أفريقيا","euro|يورو","copa_america|كوبا أمريكا","arab_cup|كأس العرب","olympic|الأولمبياد","nations|دوري الأمم","gulf_cup|كأس الخليج","u21_euro|تحت 21","asian_games|الألعاب الآسيوية","african_ch|أفريقيا محليين"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان",
"england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","turkey|تركيا","brazil|البرازيل","argentina|الأرجنتين","usa|أمريكا","mexico|المكسيك","japan|اليابان","korea|كوريا","iran|إيران","australia|أستراليا","nigeria|نيجيريا","senegal|السنغال","ghana|غانا","southafrica|جنوب أفريقيا"];

var g=document.getElementById('g'),gn=document.getElementById('gN'),gc=document.getElementById('gC');
CHAMP.forEach(c=>{var p=c.split('|');gc.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
NAT.forEach(c=>{var p=c.split('|');gn.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
ALL.forEach(c=>{var p=c.split('|');g.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
var all=[],loaded=0,total=CHAMP.length+NAT.length+ALL.length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit'})}catch(e){return d}}
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=(force||document.querySelector('.f.active').innerText).toLowerCase();
 var code=''; if(f.includes('أبطال')||f=='champ') code='champ'; else if(f.includes('منتخبات')) code='منتخبات'; else if(f.includes('عرب')) code='عرب';
 var filtered=all.filter(m=>{var mq=!q||m.home.toLowerCase().includes(q)||m.league.toLowerCase().includes(q); var mf=true;
  if(code=='منتخبات') mf=m.type=='nat'; else if(code=='champ') mf=m.type=='champ'; else if(code=='عرب') mf=['syria','saudi','egypt','algeria','morocco','tunisia','iraq','jordan','lebanon','palestine','uae','qatar','kuwait','bahrain','oman','yemen','sudan','libya'].includes(m.code);
  return mq&&mf;});
 document.getElementById('m').innerHTML=filtered.slice(0,400).map(m=>{
  var pr1=50+Math.floor(Math.random()*30),pr2=100-pr1, isNat=m.type=='nat', isChamp=m.type=='champ';
  return '<div class="card '+(isNat?'nat':isChamp?'champ':'')+'"><b>'+(isChamp?'🏆 ':isNat?'🌍 ':'⚽ ')+m.home+' vs '+m.away+'</b><br><small>⏰ '+ist(m.date)+' | '+m.league+' | 🧠 '+pr1+'%-'+pr2+'%</small><div class=bar><div style="width:'+pr1+'%;background:'+(isChamp?'#00aaff':isNat?'gold':'#00ff00')+'"></div><div style="width:'+pr2+'%;background:gold"></div></div></div>';
 }).join('')||'<div style=text-align:center;padding:15px;color:#00ff00">🔄 '+loaded+'/'+total+' - '+all.length+' مباراة</div>';
}
function loadOne(code,type){
 var box=document.getElementById('b-'+code),st=document.getElementById('s-'+code);
 if(box) box.className='box loading'; if(st) st.innerText='يحمل...';
 fetch('/api/'+code+'?t='+type).then(r=>r.json()).then(d=>{
  d.up.forEach(x=>{x.code=code;x.type=type;}); all=all.filter(m=>m.code!==code); all=all.concat(d.up); loaded++;
  document.getElementById('cnt').innerText=loaded+'/'+total+' - '+all.length+' مباراة';
  document.getElementById('progBar').style.width=(loaded/total*100)+'%';
  document.getElementById('s').innerText='✅ '+loaded+'/'+total+' - '+all.length+' مباراة - V54.1 LIGHT';
  if(box) box.className= type=='champ'?'box ok3':type=='nat'?'box ok2':'box ok';
  if(st) st.innerText=d.up.length+' ✅'; doFilter();
 }).catch(()=>{loaded++;doFilter();});
}
var queue=[...CHAMP.map(c=>({code:c.split('|')[0],type:'champ'})),...NAT.map(c=>({code:c.split('|')[0],type:'nat'})),...ALL.map(c=>({code:c.split('|')[0],type:'club'}))],idx=0;
function auto(){if(idx>=queue.length){document.getElementById('upd').innerText='✅ اكتمل! '+all.length+' مباراة';return;} var it=queue[idx]; loadOne(it.code,it.type); idx++; setTimeout(auto,300);}
setTimeout(auto,700);
</script></body></html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/api/<code>')
def api(code):
    from flask import request
    t=request.args.get('t','club')
    import datetime
    b=datetime.datetime.now()
    if t=='champ':
        mp={"ucl":[("Real Madrid","Man City"),("Barcelona","PSG"),("Bayern","Arsenal"),("Inter","Liverpool")],
        "afc_cl":[("Al Hilal","Al Ain"),("Al Nassr","Persepolis"),("Al Ittihad","Al Sadd")],
        "caf_cl":[("Al Ahly","Wydad"),("Esperance","Mamelodi")],
        "arab_cl":[("Al Hilal","Al Ittihad"),("Wydad","Al Ahly")],
        "club_world":[("Man City","Flamengo"),("Real Madrid","Al Hilal")],
        "libertadores":[("Flamengo","River Plate"),("Palmeiras","Boca")],
        "gulf_cl":[("Al Ettifaq","Al Arabi")],
        "afc2":[("Taawoun","Wakrah")],
        "caf_conf":[("Zamalek","Berkane")],
        "uel":[("Man United","Roma")]}
        teams=mp.get(code,[(code+" A",code+" B")])
        return jsonify({"up":[{"home":h,"away":a,"league":f"{code} - أبطال","date":(b+datetime.timedelta(days=1,hours=20)).isoformat()} for h,a in teams]})
    if t=='nat':
        mp={"world_cup":[("البرازيل","الأرجنتين"),("فرنسا","إسبانيا")],
        "asia_cup":[("السعودية","اليابان"),("سوريا","العراق")],
        "africa_cup":[("المغرب","السنغال"),("مصر","نيجيريا")],
        "gulf_cup":[("السعودية","العراق"),("قطر","الإمارات"),("عمان","الكويت"),("البحرين","اليمن")]}
        teams=mp.get(code,[(code+" A",code+" B")])
        return jsonify({"up":[{"home":h,"away":a,"league":f"{code} - منتخبات","date":(b+datetime.timedelta(days=2,hours=19)).isoformat()} for h,a in teams]})
    club={"syria":[("الكرامة","حطين"),("الفتوة","الوثبة"),("الجيش","الوحدة")],
    "saudi":[("الهلال","النصر"),("الاتحاد","الأهلي")],
    "egypt":[("الأهلي","الزمالك")],
    "england":[("Man City","Arsenal"),("Liverpool","Chelsea")],
    "spain":[("Real Madrid","Barcelona")]}
    teams=club.get(code,[(code+" الملكي",code+" الوطني")])
    up=[{"home":h,"away":a,"league":f"{['الدوري','كأس الملك'][i%2]} - {code}","date":(b+datetime.timedelta(days=1+i,hours=17)).isoformat()} for i,(h,a) in enumerate(teams)]
    return jsonify({"up":up})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
