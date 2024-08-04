from django.urls import path
from . import views
from django.views.generic import TemplateView
urlpatterns = [
    # ... your other URL patterns ...
    path('', TemplateView.as_view(template_name='index.html')),
]