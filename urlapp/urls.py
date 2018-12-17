from django.urls import path, re_path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
    path(r'api/create', views.CreateView.as_view(), name="create"),
    path('', views.shorturlcreation, name='createurl'),
    path('<int:url_id>/info', views.details, name='info'),
    path('manage', views.manageurls, name='manage'),
    path('<int:url_id>/delete', views.delete, name='delete'),
    re_path(r'(?P<short_url>\w+)', views.redirect, name='redirect'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
