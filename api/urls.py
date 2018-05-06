# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.generic.base import TemplateView
from .views import *

from rest_framework.authtoken.views import obtain_auth_token # add this import


urlpatterns = {
    url('accounts/', include('rest_registration.api.urls')),
    url(r'^auth/', include('rest_framework.urls',  # ADD THIS URL
                           namespace='rest_framework')),
    url(r'^mylessons/$', MyLessonsView.as_view(), name="my_lessons"),
    url(r'^lesson/$', CreateLessonView.as_view(), name="create_lesson"),
    url(r'^sensei/lessons/(?P<sensei>.+)/$', SenseiLessonView.as_view(), name="sensei_lesson"),
    url(r'^timeslot/$', CreateTimeSlotView.as_view(), name="create"),
    url(r'^seat/$', SeatView.as_view(), name="create"),
    url(r'^lesson/(?P<pk>[0-9]+)/$',LessonView.as_view(), name="lesson"),
    url(r'^timeslot/(?P<pk>[0-9]+)/$',TimeSlotView.as_view(), name="timeslots"),
    url(r'^transaction/',CreateTransaction.as_view(), name="transactions"),
    url(r'^transactions/(?P<pk>[0-9]+)/$',TransactionView.as_view(), name="transaction"),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'^sensei/$', SenseiView.as_view(), name="sensei"),
    url(r'^sensei/data/(?P<user>.+)/$', SenseiViewProfileData.as_view(), name="sensei_profile_data"),
    url(r'users/(?P<pk>[0-9]+)/$',UserLessonView.as_view(), name="user_details"),


}

urlpatterns = format_suffix_patterns(urlpatterns)