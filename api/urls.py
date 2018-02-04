# api/urls.py

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateView
from .views import DetailsView

urlpatterns = {

    url(r'^lesson/$', CreateView.as_view(), name="create"),
    url(r'^lesson/(?P<pk>[0-9]+)/$',
        DetailsView.as_view(), name="details"),

}

urlpatterns = format_suffix_patterns(urlpatterns)