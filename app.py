from flask import Flask, render_template_string, request, jsonify, Response

app = Flask(__name__)

MANIFEST = """
{
  "name": "Shaam Smart",
  "short_name": "Shaam",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#0f172a",
  "theme_color": "#8b5cf6",
  "icons": [
    {
      "src": "https://cdn-icons-png.flaticon.com/512/3004/3004776.png",
      "sizes": "512x512",
      "type": "image/png"
    }
  ]
}
"""

HTML = """
<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Shaam Smart App</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#8b5cf6">
<style>
body{margin:0;font-family:system-ui;background:linear-gradient(135deg,#0f172a,#1e293b);color:white;min-height:100vh}
.container{max-width:500px;margin:0 auto;padding:20px}
.header{text-align:center;padding:30px 0}
.logo{font-size:60px}
h1{font-size:28px;margin:10px 0}
.card{background:rgba(255,255,255,.08);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:20px;margin:15px 0}
.btn{width:100%;padding:16px;border:none;border-radius:15px;font-size:18px;font-weight:bold;cursor:pointer;margin:8px 0}
.btn-primary{background:linear-gradient(90deg,#8b5cf6,#3b82f6);color:white}
.btn-dark{background:rgba(0,0,0,.3);color:white;border:1px solid rgba(255,255,255,.2)}
.status{display:flex;justify-content:space-between;margin:10px 0}
.dot{width:12px;height:12px;background:#22c55e;border-radius:50%;display:inline-block;box-shadow:0 0 10px #22c55e}
input{width:100%;padding:15px;border-radius:12px;border:1px solid rgba(255,255,255,.2);background:rgba(0,0,0,.3);color:white;box-sizing:border-box;margin:10px 0}
.install-banner{background:linear-gradient(90deg,#22c55e,#16a34a);padding:15px;border-radius:15px;text-align:center;margin:15px 0;display:none}
</style>
</head>
<body>
<div class="container">
  <div class="header">
    <div class="logo">🏠✨</div>
    <h1>Shaam Smart</h1>
    <div>تطبيق أندرويد - النسخة الفخمة</div>
  </div>
  <div id="installBanner" class="install-banner">
    <b>📲 حوله لتطبيق!</b><br>
    <button onclick="installApp()" class="btn btn-dark" style="margin-top:10px">تثبيت التطبيق الآن</button>
  </div>
  <div class="card">
    <div class="status"><span>حالة النظام</span><span><span class="dot"></span> شغال</span></div>
    <div class="status"><span>الوقت</span><span id="time"></span></div>
  </div>
  <div class="card">
    <h3>💬 مساعد شام الذكي</h3>
    <input id="msg" placeholder="اكتب شي... مثلاً: شغل الضو">
    <button class="btn btn-primary" onclick="send()">إرسال</button>
    <div id="reply" style="margin-top:15px;background:rgba(0,0,0,.3);padding:15px;border-radius:12px;display:none"></div>
  </div>
  <div class="card">
    <h3>⚡ تحكم سريع</h3>
    <button class="btn btn-dark" onclick="quick('شغل الإنارة')">💡 شغل الإنارة</button>
    <button class="btn btn-dark" onclick="quick('شغل المكيف')">❄️ شغل المكيف</button>
    <button class="btn btn-dark" onclick="quick('وضع النوم')">🌙 وضع النوم</button>
  </div>
</div>
<script>
function updateTime(){document.getElementById('time').innerText=new Date().toLocaleTimeString('ar-EG')}
setInterval(updateTime,1000);updateTime();
function quick(t){document.getElementById('msg').value=t;send();}
async function send(){
  let m=document.getElementById('msg').value;
  if(!m) return;
  let r=document.getElementById('reply');
  r.style.display='block'; r.innerText='⏳ بفكر...';
  let res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});
  let data=await res.json();
  r.innerText='🤖: '+data.reply;
}
let deferredPrompt;
window.addEventListener('beforeinstallprompt',(e)=>{
  e.preventDefault();
  deferredPrompt=e;
  document.getElementById('installBanner').style.display='block';
});
function installApp(){
  if(deferredPrompt){
    deferredPrompt.prompt();
    deferredPrompt.userChoice.then((c)=>{
      if(c.outcome==='accepted') document.getElementById('installBanner').style.display='none';
      deferredPrompt=null;
    });
  } else {
    alert('اضغط على النقاط الثلاث فوق في المتصفح واختر Add to Home Screen');
  }
}
if('serviceWorker' in navigator){ navigator.serviceWorker.register('/sw.js'); }
</script>
</body>
</html>
"""

SW = """
self.addEventListener('install', e => self.skipWaiting());
self.addEventListener('activate', e => self.clients.claim());
"""

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/manifest.json")
def manifest():
    return Response(MANIFEST, mimetype='application/json')

@app.route("/sw.js")
def sw():
    return Response(SW, mimetype='application/javascript')

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message","").lower()
    if "ضو" in msg or "انارة" in msg: reply = "تم ✅ شغلت الإنارة، الجو صار فخم 💡"
    elif "مكيف" in msg: reply = "تم ✅ شغلت المكيف على 22° ❄️"
    elif "نوم" in msg: reply = "وضع النوم تفعّل 🌙"
    else: reply = f"وصلتني: '{msg}' - تطبيقك الأندرويد شغال 100% 📱"
    return jsonify({"reply": reply})

@app.route("/webhook", methods=["GET","POST"])
def webhook():
    return "Shaam Android App v1.0", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
