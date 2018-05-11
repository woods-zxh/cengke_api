from account.models import Nuser
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
from .serializers import BuildingCoursesSerializer, PushMessageSerializer,CoursesSerializer
from .models import AllCourses,PushMessage
from django.contrib.auth import authenticate, login, logout
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.response import Response

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


