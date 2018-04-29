"""boardingPass URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls import url, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

api_urlpatterns = [


    url('accounts/', include('rest_registration.api.urls')),
]
urlpatterns = [


    url(r'^admin/', admin.site.urls),
    url(r'^/', include('rest_auth.urls')),
    url('api/v1/', include(api_urlpatterns)),
    url('login/',LoginView.as_view()),
    url('scheduler/',SchedulerView.as_view()),
    url('createclass/',CreateClassView.as_view()),
    url('sensei/profile/',SenseiProfileView.as_view()),
    url('list/',SenseiListView.as_view()),
    url(r'^$',IndexView.as_view(),name='home'),
    url(r'^rest/', include('api.urls'))

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
