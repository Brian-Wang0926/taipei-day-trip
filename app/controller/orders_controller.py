from flask import Blueprint, request, jsonify, current_app
from ..model.orders_db import Orders_Db
from ..model.attractions_db import Attractions_Db
from ..model.models import Order
import requests
from datetime import datetime
import jwt

orders = Blueprint('orders', __name__)

orders_db = Orders_Db()

global serial_number
serial_number = 1


@orders.route('api/orders', methods=['POST'])
def create_order():
    try:
        orderData = request.get_json()
        token = request.headers.get('Authorization').split('Bearer ')[1]
        if token:
            print("驗證成功")
            prime = orderData['prime']
            order = orderData['order']
            total_price = order['price']
            contact = order['contact']
            url = 'https://sandbox.tappaysdk.com/tpc/payment/pay-by-prime'
            # 按照 Tappay 所需資料格式，整理後提交
            request_data = {
                "prime": prime,
                "partner_key": current_app.config['PARTNER_KEY'],
                "merchant_id": current_app.config['MERCHANT_ID'],
                "details": "TapPay Test",
                "amount": total_price,
                "cardholder": {
                    "phone_number": contact['phone'],
                    "name": contact['name'],
                    "email": contact['email'],
                },
            }

            headers = {
                "Content-Type": "application/json",
                "x-api-key": current_app.config['PARTNER_KEY']
            }

            print("要傳到tappay的資料", request_data)

            response = requests.post(
                url=url, json=request_data, headers=headers)
            print("tappay回傳", response)

            if response.status_code == 200:
                data = response.json()
                print("回傳資料", data)
                if data['status'] == 0:
                    print("銀行授權成功")
                    # 授權成功後，新增訂單到 order 資料庫，並更新 booking 狀態
                    decode_token = jwt.decode(
                        token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
                    user_id = decode_token.get('id')
                    order_id = get_order_id()
                    print("訂單編號", order_id)
                    new_order = Order(
                        id=order_id,
                        total_price=total_price,
                        user_id=user_id,
                        contact_name=contact['name'],
                        contact_email=contact['email'],
                        contact_phone=contact['phone'],
                    )
                    orders_db.create_order(new_order)

                    orders_db.update_bookings(user_id, order_id)
                    print("成功新增order並更新booking")

                    response = {
                        "data": {
                            "number": order_id,
                            "payment": {
                                "status": 0,
                                "message": "付款成功"
                            }
                        }
                    }
                    return jsonify(response), 200

                else:
                    print("銀行授權失敗")
                    print(data['msg'])
                    response = {
                        "error": True,
                        "message": "訂單建立失敗，輸入不正確或其他原因"
                    }
                    return jsonify(response), 400

        else:
            response = {
                "error": True,
                "message": "未登入系統，拒絕存取"
            }
            return jsonify(response), 403
    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500


def get_order_id():
    global serial_number
    current_time = datetime.now()
    formatted_date_time = current_time.strftime("%Y%m%d%H%M%S")
    order_id = f'{formatted_date_time}{serial_number:06d}'
    serial_number += 1
    return order_id


@orders.route('api/order/<int:orderNumber>', methods=['GET'])
def get_order(orderNumber):
    try:
        order, bookings = orders_db.get_order_and_bookings(orderNumber)
        print(order,bookings)
        trip =[]
        attractions_db_instance = Attractions_Db()

        for booking in bookings:
            attraction_id = booking.attraction_id
            date = booking.date.strftime('%Y-%m-%d')
            time = booking.time
            attraction = attractions_db_instance.get_single_attraction(attraction_id)
            attraction_name = attraction.name
            attraction_address = attraction.address
            first_pic = attraction.images[0].img
            booking_info = {
                "attraction": {
                    "id": attraction_id,
                    "name": attraction_name,
                    "address": attraction_address,
                    "pic": first_pic,
                },
                "date": date,
                "time": time,
            }
            print("資料",booking_info)
            trip.append(booking_info)

        print(trip)
        serialized_order = {
            "number": order.id,
            "price": order.total_price,
            "trip": trip,
            "contact": {
                "name": order.contact_name,
                "email": order.contact_email,
                "phone": order.contact_phone
            },
            "status": 1
        }

        response = {
            "data": serialized_order,
        }
        print("回傳資料", response)

        return jsonify(response), 200

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500
