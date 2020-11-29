
# -*- encoding: utf-8 -*-
from rest_framework.permissions import BasePermission

class DontDeleteSelf(BasePermission):
    """
    No eliminar el usuario con el que se esta logeado
    """
    def has_object_permission(self, request, view, obj):

        ret = False

        if request.method == 'DELETE':

            if obj.id != request.user.id:
                ret = True
        else:

            ret = request.user.is_authenticated

        return ret