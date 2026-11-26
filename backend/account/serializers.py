from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.models import User
from account.models import Profile

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