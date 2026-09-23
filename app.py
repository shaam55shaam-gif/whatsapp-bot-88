import requests
from flask import Flask, jsonify
app = Flask(__name__)
HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam V14.1 BEYOND LIGHT 🚀</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:Segoe UI}
body{background:#000;color:#fff}
.header{background:linear-gradient(90deg,#FFD700,#ff9900);padding:14px;text-align:center;position:sticky;top:0;z-index:999}
.nav{display:flex;gap:4px;padding:6px;background:#111;overflow-x:auto;position:sticky;top:56px;z-index:998}
.nav button{background:#222;color:#fff;border:1px solid #444;padding:8px 12px;border-radius:20px;font-size:9px;white-space:nowrap}
.nav button.active{background:#FFD700;color:#000;font-weight:900}
.card{background:#111;border:1px solid #333;border-radius:16px;margin:8px;padding:12px}
.beyond{border:2px solid #FFD700;box-shadow:0 0 20px rgba(255,215,0,.4)}
.live{border-right:5px solid red}
.team{display:flex;justify-content:space-between;margin:8px 0;font-weight:900;font-size:16px}
.score{font-size:32px;color:#FFD700;font-weight:900}
.btn{padding:8px 10px;border-radius:10px;border:none;font-weight:900;font-size:9px;margin:2px;cursor:pointer}
.btn-gold{background:linear-gradient(90deg,#FFD700,#ff9900);color:#000;width:94%;margin:8px 3%;padding:16px;border-radius:30px;font-weight:900;font-size:14px;display:block}
.search{width:94%;margin:8px 3%;padding:12px;border-radius:25px;border:2px solid #FFD700;background:#222;color:#fff;text-align:center}
.money{position:fixed;top:60px;left:4px;right:4px;background:linear-gradient(90deg,#FFD700,#ff9900);color:#000;padding:8px;border-radius:20px;font-weight:900;font-size:10px;z-index:1000;display:flex;justify-content:space-around;text-align:center}
.install{position:fixed;bottom:8px;left:8px;right:8px;background:linear-gradient(90deg,#FFD700,#ff9900);color:#000;padding:14px;border-radius:16px;font-weight:900;text-align:center;z-index:1000}
.modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.95);z-index:5000;align-items:center;justify-content:center;padding:10px}
.modal-box{width:100%;max-width:600px;background:#111;border-radius:16px;padding:14px;border:2px solid #FFD700}
.video{width:100%;height:300px;border-radius:12px;border:none}
</style>
</head>
<body>
<div class="header"><h1 style="color:#000;font-weight:900">🚀 Shaam V14.1 BEYOND LIGHT - خفيف وسريع</h1><div style="color:#000;font-size:10px;font-weight:900">ShaamCoin + NFT + 100K$ + Web3 + بدون Glitch</div></div>
<div class="money"><span>💰 <span id="myMoney">1000</span>$</span><span>🪙 <span id="myCoin">0</span> SMC $<span id="coinPrice">0.42</span></span><span>👑 <span id="myVip">عادي</span></span></div>
<div class="nav">
<button class="active" onclick="showTab('live',this)">🔴 مباشر</button>
<button onclick="showTab('tv',this)">📺 بث 8</button>
<button onclick="showTab('coin',this)">🪙 Coin</button>
<button onclick="showTab('nft',this)">🖼️ NFT</button>
<button onclick="showTab('game',this)">🎮 لعبة</button>
<button onclick="showTab('store',this)">💳 Web3</button>
<button onclick="showTab('ai',this)">🤖 AI</button>
</div>
<input class="search" placeholder="🚀 ابحث... برشلونة، الهلال، ShaamCoin" oninput="filterTeams(this.value)">
<button class="btn-gold" onclick="activateBeyond()">🚀🔔 فعل BEYOND LIGHT: 1000 SMC + 10K$ + VIP + بدون تعليق</button>
<div style="text-align:center;font-size:10px;color:#aaa">آخر: <span id="lastUpdate">--</span> | <span id="count">--</span> | 🪙 $<span id="price2">0.42</span> | خفيف 100%</div>

<div id="live" class="tab"><div id="matches"><div style="text-align:center;padding:40px;color:#FFD700">🚀 V14.1 يحمّل بسرعة الضوء...</div></div></div>
<div id="tv" class="tab" style="display:none"><div class="card beyond"><h3>📺 بث 8 قنوات</h3><iframe id="tvFrame" class="video" src="https://www.youtube.com/embed/jfKfPfyJRdk" allowfullscreen></iframe></div></div>
<div id="coin" class="tab" style="display:none"><div class="card beyond"><h3>🪙 ShaamCoin - عملتك!</h3><div style="background:#000;padding:15px;border-radius:12px;text-align:center;border:2px solid #FFD700"><div style="font-size:40px">🪙</div><div style="font-size:24px;color:#FFD700;font-weight:900">1 SMC = $<span id="price3">0.42</span> ↑12%</div></div><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px"><button class="btn" style="background:#FFD700;color:#000;padding:14px" onclick="buyCoin(100)">اشتري 100 SMC 42$</button><button class="btn" style="background:#ff9900;color:#000;padding:14px" onclick="buyCoin(1000)">1000 SMC خصم 10%</button></div><button class="btn" style="background:#222;color:#FFD700;border:2px solid #FFD700;width:100%;padding:12px;margin-top:8px" onclick="mineCoin()">⛏️ عدّن +10 SMC مجاناً!</button></div></div>
<div id="nft" class="tab" style="display:none"><div class="card beyond"><h3>🖼️ NFT</h3><div style="display:grid;grid-template-columns:1fr 1fr;gap:8px"><div style="background:#000;border:2px solid #FFD700;border-radius:12px;padding:10px;text-align:center"><div style="font-size:30px">👕</div>Real Madrid<br>50 SMC<br><button class="btn" style="background:#FFD700;color:#000;width:100%;margin-top:5px" onclick="buyNFT(50)">اشتري</button></div><div style="background:#000;border:2px solid #00ffff;border-radius:12px;padding:10px;text-align:center"><div style="font-size:30px">⚽</div>Goal نادر<br>200 SMC<br><button class="btn" style="background:#00ffff;color:#000;width:100%;margin-top:5px" onclick="buyNFT(200)">اشتري</button></div></div></div></div>
<div id="game" class="tab" style="display:none"><div class="card beyond"><h3>🎮 لعبة + 100K$</h3><div id="gameBox"></div></div></div>
<div id="store" class="tab" style="display:none"><div class="card beyond"><h3>💳 Web3 Store</h3><button class="btn" style="background:linear-gradient(90deg,#FFD700,#ff9900);color:#000;width:100%;padding:16px" onclick="buyReal()">👑 BEYOND VIP 99.99$ + 500 SMC هدية</button></div></div>
<div id="ai" class="tab" style="display:none"><div class="card beyond"><h3>🤖 AI</h3><div id="aiBox" style="background:#000;padding:12px;border-radius:10px;height:250px;overflow-y:auto">AI جاهز...</div><button class="btn" style="background:#FFD700;color:#000;width:100%;padding:12px;margin-top:8px" onclick="startAI()">شغّل AI + توقع سعر</button></div></div>

<div id="videoModal" class="modal" onclick="closeVideo()"><div class="modal-box" onclick="event.stopPropagation()"><div style="display:flex;justify-content:space-between"><h3 id="videoTitle" style="color:#FFD700">🚀</h3><button onclick="closeVideo()" style="background:red;color:#fff;border:none;padding:6px 12px;border-radius:10px">X</button></div><iframe id="videoFrame" class="video" allowfullscreen></iframe><div style="margin-top:10px;background:#000;padding:10px;border-radius:10px;border:1px solid #FFD700"><p id="commentary" style="color:#FFD700;font-weight:900">🎙️</p><p style="margin-top:6px;background:linear-gradient(90deg,#FFD700,#ff9900);color:#000;padding:8px;border-radius:8px;text-align:center;font-weight:900">🪙 +5 SMC هدية مشاهدة!</p></div></div></div>
<div id="installBanner" class="install" onclick="alert('📲 ⋮ > Add to Home Screen = تطبيق 🚀')">🚀📲 ثبّت V14.1 BEYOND LIGHT - خفيف + ShaamCoin + 100K$</div>

<script>
let money=parseInt(localStorage.getItem('v14_money')||'1000');let coin=parseInt(localStorage.getItem('v14_coin')||'0');let points=0;let vip=localStorage.getItem('v14_vip')||'عادي';let price=0.42;let all=[];
document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin;document.getElementById('myVip').innerText=vip;
function showTab(t,el){document.querySelectorAll('.tab').forEach(x=>x.style.display='none');document.getElementById(t).style.display='block';document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active'));el.classList.add('active');if(t=='game')loadGame();}
async function loadMatches(){try{let r=await fetch('/api/live');let d=await r.json();all=d.matches;document.getElementById('lastUpdate').innerText=new Date().toLocaleTimeString('ar-EG');document.getElementById('count').innerText=d.matches.length;render(all);}catch(e){}}
function render(list){document.getElementById('matches').innerHTML=list.map(m=>{let live=m.minute.includes("'");return `<div class="card ${live?'live':''} ${m.league.includes('champions')?'beyond':''}"><div style="display:flex;justify-content:space-between;font-size:10px"><span style="background:#222;padding:4px 10px;border-radius:12px;border:1px solid #FFD700">${m.league}</span>${live?`<span style="color:red;font-weight:900">🔴 ${m.minute}</span>`:`<span>${m.status}</span>`}</div><div class="team"><span>🚀 ${m.home}</span><span class="score">${m.score.split('-')[0]}</span></div><div class="team"><span>🚀 ${m.away}</span><span class="score">${m.score.split('-')[1]}</span></div><div style="background:#111;padding:8px;border-radius:10px;margin:6px 0;border:1px dashed #FFD700;font-size:11px">🎯 AI: ${Math.floor(Math.random()*3)}-${Math.floor(Math.random()*2)} (${80+Math.floor(Math.random()*15)}%) <button class="btn" style="background:#FFD700;color:#000" onclick="predict('${m.home} vs ${m.away}')">توقع +10 SMC</button></div><div style="display:flex;gap:3px"><button class="btn" style="background:red;color:#fff" onclick="playVideo('${m.home} ${m.away} goal','${m.home} vs ${m.away}')">🎥 هدف +5 SMC</button><button class="btn" style="background:#ff9900;color:#000" onclick="mineCoin()">⛏️ عدّن</button></div></div>`}).join('');}
function loadGame(){document.getElementById('gameBox').innerHTML=all.slice(0,5).map(m=>`<div class=card><b>${m.home} vs ${m.away}</b><br><button class="btn" style="background:#FFD700;color:#000;width:100%;margin-top:6px;padding:10px" onclick="predict('${m.home} vs ${m.away}')">توقع +10 SMC +200$</button></div>`).join('');}
function predict(t){money+=200;coin+=10;price+=0.002;localStorage.setItem('v14_money',money);localStorage.setItem('v14_coin',coin);document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin;document.getElementById('coinPrice').innerText=price.toFixed(3);document.getElementById('price2').innerText=price.toFixed(3);document.getElementById('price3').innerText=price.toFixed(3);alert('✅ '+t+'\\n+200$ +10 SMC! سعر SMC: $'+price.toFixed(3));}
function buyCoin(a){let c=a*price;if(money<c){alert('رصيدك '+money+'$ لا يكفي! تحتاج $'+c.toFixed(2));return}money-=c;coin+=a;price+=a*0.0001;localStorage.setItem('v14_money',money);localStorage.setItem('v14_coin',coin);document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin;alert('اشتريت '+a+' SMC! رصيدك: '+coin+' SMC');}
function mineCoin(){coin+=10;price+=0.001;localStorage.setItem('v14_coin',coin);document.getElementById('myCoin').innerText=coin;alert('⛏️ +10 SMC! رصيدك: '+coin+' SMC = $'+(coin*price).toFixed(2));}
function buyNFT(p){if(coin<p){alert('تحتاج '+p+' SMC، عندك '+coin);return}coin-=p;localStorage.setItem('v14_coin',coin);document.getElementById('myCoin').innerText=coin;alert('🖼️ اشتريت NFT! -'+p+' SMC');}
function buyReal(){coin+=500;vip='BEYOND 👑';localStorage.setItem('v14_coin',coin);localStorage.setItem('v14_vip',vip);document.getElementById('myCoin').innerText=coin;document.getElementById('myVip').innerText=vip;alert('✅ BEYOND VIP! +500 SMC!');}
function filterTeams(q){if(!q){render(all);return}render(all.filter(m=>(m.home+m.away).toLowerCase().includes(q.toLowerCase())));}
function playVideo(q,t){document.getElementById('videoTitle').innerText=t;document.getElementById('commentary').innerText='🚀 خليل البلوشي: هدف BEYOND! ShaamCoin يرتفع!';document.getElementById('videoFrame').src='https://www.youtube.com/embed?listType=search&list='+encodeURIComponent(q)+'&autoplay=1';document.getElementById('videoModal').style.display='flex';money+=5;coin+=5;localStorage.setItem('v14_money',money);localStorage.setItem('v14_coin',coin);document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin;}
function closeVideo(){document.getElementById('videoFrame').src='';document.getElementById('videoModal').style.display='none';}
function startAI(){let b=document.getElementById('aiBox');b.innerHTML+='<br>📈 AI: سعر SMC بعد شهر $'+(price*2.5).toFixed(2)+' - اشتري الآن! 🚀';alert('📈 AI يتوقع SMC $'+(price*2.5).toFixed(2)+'!');}
function activateBeyond(){money+=10000;coin+=1000;vip='BEYOND 👑🚀';price+=0.05;localStorage.setItem('v14_money',money);localStorage.setItem('v14_coin',coin);localStorage.setItem('v14_vip',vip);document.getElementById('myMoney').innerText=money;document.getElementById('myCoin').innerText=coin;document.getElementById('myVip').innerText=vip;alert('🚀 BEYOND LIGHT تفعّل!\\n+10K$ +1000 SMC!\\nرصيدك: '+money+'$ | '+coin+' SMC = $'+(coin*price).toFixed(2)+'\\nخفيف وسريع 100% بدون Glitch!');}
loadMatches();setInterval(loadMatches,30000);
setInterval(()=>{price+=0.0005;document.getElementById('coinPrice').innerText=price.toFixed(3);document.getElementById('price2').innerText=price.toFixed(3);let e=document.getElementById('price3');if(e)e.innerText=price.toFixed(3);},4000);
</script>
</body>
</html>
"""
@app.route('/')
def home(): return HTML
@app.route('/api/live')
def live():
    try:
        leagues=["eng.1","esp.1","ita.1","ger.1","fra.1","sau.1","uefa.champions"]
        matches=[]
        for lg in leagues:
            try:
                r=requests.get(f"https://site.api.espn.com/apis/site/v2/sports/soccer/{lg}/scoreboard",timeout=3)
                d=r.json()
                for ev in d.get('events',[])[:6]:
                    comp=ev['competitions'][0]; h=comp['competitors'][0]; a=comp['competitors'][1]
                    if h['homeAway']=='home': hN=h['team']['displayName']; aN=a['team']['displayName']; hs=h.get('score','0'); as_=a.get('score','0')
                    else: hN=a['team']['displayName']; aN=h['team']['displayName']; hs=a.get('score','0'); as_=h.get('score','0')
                    status=comp['status']['type']['description']; clock=comp['status'].get('displayClock','')
                    matches.append({"home":hN,"away":aN,"score":f"{hs}-{as_}","league":lg,"status":status,"minute":clock,"scorer":""})
            except: continue
        if not matches: matches=[{"home":"Real Madrid","away":"Barcelona","score":"2-1","league":"esp.1","status":"Live","minute":"90'","scorer":""}]
        return jsonify({"matches":matches})
    except: return jsonify({"matches":[]})
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
