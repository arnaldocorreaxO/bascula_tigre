from django.urls import path

from core.base.views.base.empresa.views import EmpresaUpdate

urlpatterns = [
    # Empresa
    path('empresa/update/', EmpresaUpdate.as_view(), name='empresa_update'),
    
]
