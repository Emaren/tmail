# track_server.py
from flask import Flask, request, send_file
import time

app = Flask(__name__)

@app.route("/track")
def track():
    user_id = request.args.get("id")
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
    with open("open_log.txt", "a") as f:
        f.write(f"{timestamp} - Opened by: {user_id}\n")
    # 1x1 transparent GIF
    return send_file("pixel.gif", mimetype='image/gif')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8008)
