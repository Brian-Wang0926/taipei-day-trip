from .models import Attraction, Image 
from sqlalchemy import or_, func
import keyword
from .. import db

class Mrts_Db:
    def get_mrts_query(self):

        # 使用 SQLAlchemy 的 func.count() 函式來計算週邊景點的數量
        subquery = (
            db.session.query(Attraction.mrt, func.count(Attraction.id).label("attraction_count"))
            .filter(Attraction.mrt.isnot(None))
            .group_by(Attraction.mrt)
            .subquery()
            )
        
        mrts_query = (
            db.session.query(subquery.c.mrt, subquery.c.attraction_count)
            .order_by(subquery.c.attraction_count.desc())
        )

        return mrts_query