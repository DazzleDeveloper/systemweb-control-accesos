import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root123",
        database="db_systemweb",
        port=3306
    )
