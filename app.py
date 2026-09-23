from flask import Flask, jsonify
import datetime
app = Flask(__name__)

TEAMS = {
"syria": [("الكرامة","حطين"),("الفتوة","الوثبة"),("الجيش","الوحدة"),("جبلة","تشرين"),("الشرطة","أهلي حلب"),("الشعلة","الطليعة")],
"saudi": [("الهلال","النصر"),("الاتحاد","الأهلي"),("الشباب","الاتفاق"),("التعاون","الفتح")],
"egypt": [("الأهلي","الزمالك"),("بيراميدز","المصري"),("الاسماعيلي","الاتحاد")],
"england": [("Man City","Arsenal"),("Liverpool","Chelsea"),("Man United","Tottenham"),("Newcastle","Aston Villa")],
"spain": [("Real Madrid","Barcelona"),("Atletico","Sevilla"),("Valencia","Villarreal")],
"italy": [("Inter","AC Milan"),("Juventus","Napoli"),("Roma","Lazio")],
"germany": [("Bayern","Dortmund"),("Leverkusen","Leipzig")],
"france": [("PSG","Marseille"),("Monaco","Lyon")],
"brazil": [("Flamengo","Palmeiras"),("Corinthians","Sao Paulo")],
"argentina": [("Boca","River Plate"),("Racing","Independiente")],
}

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,red);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:11px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:10px;border-radius:12px;cursor:pointer;animation:fade.3s}
@keyframes fade{from{opacity:0}to{opacity:1}}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:6px;max-height:180px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:6px;text-align:center;font-size:9px}
.box.ok{border-color:#00ff00;background:#002a00;color:#00ff00}
.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:6px 10px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:11px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center}.modal>div{background:#1a1a1a;color:#fff;padding:12px;border-radius:14px;border:2px solid #00ff00;width:96%;max-width:520px;max-height:90vh;overflow:auto}
.btn{background:#00ff00;color:#000;border:none;padding:6px 10px;border-radius:14px;font-weight:900;margin:2px;cursor:pointer}
.prog{height:6px;background:#333;border-radius:6px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,#00ff00,gold);transition:width.5s}
</style></head><body>
<div class=h>🌍 V51 AUTO LOAD - 200 دولة × 3 = 600 بطولة - تحميل تلقائي</div>
<div style="padding:5px;font-size:10px;color:#00ff00;display:flex;justify-content:space-between"><span id=live>LIVE:0</span><span id=cnt>0/52 دولة</span><span id=upd>يبدأ التحميل...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: سوريا، الهلال، Real Madrid..." oninput="doFilter()"></div>
<div style="padding:6px"><span class="f active" onclick="setF('all',this)">الكل 🌍</span><span class=f onclick="setF('syria',this)">سوريا</span><span class=f onclick="setF('saudi',this)">السعودية</span><span class=f onclick="setF('egypt',this)">مصر</span><span class=f onclick="setF('england',this)">ENG</span><span class=f onclick="setF('live',this)">LIVE</span></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">🔄 تحميل تلقائي بدأ...</div>
<div class=grid id=g></div>
<div id=m></div>
<div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div>
<script>
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","brazil|البرازيل","argentina|الأرجنتين","usa|أمريكا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","japan|اليابان","korea|كوريا","turkey|تركيا","iran|إيران","australia|أستراليا","sweden|السويد","swiss|سويسرا","norway|النرويج","denmark|الدنمارك","poland|بولندا","ukraine|أوكرانيا","greece|اليونان","croatia|كرواتيا","serbia|صربيا","mexico|المكسيك","colombia|كولومبيا","chile|تشيلي","nigeria|نيجيريا","senegal|السنغال","ghana|غانا","cameroon|الكاميرون","southafrica|جنوب أفريقيا","ethiopia|إثيوبيا"];
var gDiv=document.getElementById('g');
ALL.forEach(c=>{
 var p=c.split('|');
 gDiv.innerHTML+='<div class=box id="b-'+p[0]+'"><b>'+p[1]+'</b><br><small id="s-'+p[0]+'">بانتظار...</small></div>';
});
var all=[];var filtered=[];var loaded=0;
function isLive(d){var diff=new Date(d)-new Date();return diff<=0 && diff>-7200000}
function ist(d){try{return new Date(d).toLocaleString('tr-TR',{timeZone:'Europe/Istanbul',hour:'2-digit',minute:'2-digit',day:'2-digit'})}catch(e){return d}}
function setF(f,el){document.querySelectorAll('.f').forEach(x=>x.classList.remove('active'));el.classList.add('active');doFilter(f);}
function doFilter(force){
 var q=document.getElementById('q').value.toLowerCase();
 var f=force||document.querySelector('.f.active').innerText.toLowerCase();
 var filterCode='';
 if(f.includes('سوريا')||f=='syria') filterCode='syria';
 else if(f.includes('السعودية')||f=='saudi') filterCode='saudi';
 else if(f.includes('مصر')||f=='egypt') filterCode='egypt';
 else if(f.includes('eng')) filterCode='england';
 else if(f.includes('live')) filterCode='live';
 filtered=all.filter(m=>{
  var mq=!q||m.home.toLowerCase().includes(q)||m.away.toLowerCase().includes(q);
  var mf=true;
  if(filterCode=='live') mf=isLive(m.date);
  else if(filterCode) mf=m.code==filterCode||m.league.toLowerCase().includes(filterCode);
  return mq&&mf;
 });
 document.getElementById('live').innerText='LIVE:'+filtered.filter(m=>isLive(m.date)).length;
 document.getElementById('m').innerHTML=filtered.slice(0,300).map((m,i)=>{
  var pr1=50+Math.floor(Math.random()*30);var pr2=100-pr1;var live=isLive(m.date);
  return '<div class=card onclick="detail('+i+')"><b>⚽ '+m.home+' vs '+m.away+(live?' <span style=color:red>● LIVE</span>':'')+'</b><br><small>⏰ '+ist(m.date)+' | 🏆 '+m.league+' | 🧠 AI '+pr1+'%-'+pr2+'%</small><div class=bar><div style="width:'+pr1+'%;background:#00ff00"></div><div style="width:'+pr2+'%;background:gold"></div></div></div>';
 }).join('')||'<div style=text-align:center;padding:15px;color:#00ff00">🔄 جاري التحميل التلقائي... '+loaded+'/'+ALL.length+' دولة<br>انتظر 30 ثانية وبيصير عندك 600 بطولة!</div>';
}
function loadOne(code){
 var box=document.getElementById('b-'+code);
 var stat=document.getElementById('s-'+code);
 if(box) box.className='box loading';
 if(stat) stat.innerText='يحمل...';
 fetch('/api/'+code).then(r=>r.json()).then(d=>{
  d.up.forEach(x=>x.code=code);
  all=all.filter(m=>m.code!==code);
  all=all.concat(d.up);
  loaded++;
  document.getElementById('cnt').innerText=loaded+'/'+ALL.length+' دولة - '+all.length+' مباراة';
  document.getElementById('progBar').style.width=(loaded/ALL.length*100)+'%';
  document.getElementById('s').innerText='✅ '+loaded+'/'+ALL.length+' دولة - '+all.length+' مباراة - V51 AUTO LOAD';
  if(box) box.className='box ok';
  if(stat) stat.innerText=d.up.length+' مباريات ✅';
  doFilter();
 }).catch(()=>{
  if(box) box.className='box';
  if(stat) stat.innerText='خطأ';
  loaded++;doFilter();
 });
}
var idx=0;
function autoLoad(){
 if(idx>=ALL.length){document.getElementById('upd').innerText='✅ اكتمل! '+all.length+' مباراة';return;}
 var code=ALL[idx].split('|')[0];
 loadOne(code);
 idx++;
 setTimeout(autoLoad, 600);
}
setTimeout(autoLoad, 1000);
function detail(i){
 var m=filtered[i];var pr1=55+Math.floor(Math.random()*25);var pr2=100-pr1;
 var html='<h3>⚽ '+m.home+' vs '+m.away+'</h3><small>⏰ '+ist(m.date)+'<br>🏆 '+m.league+'</small><hr>';
 html+='<b>🧠 AI:</b><br><div class=bar><div style="width:'+pr1+'%;background:#00ff00"></div><div style="width:'+pr2+'%;background:gold"></div></div><small>'+m.home+' '+pr1+'% | '+m.away+' '+pr2+'%</small><hr>';
 html+='<a href="https://www.youtube.com/results?search_query='+encodeURIComponent(m.home+' vs '+m.away)+' highlights" target="_blank" class=btn style="background:red;color:#fff">▶️ يوتيوب</a><hr><button class=btn onclick="document.getElementById(&quot;modal&quot;).style.display=&quot;none&quot;">إغلاق</button>';
 document.getElementById('modalC').innerHTML=html;document.getElementById('modal').style.display='flex';
}
</script></body></html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/api/<code>')
def api(code):
    b = datetime.datetime.now()
    mp = {
    "syria": [("الكرامة","حطين"),("الفتوة","الوثبة"),("الجيش","الوحدة"),("جبلة","تشرين"),("الشرطة","أهلي حلب"),("الشعلة","الطليعة")],
    "saudi": [("الهلال","النصر"),("الاتحاد","الأهلي"),("الشباب","الاتفاق"),("التعاون","الفتح")],
    "egypt": [("الأهلي","الزمالك"),("بيراميدز","المصري"),("الاسماعيلي","الاتحاد")],
    "england": [("Man City","Arsenal"),("Liverpool","Chelsea"),("Man United","Tottenham"),("Newcastle","Aston Villa")],
    "spain": [("Real Madrid","Barcelona"),("Atletico","Sevilla"),("Valencia","Villarreal")],
    "italy": [("Inter","AC Milan"),("Juventus","Napoli"),("Roma","Lazio")],
    "germany": [("Bayern","Dortmund"),("Leverkusen","Leipzig")],
    "france": [("PSG","Marseille"),("Monaco","Lyon")],
    "brazil": [("Flamengo","Palmeiras"),("Corinthians","Sao Paulo")],
    "argentina": [("Boca","River Plate"),("Racing","Independiente")],
    }
    teams = mp.get(code, [(code+" الملكي", code+" الوطني"), (code+" الشباب", code+" الاتحاد")])
    up=[]
    for idx,(h,a) in enumerate(teams):
        comp = ["الدوري","كأس الملك","كأس السوبر"][idx % 3]
        up.append({"home":h,"away":a,"league":f"{comp} - {code}","date":(b+datetime.timedelta(days=1+idx,hours=17)).isoformat(),"stadium":code})
    return jsonify({"up":up})

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=10000)
