# # 開啟 connection pool 函式
# from flask import Flask
# import mysql.connector
# from mysql.connector import pooling, Error
# from dotenv import load_dotenv
# import os

# load_dotenv()
# db_username = os.getenv('DB_USERNAME')
# db_password = os.getenv('DB_PASSWORD')

# cnx_pool_config = {
#     "pool_name": "my_connection_pool", 
#     "pool_size": 5,
#     "host": "localhost",
#     "user": "root",
#     "password": db_password,
#     "database": "taipei_trip_db",
#     "buffered": True
# }

# # sql指令, 放進指令的參數, 抓一個或全部
# def get_db(sql, var, result_type):
#     try:
#         cnx_pool = mysql.connector.pooling.MySQLConnectionPool(**cnx_pool_config)
#         cnx = cnx_pool.get_connection()
#         cursor = cnx.cursor(dictionary=True)
#         cursor.execute(sql, tuple(var))

#         if result_type == 'one':
#             result = cursor.fetchone()
#             print("Type of result:", type(result))
#             return result
#         elif result_type == 'all':
#             result = cursor.fetchall()
#             print("Type of result:", type(result))
#             return result
#         elif result_type == 'none':
#             cnx.commit()
#             return None

#     except Error as e:
#         print("Error occured", e)
#     finally:
#         if cnx.is_connected:
#             cursor.close()
#             cnx.close()
#             print("close db connection")


# # 改成 sqlachemy
