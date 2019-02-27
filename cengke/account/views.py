from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .courseWeight import makeCourseWeight
from rest_framework.authtoken.models import Token
from .serializers import ActivateSerializer,LoginSerializer,LogoutSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from .models import Nuser
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import (
    IsAdminUser,
    IsAuthenticated,
    AllowAny,
    IsAuthenticatedOrReadOnly
)
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN)
from django.views.decorators.csrf import csrf_exempt
import requests
from .spider import save_img,spider,table,historySpider
from .spider2 import spider2
from rest_framework import permissions
from course.models import AllCourses

#用户登陆
class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    @csrf_exempt
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            try:
                user = authenticate(username=username,password=password)
            except HTTP_403_FORBIDDEN :
                return Response("请先退出当前帐号再切换帐号")
            else:
                if user is not None :
                    # login(request, user)
                    user = Nuser.objects.get(username=username)
                    if(Token.objects.filter(user=user)):
                        token = Token.objects.get(user=user)
                    else:
                        token = Token.objects.create(user=user)

                    reply = {
                        "real_name": user.real_name,
                        "school": user.school,
                        "grade": user.grade,
                        "term": user.term,
                        "is_activated": True,
                        "token" :token.key,
                    }
                    return Response(reply)
                else:
                    user1 = Nuser.objects.filter(username=username)
                    if user1 is not None:
                        reply = {
                            "is_pwd_correct":False
                        }
                    else:
                        reply={
                            "is_activated":False
                        }
                    return Response(reply)
        else:
            return Response(serializer.errors)

#用户登出
class LogoutView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LogoutSerializer
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    def post(self,request):
        # user = request.user
        # logout(user)
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            tokenKey =serializer.data['token']
            try:
                token =  Token.objects.get(key = tokenKey)
            except BaseException:
                reply = {
                    "message": "请先登陆"
                }
                return Response(reply)
            token.delete()
            reply = {
                "message":"Bye"
            }
            return  Response(reply)


#激活用户
class ActivateView(APIView):
    serializer_class = ActivateSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def post(self, request):
        serializer = ActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password = serializer.data['password']
        yzm_text = serializer.data['yzm_text']
        yzm_cookie = serializer.data['yzm_cookie']

        try:

            course_sum = {}
            table_content = spider(username, password, yzm_text, yzm_cookie,course_sum)
            course_infor = table(table_content[1],table_content[0])
            course_sum1 = {}
            history_content =historySpider(yzm_cookie, course_sum1,table_content[2])

    #创建用户
            c = course_infor
            if(Nuser.objects.filter(username= username)):
                return Response({"error":"username has been created"})
            else:

                user = Nuser.objects.create_user(
                                    username =username,
                                    password = password,
                                    grade =username[:4],
                                    school=c["school"][0],
                                    real_name =c["username"][0],
                                    term = c["term"][0],
                                    week = c["term"][1],
                )
    #创建用户的课程表
                user = Nuser.objects.get(username=username)
                cout = 1
                for key in c:
                    if cout > 3:
                        user.coursetable_set.create(course_id=c[key]["course_id"])
                    else:
                        cout = cout + 1
    #创建用户的选过的课并生成用户的初始属性
                for key in history_content:
                    if history_content[key]['course_type'] == "公共选修":
                        a = AllCourses.objects.filter(course_id=history_content[key]['course_id'])
                        for b in a:

                            user.coursehistory_set.create(course_id=b.course_id)
                            user.art += b.art
                            user.communication += b.communication
                            user.society += b.society
                            user.internation += b.internation
                            user.leader += b.leader
                            user.science += b.science
                            user.logic += b.logic
                            user.others += b.others
                            user.save()


            token = Token.objects.create(user=user)
            reply = {
                "real_name": user.real_name,
                "school": user.school,
                "grade": user.grade,
                "term": user.term,
                "is_activated": True,
                "token": token.key,

            }

        except BaseException:
            reply = {
                "is_activated": False
             }

        return Response(reply)

class Upgrade(APIView):
    serializer_class = ActivateSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def post(self, request):
        serializer = ActivateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password = serializer.data['password']
        yzm_text = serializer.data['yzm_text']
        yzm_cookie = serializer.data['yzm_cookie']
        allCoursesData(username, password, yzm_text, yzm_cookie)
        reply={
            "message":"done"
        }
        return Response(reply)


class VCodeView(APIView):
    permission_classes = [AllowAny]
    def get(self,request):
        image_url = 'http://210.42.121.241/servlet/GenImg'
        yzm = requests.get(image_url)
        yzm_image = yzm.content
        yzm_cookie = yzm.headers['Set-Cookie']
        yzm_url = "/media/yzm/" + yzm_cookie[11:43] + ".jpg"
        save_img(yzm_cookie, yzm_image)
        content = {}
        content['yzm_url'] = yzm_url
        content['yzm_cookie'] = yzm_cookie
        response = Response(content)
        return response

def allCoursesData(username, password, yzm_text, yzm_cookie):
        course_infor = spider2(username, password, yzm_text, yzm_cookie)
        c = course_infor
        for key in c:

            AllCourses.objects.create(
                data_id=c[key]["data_id"],
                course_id =c[key]["course_id"],
                name = c[key]["name"],
                type = c[key]["type"],
                school = c[key]["school"],
                major = c[key]["major"],
                teacher = c[key]["teacher"],
                credit = c[key]["credit"],
                start_week = c[key]["start_week"],
                end_week = c[key]["end_week"],
                gap = c[key]["gap"],
                day_in_week = c[key]["day_in_week"],
                start_time = c[key]["start_time"],
                end_time = c[key]["end_time"],
                area = c[key]["area"],
                building = c[key]["building"],
                room = c[key]['room'],
            )
            makeCourseWeight()