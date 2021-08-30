import pymysql


def addUser(newuserdata):
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        port = 3306)
    cursor = db.cursor()
    cursor.execute('SELECT * from user_data')
    data = cursor.fetchone()