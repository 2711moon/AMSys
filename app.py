from flask import Flask
from config import Config
from extensions import init_extensions
from routes import register_blueprints

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    init_extensions(app)
    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
