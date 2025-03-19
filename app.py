from flask import Flask
from config import config

def create_app():
    app = Flask(config.APP_NAME, static_folder="static")
    app.config.from_object(config)

    from webapp_handlers import webapp
    app.register_blueprint(webapp)

    return app

app = create_app()
