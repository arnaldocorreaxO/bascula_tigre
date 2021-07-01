from django.contrib import admin
from core.base.admin import ModeloAdminBase
from core.bascula.models import *

# Register your models here.
class ConfigSerialModelAdmin(ModeloAdminBase):
    list_display = ('cod','__str__','descripcion',)

class MonedaAdmin(ModeloAdminBase):
    list_display = ('cod_moneda','denominacion','precio_compra','precio_venta')
    search_fields = ('denominacion',)

# REGISTRO DE MODELOS
admin.site.register(ConfigSerial,ConfigSerialModelAdmin)
admin.site.register(MarcaVehiculo,ModeloAdminBase)
admin.site.register(Cliente,ModeloAdminBase)
admin.site.register(Categoria,ModeloAdminBase)
admin.site.register(Producto,ModeloAdminBase)

