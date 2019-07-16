from django.shortcuts import render
from transform import transform
import pymysql
import json
from django.http import HttpResponse
# Create your views here.
def index(request):
    context = {}
    db_pool = transform.get_db_pool(False)
    # 从数据库连接池中取出一条连接
    conn = db_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select songurl,songuuid,total from songurl")
    result=cursor.fetchall()
    conn.close()
    # context['result']=
    # print(context['result'])
    context['data']=result
    return HttpResponse(json.dumps(context), content_type="application/json")

def getCommentByUUID(request):
    uuid=request.GET.get("uuid")
    context={}
    db_pool = transform.get_db_pool(False)
    # 从数据库连接池中取出一条连接
    conn = db_pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute("select * from songcomment where songuuid=%s",uuid)
    result = cursor.fetchall()
    conn.close()
    context['data']=result
    print(context)
    return HttpResponse(json.dumps(context),content_type="application/json")

def commenthtml(request):
    uuid = request.GET.get("uuid")
    return render(request,'comment.html',{"uuid":uuid})
def indexhtml(request):
    return render(request,'hello.html')