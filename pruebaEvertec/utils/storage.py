from django.core.files.storage import FileSystemStorage
from rest_framework.fields import (ImageField,)
from drf_extra_fields.fields import Base64FieldMixin
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.utils import six
from django.utils.translation import ugettext_lazy as _
import base64
import binascii
import imghdr
import uuid
from django.conf import settings
import os
import io
import base64
from PIL import Image


"""
    Sobreescribir imagen o archivo si existe
"""


class OverwriteStorage(FileSystemStorage):

    def get_available_name(self, name, max_length=500):

        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))
        return name


"""
    Funcion modificar base64 para que no permita null
"""


class Base64ImageField(Base64FieldMixin, ImageField):
    """
    Se trae la clase base64 para modificarla y decirle que no se permita imagenes vacias o nulas
    """
    ALLOWED_TYPES = (
        "jpeg",
        "jpg",
        "png",
        "gif"
    )
    INVALID_FILE_MESSAGE = _("Please upload a valid image.")
    INVALID_FILE_NONE_MESSAGE = _("This field can not be blank.")
    INVALID_TYPE_MESSAGE = _("The type of the image couldn't be determined.")
    MAX_SIZE_IMAGE = _("Size must be less than 2mb.")
    EMPTY_VALUES = (None, '', [], (), {})

    def get_file_extension(self, filename, decoded_file):
        extension = imghdr.what(filename, decoded_file)
        extension = "jpg" if extension == "jpeg" else extension
        return extension

    def to_internal_value(self, base64_data):
        # Check if this is a base64 string
        if base64_data in self.EMPTY_VALUES:
            """
            SE cambia el none por el mensaje que se quier mostrar
            """
            if self.context['request'].method != 'PATCH':
                raise ValidationError(self.INVALID_FILE_NONE_MESSAGE)
            else:
                return None

        if isinstance(base64_data, six.string_types):
            # Strip base64 header.
            if ';base64,' in base64_data:
                header, base64_data = base64_data.split(';base64,')

            # Try to decode the file. Return validation error if it fails.
            try:
                decoded_file = base64.b64decode(base64_data)
            except (TypeError, binascii.Error, ValueError):
                raise ValidationError(self.INVALID_FILE_MESSAGE)
            # Generate file name:
            file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
            # Get the file name extension:
            file_extension = self.get_file_extension(file_name, decoded_file)
            if file_extension not in self.ALLOWED_TYPES:
                raise ValidationError(self.INVALID_TYPE_MESSAGE)
            complete_file_name = file_name + "." + file_extension
            data = ContentFile(decoded_file, name=complete_file_name)
            image_size = data._size / 1000
            if image_size > 500:
                raise ValidationError(self.MAX_SIZE_IMAGE)
            return super(Base64FieldMixin, self).to_internal_value(data)
        raise ValidationError(_('This is not an base64 string'))
