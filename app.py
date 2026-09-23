from flask import Flask, jsonify
import datetime
app = Flask(__name__)

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,#00aaff,red);color:#000;padding:9px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:10px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:6px;padding:10px;border-radius:12px}
.card.nat{border-right-color:gold;background:#1a1a00}.card.champ{border-right-color:#00aaff;background:#001a2a}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:6px;max-height:180px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #333;border-radius:8px;padding:5px;text-align:center;font-size:8px}
.box.ok{border-color:#00ff00;background:#002a00}.box.ok2{border-color:gold;background:#2a2a00}.box.ok3{border-color:#00aaff;background:#001a2a}
.box.loading{border-color:gold;background:#1a1a00}
.bar{height:8px;background:#333;border-radius:8px;display:flex;margin:4px 0}.bar div{height:100%}
.f{padding:5px 8px;border-radius:14px;border:1px solid #333;background:#1a1a1a;color:#fff;margin:2px;display:inline-block;cursor:pointer;font-size:9px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:6px;background:#333;border-radius:6px;margin:6px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,#00ff00,gold,#00aaff,red);transition:width.5s}
.sec{padding:6px 10px;font-weight:900;border-bottom:1px solid #333;margin-top:8px;font-size:11px}
</style></head><body>
<div class=h>V56 FINAL WORLD 200 - 156 دولة + 12 منتخب + 10 أبطال = 178 بطولة AUTO</div>
<div style="padding:5px;font-size:10px;color:#00ff00;display:flex;justify-content:space-between"><span id=cnt>0/0</span><span id=upd>يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="ابحث: سوريا، فلسطين، الهلال، Real Madrid..." oninput="doFilter()"></div>
<div style="padding:6px;white-space:nowrap;overflow:auto"><span class="f active" onclick="setF('all',this)">الكل 178</span><span class=f onclick="setF('champ',this)">🏆 أبطال</span><span class=f onclick="setF('منتخبات',this)">🌍 منتخبات</span><span class=f onclick="setF('عرب',this)">🇸🇦 عرب 22</span><span class=f onclick="setF('europe',this)">🇪🇺 أوروبا</span><span class=f onclick="setF('asia',this)">آسيا</span><span class=f onclick="setF('africa',this)">أفريقيا</span></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">V56 FINAL يحمل 178 بطولة...</div>
<div class=sec style="color:#00aaff">🏆 أبطال - 10</div><div class=grid id=gC></div>
<div class=sec style="color:gold">🌍 منتخبات - 12</div><div class=grid id=gN></div>
<div class=sec style="color:#00ff00">🌍 أندية - 156 دولة</div><div class=grid id=g></div>
<div id=m></div>
<script>
var CHAMP=["ucl|أبطال أوروبا","uel|الدوري الأوروبي","afc_cl|أبطال آسيا","afc2|أبطال آسيا 2","caf_cl|أبطال أفريقيا","caf_conf|الكونفدرالية","arab_cl|أبطال العرب","gulf_cl|أبطال الخليج","club_world|كأس العالم أندية","libertadores|ليبرتادوريس"];
var NAT=["world_cup|كأس العالم","asia_cup|كأس آسيا","africa_cup|كأس أفريقيا","euro|يورو","copa_america|كوبا أمريكا","arab_cup|كأس العرب","olympic|الأولمبياد","nations|دوري الأمم","gulf_cup|كأس الخليج","u21_euro|تحت 21","asian_games|الألعاب الآسيوية","african_ch|أفريقيا محليين"];
var ALL=["syria|سوريا","saudi|السعودية","egypt|مصر","algeria|الجزائر","morocco|المغرب","tunisia|تونس","libya|ليبيا","sudan|السودان","yemen|اليمن","jordan|الأردن","lebanon|لبنان","iraq|العراق","palestine|فلسطين","uae|الإمارات","qatar|قطر","kuwait|الكويت","bahrain|البحرين","oman|عمان","mauritania|موريتانيا","somalia|الصومال","djibouti|جيبوتي","comoros|جزر القمر","sahara|الصحراء",
"england|إنجلترا","spain|إسبانيا","italy|إيطاليا","germany|ألمانيا","france|فرنسا","portugal|البرتغال","netherlands|هولندا","belgium|بلجيكا","turkey|تركيا","greece|اليونان","sweden|السويد","norway|النرويج","denmark|الدنمارك","finland|فنلندا","iceland|آيسلندا","poland|بولندا","ukraine|أوكرانيا","russia|روسيا","czech|التشيك","slovakia|سلوفاكيا","hungary|المجر","romania|رومانيا","bulgaria|بلغاريا","croatia|كرواتيا","serbia|صربيا","bosnia|البوسنة","slovenia|سلوفينيا","albania|ألبانيا","macedonia|مقدونيا","montenegro|الجبل الأسود","moldova|مولدوفا","belarus|بيلاروسيا","austria|النمسا","swiss|سويسرا","luxembourg|لوكسمبورغ","malta|مالطا","cyprus|قبرص","scotland|اسكتلندا","wales|ويلز","ireland|أيرلندا","n_ireland|أيرلندا الشمالية","georgia|جورجيا","armenia|أرمينيا","azerbaijan|أذربيجان","kazakhstan|كازاخستان","estonia|إستونيا","latvia|لاتفيا","lithuania|ليتوانيا",
"brazil|البرازيل","argentina|الأرجنتين","uruguay|أوروغواي","paraguay|باراغواي","chile|تشيلي","colombia|كولومبيا","peru|بيرو","ecuador|الإكوادور","bolivia|بوليفيا","venezuela|فنزويلا","mexico|المكسيك","usa|أمريكا","canada|كندا","costa_rica|كوستاريكا","honduras|هندوراس","panama|بنما","jamaica|جامايكا","trinidad|ترينيداد","guatemala|غواتيمالا","el_salvador|السلفادور","haiti|هايتي","cuba|كوبا","dominican|الدومينيكان","nicaragua|نيكاراغوا",
"japan|اليابان","korea_s|كوريا الجنوبية","korea_n|كوريا الشمالية","china|الصين","australia|أستراليا","newzealand|نيوزيلندا","iran|إيران","uzbekistan|أوزبكستان","india|الهند","pakistan|باكستان","bangladesh|بنغلادش","thailand|
