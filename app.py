from flask import Flask, jsonify
import datetime
app=Flask(__name__)
H="""
<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>💎 V58 DIAMOND WORLD 200 - أكبر موقع بالعالم</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,#fff,gold,#fff,#00aaff,#fff);color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:11px;border-bottom:3px solid gold}
.card{background:linear-gradient(135deg,#1a1a1a,#0a0a0a);border-right:5px solid gold;margin:8px;padding:12px;border-radius:16px;box-shadow:0 0 15px rgba(255,215,0,0.2);border:1px solid #333}
.card.nat{border-right-color:gold;background:linear-gradient(135deg,#1a1a00,#0a0a00)}.card.champ{border-right-color:#00aaff;background:linear-gradient(135deg,#001a2a,#000a1a);border:1px solid #00aaff}
.grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:5px;padding:6px;max-height:220px;overflow:auto}
.box{background:#111;border:1px solid #333;border-radius:10px;padding:6px;text-align:center;font-size:8px;transition:0.3s}
.box.ok{border-color:gold;background:#1a1500;box-shadow:0 0 8px gold}.box.ok2{border-color:gold;background:#2a2a00}.box.ok3{border-color:#00aaff;background:#001a2a;box-shadow:0 0 8px #00aaff}.box.loading{border-color:#fff;background:#222;animation:pulse 1s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}
.bar{height:10px;background:#222;border-radius:10px;display:flex;margin:6px 0;overflow:hidden;border:1px solid #333}.bar div{height:100%;transition:width 1s}
.f{padding:6px 12px;border-radius:20px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:gold;color:#000;font-weight:900;box-shadow:0 0 10px gold}
.search{margin:8px;background:#111;border:2px solid gold;border-radius:25px;padding:10px 15px;display:flex;box-shadow:0 0 10px rgba(255,215,0,0.3)}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none;font-size:12px}
.prog{height:10px;background:#222;border-radius:10px;margin:8px;overflow:hidden;border:1px solid #333}.prog div{height:100%;background:linear-gradient(90deg,gold,#fff,gold,#00aaff,#fff);transition:width.5s}
.sec{padding:8px 12px;font-weight:900;border-bottom:2px solid gold;margin-top:10px;font-size:12px;background:#111}
.btn{padding:5px 10px;border-radius:12px;border:none;margin:3px;font-size:9px;cursor:pointer;font-weight:700}
.btn-yt{background:red;color:#fff}.btn-ai{background:linear-gradient(90deg,gold,#00aaff);color:#000}
.count{font-size:10px;color:#00ff00;background:#002a00;padding:3px 8px;border-radius:10px;border:1px solid #00ff00;display:inline-block;margin:3px}
</style></head><body>
<div class=h>💎 V58 DIAMOND - 200 دولة + 12 منتخب + 10 أبطال = 222 بطولة - ESPN العرب - الماسي!</div>
<div style="padding:6px;font-size:11px;color:gold;display:flex;justify-content:space-between"><span id=cnt>0/222 💎</span><span id=upd>💎 الماسي يبدأ...</span></div>
<div class=prog><div id=progBar style="width:0%"></div></div>
<div class=search><input id=q placeholder="🔍 ابحث: سوريا 🇸🇾، فلسطين 🇵🇸، الهلال، Real Madrid، كأس العالم..." oninput=doFilter()></div>
<div style="padding:8px;white-space:nowrap;overflow:auto;text-align:center"><span class="f active" onclick="setF('all',this)">الكل 222 💎</span><span class=f onclick="setF('champ',this)">🏆 أبطال</span><span class=f onclick="setF('منتخبات',this)">🌍 منتخبات</span><span class=f onclick="setF('عرب',this)">🇸🇦 عرب 23</span><span class=f onclick="setF('live',this)">🔴 LIVE</span></div>
<div id=s style="text-align:center;color:#000;padding:10px;background:linear-gradient(90deg,gold,#fff,gold);margin:6px;border-radius:12px;font-size:13px;font-weight:900;border:2px solid #fff">💎 V58 DIAMOND - 222 بطولة - الماسي يحمل...</div>
<div class=sec style="color:#00aaff">🏆 أبطال - 10 - Real Madrid vs Man City</div><div class=grid id=gC></div>
<div class=sec style="color:gold">🌍 منتخبات - 12 - كأس العالم + كأس آسيا + كأس العرب + كأس الخليج</div><div class=grid id=gN></div>
<div class=sec style="color:#fff">🌍 أندية - 200 دولة - من 🇵🇸 فلسطين ل 🇸🇾 سوريا لأمريكا 🇺🇸 - DIAMOND</div><div class=grid id=g></div>
<div id=m></div>
<script>
var CHAMP=["ucl|أبطال أوروبا","uel|الدوري الأوروبي","afc_cl|أبطال آسيا","afc2|أبطال آسيا 2","caf_cl|أبطال أفريقيا","caf_conf|الكونفدرالية","arab_cl|أبطال العرب","gulf_cl|أبطال الخليج","club_world|كأس العالم أندية","libertadores|ليبرتادوريس"];
var NAT=["world_cup|كأس العالم","asia_cup|كأس آسيا","africa_cup|كأس أفريقيا","euro|يورو","copa_america|كوبا أمريكا","arab_cup|كأس العرب","olympic|الأولمبياد","nations|دوري الأمم","gulf_cup|كأس الخليج","u21_euro|تحت 21","asian_games|الألعاب الآسيوية","african_ch|أفريقيا محليين"];
var ALL=["syria|سوريا 🇸🇾","saudi|السعودية 🇸🇦","egypt|مصر 🇪🇬","algeria|الجزائر 🇩🇿","morocco|المغرب 🇲🇦","tunisia|تونس 🇹🇳","libya|ليبيا 🇱🇾","sudan|السودان 🇸🇩","yemen|اليمن 🇾🇪","jordan|الأردن 🇯🇴","le
