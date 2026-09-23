from flask import Flask, jsonify
import requests, datetime
app = Flask(__name__)

@app.route('/')
def home():
    return """
<html dir="rtl"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>V30 PRO MAX</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#FFD700,#ff8c00);color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:99}
.tabs{display:flex;background:#111;margin:6px;border-radius:12px;border:2px solid #FFD700;overflow:hidden}
.tab{flex:1;padding:8px;text-align:center;cursor:pointer;font-weight:900;font-size:12px}
.active{background:#FFD700;color:#000}
.money{background:#111;border:1px solid #FFD700;padding:8px;border-radius:12px;margin:6px;display:flex;justify-content:space-around;font-size:11px;font-weight:900}
.filters{display:flex;gap:5px;padding:6px;overflow:auto}
.fbtn{background:#222;color:#fff;border:1px solid #555;padding:6px 12px;border-radius:15px;font-size:12px;white-space:nowrap;cursor:pointer}
.fbtnA{background:#FFD700;color:#000;border:0}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:6px;padding:6px}
.box{background:#111;border:1px solid #333;border-radius:10px;padding:10px;text-align:center;cursor:pointer;position:relative}
.has{border-color:#0f0;background:#0a1a0a;box-shadow:0 0 6px #0f05}
.boxActive{border:2px solid #FFD700!important;background:#FFD700!important;color:#000!important}
.zero{opacity:0.4}
.card{background:#151515;border-right:4px solid #FFD700;border-radius:10px;margin:6px;padding:10px;display:flex;align-items:center;gap:8px;font-size:13px;cursor:pointer;position:relative}
.fav-card{border-right-color:#ff0;background:#1a1a00}
.live-card{border-right-color:red;background:#2a0a0a}
.team-logo{width:28px;height:28px;background:#fff;border-radius:50%;padding:2px;object-fit:contain}
.vs{color:#FFD700;font-weight:900}
.search{margin:6px;background:#111;border:1px solid #333;border-radius:8px;padding:8px;display:flex;gap:6px}
.search input{flex:1;background:transparent;border:0;color:#fff;outline:none}
#modal{position:fixed;inset:0;background:rgba(0,0,0,0.92);display:none;align-items:center;justify-content:center;z-index:999;padding:12px}
#modalBox{background:#1a1a1a;border:2px solid #FFD700;border-radius:16px;padding:16px;width:100%;max-width:360px;max-height:85vh;overflow:auto}
.star{position:absolute;top:4px;left:6px;font-size:18px;cursor:pointer;z-index:2}
</style>
</head><body>
<div class="h">Shaam V30 PRO MAX - ⭐ المفضلة + 🔄 تحديث تلقائي</div>
<div class="tabs"><div class="tab active" id="t1" onclick="showTab(1)">مباريات</div><div class="tab" id="t2" onclick="showTab(2)">ترتيب</div><div class="tab" id="t3" onclick="showTab(3)">هدافين</div><div class="tab" id="t4" onclick="showTab(4)">احصائيات</div></div>

<div id="tab1">
<div class="money"><span>Live <span id="lc">0</span></span><span>Up <span id="uc">0</span></span><span>Total <span id="tc">0</span></span><span id="dn">0/18</span><span id="auto" style="color:#0f0">🔄</span></div>
<div class="filters">
<button class="fbtnA fbtn" onclick="filterAll()">الكل</button>
<button class="fbtn" onclick="filterFav()">⭐ مفضلتي</button>
<button class="fbtn" onclick="filterLive()">🔴 Live</button>
<button class="fbtn" onclick="filterLg('eng.1')">ENG</button>
<button class="fbtn" onclick="filterLg('esp.1')">ESP</button>
<button class="fbtn" onclick="filterLg('sau.1')">SAU</button>
<button class="fbtn" onclick="filterLg('uefa.champions')">UCL</button>
<button class="fbtn" onclick="clearFilter()">الغاء</button>
</div>
<div class="search"><span>🔍</span><input id="searchInput" placeholder="ابحث Real, Barca, Hilal..." oninput="doSearch()"></div>
<div id="st" style="text-align:center;color:#FFD700;padding:6px">يحمل 18 دوري...</div>
<div id="favBar" style="display:none;background:#1a1a00;border:1px solid #FFD700;border-radius:10px;margin:6px;padding:8px;text-align:center"><span style="color:#FFD700">⭐ مفضلتك:</span> <span id="favList"></span> <span onclick="clearFav()" style="color:red;cursor:pointer;margin-right:10px">مسح</span></div>
<div class="grid" id="grid"></div>
<div id="matches"></div>
</div>

<div id="tab2" style="display:none;padding:6px"><div style="display:flex;gap:4px;overflow:auto"><button onclick="loadStanding('eng.1')" class="fbtnA fbtn">ENG</button><button onclick="loadStanding('esp.1')" class="fbtn">ESP</button><button onclick="loadStanding('sau.1')" class="fbtn">SAU</button><button onclick="loadStanding('egy.1')" class="fbtn">EGY</button><button onclick="loadStanding('tur.1')" class="fbtn">TUR</button><button onclick="loadStanding('uefa.champions')" class="fbtn">UCL</button></div><div id="standing-box" style="margin-top:8px">اختر دوري...</div></div>

<div id="tab3" style="display:none;padding:6
