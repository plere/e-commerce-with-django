from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings


JWT_PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
JWT_ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER

User = get_user_model()


class CustomRegisterSerializer(RegisterSerializer):
    address = serializers.CharField(max_length = 255)
    phone_number = serializers.CharField(max_length = 13)

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['address'] = self.validated_data.get('address', '')
        data_dict['phone_number'] = self.validated_data.get('phone_number', '')
        return data_dict


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length = 30)
    password = serializers.CharField(max_length = 128, write_only=True)
    token = serializers.CharField(max_length = 255, read_only = True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password', None)

        user = authenticate(username=username, password=password)

        if user is None:
            return {'username': 'None'}
        try:
            payload = JWT_PAYLOAD_HANDLER(user)
            jwt_token = JWT_ENCODE_HANDLER(payload)
            update_last_login(None, user)

        except User.DoesNotExist:
            raise serializers.ValidationError('User with given username and password does not exist')
        return {
            'username': user.username,
            'token': jwt_token
        }


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'address', 'phone_number')


