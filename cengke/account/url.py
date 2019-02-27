
from account import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve



urlpatterns = [
    # url(r'^activate/$',views.ActivateView.as_view(), name='activate'),
    url(r'^login/$', views.LoginView.as_view(),name ='login'),#登陆账户
    url(r'^logout/$', views.LogoutView.as_view(),name ='logout'),
    url(r'^yzm/', views.VCodeView.as_view(),name='yzm'),#获取验证码
    url(r'^activate/', views.ActivateView.as_view(), name='activate'),#激活用户
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),#获取验证码图片
    url(r'^upgrade/$', views.Upgrade.as_view(),name ='upgrade'),#登陆账户
    # u(rl(r'^information',views.InforationView.as_view(),name = 'information'),
   #登陆账户)
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




# urlpatterns = format_suffix_patterns(urlpatterns)
# if settings.DEBUG:
#     urlpatterns += static(settings
