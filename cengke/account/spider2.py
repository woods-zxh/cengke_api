import urllib
from urllib import request
import hashlib
from urllib import parse
from bs4 import BeautifulSoup
import re
import os
import shutil
#用来获取静态数据
def cut_time(time,course_type2):


    PATTERN = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '日': 7, }
    day_in_week=time.split(':',1)[0][1:]

    start_end_week = time.split(':',1)[1].split(',',1)[0]

    #判断“周”与后面没用“；”
    if len(time.split(':',1)[1].split(',',1)[1].split(';'))!=1:
        time2= time.split(':',1)[1].split(',',1)[1].split(';')[1]
        gap = time.split(':', 1)[1].split(',', 1)[1].split(';')[0][1::-2]
    else:

        time2 = time.split(':', 1)[1].split(',', 1)[1].split('周')[1]
        gap = time.split(':', 1)[1].split(',', 1)[1].split('周')[0][1:]

    start_end_time = time2.split(',',1)[0]
    start_week = start_end_week.split("-", 1)[0]
    end_week = start_end_week.split("-", 1)[1][:-1]
    start_time = start_end_time.split("-", 1)[0]
    end_time = start_end_time.split("-", 1)[1][:-1]
    #判断是否包含上课地点和时间
    if len(time) > 24:
            area = time2.split(',', 1)[1].split(',', 1)[0][:-1]
            building_room = time2.split(',', 1)[1].split(',', 1)[1]

            if len(building_room.split("-",1))!=1:
                building = building_room.split("-",1)[0]
                room = building_room.split("-",1)[1]

            else:
                building =building_room.split("-",1)[0][:2]
                room = building_room.split("-", 1)[0][2:]
    #在备注里面获取上课地点和时间
    else:
            if len(course_type2)==1:
                area = 0
                building = course_type2[0]
                room = 0
            else:
                area = course_type2[1]
                building = course_type2[1]
                room = course_type2[1]

    if area == "国":
        area = "21"
    if building == "计":
        building = "21"
    elif building == '理':
        building = "22"
    elif building == '老外':
        building = '23'

    time_infor = {

        "day_in_week": PATTERN[day_in_week],
        "start_week": start_week,
        "end_week": end_week,
        "area": area,
        "building": building,
        "room": room,
        "start_time": start_time,
        "end_time": end_time,
        "gap": gap,
    }

    return time_infor

#获取所有的课程数据

def spider2(username, password, yzm_text, yzm_cookie):
    cout = 1
    course_sum = {}

    login_url = 'http://210.42.121.241/servlet/Login'
    # image_url = 'http://210.42.121.241/servlet/GenImg'
    login_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
    # 提交的数据
    data = urllib.parse.urlencode({
        'id': username,
        'pwd': login_pwd,
        'xdvfb': yzm_text,
    })

    data = data.encode(encoding='utf-8')
    # 登录请求
    request = urllib.request.Request(login_url, data, headers={'Cookie': yzm_cookie})
    content = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(content, "lxml")

    #爬取公共选修课的数据
    for page in range(1,27):
        courses_url = 'http://210.42.121.241/stu/choose_PubLsn_list.jsp?XiaoQu=0&credit=0&keyword=&pageNum='+str(page)
        requset = urllib.request.Request(courses_url, headers={'Cookie': yzm_cookie})
        courses = urllib.request.urlopen(requset).read()
        tsoup = BeautifulSoup(courses, "html")
        listTable = tsoup.find_all(attrs={'class': 'table listTable'})
        tr = listTable[0].find_all('tr')
        print(page)
        tr_num = len(tr)
        for i in range(1, tr_num):
            td = tr[i].find_all('td')
            input=td[11].find_all('input')
            course_id =input[0].attrs['id']
            course_name = re.sub('[\r\n\t]','',td[0].text).split()[0]  # 课程名字
            course_credit = re.sub('[\r\n\t]', '', td[1].text).split()[0]  # 学分
            course_teacher = re.sub('[\r\n\t]', '', td[3].text).split()[0]  # 授课老师
            course_school = re.sub('[\r\n\t]', '', td[5].text).split()[0]  # 授课学院
            course_time_place = re.sub('[\r\n\t]', '', td[9].text).split()  # 课程时间和地点
            course_type1 = re.sub('[\r\n\t]','',td[10].text).split()  # 课程类型(公选的类型）
            course_type2 = str(course_type1[0]).split('，')#抓取藏在其中的上课地点
            course_type = [course_type2[0]]
            # course_major =re.sub('[\r\n\t]','',td[10].text).split()  #专业
            #处理藏在title中的多个上课地点
            # if len(td[9].attrs)!=0:
            #     x = td[9]['title'].split('<br/>')[0]
            #     print(td[9].attrs)
            #     y = x[5:].split('\n')[0]+ x[5:].split('\n')[1]
            #     course_time_place[0]=y
            #     x = td[9]['title'].split('<br/>')[1]
            #     y = x.split('\n')[0] + x.split('\n')[1]
            #     course_time_place.append(y)

                # course_time_place[0] = re.sub('[\n]', '', td[9]['title'].split('<br/>')[0][3:]).split()

            course_infor1 = {
                "data_id": course_id,
                "course_id": course_id,
                "name": course_name,
                "type": course_type[0],
                "school": course_school,
                "teacher": course_teacher,
                "major": course_type[0],
                "credit": course_credit,

            }
            different_id = course_infor1["data_id"]
            #区别多个上课时间的数据
            if len(course_time_place) >= 1:

                for j in range(0, len(course_time_place)):
                    course_time_infor = cut_time(course_time_place[j], course_type2)

                    course_infor1["data_id"] = different_id + str(j+1)

                    course_infor = dict(course_infor1, **course_time_infor)
                    # course_infor["course_time_place"]= course_time_place[j]
                    course_sum[cout] = course_infor
                    cout = cout + 1
            #处理没数据的选项
            else:
                course_time_infor = time_infor = {
                    "day_in_week": 0,
                    "start_week": 0,
                    "end_week": 0,
                    "area":0,
                    "building": 0,
                    "room": 0,
                    "start_time": 0,
                    "end_time": 0,
                    "gap": 0,
    }
                course_infor = dict(course_infor1, **course_time_infor)
                course_sum[cout] = course_infor
                cout = cout + 1
    return course_sum
