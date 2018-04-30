from rest_framework import serializers
from .models import Nuser
# from .models import Nuser


class ActivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nuser
        fields = ['username', 'password']

class UserCreateSerializer(serializers.ModelSerializer):
    yzm_text = serializers.CharField()
    yzm_cookie = serializers.CharField()
    password = serializers.CharField(label=',write_only=True,Password',style={'input_type': 'password'})
    username = serializers.CharField()
    class Meta:
        model = Nuser
        fields = [
            'username',
            'password',
            'yzm_text',
            'yzm_cookie',
        ]
        extra_kwargs = {
            "password": {"write_only": True}
        }

class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    class Meta:
        model = Nuser
        fields = ['username', 'password', 'sigh']