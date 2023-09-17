from .models import Attraction, Image 
from sqlalchemy import or_

class Attractions_Db:
    def get_attractions_query(self, keyword, page):
        page = int(page)
        per_page = 12
        offset = page * per_page # 想成要略過筆數
        # 查詢資料庫資料， keyword 用來完全比對捷運站名稱、或模糊比對景點名稱的關鍵字，沒有給定則不做
        attractions_query = Attraction.query.filter(or_(
            Attraction.name.ilike(f"%{keyword}%"),
            Attraction.mrt == keyword
        ))

        total_count = attractions_query.count()
        attractions_query = attractions_query.offset(offset).limit(per_page)

        return  attractions_query, total_count

    def get_single_attraction(self, id):
        attraction = Attraction.query.get(id)

        return attraction