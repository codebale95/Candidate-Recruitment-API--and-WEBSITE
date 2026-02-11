from rest_framework import serializers
from .models import Candidate, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'name', 'email', 'role', 'resume', 'stage', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
