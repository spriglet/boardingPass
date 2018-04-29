from django.views.generic import TemplateView # Import TemplateView
from django.template.loader import get_template
from rest_framework.authentication import SessionAuthentication, BasicAuthentication


class IndexView(TemplateView):

    template_name = 'index.html'


class LoginView(TemplateView):

    template_name = 'login.html'


class SchedulerView(TemplateView):

    template_name = 'scheduler.html'

class SenseiListView(TemplateView):

    template_name = 'list.html'

class SenseiProfileView(TemplateView):

    template_name = 'senseiProfile.html'

class CreateClassView(TemplateView):

    template_name = 'createclass.html'