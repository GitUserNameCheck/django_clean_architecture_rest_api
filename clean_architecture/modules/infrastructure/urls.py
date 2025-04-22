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
from clean_architecture.modules.infrastructure.api.location_api import LocationViewSet
from clean_architecture.modules.infrastructure.api.employee_api import EmployeeViewSet
from clean_architecture.modules.infrastructure.api.service_api import ServiceViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'locations', LocationViewSet, basename='location')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'services', ServiceViewSet, basename='service')

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
