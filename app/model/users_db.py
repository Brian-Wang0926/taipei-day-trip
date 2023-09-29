from .models import User
from .. import db
from flask_bcrypt import check_password_hash

class Users_Db:
    # 註冊會員
    def add_user(self, user):
        try:
            db.session.add(user)
            db.session.commit() 
        except Exception as e:
            db.session.rollback()
            raise e

    # 抓取會員資料
    def get_user(self, email):
        get_user_query = User.query.filter_by(email=email).first()
        print("get_user資料庫成功",get_user_query)
        return get_user_query

    def check_password(self, user, password):
        print("開始確認密碼",user ,password)
        result = check_password_hash(user.password, password)
        print("check_password資料庫成功", result)
        return result
    