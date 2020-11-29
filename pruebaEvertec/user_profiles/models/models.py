# -*- encoding: utf-8 -*-

# Django
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from slugify import slugify
from pruebaEvertec.utils.storage import OverwriteStorage


def get_cover_photo(instance, filename):

    filename = '{0}.jpg'.format(slugify(instance.user.username))
    folder = 'images/{0}'.format(filename)
    return folder


"""
    Tabla de perfiles de usuario.
"""


class UserProfile (models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, verbose_name=_('User'))
    cover_photo = models.ImageField(verbose_name=_(
        'cover photo'), upload_to=get_cover_photo, storage=OverwriteStorage(), blank=False, null=False)
    marital_status = models.IntegerField(verbose_name=_('Marital Status'))
    siblings = models.BooleanField(verbose_name=_('Siblings'))
    birthday = models.DateField(verbose_name=_('Birthday'))

    def __str__(self):
        """Return UserProfile's str representation."""
        return str(self.user)

    class Meta:
        verbose_name_plural=_('User Profiles')
