from flask import Flask
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='CHAN'
    from .auth import auth
    from .views import views
    app.register_blueprint(auth)
    app.register_blueprint(views)
    return app