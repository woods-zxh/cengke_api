"""
WSGI config for cengke project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cengke.settings")

application = get_wsgi_application()


# 获取课程信息与个人信息
def table(course_sum, table_content):
    csoup = BeautifulSoup(table_content, 'lxml')
    listTable = csoup.find_all(attrs={'class': 'table listTable'})
    # 返回一个列表
    tr = listTable[0].find_all('tr')
    a = tr[1].find_all("td")
    tr_num = len(tr)
    cout = 1

    for i in range(1, tr_num):
        td = tr[i].find_all('td')
        course_id = re.sub('[\r\n\t]', '', td[0].text).split()[0]
        # course_name = re.sub('[\r\n\t]','',td[1].text).split()[0] # 课程名字
        # course_type = re.sub('[\r\n\t]','',td[2].text).split()[0] # 课程类型（必修或选修）
        # course_credit = re.sub('[\r\n\t]','',td[3].text).split()[0] # 学分
        # course_teacher = re.sub('[\r\n\t]','',td[4].text).split()[0] # 授课老师
        # course_school = re.sub('[\r\n\t]','',td[5].text).split()[0] # 授课学院
        # course_school = re.sub('[\r\n\t]','',td[9].text).split()[0] # 成绩

        course_infor = {
            "course_id": course_id,
        }
        course_sum[cout] = course_infor
        cout = cout + 1
    return course_sum