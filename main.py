import os

from flask import Flask, request

from recordmanager import RecordManager
from config import roomId

app = Flask(__name__)

manager = RecordManager(roomId)

@app.route("/process_handle", methods=["POST"])
def process_handle():
    if request.is_json:
        json_request = request.json
        print(json_request)
        manager.handle_hook(json_request)
    return ""

if __name__ == "__main__":
    app.run(port=13589)