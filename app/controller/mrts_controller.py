from flask import Blueprint, request, jsonify, Response
from ..model.mrts_db import Mrts_Db
import json

# 取得所有捷運站名稱列表，按照週邊景點的數量由大到小排序

mrts = Blueprint('mrts', __name__)

@mrts.route('api/mrts', methods=['GET'])
def get_mrts():
    try:
        mrts_db_instance = Mrts_Db()
        mrts_query = mrts_db_instance.get_mrts_query()

        mrts = mrts_query.all()

        mrts_list =[
            mrt[0] for mrt in mrts
        ]

        response = {
            "data": mrts_list
        }

        # response_json = json.dumps(response, ensure_ascii=False)
        # return Response(response_json, content_type='application/json; charset=utf-8')

        return jsonify(response)

    except Exception as e:
        response = {
            "error": True,
            "message": "伺服器內部錯誤"
        }

        # response_json = json.dumps(response, ensure_ascii=False)
        # return Response(response_json, content_type='application/json; charset=utf-8'), 500

        return jsonify(response)