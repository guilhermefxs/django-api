import re
from django.conf import settings
from django.forms import DateField
from rest_framework import serializers
from .models import Profile, Team

from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'date_joined': {'write_only': True},
            'groups': {'write_only': True},
            'user_permissions': {'write_only': True},
            'is_active': {'write_only': True},
            'is_staff': {'write_only': True},
            'last_name': {'write_only': True},
            'first_name': {'write_only': True},
            'last_login': {'write_only': True},
        }


    email = serializers.EmailField()

    def validate_email(self, value):
        if Profile.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists!")
        try:
            validate_email(value)
        except ValidationError as e:
            raise serializers.ValidationError(str(e))
        return value
    
    def create(self, validated_data):
        user = Profile(
            username=validated_data['username'],
            email=validated_data['email'],
            name=validated_data['name'],
            profileImage=validated_data['profileImage']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    
class TeamSerializer(serializers.ModelSerializer):
    data_fundacao = DateField(input_formats=settings.DATE_INPUT_FORMATS)
    class Meta:
        model = Team
        fields = '__all__'
