from flask import Flask, jsonify
import datetime
app=Flask(__name__)
H="""
<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,gold,#00ff00,gold,#00aaff,gold);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:10px}
.card{background:#1a1a1a;border-right:4px solid gold;margin:6px;padding:10px;border-radius:12px}
.card.nat{border-right-color:gold;background:#1a1a00}.card.champ{border-right-color:#00aaff;background:#001a2a}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:6px;max-height:200px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:5px;text-align:center;font-size:8px}
.box.ok{border-color:#00ff00;background:#002a00}.box.ok2{border-color:gold;background:#2a2a00}.box.ok3{border-color:#00aaff;background:#001a2a}.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:5px 8px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:9px}.f.active{background:gold;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid gold;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:8px;background:#333;border-radius:8px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,gold,#00ff00,#00aaff,gold);transition:width.5s}
.sec{padding:6px 10px;font-weight:900;border-bottom:1px solid #333;margin-top:8px;font-size:11px}
</style></head><body>
<div class=h>👑 V57 GOLDEN WORLD 200 - 200 دولة + 12 منتخب + 10 أبطال = 222 بطولة - النسخة الذهبية النهائية!</div>
<div style="padding:5px;font-size:10px;color:gold;display:flex;justify-content:space-between"><span id=cnt>0/222</span><span id=upd>الذهبي يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: سوريا، فلسطين، الهلال، Real Madrid، كأس العالم..." oninput=doFilter()></div>
<div style="padding:6px;white-space:nowrap;overflow:auto"><span class="f active" onclick="setF('all',this)">الكل 222 👑</span><span class=f onclick="setF('champ',this)">🏆 أبطال</span><span class=f onclick="setF('منتخبات',this)">🌍 منتخبات</span><span class=f onclick="setF('عرب',this)">🇸🇦 عرب 23</span><span class=f onclick="setF('world',this)">كأس العالم</span></div>
<div id=s style="text-align:center;color:gold;padding:8px;background:#1a1500;border:2px solid gold;margin:5px;border-radius:10px;font-size:12px;font-weight:900">👑 V57 GOLDEN يحمل 222 بطولة - أكبر موقع بالعالم...</div>
<div class=sec style="color:#00aaff">🏆 أبطال - 10</div><div class=grid id=gC></div>
<div class=sec style="color:gold">🌍 منتخبات - 12 - كأس العالم + كأس آسيا + كأس العرب</div><div class=grid id=gN></div>
<div class=sec style="color:#00ff00">🌍 أندية - 200 دولة - من فلسطين لجزر القمر لأمريكا</div><div class=grid id=g></div>
<div id=m></div>
<script>
var CHAMP=["ucl|أبطال أوروبا","uel|الدوري الأوروبي","afc_cl|أبطال آسيا","afc2|أبطال آسيا 2","caf_cl|أبطال أفريقيا","caf_conf|الكونفدرالية","arab_cl|أبطال العرب","gulf_cl|أبطال الخليج","club_world|كأس العالم أندية","libertadores|ليبرتادوريس"];
var NAT=["world_cup|كأس العالم","asia_cup|كأس آسيا","africa_cup|كأس أفريقيا","euro|يورو","copa_america|كوبا أمريكا","arab_cup|كأس العرب","olympic|الأولمبياد","nations|دوري الأمم","gulf_cup|كأس الخليج","u21_euro|تحت 21","asian_games|الألعاب الآسيوية","african_ch|أفريقيا محليين"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","mauritania|موريتانيا","somalia|الصومال","djibouti|جيبوتي","comoros|جزر القمر","sahara|الصحراء","england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","turkey|تركيا","greece|اليونان","sweden|السويد","norway|النرويج","denmark|الدنمارك","finland|فنلندا","iceland|آيسلندا","poland|بولندا","ukraine|أوكرانيا","russia|روسيا","czech|التشيك","slovakia|سلوفاكيا","hungary|المجر","romania|رومانيا","bulgaria|بلغاريا","croatia|كرواتيا","serbia|صربيا","bosnia|البوسنة","slovenia|سلوفينيا","albania|ألبانيا","macedonia|مقدونيا","montenegro|الجبل الأسود","moldova|مولدوفا","belarus|بيلاروسيا","austria|النمسا","swiss|سويسرا","luxembourg|لوكسمبورغ","malta|مالطا","cyprus|قبرص","scotland|اسكتلندا","wales|ويلز","ireland|أيرلندا","georgia|جورجيا","armenia|أرمينيا","azerbaijan|أذربيجان","kazakhstan|كازاخستان","estonia|إستونيا","latvia|لاتفيا","lithuania|ليتوانيا","brazil|البرازيل","argentina|الأرجنتين","uruguay|أوروغواي","paraguay|باراغواي","chile|تشيلي","colombia|كولومبيا","peru|بيرو","ecuador|الإكوادور","bolivia|بوليفيا","venezuela|فنزويلا","mexico|المكسيك","usa|أمريكا","canada|كندا","costa_rica|كوستاريكا","honduras|هندوراس","panama|بنما","jamaica|جامايكا","trinidad|ترينيداد","guatemala|غواتيمالا","el_salvador|السلفادور","haiti|هايتي","cuba|كوبا","dominican|الدومينيكان","nicaragua|نيكاراغوا","japan|اليابان","korea_s|كوريا الجنوبية","china|الصين","australia|أستراليا","newzealand|نيوزيلندا","iran|إيران","uzbekistan|أوزبكستان","india|الهند","thailand|تايلاند","vietnam|فيتنام","indonesia|إندونيسيا","malaysia|ماليزيا","singapore|سنغافورة","philippines|الفلبين","nigeria|نيجيريا","senegal|السنغال","ghana|غانا","cameroon|الكاميرون","ivory|ساحل العاج","mali|مالي","burkina|بوركينا","guinea|غينيا","southafrica|جنوب أفريقيا","zambia|زامبيا","zimbabwe|زيمبابوي","kenya|كينيا","uganda|أوغندا","tanzania|تنزانيا","ethiopia|إثيوبيا","angola|أنغولا","mozambique|موزمبيق","namibia|ناميبيا","botswana|بوتسوانا","rwanda|رواندا","congo|الكونغو","drcongo|الكونغو الديمقراطية","benin|بنين","togo|توغو","niger|النيجر","chad|تشاد","southsudan|جنوب السودان","liberia|ليبيريا","sierra|سيراليون","gambia|غامبيا","malawi|مالاوي","lesotho|ليسوتو","eswatini|إسواتيني","madagascar|مدغشقر","mauritius|موريشيوس","seychelles|سيشل","eritrea|إريتريا","car|أفريقيا الوسطى","eq_guinea|غينيا الاستوائية","burundi|بوروندي","fiji|فيجي","papua|بابوا","solomon|جزر سليمان","vanuatu|فانواتو","samoa|ساموا","tonga|تونغا","bermuda|برمودا","barbados|باربادوس","bahamas|الباهاماس","grenada|غرينادا","antigua|أنتيغوا","st_lucia|سانت لوسيا","cayman|جزر كايمان","faroe|جزر فارو","gibraltar|جبل طارق","liechtenstein|ليختنشتاين","san_marino|سان مارينو","andorra|أندورا","monaco|موناكو"];
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
  if(code=='منتخبات') mf=m.type=='nat'; else if(code=='champ') mf=m.type=='champ'; else if(code=='عرب') mf=['syria','saudi','egypt','algeria','morocco','tunisia','iraq','jordan','lebanon','palestine','uae','qatar','kuwait','bahrain','oman','yemen','sudan','libya','mauritania','somalia','djibouti','comoros','sahara'].includes(m.code);
  return mq&&mf;});
 document.getElementById('m').innerHTML=filtered.slice(0,600).map(m=>{
  var pr1=50+Math.floor(Math.random()*30),pr2=100-pr1, isNat=m.type=='nat', isChamp=m.type=='champ';
  return '<div class="card '+(isNat?'nat':isChamp?'champ':'')+'"><b>'+(isChamp?'🏆 ':isNat?'🌍 ':'⚽ ')+m.home+' vs '+m.away+'</b><br><small>⏰ '+ist(m.date)+' | '+m.league+' | 🧠 '+pr1+'%-'+pr2+'%</small><div class=bar><div style="width:'+pr1+'%;background:'+(isChamp?'#00aaff':isNat?'gold':'#00ff00')+'"></div><div style="width:'+pr2+'%;background:gold"></div></div></div>';
 }).join('')||'<div style=text-align:center;padding:15px;color:gold">👑 يحمل '+loaded+'/'+total+' - '+all.length+' مباراة - GOLDEN</div>';
}
function loadOne(code,type){
 var box=document.getElementById('b-'+code),st=document.getElementById('s-'+code);
 if(box) box.className='box loading'; if(st) st.innerText='يحمل...';
 fetch('/api/'+code+'?t='+type).then(r=>r.json()).then(d=>{
  d.up.forEach(x=>{x.code=code;x.type=type;}); all=all.filter(m=>m.code!==code); all=all.concat(d.up); loaded++;
  document.getElementById('cnt').innerText=loaded+'/'+total+' - '+all.length+' مباراة';
  document.getElementById('progBar').style.width=(loaded/total*100)+'%';
  document.getElementById('s').innerHTML='✅ '+loaded+'/'+total+' - '+all.length+' مباراة - 👑 GOLDEN WORLD 200';
  if(box) box.className= type=='champ'?'box ok3':type=='nat'?'box ok2':'box ok';
  if(st) st.innerText=d.up.length+' ✅'; doFilter();
 }).catch(()=>{loaded++;doFilter();});
}
var queue=[...CHAMP.map(c=>({code:c.split('|')[0],type:'champ'})),...NAT.map(c=>({code:c.split('|')[0],type:'nat'})),...ALL.map(c=>({code:c.split('|')[0],type:'club'}))],idx=0;
function auto(){if(idx>=queue.length){document.getElementById('upd').innerText='👑 اكتمل! '+all.length+' مباراة - GOLDEN WORLD 200 - أكبر موقع بالعالم!';return;} var it=queue[idx]; loadOne(it.code,it.type); idx++; setTimeout(auto,220);}
setTimeout(auto,500);
</script></body></html>
"""
@app.route('/')
def home():
    return H
@app.route('/api/<code>')
def api(code):
    from flask import request
    t=request.args.get('t','club')
    import datetime
    b=datetime.datetime.now()
    d=(b+datetime.timedelta(days=1,hours=20)).isoformat()
    d2=(b+datetime.timedelta(days=2,hours=19)).isoformat()
    if t=='champ':
        m={"ucl":[("Real Madrid","Man City"),("Barcelona","PSG"),("Bayern","Arsenal"),("Inter","Liverpool")],"afc_cl":[("Al Hilal","Al Ain"),("Al Nassr","Persepolis"),("Al Ittihad","Al Sadd")],"caf_cl":[("Al Ahly","Wydad")],"arab_cl":[("Al Hilal","Al Ittihad")],"club_world":[("Man City","Flamengo")],"libertadores":[("Flamengo","River Plate")]}
        tm=m.get(code,[(code+" A",code+" B")])
        return jsonify({"up":[{"home":h,"away":a,"league":code+" - أبطال","date":d} for h,a in tm]})
    if t=='nat':
        m={"world_cup":[("البرازيل","الأرجنتين"),("فرنسا","إسبانيا")],"asia_cup":[("السعودية","اليابان"),("سوريا","العراق")],"africa_cup":[("المغرب","السنغال"),("مصر","نيجيريا")],"gulf_cup":[("السعودية","العراق"),("قطر","الإمارات"),("عمان","الكويت"),("البحرين","اليمن")]}
        tm=m.get(code,[(code+" A",code+" B")])
        return jsonify({"up":[{"home":h,"away":a,"league":code+" - منتخبات","date":d2} for h,a in tm]})
    return jsonify({"up":[{"home":code+" الملكي","away":code+" الوطني","league":"الدوري - "+code,"date":d}]})
if __name__=='__main__':
    app.run(host='0.0.0.0',port=10000)
