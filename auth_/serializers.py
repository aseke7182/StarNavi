from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .messages import user_exists
from .models import User


class UserSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    last_activity = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')
    last_login = serializers.DateTimeField(format='%d.%m.%Y %H:%M:%S')

    class Meta:
        model = User
        fields = ('id', 'username', 'name', 'surname', 'created_at', 'last_activity', 'last_login',)


class RegistrationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, required=True)
    name = serializers.CharField(max_length=50, required=True)
    surname = serializers.CharField(max_length=50, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('name', 'surname', 'password', 'username')

    def validate_username(self, username):
        if username and User.objects.filter(username__exact=username).exists():
            raise serializers.ValidationError(user_exists)
        return username

    def create(self, validated_data):
        user = super().create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserLoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password',)

    def create(self, validated_data):
        return User(**validated_data)
