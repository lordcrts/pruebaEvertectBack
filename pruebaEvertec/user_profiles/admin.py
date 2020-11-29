"""Companies models admin."""

# Django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

# Models
from pruebaEvertec.user_profiles.models.models import (
    UserProfile
)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile model admin."""

    list_display = (
        'user',
        'cover_photo',
        'marital_status',
        'siblings',
        'birthday',
    )

    search_fields = (
        'id',
        'user',
        'cover_photo',
        'marital_status',
        'siblings',
        'birthday'
    )
    list_filter = (
        'user',
        'cover_photo',
        'marital_status',
        'siblings',
        'birthday'
    )

