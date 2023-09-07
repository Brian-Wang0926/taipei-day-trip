# how to import db from __init__.py
from .. import db

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

    # def __repr__(self):
    #     return '<Attraction %r>' % self.name

class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    attraction_id = db.Column(db.Integer, db.ForeignKey('attractions.id'))
    img = db.Column(db.String(255))

    def __init__(self, attraction_id, img):
        self.attraction_id = attraction_id
        self.img = img

    # def __repr__(self):
    #     return '<Image %r>' % self.img

# 設定外鍵關係
Attraction.images = db.relationship('Image', backref='attraction', lazy=True)
