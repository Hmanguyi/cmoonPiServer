from flask import Flask, request, render_template_string
import subprocess

app = Flask(__name__)

current_command = "none"

html = """
<h1>Raspberry Pi Control Panel</h1>

<button onclick="fetch('/start/camera')">Start Camera</button>
<button onclick="fetch('/stop/camera')">Stop Camera</button>

<p>Status: <span id="status">unknown</span></p>

<script>
setInterval(async ()=>{
 let res = await fetch('/status')
 document.getElementById('status').innerText = await res.text()
},1000)
</script>
"""

@app.route("/")
def home():
    return render_template_string(html)

@app.route("/start/<name>")
def start(name):
    global current_command
    current_command = "start " + name
    return "ok"

@app.route("/stop/<name>")
def stop(name):
    global current_command
    current_command = "stop " + name
    return "ok"

@app.route("/command")
def command():
    return current_command

@app.route("/status")
def status():
    return "running"

app.run(host="0.0.0.0", port=10000)
