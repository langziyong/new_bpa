import pymysql


def addUser(newuserdata):
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        port = 3306)
    cursor = db.cursor()
    cursor.execute('select count(1) from user_data')
    id_number = cursor.fetchall()[0][0] + 1
    sql = '''INSERT INTO user_data(id, xh, xm, mm, xy, sjhm, dz1, dz2, xxdz, tw1, tw2, email) 
             VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
             ''' % \
          (id_number, newuserdata['xh'], newuserdata['xm'], newuserdata['mm'],
           newuserdata['xy'], newuserdata['sjhm'], newuserdata['dz1'], newuserdata['dz2'],
           newuserdata['xxdz'], newuserdata['tw1'], newuserdata['tw2'], newuserdata['email'])

    try:
        cursor.execute(sql)
        db.commit()
        db.close()
        return True
    except:
        db.rollback()
        db.close()
        return False


def getUser(xh):
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        port = 3306)
    cursor = db.cursor()
    sql = '''
    SELECT * From user_data WHERE xh = '%s';''' % xh
    cursor.execute(sql)
    print(sql)
    data = cursor.fetchall()
    db.close()
    print(data)
    return data
