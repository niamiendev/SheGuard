from tokenize import TokenError
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.tokens import RefreshToken

from account.models import Disease, Profile, Treatment
from account.serializers import DiseaseSerializer, ProfileSerializer, TreatmentSerializer, UserSerializer
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User

from config.permissions import IsAdmin, IsSuperAdmin


# creer un compte
@api_view(["POST"])
def register_view(request):
    email = request.data.get("email")
    
    # Vérifier si l'utilisateur existe
    if User.objects.filter(email=email).exists():
        return Response(
            {
                "message": "Cet utilisateur existe déjà"
            },
            status=status.HTTP_409_CONFLICT
        )
    
    serializer = UserSerializer(data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message":"Inscription réuissi",
                "user": serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
            {
                "message":"Inscription a échoué ",
                "error": serializer.errors
            }
        )
        

#se connecter
@api_view(["POST"])
def login_view(request):
    email = request.data.get("email")
    password = request.data.get("password")
    
    if not email or not password:
        return Response(
            {
                "erreur":"Veuillez bien renseigner les champs"
            },
            status=status.HTTP_400_BAD_REQUEST
        )
        
    # Rechercher l'utilisateur avec son email
    try:
        user_obj = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response(
            {
                "erreur": "Email ou mot de passe incorrect"
            },
            status=status.HTTP_401_UNAUTHORIZED
        )

    
    user = authenticate(request, username = user_obj.username, password = password)
    
    if user is not None:
        login(request, user)
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message":"Connexion a réussie ",
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email
                }
            },
            status=status.HTTP_200_OK
        )
    
    return Response(
        {
            "erreur": "Email ou mot de passe incorrect"
        },
        status=status.HTTP_401_UNAUTHORIZED
    )
    
# se deconnecter
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    
    refresh_token = request.data.get("refresh")
    
    if not refresh_token:
        return Response(
            {"erreur": "Le refresh token est obligatoire"},
            status=status.HTTP_400_BAD_REQUEST
        )
        
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()

        return Response(
            {"message": "Déconnexion réussie"},
            status=status.HTTP_205_RESET_CONTENT
        )

    except TokenError:
        return Response(
            {"erreur": "Refresh token invalide ou déjà expiré"},
            status=status.HTTP_400_BAD_REQUEST
        )


# mon profile
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def me_view(request):

    user = request.user

    try:
        profile = user.profile

        return Response(
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "fullname": profile.fullname,
                "role": profile.role,
                "photo": request.build_absolute_uri(profile.photo.url) if profile.photo else None,
                "birth_day": profile.birth_day,
                "country": profile.country,
                "city": profile.city,
                "phone": profile.phone,
                "address": profile.address,
                "blood": profile.blood,
                "diseases": profile.diseases,
                "traitements": profile.traitements,
                "is_active": profile.is_active,
            },
            status=status.HTTP_200_OK
        )

    except Profile.DoesNotExist:
        return Response(
            {"erreur": "Profil introuvable"},
            status=status.HTTP_404_NOT_FOUND
        )

# modifier son profile
@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def me_update_view(request):

    user = request.user

    try:
        profile = user.profile

        serializer = ProfileSerializer(
            profile,
            data = request.data,
            partial = True,
            context = {"request":request}
        )
        if serializer.is_valid():
            serializer.save()
            
            return Response(
                {
                    "message": "Profil modifié avec succès",
                    "profile": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    except Profile.DoesNotExist:
        return Response(
            {"erreur": "Profil introuvable"},
            status=status.HTTP_404_NOT_FOUND
        )

        
# token et refresh
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def refresh_view(request):

    refresh = RefreshToken.for_user(request.user)
        
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_200_OK
    )


# récuperation de tous les utilsateur
@api_view(["GET"])
@permission_classes([IsAuthenticated, IsAdmin])
def profile_list_view(request):

    profiles = Profile.objects.all()

    serializer = ProfileSerializer(profiles, many=True)

    return Response(serializer.data)


# supprimer un utilsateur
@api_view(["DELETE"])
@permission_classes([IsAuthenticated, IsSuperAdmin])
def delete_user_view(request, pk):

    user = get_object_or_404(User, pk=pk)

    # Empêcher la suppression de son propre compte
    if user == request.user:
        return Response(
            {"erreur": "Vous ne pouvez pas supprimer votre propre compte"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user.delete()

    return Response(
        {
            "message": "Utilisateur supprimé avec succès"
        },
        status=status.HTTP_200_OK
    )

class DiseaseViewSet(ModelViewSet):
    serializer_class = DiseaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Disease.objects.filter(
            profile=self.request.user.profile
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)
        
class TreatmentViewSet(ModelViewSet):
    serializer_class = TreatmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Treatment.objects.filter(
            profile=self.request.user.profile
        ).order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)