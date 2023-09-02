# 已執行過
# 將資料抓進資料庫

import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv
import json, os, re

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

cnx_pool_config = {
    "pool_name": "my_connection_pool", 
    "pool_size": 5,
    "host": "localhost",
    "user": "root",
    "password": db_password,
    "database": "taipei_trip_db",
    "buffered": True
}

cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**cnx_pool_config)
cnx = cnx_pool.get_connection()
cursor = cnx.cursor()


with open('data/taipei-attractions.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    attractions = data['result']['results']

    for attraction in attractions:
        id = attraction['_id']
        name = attraction['name']
        category = attraction['CAT']
        description = attraction['description']
        address = attraction['address']
        transport = attraction['direction']
        mrt = attraction['MRT']
        lat = float(attraction['latitude'])
        lng = float(attraction['longitude'])

        # query = "INSERT INTO attractions (id, name, category, description, address, transport, mrt, lat, lng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(query,(id, name, category, description, address, transport, mrt, lat, lng))

        # 照片
        urls = attraction['file'].split('https')
        imgs = ['https' + i for i in urls if i.endswith(('.jpg','JPG','.png','.PNG'))]

        for img in imgs:
            # img_query = "INSERT INTO images(attraction_id, img) VALUES (%s, %s)"
            cursor.execute(img_query,(id, img))

cnx.commit()
cursor.close()
cnx.close()


