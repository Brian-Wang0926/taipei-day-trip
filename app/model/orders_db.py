from .models import Order, Booking
from .. import db
from sqlalchemy import and_
# from .models import Booking

# booking = Booking()


class Orders_Db:
    # 新增 order，並更新 booking 的 payment_status 及 order_id
    def create_order(self, new_order):
        try:
            print("order資料庫")
            db.session.add(new_order)
            db.session.commit()
            print("新增成功")
        except Exception as e:
            db.session.rollback()
            raise e

    def get_order_and_bookings(self, order_id):
        # 根據 order_id 取得 order 資訊以及 booking
        try:
            print("執行資料庫抓取order及booking")
            order = Order.query.filter_by(id=order_id).first()

            if order:
                bookings = Booking.query.filter_by(order_id=order.id).all()
                print("成功執行資料庫抓取order及booking")
                return order, bookings
            else:
                return None, None
        except Exception as e:
            db.session.rollback()
            raise e

    def update_bookings(self, user_id, order_id):
        try:
            # user_bookings = Booking.query.filter_by(user_id = user_id).all()
            user_bookings = Booking.query.filter(
                and_(Booking.user_id == user_id,
                     Booking.payment_status == False)
            ).all()
            print("於更新booking中抓取booking", user_bookings)
            for booking in user_bookings:
                booking.mark_payment_completed(order_id)
            print("更新booking")
            db.session.commit()

        except Exception as e:
            db.session.rollback()
            raise e
