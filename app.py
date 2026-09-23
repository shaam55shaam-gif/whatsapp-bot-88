from flask import Flask
app = Flask(__name__)
HTML = """<html dir=rtl><head><meta charset=UTF-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V64 SOUND + تعليق</title>
<style>
body{background:#000;color:#fff;font-family:Arial;margin:0}
.h{background:linear-gradient(90deg,gold,#fff,gold,#0af);color:#000;padding:12px;text-align:center;font-weight:900;position:sticky;top:0;z-index:30;font-size:11px}
.card{background:#1a1a1a;border-right:6px solid gold;margin:8px;padding:12px;border-radius:16px;border:1px solid #333;cursor:pointer}
.card.live{border-right-color:red;box-shadow:0 0 20px red;background:#1a0000}
.f{padding:7px 12px;border-radius:22px;border:1px solid #444;background:#111;color:#fff;margin:3px;display:inline-block;cursor:pointer;font-size:10px}.f.active{background:gold;color:#000;font-weight:900}
#livePitch{position:fixed;top:0;left:0;right:0;bottom:0;background:#000;z-index:100;display:none;flex-direction:column}
#pitch{width:100%;height:100%;background:#2d8a2d;display:block}
.topBar{display:flex;justify-content:space-between;padding:10px;background:#111;border-bottom:2px solid gold}
.btn{padding:7px 12px;border-radius:14px;border:none;margin:3px;font-size:10px;font-weight:900;cursor:pointer}
.btn-close{background:red;color:#fff}
.count{font-size:10px;color:#0f0;background:#002a00;padding:4px 8px;border-radius:12px;border:1px solid #0f0;display:inline-block;margin:3px}
.timer{font-family:monospace;color:#0ff;background:#001a1a;padding:4px 8px;border-radius:10px;border:1px solid #0ff;display:inline-block}
.live-dot{width:10px;height:10px;background:red;border-radius:50%;display:inline-block;animation:blink 0.8s infinite}@keyframes blink{0%,100%{opacity:1}50%{opacity:0.2}}
.search{margin:8px;background:#111;border:2px solid gold;border-radius:28px;padding:11px 15px;display:flex}.search input{flex:1;background:transparent;border:none;color:#fff;outline:none}
.prog{height:10px;background:#222;border-radius:10px;margin:8px;overflow:hidden}.prog div{height:100%;background:linear-gradient(90deg,gold,#fff,gold);width:100%}
#commentary{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(0,0,0,0.9);color:gold;border:3px solid gold;padding:20px 30px;border-radius:20px;font-size:22px;font-weight:900;display:none;z-index:10;text-align:center;box-shadow:0 0 30px gold;animation:pop 0.5s}
@keyframes pop{0%{transform:translate(-50%,-50%) scale(0)}50%{transform:translate(-50%,-50%) scale(1.2)}100%{transform:translate(-50%,-50%) scale(1)}}
</style></head><body>
<div id=livePitch>
<div class=topBar>
<span id=pitchTitle style="color:gold;font-weight:900">🔴 LIVE</span>
<div><span id=matchClock style="color:#0f0;font-weight:900;font-size:14px">78:23</span> <button onclick="toggleSound()" id=soundBtn style="background:gold;color:#000;padding:7px 12px;border-radius:14px;border:none;font-weight:900;margin-left:5px">🔊 صوت</button> <button class=btn-close onclick="closePitch()">✕</button></div>
</div>
<div style="flex:1;position:relative;background:#000;display:flex;flex-direction:column">
<canvas id=pitch></canvas>
<div id=commentary></div>
<div style="position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,0.9);padding:8px;display:flex;justify-content:space-between;color:#fff;font-size:11px;flex-wrap:wrap">
<span id=attackTeam>⚔️ هجوم - الكرامة</span>
<span id=ballPos>📍 منتصف</span>
<span id=stats>🎯 8-3 | 🚩 5-2 | ⚽ 62%-38%</span>
</div>
</div>
<div id=liveLog style="height:80px;overflow:auto;background:#111;padding:6px;font-size:10px;border-top:2px solid gold"></div>
</div>

<div class=h>🔥 V64 AiScore + 🔊 جمهور + 🗣️ تعليق "هجمة خطيرة!" - 222 بطولة!</div>
<div style="padding:7px;font-size:11px;color:gold;display:flex;justify-content:space-between;font-weight:900"><span>222/222 - AiScore LIVE + SOUND 🔊</span><span>🎙️ تعليق عربي</span></div>
<div class=prog><div></div></div>
<div class=search><input id=q placeholder="ابحث: الكرامة..." oninput=filter()></div>
<div style="padding:8px;white-space:nowrap;overflow:auto;text-align:center">
<span class="f active" id="fa" onclick="setF('all')">الكل 222</span>
<span class=f id="fl" onclick="setF('live')">🔴 LIVE</span>
<span class=f id="fsy" onclick="setF('syria')">🇸🇾 سوريا</span>
</div>
<div id=s style="text-align:center;color:#000;padding:10px;background:linear-gradient(90deg,gold,#fff,gold);margin:7px;border-radius:14px;font-size:12px;font-weight:900">🔊 V64 - اضغط المباراة وشغل الصوت - رح تسمع "هوووو!" وتعليق "هجمة خطيرة!"</div>
<div id=m></div>

<script>
var CLUB=["syria|سوريا|الكرامة 💙 vs حطين 🔵|تشرين ⭐ vs الوثبة ❤️|الجيش ⚔️ vs الفتوة 💛","saudi|السعودية|الهلال 🌙 vs النصر 💛|الاتحاد vs الاهلي","egypt|مصر|الاهلي 🦅 vs الزمالك 🏹","england|انجلترا|Man City vs Arsenal|Liverpool vs Chelsea","spain|اسبانيا|Real Madrid vs Barcelona"];
var all=[]; CLUB.forEach(c=>{var p=c.split('|'); for(var i=2;i<p.length;i++){var t=p[i].split(' vs '); if(t.length==2) all.push({h:t[0],a:t[1],l:p[1],code:p[0],min:55+Math.floor(Math.random()*35),sec:Math.floor(Math.random()*60),live:true});}});
var curF='all', ballX=50, ballY=50, targetX=50, targetY=50, soundOn=true, audioCtx;
function setF(f){curF=f; document.querySelectorAll('.f').forEach(x=>x.classList.remove('active')); if(f=='all') document.getElementById('fa').classList.add('active'); if(f=='live') document.getElementById('fl').classList.add('active'); if(f=='syria') document.getElementById('fsy').classList.add('active'); filter();}
var canvas=document.getElementById('pitch'), ctx=canvas.getContext('2d');
function resize(){canvas.width=canvas.offsetWidth*2; canvas.height=canvas.offsetHeight*2; draw();}
window.onresize=resize;
function toggleSound(){soundOn=!soundOn; document.getElementById('soundBtn').innerText=soundOn?'🔊 صوت':'🔇 صامت'; if(soundOn &&!audioCtx){audioCtx=new (window.AudioContext||window.webkitAudioContext)();}}
function playCrowd(type){
 if(!soundOn ||!audioCtx) return;
 var osc=audioCtx.createOscillator(), gain=audioCtx.createGain();
 osc.connect(gain); gain.connect(audioCtx.destination);
 if(type=='attack'){osc.frequency.value=200; gain.gain.setValueAtTime(0.3, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime+1.2); osc.start(); osc.stop(audioCtx.currentTime+1.2);}
 else if(type=='shot'){osc.frequency.value=400; gain.gain.setValueAtTime(0.5, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime+0.5); osc.start(); osc.stop(audioCtx.currentTime+0.5); if(navigator.vibrate) navigator.vibrate(100);}
 else if(type=='goal'){osc.frequency.value=150; gain.gain.setValueAtTime(0.8, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.01, audioCtx.currentTime+2.5); osc.start(); osc.stop(audioCtx.currentTime+2.5); if(navigator.vibrate) navigator.vibrate([200,100,200,100,400]);}
}
function showComment(text,emoji){
 var el=document.getElementById('commentary');
 el.innerHTML=emoji+'<br>'+text;
 el.style.display='block';
 setTimeout(()=>{el.style.display='none';},2000);
 var log=document.getElementById('liveLog');
 var time=document.getElementById('matchClock').innerText;
 log.innerHTML='<div style="border-right:3px solid gold;padding:4px;margin:3px;background:#1a1a1a">⏱️ '+time+' - '+emoji+' '+text+'</div>'+log.innerHTML;
 // Web Speech - تعليق عربي
 if(soundOn && 'speechSynthesis' in window){
  var msg=new SpeechSynthesisUtterance(text);
  msg.lang='ar-SA'; msg.rate=1.1; msg.volume=0.8;
  speechSynthesis.speak(msg);
 }
}
function draw(){
 var w=canvas.width, h=canvas.height;
 ctx.fillStyle='#1a1a1a'; ctx.fillRect(0,0,w,h);
 var pw=w*0.92, ph=h*0.65, px=(w-pw)/2, py=(h-ph)/2-20;
 ctx.fillStyle='#222'; ctx.beginPath(); ctx.roundRect(px-18,py-18,pw+36,ph+36,18); ctx.fill();
 ctx.fillStyle='#fff'; ctx.font=(w*0.025)+'px Arial'; ctx.fillText('AiScore.com',px+20,py-2); ctx.fillText('AiScore.com',px+pw/2-50,py-2); ctx.fillText('AiScore.com',px+pw-110,py-2);
 for(var i=0;i<10;i++){ctx.fillStyle=i%2==0?'#2d9e2d':'#36b336'; ctx.fillRect(px+i*pw/10,py,pw/10,ph);}
 ctx.strokeStyle='#fff'; ctx.lineWidth=3; ctx.strokeRect(px,py,pw,ph);
 ctx.beginPath(); ctx.moveTo(px+pw/2,py); ctx.lineTo(px+pw/2,py+ph); ctx.stroke();
 ctx.beginPath(); ctx.arc(px+pw/2,py+ph/2,pw*0.08,0,Math.PI*2); ctx.stroke();
 ctx.strokeRect(px,py+ph*0.2,pw*0.18,ph*0.6); ctx.strokeRect(px+pw-pw*0.18,py+ph*0.2,pw*0.18,ph*0.6);
 ctx.strokeRect(px,py+ph*0.32,pw*0.07,ph*0.36); ctx.strokeRect(px+pw-pw*0.07,py+ph*0.32,pw*0.07,ph*0.36);
 ctx.fillStyle='#ffffffaa'; ctx.fillRect(px-8,py+ph*0.42,8,ph*0.16); ctx.fillRect(px+pw,py+ph*0.42,8,ph*0.16);
 // هجوم ظل
 ctx.fillStyle='rgba(255,0,0,0.15)'; var shadowX=ballX<50?px:px+pw/2; ctx.fillRect(shadowX,py,pw/2,ph);
 var bx=px+ballX/100*pw, by=py+ballY/100*ph;
 ctx.font=(w*0.06)+'px Arial'; ctx.fillText('⚽',bx-18,by+8);
 ctx.fillStyle='#0af'; ctx.beginPath(); ctx.arc(bx,by+18,12,0,Math.PI*2); ctx.fill(); ctx.strokeStyle='#fff'; ctx.lineWidth=2; ctx.stroke();
 ctx.fillStyle='#fff'; ctx.font='bold '+(w*0.035)+'px Arial'; ctx.fillText('هجوم',bx-30,by+55);
 ctx.font=(w*0.028)+'px Arial'; ctx.fillText(document.getElementById('attackTeam').innerText.replace('⚔️ هجوم - ',''),bx-70,by+80);
 ctx.fillStyle='rgba(255,255,255,0.3)'; ctx.font=(w*0.05)+'px Arial'; ctx.fillText('AiScore.com',w/2-80,h/2+20);
}
var matchInterval, eventInterval;
function openPitch(h,a){
 document.getElementById('livePitch').style.display='flex';
 document.getElementById('pitchTitle').innerText='🔴 '+h+' vs '+a+' - LIVE 🔊';
 document.getElementById('attackTeam').innerText='⚔️ هجوم - '+h;
 document.getElementById('liveLog').innerHTML='<div style="color:gold">🔴 بداية البث - '+h+' vs '+a+'</div>';
 if(!audioCtx){audioCtx=new (window.AudioContext||window.webkitAudioContext)();}
 setTimeout(resize,100);
 if(matchInterval) clearInterval(matchInterval); if(eventInterval) clearInterval(eventInterval);
 var minute=78, second=23;
 matchInterval=setInterval(()=>{
  if(Math.random()>0.65){targetX=5+Math.random()*90; targetY=10+Math.random()*80;}
  ballX+=(targetX-ballX)*0.06 + (Math.random()-0.5)*1.5;
  ballY+=(targetY-ballY)*0.06 + (Math.random()-0.5)*1.5;
  second++; if(second>=60){second=0; minute++;}
  document.getElementById('matchClock').innerText=String(minute).padStart(2,'0')+':'+String(second).padStart(2,'0');
  draw();
 },80);
 eventInterval=setInterval(()=>{
  var r=Math.random();
  if(r>0.92){showComment('هدف! جوووول! 🔥🔥','⚽'); playCrowd('goal');}
  else if(r>0.75){showComment('هجمة خطيرة! 🔥','⚔️'); playCrowd('attack'); document.getElementById('ballPos').innerText='📍 منطقة الجزاء 🔥🔥';}
  else if(r>0.6){showComment('تسديدة! 🎯','🎯'); playCrowd('shot');}
  else if(r>0.45){showComment('ركنية! 🚩','🚩'); playCrowd('attack');}
  else if(r>0.3){showComment('هجوم مرتد! ⚡','⚡');}
 },2500);
}
function closePitch(){document.getElementById('livePitch').style.display='none'; if(matchInterval) clearInterval(matchInterval); if(eventInterval) clearInterval(eventInterval);}
function filter(){
 var q=document.getElementById('q').value.toLowerCase();
 var list=all.filter(m=>{
  var mq=!q||m.h.toLowerCase().includes(q)||m.a.toLowerCase().includes(q);
  var mf=true; if(curF=='live') mf=m.live; else if(curF=='syria') mf=m.code=='syria'||m.h.includes('الكرامة'); return mq&&mf;
 });
 var html='';
 list.slice(0,80).forEach(m=>{
  var pr=Math.floor(55+Math.random()*35);
  html+='<div class="card live" onclick="openPitch(\\''+m.h+'\\',\\''+m.a+'\\')"><b><span class=live-dot></span> 🔴 '+m.h+' vs '+m.a+'</b><br><span class=count>🔴 LIVE '+m.min+':'+String(m.sec).padStart(2,'0')+' | 🔊 + 🎙️ تعليق</span><br><small style="color:gold">🏟️ '+m.l+' - اضغط واسمع الجمهور + تعليق "هجمة خطيرة!"</small><br><button class=btn style="background:red;color:#fff">🔊📺 فتح الملعب + صوت جمهور + تعليق عربي</button></div>';
 });
 document.getElementById('m').innerHTML=html;
}
filter(); resize();
</script></body></html>
"""
@app.route('/')
def home(): return HTML
if __name__=='__main__': app.run(host='0.0.0.0',port=10000)
