from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from apps.user.models import Address
from PIL import Image


User = get_user_model()


class UserPassLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, allow_blank=False)
    password = serializers.CharField(max_length=128, allow_blank=False)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')
        user = authenticate(username=username, password=password)
        data["user"] = user
        return data
    

class UserSignUpSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(max_length=128, allow_blank=False, write_only=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'password_confirm', 'email']
        extra_kwargs = {
            'first_name': {'required': True, "allow_blank": False},
            'last_name': {'required': True, "allow_blank": False}
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value

    def validate(self, data):
        if data.get('password') != data.get('password_confirm'):
            raise serializers.ValidationError(_("passwords are not same."))
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            **validated_data
        )
        return user


class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image']

    def validate_image(self, value):
        image = Image.open(value)
        width, height = image.size
        if width != height:
            raise serializers.ValidationError(_("image must be square."))
        return value


class UserInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=255, allow_blank=False)
    last_name = serializers.CharField(max_length=255, allow_blank=False)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "birth_date", "username", "email"]


class UserAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"


class UserPasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    new_password1 = serializers.CharField(max_length=128, allow_blank=False, write_only=True)
    new_password2 = serializers.CharField(max_length=128, allow_blank=False, write_only=True)

    def validate(self, data):
        user = self.context['request'].user
        old_password = data.get("old_password")
        new_password1 = data.get("new_password1")
        new_password2 = data.get("new_password2")

        if not user.check_password(old_password):
            raise serializers.ValidationError(_("current password is incorrect."))

        if new_password1 != new_password2:
            raise serializers.ValidationError("passwords are not same.")

        return data

    def save(self):
        user = self.context["request"].user
        new_password = self.validated_data["new_password1"]
        user.set_password(new_password)
        user.save()
