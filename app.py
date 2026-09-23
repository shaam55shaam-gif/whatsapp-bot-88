from flask import Flask, render_template_string, request, jsonify
import datetime
app = Flask(__name__)
HTML = """
<!DOCTYPE html><html dir="rtl" lang="ar"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Shaam Smart App</title>
<style>body{margin:0;font-family:system-ui;background:linear-gradient(135deg,#0f172a,#1e293b);color:white;min-height:100vh}.container{max-width:500px;margin:0 auto;padding:20px}.header{text-align:center;padding:30px 0}.logo{font-size:60px}h1{font-size:28px;margin:10px 0}.subtitle{opacity:.7}.card{background:rgba(255,255,255,.08);backdrop-filter:blur(10px);border:1px solid rgba(255,255,255,.1);border-radius:20px;padding:20px;margin:15px 0}.btn{width:100%;padding:16px;border:none;border-radius:15px;font-size:18px;font-weight:bold;cursor:pointer;margin:8px 0}.btn-primary{background:linear-gradient(90deg,#8b5cf6,#3b82f6);color:white}.btn-dark{background:rgba(0,0,0,.3);color:white;border:1px solid rgba(255,255,255,.2)}.status{display:flex;justify-content:space-between;margin:10px 0}.dot{width:12px;height:12px;background:#22c55e;border-radius:50%;display:inline-block;box-shadow:0 0 10px #22c55e}input{width:100%;padding:15px;border-radius:12px;border:1px solid rgba(255,255,255,.2);background:rgba(0,0,0,.3);color:white;box-sizing:border-box;margin:10px 0}</style>
</head><body><div class="container"><div class="header"><div class="logo">🏠✨</div><h1>Shaam Smart</h1><div class="subtitle">التطبيق المستقل - النسخة الفخمة</div></div>
<div class="card"><div class="status"><span>حالة النظام</span><span><span class="dot"></span> شغال</span></div><div class="status"><span>الوقت</span><span id="time"></span></div></div>
<div class="card"><h3>💬 مساعد شام الذكي</h3><input id="msg" placeholder="اكتب شي... مثلاً: شغل الضو"><button class="btn btn-primary" onclick="send()">إرسال</button><div id="reply" style="margin-top:15px;background:rgba(0,0,0,.3);padding:15px;border-radius:12px;display:none"></div></div>
<div class="card"><h3>⚡ تحكم سريع</h3><button class="btn btn-dark" onclick="quick('شغل الإنارة')">💡 شغل الإنارة</button><button class="btn btn-dark" onclick="quick('شغل المكيف')">❄️ شغل المكيف</button><button class="btn btn-dark" onclick="quick('وضع النوم')">🌙 وضع النوم</button></div></div>
<script>function updateTime(){document.getElementById('time').innerText=new Date().toLocaleTimeString('ar-EG')}setInterval(updateTime,1000);updateTime();function quick(t){document.getElementById('msg').value=t;send();}async function send(){let m=document.getElementById('msg').value;if(!m)return;let r=document.getElementById('reply');r.style.display='block';r.innerText='⏳ بفكر...';let res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})});let data=await res.json();r.innerText='🤖: '+data.reply;}</script></body></html>
"""
@app.route("/")
def home(): return render_template_string(HTML)
@app.route("/api/chat", methods=["POST"])
def chat():
    data=request.get_json();msg=data.get("message","").lower()
    if "ضو" in msg or "انارة" in msg: reply="تم ✅ شغلت الإنارة، الجو صار فخم 💡"
    elif "مكيف" in msg: reply="تم ✅ شغلت المكيف على 22° ❄️"
    elif "نوم" in msg: reply="وضع النوم تفعّل 🌙 طفيت الأضوية"
    elif "كيفك" in msg or "مرحبا" in msg: reply="أهلين يا شام! أنا جاهز 100% 🚀 تطبيقك شغال"
    else: reply=f"وصلتني: '{msg}' - تطبيقك المستقل شغال تمام!"
    return jsonify({"reply":reply})
@app.route("/webhook", methods=["GET","POST"])
def webhook(): return "App is independent now",200
if __name__=="__main__": app.run(host="0.0.0.0",port=10000)
