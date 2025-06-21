from flask import Flask
from .extensions import mongo, jwt, mail, cors
from .routes.auth_routes import auth_bp
from .routes.resume_routes import resume_bp
from .routes.ats_routes import ats_bp
from .routes.suggest_routes import suggest_bp
from .routes.admin_routes import admin_bp
from .routes.activity_routes import activity_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')
    
    mongo.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    cors.init_app(app)
    CORS(app, origins='*')
    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(resume_bp, url_prefix='/api')
    app.register_blueprint(ats_bp, url_prefix='/api')
    app.register_blueprint(suggest_bp, url_prefix='/api')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(activity_bp, url_prefix='/api')
    return app 