from config import settings
from core.base.choices import choiceOperacionSaldo, choiceSiNo
#APPS
from crum import get_current_user
from django.core.validators import MinLengthValidator
from django.db import models

# Create your models here.

'''MODELO BASE'''
class ModeloBase(models.Model):
	# RefDets = RefDet.objects.filter(cod_referencia='ESTADO')
	# CAMPOS POR DEFECTO PARA TODOS LOS MODELOS
	usu_insercion = models.ForeignKey(settings.AUTH_USER_MODEL,db_column='usu_insercion',verbose_name='Creado por',on_delete=models.CASCADE,related_name='+')
	fec_insercion = models.DateTimeField(verbose_name='Fecha Creación',auto_now_add=True)
	usu_modificacion = models.ForeignKey(settings.AUTH_USER_MODEL,db_column='usu_modificacion',verbose_name='Modificado por',on_delete=models.CASCADE,related_name='+')
	fec_modificacion = models.DateTimeField(verbose_name='Fecha Modificación',auto_now=True)
	activo = models.BooleanField(default=True)
	# estado = models.ForeignKey(RefDet,db_column='estado',on_delete=models.CASCADE,limit_choices_to={'referencia': 'ESTADO'},to_field='valor',default='A')

	def get_name_usu_insercion(self):
		return self.usu_insercion.first_name
	get_name_usu_insercion.short_description = 'Creado por'
	
	def get_name_usu_modificacion(self):
		return self.usu_modificacion.first_name
	get_name_usu_modificacion.short_description = 'Modificado por'

	'''SAVE'''
	def save(self, *args, **kwargs):
		user = get_current_user()
		print(user)
		if user and not user.pk:
			user = None
		# print(dir(self))
		if not self.usu_insercion_id:
			self.usu_insercion = user
		self.usu_modificacion = user
		super(ModeloBase, self).save(*args, **kwargs)

	class Meta:
		abstract = True

'''PARAMETROS GENERALES'''
class Parametro(ModeloBase):
	parametro = models.CharField(max_length=25, unique=True)
	descripcion = models.CharField(max_length=100, unique=True)
	valor = models.CharField(max_length=100)

	def __str__(self):
		return "%s - %s " % (self.parametro, self.valor)

	class Meta:
		ordering = ['parametro', ]
		db_table = 'base_parametro'
		verbose_name = 'Parametro'
		verbose_name_plural = 'Parametros'


'''MODULOS'''
class Modulo(ModeloBase):
	# id = models.CharField('Código',db_column='cod_modulo',max_length=2,primary_key=True)
	cod_modulo = models.CharField('Código',db_column='cod_modulo',max_length=2,unique=True)
	denominacion = models.CharField(max_length=100,unique=True)

	def __str__(self):
		return f"{self.cod_modulo} - {self.denominacion}"

	class Meta:
		ordering = ['id', ]
		db_table = 'base_modulo'
		verbose_name = 'modulo'
		verbose_name_plural = 'modulos'

#EMPRESA
class Empresa(ModeloBase):
    #ID
    ruc = models.CharField(verbose_name='RUC',max_length=10,validators=[MinLengthValidator(6)])
    denominacion = models.CharField(verbose_name='Denominación',max_length=100,unique=True)
    nombre_fantasia = models.CharField(verbose_name='Nombre de Fantasía',max_length=100,unique=True)
    direccion = models.CharField(verbose_name='Dirección',max_length=100)
    telefono = models.CharField(verbose_name='Teléfono',max_length=100)

    def __str__(self):
        return '{}'.format(self.denominacion)
    
    def getNombreFantasia(self):
        return '{}'.format(self.nombre_fantasia)

    class Meta:
        # ordering = ['1',]
        db_table = 'base_empresa'
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'

#SUCURSAL
class Sucursal(ModeloBase):
    #ID
    empresa = models.ForeignKey(Empresa,verbose_name='Empresa',on_delete=models.CASCADE,related_name='empresa')
    denominacion = models.CharField(verbose_name='Denominación',max_length=100,unique=True)
    direccion = models.CharField(verbose_name='Dirección',max_length=100)
    telefono = models.CharField(verbose_name='Teléfono',max_length=100)

    def __str__(self):
        return '{}'.format(self.denominacion)
    
    class Meta:
        # ordering = ['1',]
        db_table = 'base_sucursal'
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'

#MONEDA
class Moneda(ModeloBase):
    #ID
    cod_moneda = models.CharField(verbose_name='Código',max_length=3,unique=True)
    iso = models.CharField(verbose_name='ISO',max_length=3,unique=True)
    denominacion = models.CharField(verbose_name='Denominación',max_length=100)
    decimales = models.IntegerField(verbose_name='Decimales')
    fec_cotizacion = models.DateField(verbose_name='Fecha Cotizacion')
    precio_compra = models.FloatField(verbose_name='Precio Compra')
    precio_venta = models.FloatField(verbose_name='Precio Venta')

    def __str__(self):
        return '{}'.format(self.denominacion)
    
    class Meta:
        # ordering = ['1',]
        db_table = 'base_moneda'
        verbose_name = 'moneda'
        verbose_name_plural = 'monedas'

#MONEDA
class TipoComprobante(ModeloBase):
    #ID
    tip_comprobante =models.AutoField(db_column= 'tip_comprobante',auto_created=True, primary_key=True, serialize=False, verbose_name='Tipo Comprobante')
    abreviatura = models.CharField(verbose_name='Abreviatura',max_length=6,unique=True)
    descripcion = models.CharField(verbose_name='Descripción',max_length=100,unique=True)
    operacion_stock = models.CharField(verbose_name='Operacion Stock',max_length=1,blank=True,null=True,choices=choiceOperacionSaldo())    
    operacion_saldo = models.CharField(verbose_name='Operacion Saldo',max_length=1,blank=True,null=True,choices=choiceOperacionSaldo())
    ver_en_recibo = models.CharField(verbose_name='Ver en Recibo',max_length=1,blank=True,null=True,choices=choiceSiNo())
    ver_en_compra = models.CharField(verbose_name='Ver en Compra',max_length=1,blank=True,null=True,choices=choiceSiNo())
    ver_en_venta = models.CharField(verbose_name='Ver en Venta',max_length=1,blank=True,null=True,choices=choiceSiNo())
    nro_de_lineas = models.IntegerField(verbose_name='Nro. de Lineas Pre-Impreso')
        
    def __str__(self):
        return '{} - {}'.format(self.abreviatura,self.descripcion)
    
    class Meta:
        # ordering = ['1',]
        db_table = 'base_tipo_comprobante'
        verbose_name = 'Tipo de Comprobante'
        verbose_name_plural = 'Tipos de Comprobantes'


#SECTOR OPERATIVO
class SectorOperativo(ModeloBase):
    #ID
    sucursal = models.ForeignKey(Sucursal,verbose_name='Sucursal',on_delete=models.CASCADE,related_name='fk_sucursal_%(app_label)s_%(class)s')
    denominacion = models.CharField(verbose_name='Denominación',max_length=100,unique=True)
    
    def __str__(self):
        return '{} - {}'.format(self.pk,self.denominacion)
    
    class Meta:
        ordering = ['pk',]
        db_table = 'base_sector_operativo'
        verbose_name = 'Sector Operativo'
        verbose_name_plural = 'Sectores Operativos'



#TIPO MOVIMIENTO
class Caja(ModeloBase):    
    nro_caja = models.IntegerField(verbose_name='Nro. Caja',db_column='nro_caja',primary_key=True)
    denominacion = models.CharField(verbose_name='Caja',max_length=100,unique=True)
    impresora1 = models.CharField(verbose_name='Impresora 1',max_length=100,blank=True,null=True)
    impresora2 = models.CharField(verbose_name='Impresora 2',max_length=100,blank=True,null=True)
    

    def __str__(self):
        return '{} - {}'.format(self.nro_caja,self.denominacion)

    class Meta:
        ordering = ['nro_caja',]
        db_table = 'base_caja'
        verbose_name = 'caja'
        verbose_name_plural = 'cajas'

#TIPO MOVIMIENTO
class CajaComprobante(ModeloBase):    
    nro_caja = models.ForeignKey(Caja,verbose_name='Nro. Caja',db_column='nro_caja',on_delete=models.CASCADE,related_name='fk_caja_%(app_label)s_%(class)s')
    tip_comprobante = models.ForeignKey(TipoComprobante,verbose_name='Comprobante',db_column ='tip_comprobante',on_delete=models.CASCADE,related_name='fk_tipo_comprobante_%(app_label)s_%(class)s')
    nro_ini_comprobante =models.IntegerField(verbose_name='Nro. Comprobante Inicial')
    nro_fin_comprobante =models.IntegerField(verbose_name='Nro. Comprobante Final')
    nro_act_comprobante =models.IntegerField(verbose_name='Nro. Comprobante Actual')

    def __str__(self):
        return '{} - {}'.format(self.nro_caja,self.tip_comprobante)

    class Meta:
        # ordering = ['nro_caja',]
        db_table = 'base_caja_comprobante'
        verbose_name = 'Caja Comprobante'
        verbose_name_plural = 'Caja Comprobantes'