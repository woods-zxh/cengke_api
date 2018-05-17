from account.models import CourseTable
from rest_framework.views import APIView
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
from .serializers import (
    BuildingCoursesSerializer,
    PushMessageSerializer,
    CoursesSerializer,
    CourseTableSerializer,
    CourseIdSerializer,
    )

from .models import AllCourses,PushMessage
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

#返回课表信息
class CourseTableView(APIView):
    permission_classes = [AllowAny]
    # serializer_class = Serializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def get(self,request):
        user = request.user
        course_set = CourseTable.objects.filter(user = user)
        queryset1 = AllCourses.objects.filter(course_id=20172005341)
        for course in course_set:
            queryset = AllCourses.objects.filter(course_id=course.course_id)
            queryset1 =  queryset1|queryset
        print(queryset1)
        # if queryset.exists():
        serializer = CourseTableSerializer(queryset1 ,many=True)
        # serializer.is_valid()
        print(serializer.data)
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
        # print(queryset)
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
        user  = request.user
        serializer = CourseIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_id = serializer.data['data_id']
        queryset = AllCourses.objects.filter(data_id=data_id)
        # print(queryset)
        for course in queryset:
            user.coursehistory_set.create(course_id = course.course_id)

        response = Response("OK!")
        return response

#课程收藏
class CollectView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CourseIdSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self, request):
        user = request.user
        serializer = CourseIdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data_id = serializer.data['data_id']
        queryset = AllCourses.objects.filter(data_id=data_id)
        # print(queryset)
        for course in queryset:
            user.coursecolle_set.create(course_id=course.course_id)

        response = Response("OK!")
        return response

#官方用户推送课程
class PushView(APIView):
    permission_classes = [AllowAny]
    serializer_class = PushMessageSerializer
    authentication_classes = (SessionAuthentication, BasicAuthentication)

    def post(self,request):
        user = request.user
        if(user.can_post):
            serializer = PushMessageSerializer(data = request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # author =serializer.data['author']
            # title = serializer.data['title']
            # begin_hour = serializer.data['begin_hour']
            # end_hour = serializer.data['end_hour']
            # begin_minute = serializer.data['begin_minute']
            # end_minute = serializer.data['end_minute ']
            # area = serializer.data['area']
            # building =  serializer.data['building']
            # room =  serializer.data['room']
            # introduce =  serializer.data['introduce']
            # created_time =  serializer.data['created_time']
            response = Response("OK!")
            return response