import os
import json
from threading import Thread

from flask import Flask, request, jsonify

from controller.highlight_api import HighlightAPI

app = Flask(__name__)

@app.route("/", methods=['POST'])
def sync_highlights():
    api = HighlightAPI()
    data = request.json
    sync_thread = Thread(target=api.sync_highlights, args=(data['username'], data['password']))
    sync_thread.start()
    return {
        "statusCode": 200,
        "body": "Syncing your highlights from kindle"
    }

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    