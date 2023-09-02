from flask import Blueprint, request, jsonify
from ..model.attractions_db import Attractions_Db
from flask_sqlalchemy import Pagination

attractions = Blueprint('attractions', __name__)

@attractions.route('api/attractions', methods=['GET'])
def get_attractions():
    try:
        page = request.args.get('page', default=0, type=int)
        keyword = request.args.get('keyword', default="", type=str)
        
        attractions_db_instance = Attractions_Db()
        attractions_query, total_count  = attractions_db_instance.get_attractions_query(keyword, page)

        per_page = 12
        attractions = attractions_query.all()
        # attractions_pagination = attractions_query.paginate(page=page, per_page=per_page, error_out=False)

        serialized_attractions = [{
            "id": attraction.id,
            "name": attraction.name,
            "category": attraction.category,
            "description": attraction.description,
            "address": attraction.address,
            "transport": attraction.transport,
            "mrt": attraction.mrt,
            "lat": attraction.lat,
            "lng": attraction.lng,
            "images": [image.img for image in attraction.images]
        } for attraction in attractions]

        total_pages = (total_count + per_page - 1) // per_page
        
        # current_page = page + 1

        response = {
            "nextPage": page + 1 if page < total_pages else None, 
            "data": serialized_attractions,
        }
        # raise Exception("Something went wrong")
        return jsonify(response)

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500


@attractions.route('api/attraction/<int:attractionId>', methods=['GET'])
def get_attraction(attractionId):

    try:
        attractions_db_instance = Attractions_Db()
        attraction = attractions_db_instance.get_single_attraction(attractionId)

        if attraction is None:
            response = {
                "error": True,
                "message": "景點編號不正確"
            }
            return jsonify(response), 404

        serialized_attraction = [{
            "id": attraction.id,
            "name": attraction.name,
            "category": attraction.category,
            "description": attraction.description,
            "address": attraction.address,
            "transport": attraction.transport,
            "mrt": attraction.mrt,
            "lat": attraction.lat,
            "lng": attraction.lng,
            "images": [image.img for image in attraction.images]
        }]
        
        response = { 
        "data": serialized_attraction,
        }

        return jsonify(response)

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }
        return jsonify(response), 500
