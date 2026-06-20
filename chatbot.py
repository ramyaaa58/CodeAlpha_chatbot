from flask import Flask, request, jsonify, render_template_string
import datetime

app = Flask(__name__)

def chatbot_reply(text):
    t = text.lower()

    if "hello" in t or "hi" in t:
        return "Hello, nice to meet you"
    elif "how are you" in t:
        return "I am doing great, thanks for asking"
    elif "your name" in t:
        return "I am a simple rule based chatbot"
    elif "time" in t:
        return "Current time is " + datetime.datetime.now().strftime("%H:%M:%S")
    elif "date" in t:
        return "Today is " + datetime.datetime.now().strftime("%d-%m-%Y")
    elif "thank" in t:
        return "You are welcome"
    elif "bye" in t:
        return "Goodbye, have a nice day"
    elif "help" in t:
        return "You can try saying hello, ask time, date or say bye"
    else:
        return "Sorry, I did not understand that"

@app.route("/")
def home():
    return render_template_string("""
<!DOCTYPE html>
<html>
<head>
<title>Smart Chatbot</title>
<style>
body {
    margin: 0;
    font-family: Arial;
    background: linear-gradient(135deg,#c7d2fe,#e0f2fe);
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
}
.container {
    width: 380px;
    background: white;
    border-radius: 15px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.15);
    overflow: hidden;
}
.header {
    background: #4f46e5;
    color: white;
    padding: 15px;
    text-align: center;
    font-size: 18px;
}
.chat {
    height: 320px;
    overflow-y: auto;
    padding: 10px;
    background: #f9fafb;
}
.input-area {
    display: flex;
    border-top: 1px solid #ddd;
}
input {
    flex: 1;
    padding: 12px;
    border: none;
    outline: none;
}
button {
    width: 90px;
    border: none;
    background: #4f46e5;
    color: white;
    cursor: pointer;
}
.user {
    text-align: right;
    margin: 6px;
    color: #1d4ed8;
}
.bot {
    text-align: left;
    margin: 6px;
    color: #059669;
}
</style>
</head>
<body>

<div class="container">
    <div class="header">Smart Chatbot</div>
    <div class="chat" id="chat"></div>
    <div class="input-area">
        <input id="msg" placeholder="Type your message">
        <button onclick="send()">Send</button>
    </div>
</div>

<script>
function send() {
    let input = document.getElementById("msg");
    let text = input.value;

    if (text === "") return;

    let chat = document.getElementById("chat");

    chat.innerHTML += "<div class='user'>" + text + "</div>";

    fetch("/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: text})
    })
    .then(res => res.json())
    .then(data => {
        chat.innerHTML += "<div class='bot'>" + data.reply + "</div>";
        chat.scrollTop = chat.scrollHeight;
    });

    input.value = "";
}
</script>

</body>
</html>
""")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    msg = data.get("message", "")
    return jsonify({"reply": chatbot_reply(msg)})

if __name__ == "__main__":
    app.run(debug=True)