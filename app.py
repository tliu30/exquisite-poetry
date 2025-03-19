from flask import Flask
from config import config


def create_app():
    app = Flask(config.APP_NAME, static_folder="static")
    app.config.from_object(config)

    from webapp_handlers import webapp

    app.register_blueprint(webapp)

    from extensions import db

    db.init_app(app)

    # fmt: off

    from models.poem import Poem
    Poem

    from models.segment import Segment
    Segment

    # fmt: on

    from extensions import migrate

    migrate.init_app(app, db, config.FLASK_MIGRATE_DIRECTORY)

    return app


app = create_app()
