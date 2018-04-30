
from account import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # url(r'^activate/$',views.ActivateView.as_view(), name='activate'),
    url(r'^login/$', views.LoginView.as_view(),name ='login'),
    url(r'^yzm/', views.VCodeView.as_view(),name='yzm'),
    url(r'^activate/', views.ActivateView.as_view(), name='activate'),

]

# urlpatterns = format_suffix_patterns(urlpatterns)
# if settings.DEBUG:
#     urlpatterns += static(settings