from account.models import CourseTable,Coursehistory
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import (
    AllowAny
)

from .serializers import (
    BuildingCoursesSerializer,
    PushMessageSerializer,
    CoursesSerializer,
    CourseTableSerializer,
    CourseIdSerializer,
    SearchSerializer,
    UserTokenSerializer,
    )

from .models import AllCourses,PushMessage
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response
# from django.db.modelsimports Q
from django.db.models import Q
import math
#返回课表信息

DoItUserWeight = 0.2
DoItCourseWeight=0.02
CollectUserWeight = 0.2
CollectCourseWeight=0.02

#获得课表
class CourseTableView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CourseTableSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self,request,token):
            try:
                token = Token.objects.get(key=token)
            except BaseException:
                reply = {
                    "message": "请先登陆"
                }
                return Response(reply)
            user = token.user
            course_set = CourseTable.objects.filter(user = user)
            queryset1 = AllCourses.objects.filter(course_id=000)

            for course in course_set:
                queryset = AllCourses.objects.filter(course_id=course.course_id)

                queryset1 =  queryset1|queryset

            # if queryset.exists():
            serializer = CourseTableSerializer(queryset1,many=True)

            response = Response(serializer.data)
            return response
        #
        # reply = {"message":"wrong"}
        # Response(reply)
#返回对应教学楼的课程信息
class BuildingCoursesView(APIView):
    permission_classes = [AllowAny]
    serializer_class = BuildingCoursesSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self,request):
        serializer = BuildingCoursesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        area = serializer.validated_data['area']
        building = serializer.validated_data['building']

        queryset =AllCourses.objects.filter(area = area,building =building)
        serializer = CoursesSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data)
        return response

#返回单个课程的详细信息
class CourseDetailView(APIView):
    permission_classes = [AllowAny]
    serializer_class =  CourseIdSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self,request):
        serializer = CourseIdSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        data_id =  serializer.data['data_id']
        queryset = AllCourses.objects.filter(data_id = data_id)
        serializer = CoursesSerializer(queryset, data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data)
        return response

#进行我要蹭课
class DoItView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CourseIdSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    def post(self, request):
        serializer = CourseIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokenKey = serializer.data['token']
        try:
            token = Token.objects.get(key=tokenKey)
        except BaseException:
            reply = {
                "message": "请先登陆"
            }
            return Response(reply)
        user = token.user

        data_id = serializer.data['data_id']
        queryset = AllCourses.objects.filter(data_id=data_id)
        print(queryset)
        #创建用户的足迹以及反馈给课程
        for b in queryset:
            user.coursehistory_set.create(course_id = b.course_id)
            #用户自己的向量发生改变
            user.art += b.art
            user.communication += DoItUserWeight*b.communication
            user.society += DoItUserWeight*b.society
            user.internation += DoItUserWeight*b.internation
            user.leader += DoItUserWeight*b.leader
            user.science += DoItUserWeight*b.science
            user.logic += DoItUserWeight*b.logic
            user.others += DoItUserWeight*b.others
            user.save()
            #课程的向量发生改变
            b.art += b.art
            b.communication += DoItCourseWeight * (user.communication-DoItUserWeight*b.communication)
            b.society += DoItCourseWeight * (user.society-DoItUserWeight*b.society)
            b.internation += DoItCourseWeight * (user.internation-DoItUserWeight*b.internation)
            b.leader += DoItCourseWeight * (user.leader-DoItUserWeight*b.leader)
            b.science += DoItCourseWeight * (user.science-DoItUserWeight*b.science)
            b.logic += DoItCourseWeight * (user.logic-DoItUserWeight*b.logic)
            b.others += DoItCourseWeight * (user.others-DoItUserWeight*b.others)
            b.save()
        reply = {
            "message": "done"
        }
        response = Response(reply)
        return response

#课程收藏
class CollectView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CourseIdSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):

        serializer = CourseIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokenKey = serializer.data['token']
        try:
            token = Token.objects.get(key=tokenKey)
        except BaseException:
            reply = {
                "message": "请先登陆"
            }
            return Response(reply)
        user = token.user
        data_id = serializer.data['data_id']
        queryset = AllCourses.objects.filter(data_id=data_id)
        for b in queryset:
            user.coursecolle_set.create(course_id=b.course_id)
            user.coursehistory_set.create(course_id=b.course_id)
            # 用户自己的向量发生改变
            user.art += b.art
            user.communication += DoItUserWeight * b.communication
            user.society += DoItUserWeight * b.society
            user.internation += DoItUserWeight * b.internation
            user.leader += DoItUserWeight * b.leader
            user.science += DoItUserWeight * b.science
            user.logic += DoItUserWeight * b.logic
            user.others += DoItUserWeight * b.others
            user.save()
            # 课程的向量发生改变
            b.art += b.art
            b.communication += DoItCourseWeight * (user.communication - DoItUserWeight * b.communication)
            b.society += DoItCourseWeight * (user.society - DoItUserWeight * b.society)
            b.internation += DoItCourseWeight * (user.internation - DoItUserWeight * b.internation)
            b.leader += DoItCourseWeight * (user.leader - DoItUserWeight * b.leader)
            b.science += DoItCourseWeight * (user.science - DoItUserWeight * b.science)
            b.logic += DoItCourseWeight * (user.logic - DoItUserWeight * b.logic)
            b.others += DoItCourseWeight * (user.others - DoItUserWeight * b.others)
            b.save()

        reply = {
            "message": "done"
        }
        response = Response(reply)
        return response

#官方用户推送课程
class PushView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PushMessageSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self,request):
        serializer = PushMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokenKey = serializer.data['token']
        try:
            token = Token.objects.get(key=tokenKey)
        except BaseException:
            reply = {
                "message": "请先登陆"
            }
            return Response(reply)
        user = token.user
        if(user.can_post):
            serializer.save()
            response = Response("OK!")
            return response
        else:
            reply = {
                "message": "您没有权限发布"
            }
            response = Response(reply)
            return  response


#获得官方推送
class GetPushView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PushMessageSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self,request):
        # serializer = PushMessageSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        queryset = PushMessage.objects.all()
        serializer = PushMessageSerializer(queryset, many=True)
        response = Response(serializer.data)
        return response


#进行模糊搜索
class SearchView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SearchSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self,request):
        serializer = SearchSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        keyword = serializer.data["keyword"]
        day_in_week = serializer.data["day_in_week"]
        start_time = serializer.data["start_time"]
        end_time = serializer.data["end_time"]
        area = serializer.data["area"]
        #这里还要吧TIME转化成节数

        searchResult1 = AllCourses.objects.filter( Q(teacher__icontains=keyword)\
                                                  |Q(name__icontains =keyword))


        searchResult2 = searchResult1.filter(end_time__gte = end_time).filter(start_time__lte = start_time)
        if(area!=0):
            searchResult2 = searchResult2.filter(area__icontains=area)
        if(day_in_week!=0):
            searchResult2 = searchResult2.filter(day_in_week__icantains =day_in_week)
        serializer = CoursesSerializer(searchResult2,many = True)
        # reply = {"result":searchResult2}
        reponse = Response(serializer.data)
        return reponse

#智能推荐的最后一步函数
class RecommmentView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CoursesSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self,request,token):
        try:
            token = Token.objects.get(key=token)
        except BaseException:
            reply ={
                "message": "请先登陆"
            }
            return Response(reply)
        user = token.user
        list1 =[]
        sizeOfUser = math.sqrt(
                pow(user.art,2)+pow(user.communication,2)+pow(user.society,2)+pow(user.internation,2)+pow(user.internation,2)+
                pow(user.leader,2)+pow(user.science,2)+pow(user.logic,2)+pow(user.others,2))
        for b in AllCourses.objects.all():
            sizeOfCourse = math.sqrt(
                pow(b.art,2)+pow(b.communication,2)+pow(b.society,2)+pow(b.internation,2)+\
                pow(b.internation,2)+pow(b.leader,2)+pow(b.science,2)+pow(b.logic,2)+pow(b.others,2))
            spotMul = user.art * b.art +user.communication * b.communication+user.society* b.society+\
                      user.internation* b.internation+user.leader *b.leader+user.science * b.science+\
                      user.logic*b.logic+user.others*b.others
            #得到一个分数，是两个向量的夹角，值越大就相似分数越高
            credit = spotMul/(sizeOfCourse*sizeOfUser)
            # print(credit)

            list1.append((credit,b.data_id))

        list1.sort()
        # list.sort()
        list1.reverse()


        result =[]
        for course in list1[:12]:
            query = AllCourses.objects.filter(data_id = course[1])
            for a in query:
                if a not in result:
                    result.append(a)
        serializer = CoursesSerializer(result, many=True)
        return Response(serializer.data)

#获得蹭课足迹
class CourseHistoryView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CourseTableSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    def get(self,request,token):
        # makeCourseWeight()
            try:
                token = Token.objects.get(key=token)
            except BaseException:
                reply = {
                    "message": "请先登陆"
                }
                return Response(reply)
            user = token.user
            course_set = Coursehistory.objects.filter(user = user)
            queryset1 = AllCourses.objects.filter(course_id=000)

            for course in course_set:
                queryset = AllCourses.objects.filter(course_id=course.course_id)

                queryset1 =  queryset1|queryset

            # if queryset.exists():
            serializer = CourseTableSerializer(queryset1 ,many=True)

            response = Response(serializer.data)
            return response
