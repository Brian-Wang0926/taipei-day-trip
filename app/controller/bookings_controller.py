from flask import Blueprint, request, jsonify, current_app
from ..model.bookings_db import Bookings_Db
from ..model.models import Booking
import jwt

bookings = Blueprint('bookings', __name__)
bookings_db = Bookings_Db()

# 取得尚未確認下單的預定行程資料
@bookings.route('api/booking', methods=['GET'])
def get_booking():
    try:
        print("成功進入booking get api")
        token = request.headers.get('Authorization').split('Bearer ')[1]
        if token:
            decode_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = decode_token.get('id')
            user_name = decode_token.get('name')
            user_email = decode_token.get('email')

            #  透過 user_id 到資料庫取得資料
            booking_data = bookings_db.get_booking(user_id)
            print("tttt",booking_data)
            if booking_data:
                data = {
                    "data":booking_data,
                    "user_name":user_name,
                    "user_email":user_email
                }
                print("有資料",data)
                return jsonify(data), 200
            else:
                print("沒有任何資料")
                data = {
                    "data":None,
                    "user_name":user_name,
                    "user_email":user_email
                }
                return jsonify(data) , 200
        else:
            response = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            return jsonify(response) , 403
    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500

# 建立新的預定行程資訊
@bookings.route('api/booking', methods=['POST'])
def create_booking():
    try:
        bookingData = request.get_json()
        attraction_id = bookingData.get('attractionId')
        date = bookingData.get('date')
        time = bookingData.get('time')
        price = bookingData.get('price')
        # 取得token資料
        token = request.headers.get('Authorization').split('Bearer ')[1]
        if token:
            decode_token = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = decode_token.get('id')

            # 加入資料庫
            new_booking = Booking(
                attraction_id=attraction_id,
                user_id=user_id,
                date=date,
                time=time,
                price=price
            )
            bookings_db.create_booking(new_booking)

            response = {
                "ok": True,
            }
            return jsonify(response), 200
            
        else:       
            response = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            return jsonify(response) , 403

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500


# 刪除目前的預定行程
@bookings.route('api/booking/<int:bookingId>', methods=['DELETE'])
def delete_booking(bookingId):
    try:
        print("預定景點刪除 api")
        bookings_db.delete_booking(bookingId)
        print("預定景點刪除成功")

        response = {
            "ok": True,
        }
        
        return jsonify(response), 200

    except Exception as e:
        response = {
            "error": True,
            "message": "未登入系統，拒絕存取"
        }
        return jsonify(response), 403