from rest_framework import serializers
from .models import CustomUser, Role

class UserRegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'confirm_password', 'role', 'phone_number', 'email']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password before creating user
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ('id', 'name')


class ProfileSerializer(serializers.ModelSerializer):
    role = RoleSerializer()

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email','status', 'phone_number', 'role')

class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone_number', 'email']