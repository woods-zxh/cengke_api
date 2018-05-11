from course import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^courses_table/$', views.CoursesTableView.as_view(), name='courses_table'),  #用于返回用户的课程表
    url(r'^building_courses/$', views.BuildingCoursesView.as_view(), name='building_courses'),  # 用于返回对应buiding的，当前时间段的所有粗略课程信息
    url(r'^couese_detail/$', views.CourseDetailView.as_view(),name ='couese_detail'),#用于返回课程的详细信息
    # url(r'^do_it/$', views.DoItView.as_view(), name='do_it'),  # 用于用户说去蹭课了，加入蹭课足迹,传入id
    # url(r'^collect/$', views.CollectView.as_view(),name ='collect'),#用于用户收藏课表的增删传入id
    # url(r'^recommend/$', views.Recommment.as_view(),name ='recommend'),#用于给用户推荐他的个性课程
    # url(r'^get_push/$', views.GetPush.as_view(),name ='get_push'),#用于用户获得推送课程
    # url(r'^push/$', views.Push.as_view(),name ='push'),#用于官方用户推送课程

]