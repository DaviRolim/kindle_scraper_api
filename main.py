import os
from ports.api import HighlightAPI


api = HighlightAPI()
app = api.app

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
    