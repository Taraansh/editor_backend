from rest_framework import serializers
from accounts.models import Profile
from django.contrib.auth.hashers import make_password

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id", "user_name", "user_contact", "user_email", "password"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = make_password(password)
        profile = Profile(**validated_data)
        profile.password = hashed_password
        profile.save()
        return profile

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.user_name
        token['user_email'] = user.user_email
        return token