
import urllib
from urllib import request
import hashlib
from urllib import parse
from bs4 import BeautifulSoup
import re
import os
import shutil
import time

#用来获取用户个性数据
def cut_time(time):
    # 第一步切片
    PATTERN = {'一' : 1,'二' : 2,'三' : 3,'四' : 4,'五' : 5,'六' : 6,'日' : 7,}
    day_in_week=time.split(':',1)[0][1:]

    start_end_week = time.split(':',1)[1].split(',',1)[0]

    gap = time.split(':',1)[1].split(',',1)[1].split(';')[0][1::-2]

    time2= time.split(':',1)[1].split(',',1)[1].split(';')[1]

    start_end_time = time2.split(',',1)[0]
    start_week = start_end_week.split("-", 1)[0]
    end_week = start_end_week.split("-", 1)[1][:-1]
    start_time = start_end_time.split("-", 1)[0]
    end_time = start_end_time.split("-", 1)[1][:-1]

    if len(time) > 24:
            area = time2.split(',', 1)[1].split(',', 1)[0][:-1]
            building_room = time2.split(',', 1)[1].split(',', 1)[1]
            building = building_room.split("-",1)[0]
            room = building_room.split("-",1)[1]
            if area == "国":
                area = "5"
    else:
            area = 0
            building = 0
            room = 0
    a = day_in_week
    time_infor = {
        "day_in_week": PATTERN[a],
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



#获取用户课程数据
def spider(username, password, yzm_text, yzm_cookie,course_sum):
    home_url = 'http://210.42.121.241'
    login_url ='http://210.42.121.241/servlet/Login'
    #image_url = 'http://210.42.121.241/servlet/GenImg'
    login_pwd = hashlib.md5(password.encode('utf-8')).hexdigest()
    #提交的数据
    data = urllib.parse.urlencode({
        'id': username,
        'pwd':login_pwd,
        'xdvfb': yzm_text,
    })

    data = data.encode(encoding='utf-8')
    #登录请求
    request = urllib.request.Request(login_url, data,headers={'Cookie': yzm_cookie} )
    content = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(content, "lxml")
    #爬点个人信息
    namediv = soup.find_all(attrs={'id': 'nameLable'})
    termspan = soup.find_all(attrs={'id': 'term'})
    school = soup.find_all(attrs={"id":'acade'})
    username = re.sub('[\r\n\t]', '', namediv[0].text).split()
    term = re.sub('[\r\n\t]', '', termspan[0].text).split()
    school = re.sub('[\r\n\t]', '', school[0].text).split()
    course_sum = {"username": username, "school": school, "term": term}
    #爬取课表
    table_url = 'http://210.42.121.241/stu/stu_course_parent.jsp'
    requset = urllib.request.Request(table_url, headers={'Cookie': yzm_cookie})
    class_table = urllib.request.urlopen(requset).read()
    tsoup = BeautifulSoup(class_table,"xml")

    page_iframe = tsoup.find_all(attrs={'id': 'iframe0'})
    # 课程表数据所在的url
    page_urls = home_url  + page_iframe[0].get('src')[:-19] + "&action=normalLsn&year=2018&term=%C9%CF&state="
    requset = urllib.request.Request(page_urls, headers={'Cookie': yzm_cookie})
    # 课表的详细内容：table_content
    table_content = urllib.request.urlopen(requset).read()

    return [table_content,course_sum,page_iframe[0].get('src')[:-19]]


def historySpider(yzm_cookie,course_sum,page_iframe1):
    home_url = 'http://210.42.121.241'
    table_url = 'http://210.42.121.241/stu/stu_score_parent.jsp'
    requset = urllib.request.Request(table_url, headers={'Cookie': yzm_cookie})
    class_table = urllib.request.urlopen(requset).read()
    tsoup = BeautifulSoup(class_table, "xml")
    # if(time.ctime()[8:9]==" "):
    #     tail = time.ctime()[0:8]+"0"+time.ctime()[9:11]+time.ctime()[-4:]+time.ctime()[10:20]+"GMT+0800 (CST)"
    # else:
    #     tail = time.ctime()[0:11]+time.ctime()[-4:]+time.ctime()[10:20]+"GMT+0800 (CST)
    page_urls = home_url +"/servlet/Svlt_QueryStuScore?"+ page_iframe1[26:] + "&year=0&term=&learnType=&scoreFlag=0&t="
    requset = urllib.request.Request(page_urls, headers={'Cookie': yzm_cookie})
    # 课表的详细内容：table_content
    table_content = urllib.request.urlopen(requset).read()
    csoup = BeautifulSoup(table_content, 'lxml')
    listTable = csoup.find_all(attrs={'class': 'table listTable'})
    # 返回一个列表
    tr = listTable[0].find_all('tr')
    a = tr[1].find_all("td")
    tr_num = len(tr)
    cout = 0
    for i in range(1, tr_num):
        td = tr[i].find_all('td')
        course_id = re.sub('[\r\n\t]', '', td[0].text).split()[0]
        course_name = re.sub('[\r\n\t]','',td[1].text).split()[0] # 课程名字
        course_type = re.sub('[\r\n\t]','',td[2].text).split()[0] # 课程类型（必修或选修）
        course_credit = re.sub('[\r\n\t]','',td[3].text) .split()[0] # 学分
        course_teacher = re.sub('[\r\n\t]','',td[4].text).split()[0] # 授课老师
        course_school = re.sub('[\r\n\t]','',td[5].text).split()[0] # 授课学院

        course_infor = {
            "course_id": course_id,
            "course_name ": course_name,
            "course_type":course_type,
            "course_credit":course_credit,
            "course_teacher":course_teacher,
            "course_school": course_school,
        }
        course_sum[cout] = course_infor
        cout = cout + 1
    return course_sum


#获取课程信息与个人信息
def table(course_sum,table_content):
    csoup = BeautifulSoup(table_content, 'lxml')
    listTable = csoup.find_all(attrs={'class': 'table listTable'})
    #返回一个列表
    tr = listTable[0].find_all('tr')
    # a =tr[1].find_all("td")
    tr_num = len(tr)
    cout = 1

    for i in range(1, tr_num):
        td = tr[i].find_all('td')
        course_id =re.sub('[\r\n\t]','',td[0].text).split()[0]
        # course_name = re.sub('[\r\n\t]','',td[1].text).split()[0] # 课程名字
        # course_type = re.sub('[\r\n\t]','',td[2].text).split()[0] # 课程类型（必修或选修）
        # course_school = re.sub('[\r\n\t]','',td[4].text).split()[0] # 授课学院
        # course_teacher = re.sub('[\r\n\t]','',td[5].text).split()[0] # 授课老师
        # course_major =re.sub('[\r\n\t]','',td[6].text).split() # 专业
        # course_credit = re.sub('[\r\n\t]','',td[7].text) .split()[0] # 学分
        # course_time_place = re.sub('[\r\n\t]','',td[9].text).split()# 课程时间
        course_infor = {
            "course_id": course_id,
             }
        course_sum[cout] = course_infor
        cout = cout + 1
    return course_sum


def save_img(cookie, yzm_image):
    shutil.rmtree('file/yzm')
    os.mkdir('file/yzm')
    yzm_file = 'file/yzm/' +   str(cookie)[11:43]+ ".jpg"
    with open(yzm_file, 'wb') as f:
        f.write(yzm_image)

