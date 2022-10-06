from tokenize import Name
from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.loginuser),
    path('register/', views.registeruser),
    path('logoutuser/', views.logoutuser),
    path('dashboardtask/', views.dashboardtask),
    path('dashboardtask/create/', views.createtask),
    path('dashboardtask/updatetask/<int:task__id>', views.updatetask, name="task_updatetask"),
    path('dashboardtask/<int:task__id>/terminated', views.taskterminated, name="task_terminated"),
    path('dashboardtask/terminate/', views.deletetask),
    path('dashboardtask/delete/<int:task__id>', views.deletetaskid, name="task_delete")
]
