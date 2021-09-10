import auto_bpa
import pymysql


def main():  # 主程序 筛选 zt = 0 的用户
    db = pymysql.connect(
        host = '114.55.140.138',
        user = 'root',
        password = "lzy0812..",
        database = 'bpa_user_data',
        port = 3306,
        charset = 'utf8')
    cursor = db.cursor()
    sql = '''
    SELECT * 
    FROM user_data 
    WHERE zt = 0'''
    try:
        cursor.execute(sql)
        reply_data = cursor.fetchall()
    except:
        db.rollback()
        reply_data = False
    cursor.close()
    db.close()

    all_user_data = reply_data

    if len(all_user_data):
        print('无可执行对象')
    elif not reply_data:
        print('数据库查询失败')

    for user in all_user_data:
        user = list(user)
        auto_bpa.bpa(user)


if __name__ == '__main__':
    main()
