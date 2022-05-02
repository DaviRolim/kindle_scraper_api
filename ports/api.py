from threading import Thread

from flask import Flask, request, jsonify

from controller.highlight_controller import HighlightController

class HighlightAPI:

    app = Flask(__name__)

    @app.route("/", methods=['POST'])
    def sync_highlights():
        controller = HighlightController()
        data = request.json
        sync_thread = Thread(target=controller.sync_highlights, args=(data['email'], data['password'], data['username']))
        sync_thread.start()
        return {
            "statusCode": 200,
            "body": "Syncing your highlights from kindle"
        }

    @app.route("/", methods=['GET'])
    def highlight():
        args = request.args
        controller = HighlightController()
        highlights = controller.get_highlight(args.get('name'))
        return {
            "statusCode": 200,
            "body": highlights
        }