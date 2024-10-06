import mysql.connector
cnx =None
def get_sql_connect():
    global cnx
    if cnx is None:
        cnx = mysql.connector.connect(user='root', password='root',
                                host='127.0.0.1',
                                database='db',port=3306)
    return cnx

def get_cursor():
    connection = get_sql_connect()
    return connection.cursor(buffered=True)