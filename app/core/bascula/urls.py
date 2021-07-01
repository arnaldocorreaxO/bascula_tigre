
from core.bascula.views.bascula.movimiento.views import *
from core.bascula.views.bascula.cliente.views import *

from django.urls import path



urlpatterns = [
    # Marca Vehiculo
    # path('marca_vehiculo', MarcaVehiculoListView.as_view(), name='marca_vehiculo_list'),
    # path('marca_vehiculo/add/', MarcaVehiculoCreateView.as_view(), name='marca_vehiculo_create'),
    # path('marca_vehiculo/update/<int:pk>/', MarcaVehiculoUpdateView.as_view(), name='marca_vehiculo_update'),
    # path('marca_vehiculo/delete/<int:pk>/', MarcaVehiculoDeleteView.as_view(), name='marca_vehiculo_delete'),
    # Movimiento
    
    # URL para lectura de Puerto COM
	path('ajax_puerto_serial/<str:puerto>/',leer_puerto_serial,name='leer_puerto_serial'),
	path('ajax_peso_bascula/',leer_peso_bascula,name='leer_peso_bascula'),

    # MOVIMIENTO BASCULA
    path('movimiento', MovimientoList.as_view(), name='movimiento_list'),
    path('movimiento/add/', MovimientoCreate.as_view(), name='movimiento_create'),
    path('movimiento/update/<int:pk>/', MovimientoUpdate.as_view(), name='movimiento_update'),
    path('movimiento/delete/<int:pk>/', MovimientoDelete.as_view(), name='movimiento_delete'),
    path('movimiento/print/<int:pk>/', MovimientoPrint.as_view(), name='movimiento_print'),


     # CLIENTE
    path('cliente', ClienteList.as_view(), name='cliente_list'),
    path('cliente/add/', ClienteCreate.as_view(), name='cliente_create'),
    path('cliente/update/<int:pk>/', ClienteUpdate.as_view(), name='cliente_update'),
    path('cliente/delete/<int:pk>/', ClienteDelete.as_view(), name='cliente_delete'),

   ]
