from course import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [

    url(r'^course_table/$', views.CourseTableView.as_view(), name='course_table'),  #用于返回用户的课程表
    url(r'^building_courses/$', views.BuildingCoursesView.as_view(), name='building_courses'),  # 用于返回对应buiding的，当前时间段的所有粗略课程信息
    url(r'^course_detail/$', views.CourseDetailView.as_view(),name ='couese_detail'),#用于返回单个课程的详细信息
    url(r'^do_it/$', views.DoItView.as_view(), name='do_it'),  # 用于用户说去蹭课了，加入蹭课足迹,传入id
    url(r'^collect/$', views.CollectView.as_view(),name ='collect'),#用于用户收藏课表的增删传入id
    url(r'^push/$', views.PushView.as_view(),name ='push'),#用于官方用户推送课程
    url(r'^get_push/$', views.GetPushView.as_view(),name ='get_push'),#用于用户获得官方推送课程
    url(r'^search/$', views.SearchView.as_view(),name ='search'),#用于用户的搜索
    url(r'^recommend/$', views.RecommmentView.as_view(),name ='recommend'),#用于给用户推荐他的个性课程
    #蹭课足迹的获取
    #

]

