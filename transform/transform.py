# -*- coding: utf-8 -*-
"""
数据库连接工具类
# """
import pymysql
import json
import uuid
import ast
from DBUtils.PooledDB import PooledDB, SharedDBConnection
from DBUtils.PersistentDB import PersistentDB, PersistentDBError, NotSupportedError
namespace = uuid.NAMESPACE_URL

config = {
    'host':'47.106.91.135',
    'port':3306,
    'db':'wangyiyun',
    'user':'root',
    'passwd':'jiangweidong',
    'charset':'utf8mb4',
    'use_unicode':True
}

def get_db_pool(is_mult_thread):
    if is_mult_thread:
        poolDB = PooledDB(
            # 指定数据库连接驱动
            creator=pymysql,
            # 连接池允许的最大连接数,0和None表示没有限制
            maxconnections=3,
            # 初始化时,连接池至少创建的空闲连接,0表示不创建
            mincached=2,
            # 连接池中空闲的最多连接数,0和None表示没有限制
            maxcached=5,
            # 连接池中最多共享的连接数量,0和None表示全部共享(其实没什么卵用)
            maxshared=3,
            # 连接池中如果没有可用共享连接后,是否阻塞等待,True表示等等,
            # False表示不等待然后报错
            blocking=True,
            # 开始会话前执行的命令列表
            setsession=[],
            # ping Mysql服务器检查服务是否可用
            ping=0,
            **config
        )
    else:
        poolDB = PersistentDB(
            # 指定数据库连接驱动
            creator=pymysql,
            # 一个连接最大复用次数,0或者None表示没有限制,默认为0
            maxusage=1000,
            **config
        )
    return poolDB


if __name__ == '__main__':
    # 以单线程的方式初始化数据库连接池
    db_pool = get_db_pool(False)
    # 从数据库连接池中取出一条连接
    conn = db_pool.connection()
    cursor = conn.cursor()
    cursor.execute('select song_url,song_comments from wangyiyun')
    # 随便取一条查询结果
    result = cursor.fetchall()
    for i in range(len(result)):
        # data=json.dumps(ast.literal_eval(result[i][1]))
        data = json.dumps(ast.literal_eval(result[i][1]))
        res = json.loads(data, encoding='utf-8')
        print(res)
        song_url = result[i][0]
        hotComments=res['hotComments']
        print(song_url)
        total=res['total']
        sql="insert into songurl(songurl,songuuid,total) values (%s,%s,%s)"
        uuidss=str(uuid.uuid1())
        cursor.execute(sql,(song_url,uuidss,total))
        conn.commit()
        comments=res['comments']
        print("================================")
        for j in range(len(hotComments)):
                contents=hotComments[j]['content']
                likeCount=hotComments[j]['likedCount']
                nickname=hotComments[j]['user']['nickname']
                avatarUrl=hotComments[j]['user']['avatarUrl']
                sql="insert into songcomment(content,songuuid,avatarUrl,nickname,likeCount) values(%s,%s,%s,%s,%s)"
                cursor.execute(sql,(contents,uuidss,avatarUrl,nickname,likeCount))
                conn.commit()
                print()

        for avh in range(len(comments)):
                contents=comments[avh]['content']
                nickname=comments[avh]['user']['nickname']
                avatarUrl=comments[avh]['user']['avatarUrl']
                likeCount=comments[avh]['likedCount']
                sql="insert into songcomment(content,songuuid,avatarUrl,nickname,likeCount) values(%s,%s,%s,%s,%s)"
                cursor.execute(sql,(contents,uuidss,avatarUrl,nickname,likeCount))
                conn.commit()
                print()

        conn.close()
