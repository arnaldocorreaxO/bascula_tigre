from django.db import models

# Create your models here.
import datetime
from django.utils.timezone import now
from core.base.models import ModeloBase
from django.contrib.auth.models import User
from django.db import models
from django.forms import model_to_dict


#Convertir a mayusculas
class UpperField(models.CharField):
    def to_python(self, value):
        return value.upper()


# Create your models here.

'''Configuración Puertos Seriales'''
class ConfigSerial(ModeloBase):
	TASA_BAUDIOS = (
		(600,'600'),
		(1200,'1200'),
		(2400,'2400'),
		(4800,'4800'),
		(7200,'7200'),
		(9600,'9600'),
		(14400,'14400'),
		(19200,'19200')
	)
	PARIDAD = (
		('N','Ninguna'),
		('E','Par'), #Even
		('O','Impar'), #Odd
		('S','Espacio'),
		('M','Marca'),	
	)
	cod = models.CharField(max_length=15,default=1,unique=True)
	descripcion = models.CharField(max_length=50)
	puerto = models.CharField(max_length=15)
	bits_por_segundo = models.SmallIntegerField(choices=TASA_BAUDIOS,default=9600)
	bits_de_datos = models.SmallIntegerField(default=8)
	paridad = models.CharField(max_length=1,choices=PARIDAD,default='N')
	bits_de_parada = models.SmallIntegerField(default=1)	
	pos_ini = models.SmallIntegerField(verbose_name='Posicion Desde',default=0)
	pos_fin = models.SmallIntegerField(verbose_name='Posicion Hasta',default=10)
	

	def __str__(self):
		return f'{self.puerto} - {self.bits_por_segundo}'

	class Meta:
	# ordering = ['1',]
		db_table = 'bascula_config_serial'
		verbose_name = 'Configuracion Serial'
		verbose_name_plural = 'Configuracion Serial'

#MARCAS
class MarcaVehiculo(ModeloBase):	
	denominacion = models.CharField(max_length=100,unique=True)
	
	def __str__(self):
		return self.denominacion

	class Meta:
		# ordering = ['1',]
		db_table = 'bascula_marca_vehiculo'
		verbose_name = 'marca vehiculo'
		verbose_name_plural = 'Marcas Vehiculos'
	
	#Convertir  Mayusculas tres formas de hacer en el metod clean y save
	# clean_field
	def clean_denominacion(self):
		return self.cleaned_data['denominacion'].upper()
	# #clean
	# def clean_denominacion(self):
	# 	return self.cleaned_data['denominacion'].upper()
	# #save
	# def save(self,*args,**kwargs):
	# 	self.denominacion = self.denominacion.upper()
	# 	super(MarcaVehiculo,self).save(*args,**kwargs)


#VEHICULOS
class Vehiculo(ModeloBase):
	matricula = UpperField(max_length=8,unique=True)
	marca = models.ForeignKey(MarcaVehiculo,on_delete=models.CASCADE)
	
	def toJSON(self):
		item = model_to_dict(self)
		item['full_name'] = self.get_full_name()
		return item
	
	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		return f"{self.matricula} - {self.marca}"
	
	# def clean_matricula(self):
	# 	return self.cleaned_data['matricula'].upper()

	class Meta:
		# ordering = ['1',]
		db_table = 'bascula_vehiculo'
		verbose_name = 'vehiculo'
		verbose_name_plural = 'vehiculos'

	


#CHOFERES
class Transportista(ModeloBase):	
	codigo = models.IntegerField(verbose_name='CI',unique=True)
	nombre = models.CharField(max_length=100)
	apellido = models.CharField(max_length=100)

	def toJSON(self):
		item = model_to_dict(self)
		item['full_name'] = self.get_full_name()
		return item
	
	def __str__(self):
		return self.get_full_name()

	def get_full_name(self):
		return f"{self.codigo}-{self.nombre} {self.apellido}"
	
	class Meta:
	# ordering = ['1',]
		db_table = 'bascula_transportista'
		verbose_name = 'transportista'
		verbose_name_plural = 'transportistas'
	
	# Convertir Mayusculas 
	def clean(self):
		self.nombre = self.nombre.upper()
		self.apellido = self.apellido.upper()
		

#CLIENTES/PROVEEDORES
class Cliente(ModeloBase):	
	codigo = models.CharField(max_length=10,unique=True)
	denominacion = models.CharField(max_length=100)
	
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
	def __str__(self):
		return f"{self.codigo} - {self.denominacion}"
	
	def get_full_name(self):
		return f"{self.codigo}-{self.denominacion}"

	class Meta:
	# ordering = ['1',]
		db_table = 'bascula_cliente'
		verbose_name = 'cliente'
		verbose_name_plural = 'clientes'

#CATEGORIAS
class Categoria(ModeloBase):	
	denominacion = models.CharField(max_length=100)
	

	def toJSON(self):
		item = model_to_dict(self)
		return item
	
	def __str__(self):
		return f"{self.id} - {self.denominacion}"
	class Meta:
	# ordering = ['1',]
		db_table = 'bascula_categoria'
		verbose_name = 'categoria'
		verbose_name_plural = 'categorias'

#PRODUCTOS
class Producto(ModeloBase):	
	categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
	codigo = models.CharField(max_length=20,unique=True)
	denominacion = models.CharField(max_length=100)
	
	def toJSON(self):
		item = model_to_dict(self)
		return item
	
	def __str__(self):
		return f"{self.codigo} - {self.denominacion}"
	class Meta:
	# ordering = ['1',]
		db_table = 'bascula_producto'
		verbose_name = 'producto'
		verbose_name_plural = 'productos'

#MOVIMIENTO DE BASCULA PESAJES
class Movimiento(ModeloBase):
	nro_ticket = models.BigIntegerField(default=1)
	fecha = models.DateField(default=now)
	nro_mic = models.IntegerField(null=True,blank=True) #MIC o DTA
	nro_remision = models.IntegerField(default=0) 
	porc_humedad = models.DecimalField(max_digits=5,decimal_places=2,default=0.00)	
	vehiculo = models.ForeignKey(Vehiculo,on_delete=models.CASCADE)
	chofer = models.ForeignKey(Transportista,on_delete=models.CASCADE)
	cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE)
	producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
	peso_embarque = models.IntegerField(default=0)
	peso_entrada = models.IntegerField(default=0)
	peso_salida = models.IntegerField(default=0)
	peso_bruto = models.IntegerField(default=0)
	peso_tara = models.IntegerField(default=0)		
	peso_neto = models.IntegerField(default=0)	
	
	bascula_entrada = models.SmallIntegerField(null=True,default=1)
	bascula_salida = models.SmallIntegerField(null=True,blank=True,default=1)

	def toJSON(self):
		item = model_to_dict(self)
		item['fecha'] = self.fecha.strftime('%d/%m/%Y')
		# item['vehiculo'] = self.vehiculo.toJSON()
		item['vehiculo'] = str(self.vehiculo)
		# item['chofer'] = self.chofer.toJSON()
		item['chofer'] = str(self.chofer)
		# item['producto'] = self.producto.toJSON()
		item['producto'] = str(self.producto)
		item['porc_humedad'] = format(self.porc_humedad,',.2f')
		item['nro_remision'] = format(self.nro_remision,',.2f')
		item['peso_entrada'] = format(self.peso_entrada,',.2f')
		item['peso_salida'] = format(self.peso_salida,',.2f')
		item['peso_neto'] = format(self.peso_neto,',.2f')
		return item
	
	def __str__(self):
		return str(self.nro_ticket)

	class Meta:
	# ordering = ['1',]
		db_table = 'bascula_movimiento'
		verbose_name = 'movimiento'
		verbose_name_plural = 'movimientos'


	