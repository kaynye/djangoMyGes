from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth import login, authenticate, logout
from django_app.models import *
from django.contrib import messages  # import messages
import django.utils.timezone as timezone
from django.contrib import messages  # import messages
from django.contrib.auth.models import User, Group
from .forms import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.http import JsonResponse
from pprint import pprint

@login_required
def home(request):
    return render(request,"django_app/home.html", {"range": range(9), "random": range(20, 60)})


def login_page(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect("django_app:home")
    else:
        return render(request, "django_app/index.html")


@login_required
def profile(request):
    getClass = Classroom.objects.filter(c_student=request.user).all().order_by("c_promotion").first()
    form = ProfileUserForm()

    return render(request,"django_app/profile.html", {"class": getClass, "form": form})

@login_required
def planning(request):
    return render(request, "django_app/planning.html")

@login_required
def notes(request):
    getClass = Classroom.objects.filter(c_student=request.user).all().order_by("c_promotion")
    
    content = {}

    #  Add Matiere

    moyennes = []

    for elem in getClass:
        notesGlobal = []
        content[elem.c_name] = {}
        getMatieres = Matiere.objects.filter(m_classroom=elem)
        for matiere in getMatieres:
            content[elem.c_name][matiere.m_name] = {}
            content[elem.c_name][matiere.m_name]["intervenants"] = []
            content[elem.c_name][matiere.m_name]["notes"] = []
            content[elem.c_name][matiere.m_name]["coef"] = matiere.m_coefficient
            notes = []
            for intervenant in matiere.m_profs.all():
                content[elem.c_name][matiere.m_name]["intervenants"].append(intervenant.first_name + " " + intervenant.last_name)
            for note in matiere.m_note.all().filter(n_eleve=request.user).filter(n_matiere__m_classroom=elem):
                notes.append(note.n_note)
                content[elem.c_name][matiere.m_name]["notes"].append({"note": note.n_note, "type": note.n_type.tn_name})
            
            if len(notes) != 0:
                content[elem.c_name][matiere.m_name]["moy"] = round(sum(notes) / len(notes), 2)
                notesGlobal.append((content[elem.c_name][matiere.m_name]["moy"], matiere.m_coefficient))

        calcMoyenne = 0
        totalCoef = 0

        for k,v in notesGlobal:
            calcMoyenne += k*v
            totalCoef += v 

        calcMoyenne = calcMoyenne / totalCoef
        moyennes.append(round(calcMoyenne, 2))

    return render(request, "django_app/notes.html", {"data": content, "moy": moyennes})


@login_required
def change_password(request):
    if (
        request.POST.get("actual_password")
        and request.POST.get("new_password")
        and request.POST.get("re_password")
    ):
        if (
            authenticate(
                username=request.user.username,
                password=request.POST.get("actual_password"),
            )
            is not None
        ):
            if request.POST.get("new_password") == request.POST.get("re_password"):
                request.user.set_password(request.POST.get("new_password"))
                request.user.save()
                messages.success(request, "Le mot de passe à correctement été changée.")
                return redirect("django_app:login_page")
            else:
                messages.error(request, "Les mots de passes ne correspondent pas.")
                return redirect("django_app:profile")
        else:
            messages.error(request, "Le mot de passe actuel est incorrect.")
            return redirect("django_app:profile")


@login_required
def student_class(request):
    getClass = Classroom.objects.filter(c_student=request.user).all().order_by("c_promotion")
    print("CLASE CLASSE CLASSE", getClass)
    return render(request, "django_app/classes.html", {"classes": getClass})

@csrf_exempt
def loginUser(request):
    res = {}
    print(request.POST)
    if request.POST.get("pseudo") and request.POST.get("password"):
        user = authenticate(
            username=request.POST.get("pseudo"), password=request.POST.get("password")
        )
        if user is not None:
            login(request, user)
            return redirect("django_app:home")
        else:
            return render(request, "django_app/index.html", {"erreur": True})


@login_required
def logoutUser(request):
    logout(request)
    return redirect("django_app:login_page")

@login_required
def profCourse(request):
    courses = Matiere.objects.all()

    return render(request, "django_app/prof.course.html", {"courses": courses})


@login_required
def profCourseStudents(request, id):
    course = Matiere.objects.get(id=id)
    
    return render(
        request,
        "django_app/prof.course.students.html",
        {"classrooms": course.m_classroom.all()},
    )


@login_required
def profCourseDetails(request, id):
    course = Matiere.objects.get(id=id)
    classrooms = course.m_classroom.filter(c_promotion=timezone.now().year)
    
    return render(
        request,
        "django_app/prof.course.details.html",
        {"course": course, "classrooms": classrooms},
    )


@login_required
def students(request):
    group = Group.objects.filter(name="eleve").first()
    students = User.objects.filter(groups=group).all()

    return render(
        request,
        "django_app/prof.all.students.html",
        {
            "students": students,
        },
    )

@login_required
def profCourseStudents(request, id, class_id):
    course = Matiere.objects.get(id=id)
    classroom = course.m_classroom.get(id=class_id)
    students = classroom.c_student.all()
    
    return render(
        request,
        "django_app/prof.all.students.html",
        {"students": students,"displyNote": True},
    )
    
def notePost(request,id):
    student = User.objects.get(id=id)
    notes = Note.objects.filter(n_eleve=id).all()
    form = NoteForm(request.POST or None)
    if form.is_valid():
        note=form.save()
        note.n_eleve=student
        note.save()

    
    return render(request, "django_app/prof.student.note.html",
                  {
                   "notes":notes,
                    "form": form,
                    "title": "Note"
                  })
    
    
# delete view for details
def NoteDelete(request, id,id_student):

    note = Note.objects.get(id=id)
    current_user = request.user
    note.delete()  
    return redirect('django_app:notePost', id=id_student)

@login_required
def NoteUpdate(request, id,id_student):
    note = Note.objects.get(id=id)
    
    if request.method == "POST":
        form = NoteForm(request.POST or None,instance = note)

        if form.is_valid():
            note = form.save()
            form = NoteForm(instance = note)

        return redirect('django_app:notePost', id=id_student)

    else:
        form = NoteForm(instance = note)


    return render(
        request,
        "django_app/form.update.note.html",
        {"form": form, "title": "Notes"},
    )

@login_required
def coordinateurUserCreate(request):
    users = User.objects.all()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = UserCreationForm()

            return render(
                request,
                "django_app/coordinateur.user.html",
                {
                    "form": form,
                    "users": users,
                    "title": "Utilisateurs",
                    "method": "POST",
                },
            )
    else:
        form = UserCreationForm()

    return render(
        request,
        "django_app/coordinateur.user.html",
        {"form": form, "users": users, "title": "Utilisateurs", "method": "POST"},
    )


@login_required
def coordinateurUserEdit(request, id):
    user = User.objects.get(id=id)

    if request.method == "POST":
        form = EditUserForm(request.POST, instance = user)
        if form.is_valid():
            user = form.save()
            form = EditUserForm(instance = user)

            return redirect('django_app:coordinateurUserCreate')

    else:
        form = EditUserForm(instance = user)


    return render(
        request,
        "django_app/form_generique.html",
        {"form": form, "title": "Utilisateurs", "method": "POST"},
    )

@login_required
def coordinateurUserDelete(request, id):
    user = User.objects.get(id=id)

    user.delete()
        
    return redirect('django_app:coordinateurUserCreate')

@login_required
def coordinateurMatiereCreate(request):
    matieres = Matiere.objects.all()

    if request.method == "POST":
        form = MatiereCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = MatiereCreationForm()

            return render(
                request,
                "django_app/coordinateur.matiere.html",
                {
                    "form": form,
                    "matieres": matieres,
                    "title": "Matieres",
                    "method": "POST",
                },
            )
    else:
        form = MatiereCreationForm()

    return render(
        request,
        "django_app/coordinateur.matiere.html",
        {"form": form, "matieres": matieres, "title": "Matieres", "method": "POST"},
    )


@login_required
def coordinateurMatiereEdit(request, id):
    matiere = Matiere.objects.get(id=id)

    if request.method == "POST":
        form = EditEventForm(request.POST, instance = matiere)
        if form.is_valid():
            matiere = form.save()
            form = EditEventForm(instance = matiere)

            return redirect('django_app:coordinateurMatiereCreate')

    else:
        form = EditEventForm(instance = matiere)


    return render(
        request,
        "django_app/form_generique.html",
        {"form": form, "title": "Matieres", "method": "POST"},
    )

@login_required
def coordinateurMatiereDelete(request, id):
    matiere = Matiere.objects.get(id=id)

    matiere.delete()
        
    return redirect('django_app:coordinateurMatiereCreate')

@login_required
def model_form_upload(request):
    if request.method == 'POST':
        form = ProfileUserForm(request.POST, request.FILES)
        if form.is_valid():
            f = form.save(commit=False)
            
            if ProfileUser.objects.filter(pu_user=request.user).exists():
                ProfileUser.objects.filter(pu_user=request.user).first().delete()

            messages.success(request, "L'image à correctement été changée." )
            f.pu_user = request.user
            f.save()
        else:
            messages.error(request, "L'image envoyé ne correspond pas aux attentes de l'application." )
        
    return redirect("django_app:profile")

@csrf_exempt
@login_required
def get_events(request):
    if request.method == 'POST':
        results = []
        getClass = Classroom.objects.filter(c_student=request.user).all().order_by("c_promotion").first()
        getEvenements = Evenement.objects.filter(e_class=getClass).all()

        for event in getEvenements:
            results.append({"title": event.e_name, "start": event.e_date_debut, "end": event.e_date_fin})

        return JsonResponse(results, safe=False)
    else:
        return JsonResponse({"method_allowed": ["POST"]})

@login_required
def coordinateurEventCreate(request):
    events = Evenement.objects.all()

    if request.method == "POST":
        form = EventCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = EventCreationForm()

            return render(
                request,
                "django_app/coordinateur.event.html",
                {
                    "form": form,
                    "events": events,
                    "title": "Événements",
                    "method": "POST",
                },
            )
    else:
        form = EventCreationForm()

    return render(
        request,
        "django_app/coordinateur.event.html",
        {"form": form, "events": events, "title": "Événements", "method": "POST"},
    )


@login_required
def coordinateurEventEdit(request, id):
    event = Evenement.objects.get(id=id)

    if request.method == "POST":
        form = EditEventForm(request.POST, instance = event)
        if form.is_valid():
            event = form.save()
            form = EditEventForm(instance = event)

            return redirect('django_app:coordinateurEventCreate')

    else:
        form = EditEventForm(instance = event)


    return render(
        request,
        "django_app/form_generique.html",
        {"form": form, "title": "Événements", "method": "POST"},
    )

@login_required
def coordinateurEventDelete(request, id):
    event = Evenement.objects.get(id=id)

    event.delete()
        
    return redirect('django_app:coordinateurEventCreate')

@login_required
def coordinateurClassroomCreate(request):
    classrooms = Classroom.objects.all()

    if request.method == "POST":
        form = ClassroomCreationForm(request.POST)
        if form.is_valid():
            form.save()
            form = ClassroomCreationForm()

            return render(
                request,
                "django_app/coordinateur.classroom.html",
                {
                    "form": form,
                    "classrooms": classrooms,
                    "title": "Classes",
                    "method": "POST",
                },
            )
    else:
        form = ClassroomCreationForm()

    return render(
        request,
        "django_app/coordinateur.classroom.html",
        {"form": form, "classrooms": classrooms, "title": "Classes", "method": "POST"},
    )


@login_required
def coordinateurClassroomEdit(request, id):
    classroom = Classroom.objects.get(id=id)

    if request.method == "POST":
        form = EditClassroomForm(request.POST, instance = classroom)
        if form.is_valid():
            classroom = form.save()
            form = EditClassroomForm(instance = classroom)

            return redirect('django_app:coordinateurClassroomCreate')

    else:
        form = EditClassroomForm(instance = classroom)


    return render(
        request,
        "django_app/form_generique.html",
        {"form": form, "title": "Classes", "method": "POST"},
    )

@login_required
def coordinateurClassroomDelete(request, id):
    classroom = Classrooom.objects.get(id=id)

    classroom.delete()
        
    return redirect('django_app:coordinateurClassroomCreate')