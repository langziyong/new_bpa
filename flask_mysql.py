import configparser
import os

import pymysql

# 更改运行路径
os.chdir(os.path.dirname(__file__))
# 20210907
# 20211005
# 数据库配置读取
conf = configparser.ConfigParser()
with open('config', encoding = 'utf-8') as f:
    conf.read_file(f)
    host = conf.get('db', 'host')
    user = conf.get('db', 'user')
    password = conf.get('db', 'password')
    database = conf.get('db', 'database')
    port = int(conf.get('db', 'port'))
    f.close()


def get_db():
    db = pymysql.connect(
        host = host,
        user = user,
        password = password,
        database = database,
        port = port,
        charset = 'utf8')
    return db


# 2021/12/27 更新
# updateuserdata  用户数据,字典
def addUser(userdata):
    reply_data = {
        'status':None,
        'data':{}
    }

    sql = '''INSERT INTO user_data(xh, passwd, xm, xy, sjhm, jg, szd, jtdz, tw1, tw2, email) 
             VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');
             ''' % \
          (userdata['xh'], userdata['passwd'], userdata['xm'],
           userdata['xy'], userdata['sjhm'], userdata['jg'], userdata['szd'],
           userdata['jtdz'], userdata['tw1'], userdata['tw2'], userdata['email'])
    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
        db.commit()
    except Exception as e:
        reply_data['status'] = False
        reply_data['error'] = "数据库添加新用户失败。error：" + str(e)
    else:
        new_user = getUser(userdata['xh'])
        if new_user['status'] and len(new_user['data']['user_data']) != 0:
            reply_data['status'] = True
            reply_data['data']['new_user_id'] = new_user['data']['user_data'][0][0]
        else:
            reply_data['status'] = False
            reply_data['error'] = "数据库添加新用户失败。error：已添加但测试查询不通过。"
    try:
        cursor.close()
        db.close()
    except:
        pass
    return reply_data


# 2021/12/29 已更新
# xh = 学号
def getUser(xh):
    reply_data = {
        'status': None,
        'data': {}
    }

    sql = '''
        SELECT * FROM user_data WHERE xh = '%s';''' % xh

    try:
        db = get_db()
        cursor = db.cursor()
        cursor.execute(sql)
    except Exception as e:
        reply_data['status'] = False
        reply_data['error'] = "数据库查询用户失败。error：" + str(e)
    else:
        get_user = cursor.fetchall()
        if get_user is None or len(get_user) != 1 or get_user == '':
            reply_data = {
                'status': True,
                'data': {
                    'user': None
                },
            }
        else:
            _user = get_user[0]
            reply_data['status'] = True
            reply_data['data'] = {
                'user': {
                    'id': _user[0],
                    'xh': _user[1],
                    'passwd': _user[2],
                    'xm': _user[3],
                    'xy': _user[4],
                    'sjhm': _user[5],
                    'jg': _user[6],
                    'szd': _user[7],
                    'jtdz': _user[8],
                    'tw1': _user[9],
                    'tw2': _user[10],
                    'email': _user[11],
                    'zt': _user[12],
                    }
            }
    try:
        cursor.close()
        db.close()
    except:
        pass
    return reply_data


# new_data = 新的用户数据字典
def updateUser(updateuserdata):
    reply_data = None
    db = get_db()
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
