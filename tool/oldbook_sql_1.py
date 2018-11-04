import MySQLdb
import MySQLdb.cursors as cursors


try:

    conn = MySQLdb.connect(
        host='60.171.117.207',
        user='cbscbx',
        passwd='chenbenshouchenbenxing5566778899',
        db='shubao',
        charset='utf8',
        cursorclass=cursors.SSCursor)
    conn2 = MySQLdb.connect(
        host='60.171.117.207',
        user='cbscbx',
        passwd='chenbenshouchenbenxing5566778899',
        db='shubao',
        charset='utf8')

    cursor = conn.cursor()
    cursor2 = conn2.cursor()
    # 使用execute方法执行SQL语句
    #cursor.execute('set global max_allowed_packet = 67108864')
    cursor.execute(
        "select * from novels_noveldetail where novel_old_id > 89999 and novel_old_id<= 98000 order by novel_old_id asc")
    # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()

    batch_size = 1000

    while True:

        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = cursor.fetchmany(batch_size)

        # 数据为空的时候中断循环
        if not data:
            print('没有数据了')
            break
        else:
            for item in data:

                sql = """
                 select count(*) from novels_novelchapter where noveldetail_id = %s
                
                 """
                cursor2.execute(sql, (item[2],))
                count = cursor2.fetchone()[0]
                if count > 0:
                    sql1 = """
                     update novels_noveldetail set have_chapter = 1 where url_md5 = %s

                     """
                    cursor2.execute(sql1, (item[2],))
                    conn2.commit()
                    print('%s 更新成功' % item[3])
                else:
                    print('%s 没有章节'%item[3])

except Exception as e:
    print(e)


# 关闭数据库连接
cursor.close()
conn.close()

cursor2.close()
conn2.close()