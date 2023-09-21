from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__, instance_relative_config=True, static_folder="static", static_url_path="/")
    bcrypt = Bcrypt(app)
    
    app.config["JSON_AS_ASCII"]=False
    app.config["TEMPLATES_AUTO_RELOAD"]=True
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@localhost/taipei_trip_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 20  # 設定連接池大小
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10  # 設定連接超時時間
    
    db.init_app(app)

    from .controller.attractions_controller import attractions
    from .controller.mrts_controller import mrts
    from .controller.users_controller import users
    
    app.register_blueprint(attractions, url_prefix='/')
    app.register_blueprint(mrts, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')

    from .model.models import Attraction, Image, User

    with app.app_context():
        db.create_all()

    return app