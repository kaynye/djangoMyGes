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
    path('prof/course/<int:id>/class/<int:class_id>/students', views.profCourseStudents,name="profCourseStudents"),
    path('profile', views.profile,name="profile"),
    path("change_password", views.change_password, name="change_password"),
    path("classes", views.student_class, name="classes"),
    path("planning", views.planning, name="planning"),
    path("notes", views.notes, name="notes"),
<<<<<<< HEAD
    path('prof/course/<int:id>', views.profCourseDetails, name="profCourseDetails"),
    path('prof/students', views.students, name="students"),
    path('prof/students/note', views.noteOperation, name="noteOperation"),

    path("change_profile", views.model_form_upload, name="change_profile")
=======
    path("change_profile", views.model_form_upload, name="change_profile"),
    path("get_events", views.get_events, name="get_events")
>>>>>>> student
]
