from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ActivateSerializer,LoginSerializer,UserCreateSerializer
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
    HTTP_404_NOT_FOUND, )
from django.views.decorators.csrf import csrf_exempt
import requests
from .spider import save_img,spider,table
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
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return Response("OK!")
            else:
                return Response("NO!")
        else:
            return Response(serializer.errors)


#激活用户
class ActivateView(APIView):
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    @csrf_exempt
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.data['username']
        password = serializer.data['password']
        yzm_text = serializer.data['yzm_text']
        yzm_cookie = serializer.data['yzm_cookie']
        try:
            course_sum = {}

            table_content = spider(username, password, yzm_text, yzm_cookie,course_sum)

            course_infor = table(table_content[1],table_content[0])
            print("ASdasd")
        except:
            reply = {'error':'用户激活失败'}
            return Response(reply)

#创建用户
        if(Nuser.objects.filter(username= username)):
            return Response({"error":"username has been created"})
        else:

            user = Nuser.objects.create(
                                username =username,
                                password = password,
                                grade =username[:4],
                                school=c["school"][0],
                                real_name =c["username"][0])

#创建用户的课程表
            c = course_infor
            user = Nuser.objects.get(username=username)
            cout = 1
            for key in c:

                if cout > 3:

                    user.coursetable_set.create(course_id=c[key]["course_id"])
                else:
                    cout = cout + 1

#这里的是用来爬取总数据的
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


        return Response(course_infor)

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
