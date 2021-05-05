from django.db import models
from django.contrib.auth.models import User
from datetime import datetime



# description = models.CharField(max_length=200)
class Classroom(models.Model):
    c_name = models.CharField(max_length=10, verbose_name="Nom de la classe")
    c_student = models.ManyToManyField(User,verbose_name="Eleves de la classe")
    c_promotion = models.IntegerField(default=datetime.now().year, verbose_name="Année de la promotion")
    
    def __str__(self):
        return self.c_name

class Evenement(models.Model):
    e_name = models.CharField(max_length=255, verbose_name="Nom de l'evenement")
    e_date_debut = models.DateTimeField(default=datetime.now(), verbose_name="date de debut")
    e_date_fin = models.DateTimeField(default=datetime.now(), verbose_name="date de fin")
    e_frequent = models.BooleanField(default=False,verbose_name="Arrive toute les semaines")
    e_is_presenciel = models.BooleanField(default=True,verbose_name="Cours en presentiel")
    e_commentaire = models.TextField(max_length=400, verbose_name="Detail")
    e_class = models.ManyToManyField(Classroom,verbose_name="Classes de l'evenement")

    def __str__(self):
        return self.e_name
class Matiere(models.Model):
    m_name = models.CharField(max_length=255, verbose_name="Nom de la matiere")
    m_description = models.TextField(max_length=400, verbose_name="description")
    m_coefficient = models.IntegerField(verbose_name="Coefficient de la matiere")
    m_profs = models.ManyToManyField(User,verbose_name="Prof de la matiére")
    m_evenement = models.ManyToManyField(Evenement, verbose_name="Evenements")
    m_classroom = models.ManyToManyField(Classroom, verbose_name="Classrooms")


    def __str__(self):
        return self.m_name
    
class SupportDeCours(models.Model):
    sdc_name=models.CharField(max_length=255, verbose_name="Nom du support")
    sdc_file = models.FileField(blank=True, verbose_name="fichier")
    sdc_matiere = models.ManyToManyField(Matiere, verbose_name="Support de cours")
    e_proprietaire = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name="proprietaire", null=True)


class TypeNote(models.Model):
    class Meta:
        verbose_name = "Type de note"
        verbose_name_plural = "Type de notes"
    tn_name = models.CharField(max_length=50, verbose_name="nom du type de cours")
    
    def __str__(self):
        return self.tn_name
class Note(models.Model):
    n_note = models.IntegerField(verbose_name="node")
    n_type = models.ForeignKey(TypeNote, on_delete=models.PROTECT, related_name="tn_note",verbose_name="type de cours")
    n_matiere = models.ForeignKey(Matiere, on_delete=models.PROTECT,related_name="m_note", verbose_name="Matiére", null=True,blank=True)
    n_eleve = models.ForeignKey(User, on_delete=models.PROTECT,related_name="e_note", verbose_name="Eleve", null=True,blank=True)

    def __str__(self):
        return self.n_eleve+n_matiere





# Create your models here.
