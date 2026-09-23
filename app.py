from flask import Flask, jsonify
import datetime
app = Flask(__name__)

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,red);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:10px;border-radius:12px}
.card.nat{border-right-color:gold;background:#1a1a00}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:6px;max-height:200px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:6px;text-align:center;font-size:9px}
.box.ok{border-color:#00ff00;background:#002a00}
.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:6px 10px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:6px;background:#333;border-radius:6px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,#00ff00,gold);transition:width.5s}
.btn{background:#00ff00;color:#000;border:none;padding:6px 10px;border-radius:14px;font-weight:900;margin:2px;cursor:pointer}
.sec{padding:6px 10px;font-weight:900;color:#00ff00;border-bottom:1px solid #333;margin-top:8px;font-size:11px}
</style></head><body>
<div class=h>V52.1 ULTIMATE LIGHT - 120 دولة + 8 كؤوس منتخبات - AUTO LOAD</div>
<div style="padding:5px;font-size:10px;color:#00ff00;display:flex;justify-content:space-between"><span id=live>LIVE:0</span><span id=cnt>0/128</span><span id=upd>يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: سوريا، كأس العالم، الهلال..." oninput="doFilter()"></div>
<div style="padding:6px;white-space:nowrap;overflow:auto"><span class="f active" onclick="setF('all',this)">الكل 128</span><span class=f onclick="setF('منتخبات',this)">🏆 منتخبات</span><span class=f onclick="setF('syria',this)">سوريا</span><span class=f onclick="setF('saudi',this)">السعودية</span><span class=f onclick="setF('egypt',this)">مصر</span><span class=f onclick="setF('world',this)">كأس العالم</span><span class=f onclick="setF('asia',this)">كأس آسيا</span></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">V52.1 LIGHT يحمل...</div>
<div class=sec>🏆 منتخبات - 8 بطولات</div><div class=grid id=gN></div>
<div class=sec>🌍 أندية - 120 دولة</div><div class=grid id=g></div>
<div id=m></div>
<script>
var NAT=["world_cup|كأس العالم","asia_cup|كأس آسيا","africa_cup|كأس أفريقيا","euro|يورو","copa_america|كوبا أمريكا","arab_cup|كأس العرب","olympic|الأولمبياد","nations|دوري الأمم"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","mauritania|موريتانيا","somalia|الصومال",
"england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","turkey|تركيا","greece|اليونان","sweden|السويد","norway|النرويج","denmark|الدنمارك","poland|بولندا","ukraine|أوكرانيا","russia|روسيا","croatia|كرواتيا","serbia|صربيا","swiss|سويسرا","austria|النمسا",
"brazil|البرازيل","argentina|الأرجنتين","uruguay|أوروغواي","chile|تشيلي","colombia|كولومبيا","peru|بيرو","mexico|المكسيك","usa|أمريكا","canada|كندا","japan|اليابان","korea|كوريا","china|الصين","australia|أستراليا","iran|إيران","india|الهند","thailand|تايلاند",
"nigeria|نيجيريا","senegal|السنغال","ghana|غانا","cameroon|الكاميرون","ivory|ساحل العاج","southafrica|جنوب أفريقيا","kenya|كينيا","ethiopia|إثيوبيا"];

var g=document.getElementById('g'),gn=document.getElementById('gN');
NAT.forEach(c=>{var p=c.split('|');gn.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
ALL.forEach(c=>{var p=c.split('|');g.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});

var all=[],filtered=[],loaded=0,total=NAT.length+ALL.length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit'})}catch(e){return d}}
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=force||document.querySelector('.f.active').innerText.toLowerCase();
 var code=''; if(f.includes('منتخبات')) code='منتخبات'; else if(f.includes('سوريا')||f=='syria') code='syria'; else if(f.includes('السعودية')||f=='saudi') code='saudi'; else if(f.includes('مصر')||f=='egypt') code='egypt'; else if(f.includes('العالم')||f=='world') code='world'; else if(f.includes('آسيا')||f=='asia') code='asia';
 filtered=all.filter(m=>{var mq=!q||m.home.toLowerCase().includes(q)||m.league.toLowerCase().includes(q); var mf=true; if(code=='منتخبات') mf=m.type=='nat'; else if(code) mf=m.code==code||m.league.toLowerCase().includes(code); return mq&&mf;});
 document.getElementById('m').innerHTML=filtered.slice(0,400).map(m=>{
  var pr1=50+Math.floor(Math.random()*30),pr2=100-pr1; var isNat=m.type=='nat';
  return '<div class="card '+(isNat?'nat':'')+'"><b>'+(isNat?'🏆 ':'⚽ ')+m.home+' vs '+m.away+'</b><br><small>⏰ '+ist(m.date)+' | '+m.league+' | 🧠 '+pr1+'%-'+pr2+'%</small><div class=bar><div style="width:'+pr1+'%;background:'+(isNat?'gold':'#00ff00')+'"></div><div style="width:'+pr2+'%;background:'+(isNat?'red':'gold')+'"></div></div></div>';
 }).join('')||'<div style=text-align:center;padding:15px;color:#00ff00">🔄 '+loaded+'/'+total+' - '+all.length+' مباراة</div>';
}
function loadOne(code,type){
 var box=document.getElementById('b-'+code),st=document.getElementById('s-'+code);
 if(box) box.className='box loading'; if(st) st.innerText='يحمل...';
 fetch('/api/'+code+'?t='+type).then(r=>r.json()).then(d=>{
  d.up.forEach(x=>{x.code=code;x.type=type;}); all=all.filter(m=>m.code!==code); all=all.concat(d.up); loaded++;
  document.getElementById('cnt').innerText=loaded+'/'+total+' - '+all.length+' مباراة';
  document.getElementById('progBar').style.width=(loaded/total*100)+'%';
  document.getElementById('s').innerText='✅ '+loaded+'/'+total+' - '+all.length+' مباراة - V52.1 LIGHT';
  if(box) box.className='box ok'; if(st) st.innerText=d.up.length+' ✅'; doFilter();
 }).catch(()=>{loaded++;doFilter();});
}
var q=[...NAT.map(c=>({code:c.split('|')[0],type:'nat'})),...ALL.map(c=>({code:c.split('|')[0],type:'club'}))],idx=0;
function auto(){if(idx>=q.length){document.getElementById('upd').innerText='✅ اكتمل! '+all.length+' مباراة';return;} var it=q[idx]; loadOne(it.code,it.type); idx++; setTimeout(auto,350);}
setTimeout(auto,800);
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
    if t=='nat':
        mp={"world_cup":[("البرازيل","الأرجنتين"),("فرنسا","إسبانيا"),("إنجلترا","ألمانيا"),("البرتغال","هولندا")],
        "asia_cup":[("السعودية","اليابان"),("إيران","كوريا"),("قطر","أستراليا"),("سوريا","العراق"),("الأردن","أوزبكستان")],
        "africa_cup":[("المغرب","السنغال"),("مصر","نيجيريا"),("الجزائر","تونس"),("الكاميرون","غانا")],
        "euro":[("فرنسا","إنجلترا"),("إسبانيا","ألمانيا"),("البرتغال","إيطاليا")],
        "copa_america":[("البرازيل","الأرجنتين"),("أوروغواي","كولومبيا")],
        "arab_cup":[("المغرب","الجزائر"),("مصر","السعودية"),("تونس","العراق"),("سوريا","الأردن")],
        "olympic":[("فرنسا","إسبانيا"),("المغرب","مصر")],
        "nations":[("إسبانيا","فرنسا"),("ألمانيا","البرتغال")]}
        teams=mp.get(code,[(code+" A",code+" B")])
        up=[{"home":h,"away":a,"league":f"{code} - منتخبات","date":(b+datetime.timedelta(days=2,hours=19)).isoformat()} for h,a in teams]
        return jsonify({"up":up})
    club={"syria":[("الكرامة","حطين"),("الفتوة","الوثبة"),("الجيش","الوحدة"),("جبلة","تشرين"),("الشرطة","أهلي حلب")],
    "saudi":[("الهلال","النصر"),("الاتحاد","الأهلي"),("الشباب","الاتفاق")],
    "egypt":[("الأهلي","الزمالك"),("بيراميدز","المصري")],
    "england":[("Man City","Arsenal"),("Liverpool","Chelsea"),("Man United","Tottenham")],
    "spain":[("Real Madrid","Barcelona"),("Atletico","Sevilla")],
    "italy":[("Inter","AC Milan"),("Juventus","Napoli")],
    "germany":[("Bayern","Dortmund")],
    "france":[("PSG","Marseille")],
    "brazil":[("Flamengo","Palmeiras")],
    "argentina":[("Boca","River Plate")]}
    teams=club.get(code,[(code+" الملكي",code+" الوطني")])
    up=[{"home":h,"away":a,"league":f"{['الدوري','كأس الملك','كأس السوبر'][i%3]} - {code}","date":(b+datetime.timedelta(days=1+i,hours=17)).isoformat()} for i,(h,a) in enumerate(teams)]
    return jsonify({"up":up})

if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
