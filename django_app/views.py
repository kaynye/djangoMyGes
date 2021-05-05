from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth import login, authenticate,logout
from django_app.models import *



@login_required
def home(request):
    return render(request,"django_app/home.html")


def login_page(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('django_app:home')
    else:
        return render(request,"django_app/index.html")



@csrf_exempt
def loginUser(request):
    res={}
    print(request.POST)
    if request.POST.get("pseudo") and request.POST.get("password"):
        user = authenticate(username=request.POST.get("pseudo"), password=request.POST.get("password"))
        if user is not None:
            login(request, user)
            return redirect('django_app:home')
        else:
            return render(request,"django_app/index.html",{"erreur": True})

@login_required
def logoutUser(request):
    logout(request)
    return redirect('django_app:login_page')

@login_required
def profCourse(request):
    courses = Matiere.objects.all()
    return render(request,"django_app/prof.course.html",{
            "courses" : courses
            })

@login_required
def profCourseStudents(request,id):
    course = Matiere.objects.get(id=id)
    print(course.m_classroom)
    return render(request,"django_app/prof.course.students.html",{
            "classrooms" : course.m_classroom.all()
            })

