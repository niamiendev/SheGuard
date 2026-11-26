from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Disease, Profile, Treatment

class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        
        model = Profile
        fields = "__all__"
        read_only_fields = ["id", "role", "user", "is_active", "created_at", "updated_at"]
        
        
class UserSerializer(serializers.ModelSerializer):
    
    profile = ProfileSerializer(required=False)
    
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ["id", "username", "email", "password","profile"]

    @transaction.atomic
    def create(self, validated_data):
        
        # récuperer le profile
        profile_data = validated_data.pop("profile",{})
        
        user = User.objects.create_user(**validated_data)
        
        Profile.objects.create(
            user = user,
            **profile_data
        )
        
        return user
    
class DiseaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Disease
        fields = [
            "id",
            "name",
            "description",
            "diagnosed_at",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

class TreatmentSerializer(serializers.ModelSerializer):

    disease_name = serializers.CharField(
        source="disease.name",
        read_only=True
    )

    class Meta:
        model = Treatment
        fields = [
            "id",
            "disease",
            "disease_name",
            "name",
            "dosage",
            "frequency",
            "start_date",
            "end_date",
            "description",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "disease_name",
            "created_at",
            "updated_at",
        ]

    def validate_disease(self, disease):
        request = self.context.get("request")

        if disease and request:
            if disease.profile != request.user.profile:
                raise serializers.ValidationError(
                    "Cette maladie n'appartient pas à votre profil."
                )

        return disease