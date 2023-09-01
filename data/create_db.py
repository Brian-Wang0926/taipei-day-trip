# 建立 mysql 資料庫
# 可改成 sqlachemy 串接 mysql 

import mysql.connector
from mysql.connector import pooling
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')

cnx_pool_config = {
    "pool_name": "my_connection_pool", 
    "pool_size": 5,
    "host": "localhost",
    "user": "root",
    "password": db_password,
    "buffered": True
}

cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**cnx_pool_config)
cnx = cnx_pool.get_connection()
cursor = cnx.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS taipei_trip_db")
cursor.execute("USE taipei_trip_db")
# cursor.execute("CREATE TABLE IF NOT EXISTS attractions (id INT PRIMARY KEY, name VARCHAR(255), address VARCHAR(255), category VARCHAR(255), transport TEXT(65535), description TEXT(65535), mrt VARCHAR(255), latitude FLOAT, longitude FLOAT)")
# cursor.execute("CREATE TABLE IF NOT EXISTS images (id INT PRIMARY KEY AUTO_INCREMENT, attraction_id INT, img VARCHAR(255), FOREIGN KEY (attraction_id) REFERENCES attractions(id))")
cnx.commit()
cursor.close()
cnx.close()

