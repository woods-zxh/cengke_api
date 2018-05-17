from rest_framework import serializers
from .models import Nuser
# from .models import Nuser




class ActivateSerializer(serializers.ModelSerializer):
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

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        if not username:
            raise serializers.ValidationError('lack username')
        if not password:
            raise serializers.ValidationError('lack password')
        return data

    def validate_username(self,value):
        data = self.get_initial()
        username = data.get('username')
        user_qs = Nuser.objects.filter(username=username)
        if user_qs.exists():
            raise serializers.ValidationError("The username has been registered.")
        return value

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(label=',write_only=True,Password',style={'input_type': 'password'})
