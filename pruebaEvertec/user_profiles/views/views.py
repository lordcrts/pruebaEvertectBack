# -*- encoding: utf-8 -*-

# Django
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

# Django Rest
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, mixins, permissions, views

# Models
from pruebaEvertec.user_profiles.models.models import UserProfile

# Serializers
from pruebaEvertec.user_profiles.serializers.serializers import UserAdminSerializer

from rest_framework_jwt.views import JSONWebTokenAPIView, jwt_response_payload_handler
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework_jwt.settings import api_settings

# Extras
from pruebaEvertec.utils.permissions import DontDeleteSelf
class UserAdminViewSet(viewsets.ModelViewSet):

    """
        Vista que permite  al administrador listar, ver, crear, actualizar y eliminar usuarios
    """
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = (permissions.IsAuthenticated,DontDeleteSelf)

    # def perform_destroy(self, instance):
    #     instance.is_active = False
    #     instance.save()


class Login(JSONWebTokenAPIView):

    """
    vista para el login, permite crear un token y crear el userprofile en caso de que no lo tenga
    """

    serializer_class = JSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            user = serializer.object.get('user') or request.user
            token = serializer.object.get('token')
            response_data = jwt_response_payload_handler(token, user, request)
            resp = {'id': user.id, 'username': user.username}
            resp.update(response_data)
            response = Response(resp)
            # response = Response(response_data)
            if api_settings.JWT_AUTH_COOKIE:
                expiration = (datetime.utcnow() +
                              api_settings.JWT_EXPIRATION_DELTA)
                response.set_cookie(api_settings.JWT_AUTH_COOKIE,
                                    response.data['token'],
                                    expires=expiration,
                                    httponly=True)
            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
