from django.urls import path, re_path, include
from . import views
app_name = 'groups'
urlpatterns = [
    path("", views.ListGroup, name="group"),
    re_path("add_groups/", views.add_Group, name="add_groups"),
    re_path(r"join/(?P<slug>[-\w]+)/$",views.JoinGroup.as_view(),name="join"),
    re_path(r"leave/(?P<slug>[-\w]+)/$",views.LeaveGroup.as_view(),name="leave"),
   
]