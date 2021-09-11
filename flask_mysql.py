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
    reply_data = None
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        port = 3306,
        charset = 'utf8')
    cursor = db.cursor()
    for i in updateuserdata:
        if i == 'xh':
            continue
        sql = f'''UPDATE  user_data
                  SET {i} = '{updateuserdata[i]}'
                  WHERE xh = '{updateuserdata['xh']}';'''
        try:
            cursor.execute(sql)
            db.commit()
        except:
            db.rollback()
            reply_data = False
            print("数据库数据更新失败。")
            break
        print(f"学号：{updateuserdata['xh']} 字段：{i} 更新为{updateuserdata[i]}")
        reply_data = True

    cursor.close()
    db.close()
    return reply_data
