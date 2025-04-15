"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
# from clean_architecture.modules.infrastructure.api.client_api import get_clients, get_client_by_id, create_client, update_client, delete_client
from clean_architecture.modules.infrastructure.api.client_api import ClientViewSet
from rest_framework import routers, serializers, viewsets
from django.contrib.auth.models import User

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'is_staff']

# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Routers provide an easy way of automatically determining the URL conf.
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('', include(router.urls)),
    # path('api/clients/', get_clients, name='get_clients'),
    # path('api/clients/<str:id>/', get_client_by_id, name='get_client_by_id'),
    # path('api/clients/create/', create_client, name='create_client'),
    # path('api/clients/<str:id>/update/', update_client, name='update_client'),
    # path('api/clients/<str:id>/delete/', delete_client, name='delete_client'),
]
