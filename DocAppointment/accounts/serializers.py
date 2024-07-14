from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from .models import Profile

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

class ProfileSerializer(ModelSerializer):
    user = UserSerializer(read_only = True)

    class Meta:
        model = Profile
        fields = "__all__"