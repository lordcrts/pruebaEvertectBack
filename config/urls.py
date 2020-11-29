"""tolimatravel2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from rest_framework import routers


from django.conf.urls.static import static
from django.conf import settings

# Views
from pruebaEvertec.user_profiles.views.views import Login

from pruebaEvertec.user_profiles.views.views import (
    UserAdminViewSet,
)

router = routers.SimpleRouter()

router.register(r'users', UserAdminViewSet)

urlpatterns = [
    # Django Admin
    url(settings.ADMIN_URL, admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^login/$', Login.as_view(), name='login'),
    # url(r'^api/profile/$', UserProfileView.as_view({'get':'retrieve', 'put':'update'}), name='profile'),
    # url(r'^api/profile/password/$', UserPasswordChangeProfileViewSet.as_view({'put':'update'}), name='change-password-profile'),
    # url(r'^api/password/(?P<pk>\d+)/$', UserPasswordChangeGeneralViewSet.as_view({'put':'update'}), name='change-password'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
