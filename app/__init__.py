from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')  
db_name = os.getenv('DB_NAME') 

db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__, instance_relative_config=True, static_folder="static", static_url_path="/")
    bcrypt = Bcrypt(app)
    
    app.config["JSON_AS_ASCII"]=False
    app.config["TEMPLATES_AUTO_RELOAD"]=True
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['PARTNER_KEY'] = os.getenv('PARTNER_KEY')
    app.config['MERCHANT_ID'] = os.getenv('MERCHANT_ID')


    app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_POOL_SIZE'] = 20  # 設定連接池大小
    app.config['SQLALCHEMY_POOL_TIMEOUT'] = 10  # 設定連接超時時間



    
    db.init_app(app)

    from .controller.attractions_controller import attractions
    from .controller.mrts_controller import mrts
    from .controller.users_controller import users
    from .controller.bookings_controller import bookings
    from .controller.orders_controller import orders
    
    with app.app_context():
        db.create_all()

    app.register_blueprint(attractions, url_prefix='/')
    app.register_blueprint(mrts, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')
    app.register_blueprint(bookings, url_prefix='/')
    app.register_blueprint(orders, url_prefix='/')
    
    from .model.models import Attraction, Image, User, Booking, Order

    return app