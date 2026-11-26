from django.db import models
from django.contrib.auth.models import User


# Create your models here.

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
    diseases = models.CharField(null=True, blank=True, max_length=225)
    traitements = models.CharField(null=True, blank=True, max_length=225)
    
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    is_active = models.BooleanField(default=False)
    
    
    def __set__(self, instance, value):
        return self.fullname
