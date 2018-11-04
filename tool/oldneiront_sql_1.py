import MySQLdb
import MySQLdb.cursors as cursors
import base64
import urllib.parse

def encryption_urllib_base64(v):
    """
    加密
    """
    s = bytes(v, encoding="utf8")
    s = base64.b64encode(s)
    s = str(s, encoding="utf-8")
    return urllib.parse.quote(s)


def decrypt_urllib_base64(v):
    s = urllib.parse.unquote(v)
    s = bytes(s, encoding="utf8")
    s = base64.b64decode(s)
    return str(s, encoding="utf-8")
try:

    conn = MySQLdb.connect(
        host='127.0.0.1',
        user='root',
        passwd='123456',
        db='dashubao',
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
    # 使用execute方法执行SQL语句 1850000
    #cursor.execute('set global max_allowed_packet = 67108864')
    cursor.execute(
        "select id , content from novels_novelcontent where id >92863 and id<= 1000000  order by id asc")
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
                id ,content = item
                jiami_c = encryption_urllib_base64(content)
                sql = """
                    update novels_novelcontent set content = %s where id = %s
                 """

                params = (jiami_c, id)

                cursor2.execute(sql, params)

                conn2.commit()

                print('%s 更新成功' % id)

except Exception as e:
    print(e)


# 关闭数据库连接
cursor.close()
conn.close()

cursor2.close()
conn2.close()