#SYSTEM
import json
import os
from django.db.models.aggregates import Max

from django.http.response import HttpResponseRedirect

from config import settings
from core.bascula.forms import (ChoferForm, MovimientoEntradaForm,
								MovimientoSalidaForm, ShearchForm,
								VehiculoForm)
#MODELS
from core.bascula.models import ConfigSerial, Movimiento
#LOCALS
from core.base.comserial import *
from core.base.models import Empresa
from core.base.views import printSeparador
from core.security.mixins import PermissionMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
#DJANGO
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.base import View
from django.views.generic.edit import FormView

from weasyprint import HTML, CSS

"""Listado de Movimiento de Bascula"""
class MovimientoList(PermissionMixin,ListView):	
	model = Movimiento
	template_name = 'movimiento/list.html'
	permission_required = 'view_movimiento'
	# form_class = ShearchForm
	
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
		
	def post(self,request,*args,**kwargs):
		data ={}		
		try:
			action = request.POST['action']
			if action == 'searchdata':
				data =[]
				for i in Movimiento.objects.filter(peso_salida__lte=0):
					data.append(i.toJSON())
			else:	
				data['error']= 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		# return JsonResponse(data,safe=False)
		return HttpResponse(json.dumps(data), content_type='application/json')

	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = ' Movimiento de Bascula'
		context['create_url'] = reverse_lazy('movimiento_create')
		context['list_url'] = reverse_lazy('movimiento_list')
		context['entity'] = 'Movimiento'
		return context


"""Crear Movimiento de Bascula"""
class MovimientoCreate(PermissionMixin,CreateView):
	model = Movimiento
	form_class=MovimientoEntradaForm
	success_url = reverse_lazy('movimiento_list')
	template_name = 'movimiento/create.html'
	permission_required = 'add_movimiento'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'add':
				with transaction.atomic():
					form = self.get_form()
					data = form.save()
			elif action == 'create-vehiculo':
				with transaction.atomic():
					frmVehiculo = VehiculoForm(request.POST)
					data = frmVehiculo.save()
			elif action == 'create-chofer':
				with transaction.atomic():
					frmChofer = ChoferForm(request.POST)
					data = frmChofer.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		# return JsonResponse(data,safe=False)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Entrada Bascula'
		context['entity'] = 'Bascula'
		context['list_url'] = self.success_url
		context['action'] = 'add'
		context['frmVehiculo'] = VehiculoForm()
		context['frmChofer'] = ChoferForm()
		context['puerto_bascula1'] = ConfigSerial.objects.get(id=1).puerto
		context['puerto_bascula2'] = ConfigSerial.objects.get(id=2).puerto
		return context


"""Actualizar Movimiento de Bascula"""
class MovimientoUpdate(PermissionMixin,UpdateView):
	model = Movimiento
	form_class=MovimientoSalidaForm
	success_url = reverse_lazy('movimiento_list')
	template_name = 'movimiento/create.html'
	permission_required = 'change_movimiento'

	
	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)
	
	# def get_form(self, form_class=None):
	# 	instance = self.get_object()
	# 	form = MovimientoSalidaForm(instance=instance)
	# 	# form.fields['cli'].queryset = Client.objects.filter(id=instance.cli.id)
	# 	return form

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'edit':
				with transaction.atomic():
					with transaction.atomic():
						form = self.get_form()
						data = form.save()
						movimiento = self.get_object()
						max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
						if max_nro_ticket is None:
							max_nro_ticket = 0 
						movimiento.nro_ticket = max_nro_ticket + 1
						if movimiento.peso_entrada > movimiento.peso_salida:
							movimiento.peso_neto = movimiento.peso_entrada - movimiento.peso_salida
							movimiento.peso_bruto = movimiento.peso_entrada
							movimiento.peso_tara = movimiento.peso_salida
						else:
							movimiento.peso_neto = movimiento.peso_salida - movimiento.peso_entrada
							movimiento.peso_bruto = movimiento.peso_salida
							movimiento.peso_tara = movimiento.peso_entrada
					movimiento.save()
			elif action == 'create-vehiculo':
				with transaction.atomic():
					frmVehiculo = VehiculoForm(request.POST)
					data = frmVehiculo.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Salida Bascula'
		context['entity'] = 'Bascula'
		context['list_url'] = self.success_url
		context['action'] = 'edit'
		context['frmVehiculo'] = VehiculoForm()
		context['frmChofer'] = ChoferForm()
		context['puerto_bascula1'] = ConfigSerial.objects.get(cod='BSC1').puerto
		context['puerto_bascula2'] = ConfigSerial.objects.get(cod='BSC2').puerto
		return context

class MovimientoDelete(PermissionMixin, DeleteView):
	model = Movimiento
	template_name = 'bascula/movimiento/delete.html'
	success_url = reverse_lazy('movimiento_list')
	permission_required = 'delete_movimiento'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			self.get_object().delete()
		except Exception as e:
			data['error'] = str(e)
		return HttpResponse(json.dumps(data), content_type='application/json')

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Notificación de eliminación'
		context['list_url'] = self.success_url
		return context

"""Pruebas de Lectura"""
def test_bascula(request):
	return render(
		request=request,
		template_name='bascula/bascula.html',
	)

"""Obtener peso directamente del Puerto Serial"""
@method_decorator(csrf_exempt)
def leer_puerto_serial(request,puerto):
	config = ConfigSerial.objects.get(puerto=puerto)	
	buffer = leerPuertoSerial(config)
	printSeparador()
	print('# BUFFER DATO DIRECTO SERIAL')	
	print(buffer)
	if 'error' in buffer:
		return JsonResponse({'error': buffer})
	if buffer:		
		data = getPeso(config,buffer)
	printSeparador()
	print('Resultado\t:', data)
	printSeparador()
	return JsonResponse({ 'resultado': data })          

"""Obtener peso de archivo txt"""
@method_decorator(csrf_exempt)
def leer_peso_bascula(request):
	peso = 0
	if os.path.exists("peso.txt"):
		with open("peso.txt", "r") as archivo:
			archivo.seek(0)
			linea = archivo.readline()
			print(linea)
			if linea: 
				peso = float(linea[29:8])
				print(peso)
				#os.remove("peso.txt")
			
	return JsonResponse({ 'resultado': peso })          

def getPeso(config,buffer):

	"""Obtener valores del buffer de la Bascula 1"""
	if config.cod == 'BSC1': 
		pos_ini = buffer.find('+') + 1
		print('Posicion Inicial:', pos_ini)
		pos_fin = pos_ini + (config.pos_fin - config.pos_ini)
		print('Posicion Final\t:', pos_fin)
		return buffer[pos_ini:pos_fin]
	
	"""Obtener valores del buffer de la Bascula 2"""
	if config.cod == 'BSC2': 
		pos_ini = config.pos_ini
		print('Posicion Inicial:', pos_ini)
		pos_fin = config.pos_fin
		print('Posicion Final\t:', pos_fin)
		return buffer[pos_ini:pos_fin]


'''IMPRESION DE TICKET'''
class MovimientoPrint(View):
	success_url = reverse_lazy('movimiento_list')

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def get_height_ticket(self):
		movimiento = Movimiento.objects.get(pk=self.kwargs['pk'])
		height = 100		
		# increment = movimiento.all().count() * 5.45
		increment = 1 * 5.45
		height += increment
		print(round(height))
		return round(height)

	def get(self, request, *args, **kwargs):
		try:
			movimiento = Movimiento.objects.get(pk=self.kwargs['pk'])
			context = {'movimiento': movimiento, 'company': Empresa.objects.first()}
			context['height'] = self.get_height_ticket()
			template = get_template('movimiento/ticket.html')
			html_template = template.render(context).encode(encoding="UTF-8")
			url_css = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.3.1/css/bootstrap.min.css')
			pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(
				stylesheets=[CSS(url_css)], presentational_hints=True)
			response = HttpResponse(pdf_file, content_type='application/pdf')
			# response['Content-Disposition'] = 'filename="generate_html.pdf"'
			return response
		except Exception as e:
			print(str(e))
		return HttpResponseRedirect(self.success_url)
