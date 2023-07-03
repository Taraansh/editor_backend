from rest_framework import serializers
from accounts.models import Profile
from .models import Page

class PageSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = Page
        fields = ['id', 'title', 'html_content', 'css_content', 'user_email']

    def get_user_email(self, obj):
        return obj.user_email.email
