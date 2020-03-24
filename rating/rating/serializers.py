from rest_framework import serializers
from .models import Professor, Module, User, Rate

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields='__all__'

class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields='__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields='__all__'

class RateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rate
        fields='__all__'
