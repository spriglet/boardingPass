# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *
from rest_framework.authtoken.views import obtain_auth_token # add this import


urlpatterns = {
    url(r'^auth/', include('rest_framework.urls',  # ADD THIS URL
                           namespace='rest_framework')),
    url(r'^lesson/$', CreateLessonView.as_view(), name="create"),
    url(r'^timeslot/$', CreateTimeSlotView.as_view(), name="create"),
    url(r'^seat/$', CreateTimeSlotView.as_view(), name="create"),
    url(r'^lesson/(?P<pk>[0-9]+)/$',LessonView.as_view(), name="lesson"),
    url(r'^timeslot/(?P<pk>[0-9]+)/$',TimeSlotView.as_view(), name="timeslots"),
    url(r'^users/$', UserView.as_view(), name="users"),
    url(r'users/(?P<pk>[0-9]+)/$',UserLessonView.as_view(), name="user_details"),
    url(r'^get-token/', obtain_auth_token), # Add this line
}

urlpatterns = format_suffix_patterns(urlpatterns)