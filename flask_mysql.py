import pymysql


# 20210907

# updateuserdata = 用户数据字典
def addUser(updateuserdata):
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        port = 3306,
        charset = 'utf8')
    cursor = db.cursor()
    sql = '''INSERT INTO user_data(xh, mm, xm, xy, sjhm, dz1, dz2, xxdz, tw1, tw2, email) 
             VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
             ''' % \
          (updateuserdata['xh'], updateuserdata['mm'], updateuserdata['xm'],
           updateuserdata['xy'], updateuserdata['sjhm'], updateuserdata['dz1'], updateuserdata['dz2'],
           updateuserdata['xxdz'], updateuserdata['tw1'], updateuserdata['tw2'], updateuserdata['email'])
    try:
        cursor.execute(sql)
        db.commit()
        reply_data = 'Success!'
    except:
        db.rollback()
        reply_data = False
    cursor.close()
    db.close()
    return reply_data


# xh = 学号
def getUser(xh):
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        charset = 'utf8',
        port = 3306
    )
    cursor = db.cursor()
    sql = '''
    SELECT * FROM user_data WHERE xh = '%s';''' % xh
    try:
        cursor.execute(sql)
        reply_data = cursor.fetchall()
    except:
        reply_data = False
    cursor.close()
    db.close()
    return reply_data


# new_data = 新的用户数据字典
def updateUser(updateuserdata):
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        port = 3306,
        charset = 'utf8')
    cursor = db.cursor()
    cursor.execute('select count(1) from user_data')
    print(updateuserdata)
    id_number = cursor.fetchall()[0][0] + 1
    sql = '''UPDATE  user_data
             SET mm = '%s', xm = '%s', xy = '%s', sjhm = '%s', dz1 = '%s',dz2 = '%s', xxdz = '%s', tw1 = '%s', tw2 = '%s', email = '%s'
             WHERE xh = '%s';
             ''' % \
          (updateuserdata['mm'], updateuserdata['xm'], updateuserdata['xy'],
           updateuserdata['sjhm'], updateuserdata['dz1'], updateuserdata['dz2'],
           updateuserdata['xxdz'], updateuserdata['tw1'], updateuserdata['tw2'],
           updateuserdata['email'], updateuserdata['xh'])
    print(sql)
    try:
        cursor.execute(sql)
        db.commit()
        reply_data = 'Update Success!'
    except:
        db.rollback()
        reply_data = False
    cursor.close()
    db.close()
    return reply_data