from flask import Flask

from . import csrf
import ishuhui.data as data
import env

from flask_assets import Environment, Bundle

def create_app(config, should_register_blueprints=True):
    app = Flask(__name__,static_folder = r'D:\test',static_url_path='/assets')
    
    assets = Environment(app)
    js = Bundle('app.js','style.css')
    assets.register('assets',js)

    app.config.from_object(config)
    app.config.from_envvar('FLASKR_SETTINGS', silent=True)
    from ishuhui.extensions.loginmanger import login_manager
    from ishuhui.extensions.flasksqlalchemy import db
    login_manager.setup_app(app)
    db.init_app(app)

    

    csrf.init(app)

    from ishuhui.logger import init_logger
    init_logger(app)

    if should_register_blueprints:
        register_blueprints(app)

    with app.app_context():
        db.create_all()
        fake_db()
    return app

def fake_db():
    from ishuhui.extensions.flasksqlalchemy import db
    data.Comic.query.delete()
    for item in env.COMICS:
        comic = data.Comic()
        comic.title = item['title']
        comic.description = item['description']
        comic.classify_id = item['classify_id']
        db.session.add(comic)
        db.session.commit()


def register_blueprints(app):
    from ishuhui.controllers.comic import bp_comic
    app.register_blueprint(bp_comic)

    from ishuhui.controllers.admin import bp_admin
    app.register_blueprint(bp_admin)

    from ishuhui.controllers.auth import bp_auth
    app.register_blueprint(bp_auth)

    from ishuhui.controllers.error import bp_error
    app.register_blueprint(bp_error)
