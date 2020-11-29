# -*- encoding: utf-8 -*-

# Django
from django.contrib.auth.models import User
from django.conf import settings

# Django Rest
from rest_framework import serializers, exceptions
from drf_extra_fields.fields import Base64ImageField
from rest_framework.utils import model_meta
# Models
from pruebaEvertec.user_profiles.models.models import UserProfile
from drf_dynamic_fields import DynamicFieldsMixin

"""
    Serializador de perfil de usuario donde se definen los campos necesarios
"""


class UserProfileSerializer(DynamicFieldsMixin, serializers.ModelSerializer):
    cover_photo = Base64ImageField()
    class Meta:
        model = UserProfile
        exclude = ('user',)

"""
    Serializador de usuarios donde se definen los campos necesarios de éste
    Ademas se relaciona al Serializador de perfil de usuario con el fin de tener ambos como un todo.
    Se redefinen los metodos de crear y actualizar con el fin de dar la logica correspondiente al uso final en la aplicación
"""


class UserAdminSerializer(DynamicFieldsMixin, serializers.ModelSerializer):

    userprofile = UserProfileSerializer()
    
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'userprofile')
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        instance = User.objects.create(**validated_data)
        UserProfile.objects.create(user=instance, **userprofile_data)
        return instance

    # def create(self, validated_data):
    #     uu = User.objects.filter(username__iexact=self.data["username"]).first()
    #     if uu != " " and uu is not None:
    #         raise exceptions.ParseError(detail='El username ya existe')
    #     else:
    #         password = validated_data.pop('password', None)
    #         userprofile_data = validated_data.pop('userprofile')
    #         instance = self.Meta.model(**validated_data)
    #         if password is not None:
    #             instance.set_password(password)
    #         instance.save()
    #         UserProfile.objects.create(user=instance, **userprofile_data)
    #     print(instance)
    #     print(userprofile_data)
    #     return instance

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile')
        userprofile = instance.userprofile
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)

        for attr, value in validated_data.items():
            if attr == 'password':
                pass
            else:
                setattr(instance, attr, value)

        for attr, value in userprofile_data.items():
            setattr(userprofile, attr, value)

        instance.save()
        userprofile.save()

        return instance
