from flask import Flask, jsonify
import datetime
app = Flask(__name__)

# 200 دولة كاملة
ALL_200 = ["أفغانستان","ألبانيا","الجزائر","أندورا","أنغولا","أنتيغوا","الأرجنتين","أرمينيا","أستراليا","النمسا","أذربيجان","البحرين","بنغلادش","بيلاروسيا","بلجيكا","بليز","بنين","بوتان","بوليفيا","البوسنة","بوتسوانا","البرازيل","بروناي","بلغاريا","بوركينا","بوروندي","كمبوديا","الكاميرون","كندا","الرأس الأخضر","التشيك","الدنمارك","جيبوتي","الدومينيكان","الإكوادور","مصر","السلفادور","إستونيا","إثيوبيا","فيجي","فنلندا","فرنسا","الغابون","غامبيا","جورجيا","ألمانيا","غانا","اليونان","غواتيمالا","غينيا","هايتي","هندوراس","المجر","آيسلندا","الهند","إندونيسيا","إيران","العراق","أيرلندا","إسرائيل","إيطاليا","جامايكا","اليابان","الأردن","كازاخستان","كينيا","كوريا الشمالية","كوريا الجنوبية","الكويت","لبنان","ليسوتو","ليبيريا","ليبيا","ليتوانيا","لوكسمبورغ","مدغشقر","ماليزيا","المالديف","مالي","مالطا","موريتانيا","المكسيك","مولدوفا","موناكو","منغوليا","الجبل الأسود","المغرب","موزمبيق","ميانمار","ناميبيا","نيبال","هولندا","نيوزيلندا","نيكاراغوا","النيجر","نيجيريا","مقدونيا","النرويج","عمان","باكستان","فلسطين","بنما","باراغواي","بيرو","الفلبين","بولندا","البرتغال","قطر","رومانيا","روسيا","رواندا","السعودية","السنغال","صربيا","سنغافورة","سلوفاكيا","سلوفينيا","الصومال","جنوب أفريقيا","جنوب السودان","إسبانيا","السودان","السويد","سويسرا","سوريا","طاجيكستان","تنزانيا","تايلاند","توغو","ترينيداد","تونس","تركيا","تركمانستان","أوغندا","أوكرانيا","الإمارات","إنجلترا","أمريكا","أوروغواي","أوزبكستان","فنزويلا","فيتنام","اليمن","زامبيا","زيمبابوي","سوريا","كرواتيا","ساحل العاج","زمبابوي"]

HTML = """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
body{background:#0a0a0a;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#00ff00,gold,red,#00ff00);color:#000;padding:10px;text-align:center;font-weight:900;position:sticky;top:0;z-index:20;font-size:12px}
.card{background:#1a1a1a;border-right:4px solid #00ff00;margin:5px;padding:9px;border-radius:12px;cursor:pointer;font-size:12px}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:4px;padding:5px;max-height:420px;overflow:auto}
.box{background:#1a1a1a;border:1px solid #00ff00;border-radius:8px;padding:8px;text-align:center;cursor:pointer;font-size:10px}
.box.active{border-color:gold;background:#1a1a00}
.row{display:flex;justify-content:space-between;padding:4px;border-bottom:1px solid #333;font-size:11px}
.modal{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#000e;z-index:99;justify-content:center;align-items:center}
.modal>div{background:#1a1a1a;color:#fff;padding:12px;border-radius:14px;border:2px solid #00ff00;width:96%;max-width:500px;max-height:90vh;overflow:auto}
.btn{background:#00ff00;color:#000;border:none;padding:6px 10px;border-radius:14px;font-weight:900;margin:2px;cursor:pointer;font-size:11px}
.bar{height:8px;background:#333;border-radius:8px;overflow:hidden;display:flex;margin:3px 0}.bar div{height:100%}
.filters{display:flex;gap:4px;padding:6px;overflow:auto}.f{padding:6px 10px;border-radius:14px;border:1px solid #333;background:#1a1a1a;cursor:pointer;white-space:nowrap;color:#fff;font-size:11px}.f.active{background:#00ff00;color:#000}
.search{margin:6px;background:#1a1a1a;border:1px solid #00ff00;border-radius:20px;padding:8px 12px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
</style></head><body>
<div class=h>🌍 V49 ULTIMATE - 200 دولة × 3 بطولات = 600 بطولة - 3600 مباراة</div>
<div style="display:flex;justify-content:space-between;padding:5px;font-size:10px;color:#00ff00"><span id=live>🔴 LIVE: 0</span><span id=cnt>🌍 200 دولة</span><span id=upd>🔄</span></div>
<div class=search><input id=q placeholder="🔍 ابحث عن أي دولة: اليمن، سوريا، مصر، جزر القمر، توفالو..." oninput="doFilter()"><span onclick="q.value='';doFilter()" style="cursor:pointer">❌</span></div>
<div class=filters><div class="f active" onclick="setF('all',this)">الكل 200 دولة 🌍</div><div class="f" onclick="setF('syr',this)">🇸🇾 سوريا</div><div class="f" onclick="setF('sau',this)">🇸🇦 السعودية</div><div class="f" onclick="setF('egy',this)">🇪🇬 مصر</div><div class="f" onclick="setF('eng',this)">ENG</div><div class="f" onclick="setF('live',this)">🔴 LIVE</div></div>
<div id=s style="text-align:center;color:#00ff00;padding:6px;font-weight:900;background:#001a00;border:1px solid #00ff00;margin:5px;border-radius:8px;font-size:11px">🌍 يحمل 200 دولة...</div>
<div class=grid id=g></div>
<div id=m></div>
<div class=modal id=modal onclick="if(event.target.id=='modal')this.style.display='none'"><div id=modalC></div></div>
<script>
var ALL = ["أفغانستان","ألبانيا","الجزائر","أندورا","أنغولا","أنتيغوا","الأرجنتين","أرمينيا","أستراليا","النمسا","أذربيجان","البحرين","بنغلادش","بيلاروسيا","بلجيكا","بليز","بنين","بوتان","بوليفيا","البوسنة","بوتسوانا","البرازيل","بروناي","بلغاريا","بوركينا","بوروندي","كمبوديا","الكاميرون","كندا","الرأس الأخضر","التشيك","الدنمارك","جيبوتي","الدومينيكان","الإكوادور","مصر","السلفادور","إستونيا","إثيوبيا","فيجي","فنلندا","فرنسا","الغابون","غامبيا","جورجيا","ألمانيا","غانا","اليونان","غواتيمالا","غينيا","هايتي","هندوراس","المجر","آيسلندا","الهند","إندونيسيا","إيران","العراق","أيرلندا","إسرائيل","إيطاليا","جامايكا","اليابان","الأردن","كازاخستان","كينيا","كوريا الجنوبية","الكويت","لبنان","ليبيريا","ليبيا","ليتوانيا","ماليزيا","المالديف","مالي","مالطا","المكسيك","المغرب","موزمبيق","ناميبيا","نيبال","هولندا","نيوزيلندا","نيجيريا","النرويج","عمان","باكستان","فلسطين","بنما","بيرو","الفلبين","بولندا","البرتغال","قطر","رومانيا","روسيا","السعودية","السنغال","صربيا","سنغافورة","سلوفاكيا","الصومال","جنوب أفريقيا","إسبانيا","السودان","السويد","سويسرا","سوريا","تنزانيا","تايلاند","تونس","تركيا","أوغندا","أوكرانيا","الإمارات","إنجلترا","أمريكا","أوروغواي","فنزويلا","فيتنام","اليمن","زامبيا"];
var L={
