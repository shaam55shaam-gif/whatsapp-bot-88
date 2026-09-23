from flask import Flask, jsonify
import datetime
app = Flask(__name__)

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,red);color:#000;padding:9px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:10px;border-radius:12px}
.card.nat{border-right-color:gold;background:#1a1a00}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:6px;max-height:220px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:5px;text-align:center;font-size:9px}
.box.ok{border-color:#00ff00;background:#002a00}.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:6px 10px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:6px;background:#333;border-radius:6px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,#00ff00,gold);transition:width.5s}
.sec{padding:6px 10px;font-weight:900;color:#00ff00;border-bottom:1px solid #333;margin-top:8px;font-size:11px}
</style></head><body>
<div class=h>V53 WORLD 200 - 200 دولة + 12 كأس منتخبات = 212 بطولة AUTO LOAD</div>
<div style="padding:5px;font-size:10px;color:#00ff00;display:flex;justify-content:space-between"><span id=live>LIVE:0</span><span id=cnt>0/212</span><span id=upd>يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: سوريا، كأس العالم، الهلال، فلسطين..." oninput="doFilter()"></div>
<div style="padding:6px;white-space:nowrap;overflow:auto"><span class="f active" onclick="setF('all',this)">الكل 212</span><span class=f onclick="setF('منتخبات',this)">🏆 منتخبات</span><span class=f onclick="setF('عرب',this)">🇸🇦 عرب</span><span class=f onclick="setF('syria',this)">سوريا</span><span class=f onclick="setF('world',this)">كأس العالم</span><span class=f onclick="setF('asia',this)">كأس آسيا</span></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">V53 WORLD 200 يحمل...</div>
<div class=sec>🏆 منتخبات - 12 بطولة</div><div class=grid id=gN></div>
<div class=sec>🌍 أندية - 200 دولة</div><div class=grid id=g></div>
<div id=m></div>
<script>
var NAT=["world_cup|كأس العالم","asia_cup|كأس آسيا","africa_cup|كأس أفريقيا","euro|يورو","copa_america|كوبا أمريكا","arab_cup|كأس العرب","olympic|الأولمبياد","nations|دوري الأمم","asian_games|الألعاب الآسيوية","african_nations|بطولة أفريقيا محليين","gulf_cup|كأس الخليج","u21_euro|يورو تحت 21"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","mauritania|موريتانيا","somalia|الصومال","djibouti|جيبوتي","comoros|جزر القمر","west_sahara|الصحراء الغربية",
"england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","swiss|سويسرا","austria|النمسا","sweden|السويد","norway|النرويج","denmark|الدنمارك","finland|فنلندا","iceland|آيسلندا","poland|بولندا","ukraine|أوكرانيا","russia|روسيا","czech|التشيك","slovakia|سلوفاكيا","hungary|المجر","romania|رومانيا","bulgaria|بلغاريا","greece|اليونان","turkey|تركيا","croatia|كرواتيا","serbia|صربيا","bosnia|البوسنة","slovenia|سلوفينيا","albania|ألبانيا","macedonia|مقدونيا","montenegro|الجبل الأسود","moldova|مولدوفا","belarus|بيلاروسيا","luxembourg|لوكسمبورغ","malta|مالطا","cyprus|قبرص","scotland|اسكتلندا","wales|ويلز","ireland|أيرلندا","georgia|جورجيا","armenia|أرمينيا","azerbaijan|أذربيجان","kazakhstan|كازاخستان","estonia|إستونيا","latvia|لاتفيا","lithuania|ليتوانيا",
"brazil|البرازيل","argentina|الأرجنتين","uruguay|أوروغواي","paraguay|باراغواي","chile|تشيلي","colombia|كولومبيا","peru|بيرو","ecuador|الإكوادور","bolivia|بوليفيا","venezuela|فنزويلا","mexico|المكسيك","usa|أمريكا","canada|كندا","costa_rica|كوستاريكا","honduras|هندوراس","panama|بنما","jamaica|جامايكا","guatemala|غواتيمالا","el_salvador|السلفادور","haiti|هايتي","trinidad|ترينيداد","cuba|كوبا","dominican|الدومينيكان",
"japan|اليابان","korea_s|كوريا الجنوبية","korea_n|كوريا الشمالية","china|الصين","australia|أستراليا","newzealand|نيوزيلندا","iran|إيران","uzbekistan|أوزبكستان","india|الهند","pakistan|باكستان","bangladesh|بنغلادش","thailand|تايلاند","vietnam|فيتنام","indonesia|إندونيسيا","malaysia|ماليزيا","singapore|سنغافورة","philippines|الفلبين","myanmar|ميانمار","nepal|نيبال","srilanka|سريلانكا","afghanistan|أفغانستان","taiwan|تايوان","hongkong|هونغ كونغ","mongolia|منغوليا","cambodia|كمبوديا","laos|لاوس","brunei|بروناي","bhutan|بوتان","maldives|المالديف",
"nigeria|نيجيريا","senegal|السنغال","ghana|غانا","cameroon|الكاميرون","ivory|ساحل العاج","mali|مالي","burkina|بوركينا فاسو","guinea|غينيا","southafrica|جنوب أفريقيا","zambia|زامبيا","zimbabwe|زيمبابوي","kenya|كينيا","uganda|أوغندا","tanzania|تنزانيا","ethiopia|إثيوبيا","angola|أنغولا","mozambique|موزمبيق","namibia|ناميبيا","botswana|بوتسوانا","rwanda|رواندا","congo|الكونغو","drcongo|الكونغو الديمقراطية","gabon|الغابون","benin|بنين","togo|توغو","niger|النيجر","chad|تشاد","southsudan|جنوب السودان","liberia|ليبيريا","sierra|سيراليون","gambia|غامبيا","malawi|مالاوي","lesotho|ليسوتو","eswatini|إسواتيني","madagascar|مدغشقر","mauritius|موريشيوس","seychelles|سيشل","eritrea|إريتريا","central_africa|أفريقيا الوسطى","equatorial|غينيا الاستوائية","burundi|بوروندي"];

var g=document.getElementById('g'),gn=document.getElementById('gN');
NAT.forEach(c=>{var p=c.split('|');gn.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
ALL.forEach(c=>{var p=c.split('|');g.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">...</small></div>';});
var all=[],loaded=0,total=NAT.length+ALL.length;
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit'})}catch(e){return d}}
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=(force||document.querySelector('.f.active').innerText).toLowerCase();
 var code=''; if(f.includes('منتخبات')) code='منتخبات'; else if(f.includes('عرب')) code='عرب'; else if(f.includes('سوريا')||f=='syria') code='syria'; else if(f.includes('العالم')||f=='world') code='world'; else if(f.includes('آسيا')||f=='asia') code='asia';
 var filtered=all.filter(m=>{var mq=!q||m.home.toLowerCase().includes(q)||m.league.toLowerCase().includes(q); var mf=true; if(code=='منتخبات') mf=m.type=='nat'; else if(code=='عرب') mf=['syria','saudi','egypt','algeria','morocco','tunisia','iraq','jordan','lebanon','palestine','uae','qatar','kuwait','bahrain','oman','yemen','sudan','libya','mauritania','somalia'].includes(m.code); else if(code) mf=m.code==code||m.league.toLowerCase().includes(code); return mq&&mf;});
 document.getElementById('m').innerHTML=filtered.slice(0,500).map(m=>{
  var pr1=50+Math.floor(Math.random()*30),pr2=100-pr1, isNat=m.type=='nat';
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
  document.getElementById('s').innerText='✅ '+loaded+'/'+total+' - '+all.length+' مباراة - V53 WORLD 200';
  if(box) box.className='box ok'; if(st) st.innerText=d.up.length+' ✅'; doFilter();
 }).catch(()=>{loaded++;doFilter();});
}
var queue=[...NAT.map(c=>({code:c.split('|')[0],type:'nat'})),...ALL.map(c=>({code:c.split('|')[0],type:'club'}))],idx=0;
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
    if t=='nat':
        mp={"world_cup":[("البرازيل","الأرجنتين"),("فرنسا","إسبانيا"),("إنجلترا","ألمانيا"),("البرتغال","هولندا")],
        "asia_cup":[("السعودية","اليابان"),("إيران","كوريا"),("قطر","أستراليا"),("سوريا","العراق"),("الأردن","أوزبكستان")],
        "africa_cup":[("المغرب","السنغال"),("مصر","نيجيريا"),("الجزائر","تونس"),("الكاميرون","غانا")],
        "euro":[("فرنسا","إنجلترا"),("إسبانيا","ألمانيا"),("البرتغال","إيطاليا")],
        "copa_america":[("البرازيل","الأرجنتين"),("أوروغواي","كولومبيا")],
        "arab_cup":[("المغرب","الجزائر"),("مصر","السعودية"),("تونس","العراق"),("سوريا","الأردن")],
        "olympic":[("فرنسا","إسبانيا"),("المغرب","مصر")],
        "nations":[("إسبانيا","فرنسا"),("ألمانيا","البرتغال")],
        "gulf_cup":[("السعودية","العراق"),("قطر","الإمارات"),("عمان","الكويت"),("البحرين","اليمن")],
        "asian_games":[("اليابان","كوريا"),("السعودية","إيران")],
        "african_nations":[("المغرب","السنغال"),("مصر","الجزائر")],
        "u21_euro":[("إنجلترا","إسبانيا"),("ألمانيا","فرنسا")]}
        teams=mp.get(code,[(code+" A",code+" B")])
        return jsonify({"up":[{"home":h,"away":a,"league":f"{code} - منتخبات - {h} vs {a}","date":(b+datetime.timedelta(days=2,hours=19)).isoformat()} for h,a in teams]})
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
