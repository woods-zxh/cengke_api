from course import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    url(r'^buiding_courses/(?P<pk>[0-9]+)/$', views.BuidingCoursesView.as_view(), name='buiding_courses'),  # 用于返回对应buiding的，当前时间段的所有粗略课程信息
    url(r'^couese_detail/(?P<pk>[0-9]+)/$', views.CourseDetailView.as_view(),name ='couese_detail'),#用于返回课程的详细信息
    url(r'^do_it/(?P<pk>[0-9]+)/$', views.DoItView.as_view(), name='do_it'),  # 用于用户说去蹭课了，加入蹭课足迹
    url(r'^collect/(?P<pk>[0-9]+)/$', views.CollectView.as_view(),name ='collect'),#用于用户收藏课表的增删
    url(r'^recommend/(?P<pk>[0-9]+)/$', views.Recommment.as_view(),name ='recommend'),#用于给用户推荐他的个性话课程
    url(r'^recommend/(?P<pk>[0-9]+)/$', views.Recommment.as_view(),name ='recommend'),#用于用户收藏课表的增删
    




]