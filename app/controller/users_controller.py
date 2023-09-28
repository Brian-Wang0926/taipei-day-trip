from flask import Blueprint, request, jsonify, current_app
from ..model.users_db import Users_Db
from ..model.models import User
import jwt
from datetime import datetime, timedelta

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
        print("是否存在使用者", existing_user)

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
            return jsonify(response), 400

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
            
            decode_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        
            user_info = {
                'id': decode_token.get('id'),
                'name': decode_token.get('name'),
                'email': decode_token.get('email'),
            }
            return jsonify({"data": user_info}), 200
        else:
            return jsonify({"data": None}) , 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": True, "message": "Token已過期"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": True, "message": "無效的Token"}), 401
    except Exception as e:
        return jsonify({"data": None}) , 401

# 登入會員 
@users.route('/api/user/auth', methods=['PUT']) 
def login():
    try:
        print("登入api")
        # 會員由前端輸入資料，透過 fetch 呼叫 api
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        # 後端接收資料到資料庫檢查email和密碼是否配對成功
        user = users_db.get_user(email)
        print("取得資料",data, email, password, user)

        # 將會員的編號、姓名、Email 等關鍵資訊利用 JWT 機制編碼簽名，取得簽名後的 Token，回應給前端
        if user:
            print("有使用者帳號")
            if users_db.check_password(user, password):
                print("密碼確認")
                expiration_time = datetime.utcnow() + timedelta(days=7)
                payload = {
                    'id':user.id,
                    'name':user.name,
                    'email':user.email,
                    'exp':expiration_time
                    }
                token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
                print("取得token", token)
                return jsonify({"token":token}), 200
            else:
                return jsonify({"error": True, "message": "登入失敗，帳號或密碼錯誤"}), 400
        else:
            return jsonify({"error": True, "message": "登入失敗，帳號或密碼錯誤"}), 400

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500
