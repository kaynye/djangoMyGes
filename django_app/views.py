from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages #import messages
from .models import Classroom
from .models import Matiere
from .models import Note
from .models import ProfileUser
from .models import Evenement
from .forms import ProfileUserForm
from pprint import pprint
from django.http import JsonResponse

@login_required
def home(request):
    return render(request,"django_app/home.html", {"range": range(9), "random": range(20, 60)})


def login_page(request):
    print(request.user)
    if request.user.is_authenticated:
        return redirect('django_app:home')
    else:
        return render(request,"django_app/index.html")

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
    getClass = Classroom.objects.filter(c_student=request.user).all().order_by("c_promotion")

    return render(request, "django_app/classes.html", {"classes": getClass})

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
