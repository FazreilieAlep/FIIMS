from flask import Flask
from flask_cors import CORS
import pmetal
import minstrument

app = Flask(__name__)
CORS(app)

# Get the blueprints from pmetal.py and minstrument.py
pmetal_blueprint = pmetal.get_pmetal_blueprint()
minstrument_blueprint = minstrument.get_minstrument_blueprint()

# Register the blueprints with the Flask app
app.register_blueprint(pmetal_blueprint)
app.register_blueprint(minstrument_blueprint)


if __name__ == '__main__':
    app.run()
