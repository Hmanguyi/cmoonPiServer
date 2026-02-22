from flask import Flask, request, render_template_string, send_from_directory
import os
import base64
import datetime

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

latest_label = "none"
latest_image = None

# ---------------- HTML for viewing ----------------
html = """
<h1>Latest Uploaded Image</h1>

<h2>Label: <span id="label">none</span></h2>
<img id="img" width="400"/>

<script>
async function update(){
    document.getElementById("label").innerText =
        await (await fetch('/latest_label')).text()

    let img = await (await fetch('/latest_image')).text()
    if(img != "none"){
        document.getElementById("img").src = "/uploads/" + img + "?t=" + new Date().getTime()
    }
}

setInterval(update, 1000)
update()
</script>
"""

@app.route("/")
def home():
    return render_template_string(html)

# ---------------- Receive image from Pi ----------------
@app.route("/upload", methods=["POST"])
def upload():
    global latest_label, latest_image

    label = request.form.get("label", "unknown")
    image_b64 = request.form.get("image")

    if not image_b64:
        return "No image provided", 400

    # Use timestamp to prevent overwriting previous images
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{label}_{timestamp}.png"

    with open(os.path.join(UPLOAD_FOLDER, filename), "wb") as f:
        f.write(base64.b64decode(image_b64))

    latest_label = label
    latest_image = filename
    print(f"Received image: {filename}")

    return "ok"

# ---------------- Serve uploaded images ----------------
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/latest_label")
def get_label():
    return latest_label

@app.route("/latest_image")
def get_image():
    return latest_image if latest_image else "none"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
