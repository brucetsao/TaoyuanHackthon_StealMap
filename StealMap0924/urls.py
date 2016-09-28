"""StealMap0924 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from game.views import index,one_story,two_story,three_story,four_question,five_analyze,six_output,seven_suggest,eight_success,page_guard_info,page_login,action_login,nine_coupon,personnel,page_window_info,page_officer_info,page_light_info,page_QRCode,page_camera_info,page_map
from monitor.views import monitor_index,page_data

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^index/',index),
    url(r'^1_Story/', one_story),
    url(r'^2_Story/', two_story),
    url(r'^3_Story/', three_story),
    url(r'^4_Question/', four_question),
    url(r'^4_Question/', four_question),
    url(r'^5_Analyze/', five_analyze),
    url(r'^6_Output/', six_output),
    url(r'^7_Suggest/', seven_suggest),
    url(r'^8_Success/', eight_success),
    url(r'^9_Coupon/', nine_coupon),
    url(r'^Personnel/',personnel),
    url(r'^page_guard_info/',page_guard_info),
    url(r'^page_window_info/', page_window_info),
    url(r'^page_officer_info/', page_officer_info),
    url(r'^page_light_info',page_light_info),
    url(r'^login/',page_login),
    url(r'^action_login/',action_login),
    url(r'^Monitor/Index',monitor_index),
    url(r'^Data',page_data),
    url(r'page_QRCode',page_QRCode),
    url(r'page_camera_info',page_camera_info),
    url(r'page_map',page_map)

]
