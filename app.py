from datetime import date

from flask import Flask
from flask.json import JSONEncoder

from routes import api


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, date):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)


app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
app.register_blueprint(api)

if __name__ == '__main__':
    app.run()
