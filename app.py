from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running - Shamm Edition!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        if request.args.get("hub.verify_token") == "bot123":
            return request.args.get("hub.challenge")
        return "verify error"
    data = request.get_json()
    try:
        entry = data['entry'][0]['changes'][0]['value']
        if 'messages' in entry:
            msg = entry['messages'][0]
            text = msg['text']['body']
            print(f"New message: {text}")
    except Exception as e:
        print(e)
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
