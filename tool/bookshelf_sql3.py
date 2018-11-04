import MySQLdb
import MySQLdb.cursors as cursors
from datetime import datetime



try:
    # 开始时间
    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='root',
        db='xiaoshubao',
        charset='utf8',
        cursorclass=cursors.SSCursor)

    conn2 = MySQLdb.connect(
        host='60.171.117.207',
        user='root',
        passwd='chenbenshouchenbenxing123!@#',
        db='shubao',
        charset='utf8')
    # conn3 = MySQLdb.connect(
    #     host='60.171.117.207',
    #     user='cbscbx',
    #     passwd='chenbenshouchenbenxing5566778899',
    #     db='shubao',
    #     charset='utf8')
    # conn4 = MySQLdb.connect(
    #     host='60.171.117.207',
    #     user='cbscbx',
    #     passwd='chenbenshouchenbenxing5566778899',
    #     db='shubao',
    #     charset='utf8')
    cursor = conn.cursor()
    cursor2 = conn2.cursor()
    # cursor3 = conn3.cursor()
    # cursor4 = conn4.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute('set global max_allowed_packet = 67108864')
    cursor2.execute('set global max_allowed_packet = 67108864')
    cursor.execute(
        "select * from jieqi_article_bookcase where caseid > 1511123  and caseid<=1611123 order by caseid asc")
    # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()


    batch_size = 10

    while True:

        # 每次获取时会从上次游标的位置开始移动size个位置，返回size条数据
        data = cursor.fetchmany(batch_size)

        # 数据为空的时候中断循环
        if not data:
            print('没有数据了')
            break
        else:

            for item in data:
                novel_old_id = item[1]
                olduserid = item[4]
                chapterid = item[6]

                user_sql = """
                    select * from users_userprofile where olduserid = %s
                """
                cursor2.execute(user_sql, (olduserid,))
                user = cursor2.fetchone()


                if user:
                    newuserid = user[0]
                    book_sql = """
                                        select * from novels_noveldetail where novel_old_id = %s 
                                    """
                    cursor2.execute(book_sql, (novel_old_id,))

                    book = cursor2.fetchone()



                    if book:
                        newbookid = book[2]
                        chapter_sql = """
                                            select * from novels_novelchapter where chapter_old_id = %s 
                                        """

                        cursor2.execute(chapter_sql, (chapterid,))
                        chapter = cursor2.fetchone()

                        if not chapter:
                            chapter_sql = """
                                                select * from novels_novelchapter where noveldetail_id = %s  order by chapter_order asc limit 1
                                            """

                            cursor2.execute(chapter_sql, (newbookid,))
                            chapter = cursor2.fetchone()


                        if chapter:
                            newchapterid = chapter[2]
                            sql = """
                                 insert into operation_novelfavorite(chapterid,novel_id,user_id,create_time,update_time)VALUES (%s,%s, %s, %s ,%s) ON DUPLICATE KEY UPDATE novel_id=VALUES(novel_id),user_id=VALUES(user_id)

                                 """
                            t = datetime.now()
                            params = (
                                newchapterid,
                                newbookid,
                                newuserid,
                                t,
                                t
                            )

                            cursor2.execute(sql, params)
                            conn2.commit()

                            print('%s 书架添加完毕'%item[0])

                        else:
                            print('书籍 %s 的章节不存在' % novel_old_id)

                    else:
                        print('书籍 %s 不存在' % novel_old_id)

                else:
                    print('用户 %s 不存在'%olduserid)

except Exception as e:
    print(e)

# 关闭数据库连接
cursor.close()
conn.close()

cursor2.close()
conn2.close()

