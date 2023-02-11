from flask import Flask

from .blueprints.site.routes import site

def create_app():
    app = Flask(__name__)
    
    app.register_blueprint(site)

    return app