from .. import db
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import Date

# 定義資料模型
class Attraction(db.Model):
    __tablename__ = 'attractions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    category = db.Column(db.String(255))
    description = db.Column(db.Text)
    address = db.Column(db.String(255))
    transport = db.Column(db.Text)
    mrt = db.Column(db.String(255))
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __init__(self, name, category, description, address, transport, mrt, lat, lng):
        self.name = name
        self.category = category
        self.description = description
        self.address = address
        self.transport = transport
        self.mrt = mrt
        self.lat = lat
        self.lng = lng

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'))
    img = db.Column(db.String(255))

    # 設定外鍵關係
    Attraction.images = db.relationship('Image', backref='attraction', lazy=True)

    def __init__(self, attraction_id, img):
        self.attraction_id = attraction_id
        self.img = img

# 建立會員資料庫
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = generate_password_hash(password).decode('utf-8')
        
# 建立預定景點資料庫
class Booking(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(Date)
    time = db.Column(db.String(50))
    price = db.Column(db.Integer)
    payment_status = db.Column(db.Boolean, default=False)       # 預設為 False，若完成付款則變為 True
    order_id = db.Column(db.String(20), db.ForeignKey('orders.id')) 
    # 一個 order 有多個 booking ， 但一個 booking 只會對應到一個 order
    attraction = db.relationship('Attraction',backref='bookings')
    user = db.relationship('User',backref='bookings')
    order = db.relationship('Order', backref='bookings')

    def __init__(self, attraction_id, user_id, date, time, price, payment_status=False):
        self.attraction_id = attraction_id
        self.user_id = user_id
        self.date = date
        self.time = time
        self.price = price
        self.payment_status = payment_status
    # 當完成訂單付款後，payment_status會改為 True，且新增 order_id 
    def mark_payment_completed(self, order_id):
        self.payment_status = True
        self.order_id = order_id


# 建立訂單資料庫
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.String(20), primary_key=True) # 訂單編號
    total_price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    contact_name = db.Column(db.String(255))
    contact_email = db.Column(db.String(255))
    contact_phone = db.Column(db.String(20))

    def __init__(self, id, total_price, user_id, contact_name, contact_email, contact_phone):
        self.id = id
        self.total_price = total_price
        self.user_id = user_id
        self.contact_name = contact_name
        self.contact_email = contact_email
        self.contact_phone = contact_phone



