from rest_framework import serializers

from account.models import Profile

class ProfileSerilizer(serializers.ModelSerilizer):
    
    class Meta:
        
        model = Profile
        fields = "__all__"
        read_only_fields = ["created_at","updated_at"]