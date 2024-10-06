import mysql.connector
cnx =None
def get_sql_connect():
    global cnx
    if cnx is None:
        cnx = mysql.connector.connect(user='sql12734431', password='nCDegURrDs',
                                host='sql12.freesqldatabase.com',
                                database='sql12734431',port=3306)
    return cnx

def get_cursor():
    connection = get_sql_connect()
    return connection.cursor(buffered=True)