from .models import Booking, User, Attraction
from .. import db
from sqlalchemy import and_


class Bookings_Db:
    # 建立新預定訂單
    def create_booking(self, booking):
        try:
            db.session.add(booking)
            print("新增")
            db.session.commit()
            print("資料庫建立成功")
        except Exception as e:
            db.session.rollback()
            print("資料庫建立失敗")
            print(str(e))
            return "建立失敗，輸入不正確或其他原因", 400

    def get_booking(self, user_id):
        # 透過 user_id 取得 name, 以及她的所有 booking_id
        print("開始資料庫")
        user = User.query.filter_by(id=user_id).first()
        user_name = user.name
        user_email = user.email

        # bookings = Booking.query.filter_by(user_id=user_id).all()
        bookings = Booking.query.filter(
            and_(Booking.user_id == user_id, Booking.payment_status == False)
        ).all()

        booking_data = []
        # 透過 booking_id，取得 attraction_id, date, time, price
        # 透過 attraction_id 取得 name, pic(第一張)
        for booking in bookings:
            attraction_id = booking.attraction_id
            date = booking.date.strftime('%Y-%m-%d')
            time = booking.time
            price = booking.price
            booking_id = booking.id
            print("booking", attraction_id, date, time, price, booking_id)

            attraction = Attraction.query.filter_by(id=attraction_id).first()
            attraction_name = attraction.name
            attraction_address = attraction.address
            first_pic = attraction.images[0].img

            booking_info = {
                "attraction": {
                    "id": attraction_id,
                    "attraction_name": attraction_name,
                    "attraction_address": attraction_address,
                    "pic": first_pic,
                },
                "date": date,
                "time": time,
                "price": price,
                "booking_id": booking_id
            }

            booking_data.append(booking_info)

        return booking_data

    def delete_booking(self, booking_id):
        try:
            print("資料庫刪除預定景點")
            booking_to_delete = Booking.query.filter_by(id=booking_id).first()
            db.session.delete(booking_to_delete)
            db.session.commit()
            print("資料庫刪除預定景點成功")
        except Exception as e:
            db.session.rollback()
            print("資料庫刪除失敗")
            print(str(e))
            raise e
