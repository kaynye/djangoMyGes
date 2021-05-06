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
    path('prof/course/<int:id>', views.profCourseDetails, name="profCourseDetails"),
    path('prof/students', views.students, name="students"),
    path('prof/students/<int:id>/notes', views.notePost, name="noteOperation"),
    path('prof/students/notes/<int:id>/<int:id_student>/delete', views.NoteDelete, name="NoteDelete"),
    path('prof/students/<int:id>/note', views.notePost, name="notePost"),
    
    path('coordinateur/user', views.coordinateurUserCreate, name="coordinateurUserCreate"),
    path('coordinateur/user/<int:id>/edit', views.coordinateurUserEdit, name="coordinateurUserEdit"),
    path('coordinateur/user/<int:id>/delete', views.coordinateurUserDelete, name="coordinateurUserDelete"),
    
    path('coordinateur/matiere', views.coordinateurMatiereCreate, name="coordinateurMatiereCreate"),
    path('coordinateur/matiere/<int:id>/edit', views.coordinateurMatiereEdit, name="coordinateurMatiereEdit"),
    path('coordinateur/matiere/<int:id>/delete', views.coordinateurMatiereDelete, name="coordinateurMatiereDelete"),
    
    path('coordinateur/event', views.coordinateurEventCreate, name="coordinateurEventCreate"),
    path('coordinateur/event/<int:id>/edit', views.coordinateurEventEdit, name="coordinateurEventEdit"),
    path('coordinateur/event/<int:id>/delete', views.coordinateurEventDelete, name="coordinateurEventDelete"),
    
    path('coordinateur/classroom', views.coordinateurClassroomCreate, name="coordinateurClassroomCreate"),
    path('coordinateur/classroom/<int:id>/edit', views.coordinateurClassroomEdit, name="coordinateurClassroomEdit"),
    path('coordinateur/classroom/<int:id>/delete', views.coordinateurClassroomDelete, name="coordinateurClassroomDelete"),
    
    path("change_profile", views.model_form_upload, name="change_profile"),
    path("change_profile", views.model_form_upload, name="change_profile"),
    
    path("get_events", views.get_events, name="get_events"),
    
    path('prof/students/notes/<int:id>/<int:id_student>/update', views.NoteUpdate, name="NoteUpdate")
]
