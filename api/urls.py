# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.authtoken.views import obtain_auth_token # add this import


urlpatterns = {
    url(r'^auth/', include('rest_framework.urls',  # ADD THIS URL
                           namespace='rest_framework')),
    url(r'^lesson/$', CreateLessonView.as_view(), name="create_lesson"),
    url(r'^timeslot/$', CreateTimeSlotView.as_view(), name="create"),
    url(r'^seat/$', SeatView.as_view(), name="create"),
    url(r'^lesson/(?P<pk>[0-9]+)/$',LessonView.as_view(), name="lesson"),
    url(r'^timeslot/(?P<pk>[0-9]+)/$',TimeSlotView.as_view(), name="timeslots"),
    url(r'^transaction/',CreateTransaction.as_view(), name="transactions"),
    url(r'^transactions/(?P<pk>[0-9]+)/$',TransactionView.as_view(), name="transaction"),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'^sensei/$', SenseiView.as_view(), name="sensei"),
    url(r'users/(?P<pk>[0-9]+)/$',UserLessonView.as_view(), name="user_details"),
    url(r'^get-token/', obtain_auth_token), # Add this line
}

urlpatterns = format_suffix_patterns(urlpatterns)