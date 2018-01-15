from django.urls import path, re_path
from . import views

urlpatterns = [
    path('',  views.shorturlcreation, name='createurl'),
    path('<int:url_id>/info', views.details, name='info'),
    path('manage', views.manageurls, name='manage'),
    path('<int:url_id>/delete', views.delete, name='delete'),
    re_path(r'(?P<short_url>\w+)',views.redirect, name='redirect'),
]
