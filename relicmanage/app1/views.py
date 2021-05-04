import socket

import xlrd
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, FileResponse
from datetime import datetime
import os
from django.template import Template, Context
from . import models
from django.contrib import messages, auth
from django.utils import timezone #引入timezone模块
import datetime
import time
from django.core.files.base import ContentFile
from collections import Counter
import numpy as np
import json


from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

from django.contrib.auth.models import User




# Create your views here.
'''用户列表'''
def user_list(request):
    users = models.Visitor.objects.filter(is_delete=0)
    return render(request, 'user_list.html', {'user_list': users})


'''文物列表'''
def relic_list(request):
    relics = models.Relic.objects.filter(is_delete=0)
    return render(request, 'relic_list.html', {'relic_list': relics})


'''照片列表'''
def photo_list(request):
    photos = models.Photo.objects.values('photo')
    photo_dict = np.array(photos)
    photo_dict = photo_dict[::-1]
    photo_list = []
    temp = []
    for i, photo in enumerate(photo_dict, 1):
        photo_url = photo['photo']
        temp.append(photo_url)
        if i%3 == 0:
            photo_list.append(temp)
            temp = []
    # print(photo_list)

    return render(request, 'photo_list.html', {'photo_list': photo_list})


'''视频列表'''
def video_list(request):
    videos = models.Video.objects.all()
    return render(request, 'video_list.html', {'video_list': videos})


'''添加用户'''
def add_user(request):
    if request.method == 'POST':
        new_user_name = request.POST.get('user_name')
        new_phone = request.POST.get('phone')
        new_sex = request.POST.get('sex')
        new_city = request.POST.get('city')
        models.Visitor.objects.create(user_name=new_user_name, phone=new_phone, sex=new_sex, city=new_city)
        return redirect('/user_list/') #重定向
    return render(request, 'add_user.html')


'''修改用户备注'''
def remark_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('data')
        new_remark_content = request.POST.get('content')
        models.Visitor.objects.extra(where=['id IN (' + user_id + ')']).update(other=new_remark_content)
        return redirect('/user_list/') #重定向
    # return render(request, 'add_user.html')


'''删除用户'''
def delete_user(request):
    if request.method == 'POST':
        # if not request.user.is_authenticated: # 判断用户登录状态
        #     return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        ids = request.POST.get('data')  # django接收数组
        print(ids)
        try:
            models.Visitor.objects.extra(where=['id IN (' + ids + ')']).update(is_delete=1)
        except:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')
    return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')


'''上传excel并添加用户'''
def upload_user(request):
    data = {'code': 0, 'msg': '上传成功', 'data': []}

    f = request.FILES.get('file', '')
    file_type = f.name.split('.')[1]  # 拿到文件后缀
    if file_type in ['xlsx', 'xls']:  # 支持这两种文件格式
        wb = xlrd.open_workbook(filename=None, file_contents=f.read())

    table = wb.sheets()[0]  #sheet0
    nrows = table.nrows  # 行数
    print('nrows', nrows)
    try:
        for i in range(1, nrows):  # 从0开始把表头省略则读取表头信息,如果从1开始则直接读取数据
            rowValues = table.row_values(i)  # 一行的数据
            print(rowValues[0], str(int(rowValues[1])), rowValues[2], rowValues[3])
            print('-----------')
            models.Visitor.objects.create(user_name=rowValues[0], phone=str(int(rowValues[1])), sex=rowValues[2], city=rowValues[3])

    except Exception as e:
        data["msg"] = '上传失败'
        print('??????????????')
        return JsonResponse(data)
    return JsonResponse(data)


# def get_sheets_mg(data, num):      # data:Excel数据对象，num要读取的表
#     table = data.sheets()[num]  # 打开第一张表
#     nrows = table.nrows  # 获取表的行数
#     ncole = table.ncols  # 获取列数
#     all_list = []
#     for i in range(nrows):  # 循环逐行打印
#         one_list = []
#         for j in range(ncole):
#             cell_value = table.row_values(i)[j]
#             one_list.append(cell_value)
#         all_list.append(one_list)
#     del (all_list[0])  # 删除标题   如果Excel文件中第一行是标题可删除掉，如果没有就不需要这行代码
#     return all_list


'''添加文物'''
def add_relic(request):
    if request.method == 'POST':
        new_relic_name = request.POST.get('relic_name')
        new_dynamic = request.POST.get('dynamic')
        new_pic = request.POST.get('pic')
        new_file = request.POST.get('model')
        new_type = request.POST.get('type')

        pic_name = int(time.time())
        pic_name = (pic_name + new_pic.name) if new_pic else ''

        if pic_name:
            destination = open(os.path.join("../../upload/pic/", pic_name), 'wb+')    # 打开特定的文件进行二进制的写操作
            for chunk in new_pic.chunks():
                destination.write(chunk)
            destination.close()


        model_name = int(time.time())
        model_name = (model_name + new_file.name) if new_file else ''

        if model_name:
            destination = open(os.path.join("../../upload/model/", model_name), 'wb+')    # 打开特定的文件进行二进制的写操作
            for chunk in new_file.chunks():
                destination.write(chunk)
            destination.close()

        models.Relic.objects.create(relic_name=new_relic_name, dynamic=new_dynamic, picture=pic_name, relic_file=model_name, type = new_type)
        return redirect('/relic_list/') #重定向
    return render(request, 'relic_list.html')


'''删除文物'''
def delete_relic(request):
    if request.method == 'POST':
        # if not request.user.is_authenticated: # 判断用户登录状态
        #     return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        ids = request.POST.get('data')  # django接收数组
        try:
            models.Relic.objects.extra(where=['id IN (' + ids + ')']).update(is_delete=1)
        except:
            return HttpResponse('{"status":"fail", "msg":"删除失败"}', content_type='application/json')
    return HttpResponse('{"status":"success", "msg":"删除成功"}', content_type='application/json')


def upload_photo(request):
    f = request.FILES['img']

    # image_data = [f.file, f.field_name, f.name, f.content_type,
    #               f.size, f.charset, f.content_type_extra]

    f_name = f.name
    relic_id = f_name.split('_')[0]
    relic_id = str(relic_id)
    if not is_number(relic_id[0]):
        relic_id = '1'

    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:

        models.Photo.objects.create(photo=f, relic=relic_id, add_time=str(t))

        hot_last = models.Relic.objects.get(id=relic_id)
        hot_last = hot_last.hot
        hot_new = hot_last + 1

        models.Relic.objects.extra(where=['id IN (' + relic_id + ')']).update(hot=hot_new)
    except Exception as e:
        print('?????????????')
        print(e)
        return render(request, 'photo_list.html')
    return HttpResponse('{"res":"success", "msg":"添加成功"}', content_type='application/json')


def upload_video(request):
    f = request.FILES['video']

    file_data = [f.file, f.name, f.content_type,
                  f.size, f.charset, f.content_type_extra]

    f_name = f.name
    relic_id = f_name.split('_')[0]
    relic_id = str(relic_id)
    if not is_number(relic_id[0]):
        relic_id = '1'

    t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    try:
        relic = models.Relic.objects.get(id=relic_id)
        relic_name = relic.relic_name

        models.Video.objects.create(video=f, relic_id=relic_id, relic_name=relic_name, add_time=str(t))

        hot_last = relic.hot
        hot_new = hot_last + 1

        models.Relic.objects.extra(where=['id IN (' + relic_id + ')']).update(hot=hot_new)
    except Exception as e:
        print('?????????????')
        print(e)
        return render(request, 'video_list.html')
    return HttpResponse('{"res":"success", "msg":"添加成功"}', content_type='application/json')


def data_analyse(request):
    # users = models.Visitor.objects.filter(is_delete=0)
    # 分析男女比
    man_num = models.Visitor.objects.filter(is_delete=0, sex='男').count()
    woman_num = models.Visitor.objects.filter(is_delete=0, sex='女').count()
    # print('______________')
    # print(man_num)
    # print(woman_num)

    # 分析城市分布
    city_list = models.Visitor.objects.values('city')
    city_list = np.array(city_list)
    cities = []
    for c in city_list:
        cities.append(c.get('city'))
    city_set = Counter(cities)
    city_set = dict(city_set)
    cityname_list = city_set.items()
    citynum_list = city_set.values()
    cityname_list = list(cityname_list)
    citynum_list = list(citynum_list)
    # print('city_set', city_set)


    # 分析文物热度，做文物的热词
    relic_list = models.Relic.objects.values('relic_name', 'hot')
    relic_list = np.array(relic_list)
    relic_set = {}
    relicname_list = []
    hot_list = []
    for i in relic_list:
        n = i.get('relic_name')
        h = i.get('hot')
        relic_set[n] = h
        relicname_list.append(n)
        hot_list.append(h)

    # print('relic_set', relic_set)
    relic_list = list(zip(relicname_list, hot_list))
    # print('relic_list', relic_list)

    relic_type_list = models.Relic.objects.values('type')
    relic_type_list = np.array(relic_type_list)
    relic_types = []
    for t in relic_type_list:
        relic_types.append(t.get('type'))
    type_set = Counter(relic_types)
    type_set = dict(type_set)
    type_name = list(type_set.keys())
    type_num = list(type_set.values())


    date_person = models.Visits.objects.values('date', 'person')
    date_person = np.array(date_person)

    date_person_list = []
    date_list = []
    for i in date_person:
        d = i.get('date')
        p = i.get('person')
        date_person_list.append([d, p])
        date_list.append(d)

    # print('date_person_list', date_person_list)
    # print('date_list', date_list)

    return render(request, 'data_analyse.html',
                  {"man_num": man_num, "woman_num": woman_num,
                    "cityname_list": json.dumps(cityname_list), "citynum_list": json.dumps(citynum_list), "city_set": json.dumps(city_set),
                    "relic_list": json.dumps(relic_list), "hot_list": json.dumps(hot_list), "relicname_list": json.dumps(relicname_list),
                   "type_num": json.dumps(type_num), "type_name": json.dumps(type_name),
                   "date_person_list": json.dumps(date_person_list), "date_list": json.dumps(date_list)
                   })


def regist(request):
    if request.method == 'GET':
        return render(request, 'regist.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        User.objects.create_user(username=name, password=password)
        return redirect('/login/')



def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 验证用户名和密码，通过的话，返回User对象
        user = auth.authenticate(username=name, password=password)
        print('user', user)
        if user:
            auth.login(request, user)
            return redirect('/user_list/')
        else:
            return redirect('/login/')

def logout(request):

    if request.method == 'GET':
        auth.logout(request)
        return redirect('/login/')
    return redirect('/login/')


def test(request):
    pass
    # for i in range(336, 670):
    #     v = models.Visits.objects.filter(id=i).first()
    #     if v:
    #         v.delete()


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False