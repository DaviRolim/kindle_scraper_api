from threading import Thread

from flask import Flask, request, jsonify

from controller.highlight_controller import HighlightController
from repository.remote_repository import RemoteRepository

class HighlightAPI:

    app = Flask(__name__)

    @app.route("/", methods=['POST'])
    def sync_highlights():
        repository = RemoteRepository()
        api = HighlightController(repository)
        data = request.json
        sync_thread = Thread(target=api.sync_highlights, args=(data['username'], data['password']))
        sync_thread.start()
        return {
            "statusCode": 200,
            "body": "Syncing your highlights from kindle"
        }

    @app.route("/", methods=['GET'])
    def highlight():
        repository = RemoteRepository()
        api = HighlightController(repository)
        highlights = api.get_highlight()
        return {
            "statusCode": 200,
            "body": highlights
        }