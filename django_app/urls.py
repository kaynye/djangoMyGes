from django.contrib import admin
from django.urls import include, path

from django_app import views


app_name = 'django_app'



urlpatterns = [
    path('', views.login_page,name="login_page"),
    path('home', views.home,name="home"),
    path('loginUser', views.loginUser,name="loginUser"),
    path('logoutUser', views.logoutUser,name="logoutUser"),
    path('prof/course', views.profCourse,name="profCourse"),
    path('prof/course/<int:id>/students/', views.profCourseStudents,name="profCourseStudents"),




]
