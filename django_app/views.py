from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth import login, authenticate,logout
from django_app.models import *
from django.contrib import messages #import messages


@login_required
def home(request):
    return render(request,"django_app/home.html")


def login_page(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('django_app:home')
    else:
        return render(request,"django_app/index.html")

@login_required
def profile(request):
    getClass = Classroom.objects.filter(c_student=request.user).all().order_by("c_promotion").first()

    print(getClass)
    return render(request,"django_app/profile.html", {"class": getClass})

@login_required
def planning(request):
    return render(request, "django_app/planning.html")

def notes(request):
    return render(request, "django_app/notes.html")

@login_required
def change_password(request):
    if request.POST.get("actual_password") and request.POST.get("new_password") and request.POST.get("re_password"):
        if authenticate(username=request.user.username, password=request.POST.get("actual_password")) is not None:
            if request.POST.get("new_password") == request.POST.get("re_password"):
                request.user.set_password(request.POST.get("new_password"))
                request.user.save()
                messages.success(request, "Le mot de passe à correctement été changée." )
                return redirect("django_app:login_page")
            else:
                messages.error(request, "Les mots de passes ne correspondent pas.")
                return redirect("django_app:profile")
        else:
            messages.error(request, "Le mot de passe actuel est incorrect.")
            return redirect("django_app:profile")

@login_required
def student_class(request):
    getClass = Classroom.objects.filter(c_student=request.user).all().order_by("c_promotion").first()
    getStudents = getClass.c_student.all()
    return render(request, "django_app/classes.html", {"students": getStudents, "class": getClass})

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

    return render(request,"django_app/prof.course.students.html",{
            "classrooms" : course.m_classroom.all()
            })

@login_required
def profCourseDetails(request,id):
    course = Matiere.objects.get(id=id)

    return render(request,"django_app/prof.course.students.html",{
            "course" : course
            })