from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegistSerializer,LoginSerializer,UserCreateSerializer
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
from .spider import save_img,spider
from rest_framework import permissions


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    authentication_classes = (SessionAuthentication,BasicAuthentication)
    @csrf_exempt
    def post(self, request):
        # return Response("ha")
        serializer = LoginSerializer(data=request.data)
        # return Response("ha")
        # print("gege")
        if serializer.is_valid():
            # return Response("ha")
            username = serializer.data['username']
            password = serializer.data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                return Response("OK!")
            else:

                return Response("NO!")
        else:
            # content = {'msg': ' "no!"'}
            return Response(serializer.errors)

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
            course_infor = spider(username, password, yzm_text, yzm_cookie)

        except:
            reply = {'error':'用户激活失败'}
            return Response(reply)

        # # HTTP_400_BAD_REQUEST
        # if(Nuser.objects.filter(username= username)):
        #     return Response({"error":"username has been created"})
        #
        # else:
        #     user = Nuser.objects.create_user(username=username, password=password)
        #     user.save()
        #     # user = authenticate(username=username, password=password)
        #     # logout(request)
        #     return Response(course_infor)
        return Response(course_infor)

class VCodeView(APIView):
    permission_classes = [AllowAny]
    # serializer_class = UserCreateSerializer
    def get(self,request):
        # username = request.user.username
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
