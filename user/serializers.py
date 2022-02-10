from django.contrib.auth import get_user_model, authenticate
from core.models import GlobalContact

from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _

from core.models import GlobalContact


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["phone_number", "password", "name", "email"]
        extra_kwargs = {
            "password": {"write_only": True, "min_length": 5},
            "phone_number": {"min_length": 10, "max_length": 10},
        }

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


class UserUpdateSerializer(UserSerializer):
    class Meta:
        model = get_user_model()
        fields = ["password", "name", "email"]
        extra_kwargs = {
            "password": {"write_only": True, "required": False, "min_length": 5},
        }

    def update(self, instance, validated_data):
        password = validated_data.pop("password", None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

class GlobalContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalContact
        exclude = ["owner"]
# class GlobalContactListSerializer(serializers.ListSerializer):

#     contacts = GlobalContctSerializer(many=True)
#     def up 


class AuthTokenSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    password = serializers.CharField(
        style={"input_type": "password"}, trim_whitespace=False
    )

    def validate(self, attrs):
        phone_number = attrs.get("phone_number")
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=phone_number,
            password=password,
        )
        if not user:
            msg = _("Unable to authenticate with provided credentials")
            raise serializers.ValidationError(msg, code="authetication")
        attrs["user"] = user
        return attrs
