from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Disease(models.Model):
    profile = models.ForeignKey(
        "account.Profile",
        on_delete=models.CASCADE,
        related_name="diseases"
    )

    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)

    diagnosed_at = models.DateField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Maladie"
        verbose_name_plural = "Maladies"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Treatment(models.Model):
    profile = models.ForeignKey(
        "account.Profile",
        on_delete=models.CASCADE,
        related_name="treatments"
    )

    disease = models.ForeignKey(
        Disease,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="treatments"
    )

    name = models.CharField(max_length=150)
    dosage = models.CharField(max_length=100, blank=True, null=True)
    frequency = models.CharField(max_length=150, blank=True, null=True)

    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Traitement"
        verbose_name_plural = "Traitements"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

class Profile(models.Model):

    ROLE = [
        ("SUPERADMIN", "Super Administrateur"),
        ("ADMIN", "Administrateur"),
        ("OPERATEUR", "Operateur"),
        ("VICTIM", "Victime")
    ]
    
    BLOODS = [
        ("UNDEFINED", "Indéfini"),
        ("A_POS", "A POSITIF"),
        ("AB_POS", "AB POSITIF"),
        ("B_POS", "B POSITIF"),
        ("O_POS", "O POSITIF"),
        ("A_NEG", "A NEGATIF"),
        ("AB_NEG", "AB NEGATIF"),
        ("B_NEG", "B NEGATIF"),
        ("O_NEG", "O NEGATIF")
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(choices=ROLE, default="VICTIM", max_length=10)
    photo = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    #username = models.CharField(max_length=50)
    fullname = models.CharField(max_length=50)
    #email = models.EmailField(max_length=50)
    birth_day = models.CharField(max_length=50, null=True, blank=True)
    
    
    country = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    
    blood = models.CharField(choices=BLOODS, default="UNDEFINED", max_length=10)
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    is_active = models.BooleanField(default=True)
    
    
    def __set__(self, instance, value):
        return self.fullname
