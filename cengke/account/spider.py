
import urllib
from urllib import request
import hashlib
from urllib import parse
from bs4 import BeautifulSoup
import re
import os
import shutil

import json


    # data = parse.urlencode(Form_Data).encode('utf-8')
    #
    # response = request.urlopen(login_url,data)
    #
    # html = response.read().decode('utf-8')

def spider(username, password, yzm_text, yzm_cookie):
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
    req = urllib.request.Request(login_url, data,headers={'Cookie': yzm_cookie} )
    content = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(content, "lxml")
    namediv = soup.find_all(attrs={'id': 'nameLable'})
    termspan = soup.find_all(attrs={'id': 'term'})
    # print("等防疫")
    # print(namediv)


    #爬取课表
    table_url = 'http://210.42.121.241/stu/stu_course_parent.jsp'
    requset = urllib.request.Request(table_url, headers={'Cookie': yzm_cookie})
    class_table = urllib.request.urlopen(requset).read()

    tsoup = BeautifulSoup(class_table,"xml")
    # print(tsoup)
    page_iframe = tsoup.find_all(attrs={'id': 'iframe0'})
    page_url = home_url  # 课程表所在的url

    page_urls = page_url + page_iframe[0].get('src')[:-19] + "&action=normalLsn&year=2017&term=%CF%C2&state="
    print("哈哈")
    print(page_urls)
    requset = urllib.request.Request(page_urls, headers={'Cookie': yzm_cookie})
    # 课表的详细内容：table_content
    table_content = urllib.request.urlopen(requset).read()
    print("qweqeqeqweqwewq")

#获取课程信息

    csoup = BeautifulSoup(table_content, 'lxml')
    listTable = csoup.find_all(attrs={'class': 'table listTable'})
    #返回一个列表
    # print(csoup)
    tr = listTable[0].find_all('tr')
    a =tr[1].find_all("td")
    print(a[0].string)
    tr_num = len(tr)
    username = re.sub('[\r\n\t]', '', namediv[0].text).split()
    term =  re.sub('[\r\n\t]', '',termspan[0].text).split()
    course_sum = {"username":username,"term":term}
    for i in range(1, tr_num):
        td = tr[i].find_all('td')
        # course_num = td[0].text.encode("utf-8").strip() #课头号
        # course_name = td[1].text.encode("utf-8").strip() #课程名字
        # course_type = td[2].text.encode("utf-8").strip() #课程类型（必修或选修）
        # course_college = td[4].text.encode("utf-8").strip() #授课学院
        # course_teacher = td[5].text.encode("utf-8").strip() #授课老师
        # course_major = td[6].text.encode("utf-8").strip() #专业
        # course_point = td[7].text.encode("utf-8").strip() #学分
        # course_time = td[9].text.encode("utf-8").strip() #课程时间
        # time_dict = course_time.split(b":")
        # day =  time_dict[0] #形式为"周一"
        # class_num = time_dict[1].split(b";")[1].split(b"--")[0].split(b"-")
        # start_num = class_num[0] #开始节数
        # end_num = class_num[1] #结束节数
        # course_name = course_name.decode("utf-8")
        # course_time = course_time.decode('utf-8')
        #课程名

        # course_num = td[0].text.repalce('\t',"")
        course_num =re.sub('[\r\n\t]','',td[0].text).split()
        course_name = re.sub('[\r\n\t]','',td[1].text).split()  # 课程名字
        course_type = re.sub('[\r\n\t]','',td[2].text).split()  # 课程类型（必修或选修）
        course_college = re.sub('[\r\n\t]','',td[4].text).split() # 授课学院
        course_teacher = re.sub('[\r\n\t]','',td[5].text).split() # 授课老师
        course_major =re.sub('[\r\n\t]','',td[6].text).split()  # 专业
        course_credit = re.sub('[\r\n\t]','',td[7].text) .split() # 学分
        course_time = re.sub('[\r\n\t]','',td[9].text).split() # 课程时间
        course_infor={
            "num": course_num,
            "name" :course_name,
            "type": course_type,
            "school": course_college,
            "teacher": course_teacher,
            "major":course_major ,
            "credit":course_credit,
            "time": course_time,

        }

        # lesson_file = 'file/yzm/' + "data.txt"
        # with open(lesson_file, 'w') as f:
        #     f.write(str(course_infor))
        course_sum[i+1]=course_infor
        print("qweqeqeqweqwewq")
    return course_sum

def save_img(cookie, yzm_image):
    shutil.rmtree('file/yzm')
    os.mkdir('file/yzm')
    # os.remove(remove_file)
    yzm_file = 'file/yzm/' +   str(cookie)[11:43]+ ".jpg"
    # str(cookie)[11:43]
    # print ("sadasdasd")
    with open(yzm_file, 'wb') as f:
        f.write(yzm_image)
        f.close()