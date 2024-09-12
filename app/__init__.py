import secrets

from flask import Flask, session


def create_app():
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    @app.before_request
    def make_session_permanent():
        session.permanent = True

    app.config['SECRET_KEY'] = secrets.token_urlsafe(30)
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    from .user.userr import user

    app.register_blueprint(user, url_prefix='/')

    return app