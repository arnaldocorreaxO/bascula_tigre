import locale
import datetime

from django.db.models.fields import FloatField

from core.bascula.models import Categoria, Cliente, Movimiento, Producto
from core.base.models import Empresa
from core.security.models import Dashboard
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, requires_csrf_token
from django.views.generic import TemplateView

locale.setlocale(locale.LC_TIME, '')

class DashboardView(LoginRequiredMixin, TemplateView):

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return 'vtcpanel.html'
        return 'hztpanel.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'get_graph_1':
                info = []          
                hoy = datetime.datetime.now()  
                for i in Movimiento.objects.values('producto__denominacion') \
                        .filter(fecha=hoy,peso_neto__gt=0)\
                        .annotate(tot_recepcion=Sum('peso_neto',output_field=FloatField())) \
                        .order_by('-tot_recepcion'):
                        info.append([i['producto__denominacion'],
                                     i['tot_recepcion']/1000])
                        
                data = {
                    'name': 'Stock de Productos',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_2':
                data = []               
                now = datetime.datetime.now() 
                for i in Movimiento.objects.values('producto__denominacion','cliente__denominacion') \
                        .filter(fecha = now,peso_neto__gt=0)\
                        .annotate(tot_recepcion=Sum('peso_neto',output_field=FloatField())) \
                        .order_by('-tot_recepcion'):
                        data.append({'name':  i['producto__denominacion']+ ' - ' +i['cliente__denominacion'],
                                     'data': [i['tot_recepcion']/1000]})              
            elif action == 'get_graph_3':
                data = []
                month = datetime.datetime.now().month 
                year = datetime.datetime.now().year
                for i in Movimiento.objects.values('fecha') \
                        .filter(producto=1,fecha__month=month, fecha__year=year)\
                        .annotate(tot_recepcion=Sum('peso_neto',output_field=FloatField())) \
                        .order_by('fecha'):
                        data.append({'name':  i['fecha'].strftime('%d'),
                                     'data': [i['tot_recepcion']/1000]})     
                        # print(data)         
            elif action == 'get_graph_4':
                data = []                
                year = datetime.datetime.now().year
                for i in Movimiento.objects.values('fecha__month') \
                        .filter(producto=1, fecha__year=year)\
                        .annotate(tot_recepcion=Sum('peso_neto',output_field=FloatField())) \
                        .order_by('fecha__month'):
                        #Utilizamos una fecha cualquiera para retornar solo el mes ;)
                        mes = datetime.date(1900, i['fecha__month'], 1).strftime('%B').capitalize()
                        data.append({'name':  mes,
                                     'data': [i['tot_recepcion']/1000]})     
                        # print(data)         
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['current_day'] = datetime.datetime.today().strftime("%d/%m/%Y %H:%M:%S")
        context['current_month'] = datetime.datetime.today().strftime("%B de %Y")
        context['current_year'] = datetime.datetime.today().strftime("%Y")
        context['company'] = Empresa.objects.first()
        context['clientes'] = Cliente.objects.all().count()
        context['categorias'] = Categoria.objects.filter().count()
        context['productos'] = Producto.objects.all().count()
        context['movimiento'] = Movimiento.objects.filter().order_by('-id')[0:10]
        return context


@requires_csrf_token
def error_404(request, exception):
    return render(request, '404.html', {})


@requires_csrf_token
def error_500(request, exception):
    return render(request, '500.html', {})
