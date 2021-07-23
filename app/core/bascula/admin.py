from django.contrib import admin
from core.base.admin import ModeloAdminBase
from core.bascula.models import *
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
class ConfigSerialModelAdmin(ModeloAdminBase):
    list_display = ('cod','__str__','descripcion',)

class MonedaAdmin(ModeloAdminBase):
    list_display = ('cod_moneda','denominacion','precio_compra','precio_venta')
    search_fields = ('denominacion',)

class MovimientoAdmin(ModeloAdminBase):
    list_display = ('id','fecha','nro_ticket','cliente','producto','vehiculo','chofer','fec_impresion')
    search_fields = ['cliente__denominacion','producto__denominacion','chofer__nombre',
                     'chofer__apellido','nro_ticket','vehiculo__matricula']
    readonly_fields = ('fecha', 'nro_ticket', 'peso_embarque','peso_entrada', 'peso_salida', 
                       'peso_tara', 'peso_bruto', 'peso_neto','fec_entrada', 'fec_salida',
                       'usu_insercion', 'fec_insercion', 'usu_modificacion', 'fec_modificacion',)
    list_editable =['fec_impresion'] #Consume muchos recursos (tarda mucho la consulta)
    list_filter =['cliente','producto','vehiculo','chofer','fecha']
    list_per_page = 10


''' 
=========================
===   ASOCIACIONES    ===
========================= '''
class AsociacionResource(resources.ModelResource):
    class Meta:
        model = Asociacion        

class AsociacionAdmin(ImportExportModelAdmin):
    resource_class = AsociacionResource
    fields = ('cod', 'denominacion',)
''' 
=====================
===   CLIENTES    ===
===================== '''
class ClienteResource(resources.ModelResource):
    class Meta:
        model = Cliente        

class ClienteAdmin(ImportExportModelAdmin):
    resource_class = ClienteResource
    fields = ('codigo', 'denominacion',)

''' 
=====================
===   VEHICULO    ===
===================== '''
class VehiculoResource(resources.ModelResource):
    class Meta:
        model = Vehiculo        

class VehiculoAdmin(ImportExportModelAdmin):
    resource_class = VehiculoResource
    fields = ('matricula', 'marca',)
''' 
=====================
===   CHOFER    ===
===================== '''
class ChoferResource(resources.ModelResource):
    class Meta:
        model = Chofer        

class ChoferAdmin(ImportExportModelAdmin):
    resource_class = ChoferResource
    fields = ('codigo', 'nombre','apellido')


# REGISTRO DE MODELOS
admin.site.register(ConfigSerial,ConfigSerialModelAdmin)
admin.site.register(MarcaVehiculo,ModeloAdminBase)
admin.site.register(Vehiculo,VehiculoAdmin)
admin.site.register(Chofer,ChoferAdmin)
admin.site.register(Asociacion,AsociacionAdmin)
admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Categoria,ModeloAdminBase)
admin.site.register(Producto,ModeloAdminBase)
admin.site.register(Movimiento,MovimientoAdmin)

