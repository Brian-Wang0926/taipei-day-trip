from flask import Blueprint, request, jsonify
from ..model.users_db import Users_Db
from ..model.models import User
import jwt

secret_key = 'hjshjhdjah kjshkjdhjs'
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash

users = Blueprint('users', __name__)

users_db = Users_Db()

# 註冊會員
@users.route('/api/user', methods=['POST'])
def sign_up():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')

        # 送進資料庫檢查 email 是否以存在
        existing_user = users_db.get_user(email)
        print("有存在使用者", existing_user)

        if existing_user is None:
            # 註冊新帳戶
            new_user = User(name=name, email=email, password=password)
            users_db.add_user(new_user)

            response = {
                "ok": True,
                "message": "註冊成功"
            }
            return jsonify(response), 200
        else:
            response = {
                "error": True,
                "message": "註冊失敗，該電子郵件已被使用"
            }
            return jsonify(response)

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500

# 取得當前會員登入資訊
@users.route('/api/user/auth', methods=['GET'])
def user_status():
    try:
        token = request.headers.get('Authorization').split('Bearer ')[1]

        if token:
            decode_token = jwt.decode(token, secret_key, algorithms=['HS256'])
        
            user_info = {
                'id': decode_token.get('id'),
                'name': decode_token.get('name'),
                'email': decode_token.get('email'),
            }
            return jsonify({"data": user_info}), 200
        else:
            return jsonify({"data": None}) , 200

    except Exception as e:
        return jsonify({"data": None}) , 401

# 登入會員 
@users.route('/api/user/auth', methods=['PUT']) 
def login():
    try:
        # 會員由前端輸入資料，透過 fetch 呼叫 api
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        # 後端接收資料到資料庫檢查email和密碼是否配對成功
        user = users_db.get_user(email)
        
        # 將會員的編號、姓名、Email 等關鍵資訊利用 JWT 機制編碼簽名，取得簽名後的 Token，回應給前端
        if user:
            if users_db.check_password(user, password):

                payload = {
                    'id':user.id,
                    'name':user.name,
                    'email':user.email
                    }
                token = jwt.encode(payload, secret_key, algorithm='HS256')
                
                return jsonify({"token":token})

        response = {
            "error": True,
            "message":"登入失敗，帳號或密碼錯誤"
        }
        return jsonify(response)

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500
