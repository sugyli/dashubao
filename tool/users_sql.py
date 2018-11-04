import MySQLdb
import MySQLdb.cursors as cursors
from datetime import datetime
try:
    # 开始时间
    start_time = datetime.now()
    print(start_time)
    conn = MySQLdb.connect(
        host='98.126.65.66',
        user='root',
        passwd='chenbenshouchenbenxing!@#123',
        db='xiaoshubao',
        charset='utf8',
        cursorclass=cursors.SSCursor)

    conn2 = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        db='dashubao',
        charset='utf8')
    cursor = conn.cursor()
    cursor2 = conn2.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute(
        "select * from jieqi_system_users where pass != '' and groupid = 3 and uname != ''  order by uid asc")
    # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()

    count = 0
    batch_size = 100
    while True:
        count = count + 1
        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = cursor.fetchmany(batch_size)

        # 数据为空的时候中断循环
        if not data:
            print('没有数据了')
            break
        else:
            for item in data:
                print('获取到 %s 的数据 准备添加'%item[2])
                sql = """
                insert into users_userprofile(username,password, old_password,score,olduserid,is_superuser,first_name,last_name,email,is_staff,is_active,date_joined,gender)
                    VALUES (%s, %s, %s ,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE old_password=VALUES(old_password),score=VALUES(score),email=VALUES(email),olduserid=VALUES(olduserid)

                """
                d = datetime.fromtimestamp(item[6]).strftime("%Y-%m-%d %H:%M:%S")
                params = (item[2], item[4], item[4], item[31], item[0], 0,'','','%s@123.com'%item[2],0,1,d,'male')
                cursor2.execute(sql, params)
                # 提交到数据库执行
                conn2.commit()
                print('%s 的数据入库成功'%item[2])


        print('获取%s到%s数据成功' % ((count - 1) * batch_size, count * batch_size-1))
        print('fetchmany获取全量数据所用时间:', (datetime.now() - start_time).seconds)


    # 关闭数据库连接
    cursor.close()
    conn.close()

    cursor2.close()
    conn2.close()

except Exception as e:
    print(e)
