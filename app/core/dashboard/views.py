import locale
from datetime import datetime

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
            if action == 'get_graph_stock_products':
                info = []          
                hoy = datetime.now()  
                for i in Movimiento.objects.values('producto__denominacion') \
                        .filter(fecha=hoy)\
                        .annotate(tot_recepcion=Sum('peso_neto')/1000) \
                        .order_by('-tot_recepcion'):
                        info.append([i['producto__denominacion'],
                                     i['tot_recepcion']])
                        
                data = {
                    'name': 'Stock de Productos',
                    'type': 'pie',
                    'colorByPoint': True,
                    'data': info,
                }
            elif action == 'get_graph_purchase_vs_sale':
                data = []               
                now = datetime.now() 
                for i in Movimiento.objects.values('producto__denominacion') \
                        .filter(fecha = now)\
                        .annotate(tot_recepcion=Sum('peso_neto')) \
                        .order_by('-tot_recepcion'):
                        data.append({'name':  i['producto__denominacion'],
                                     'data': [i['tot_recepcion']]})              
            elif action == 'get_graph_purchase_vs_sale2':
                data = []
                month = datetime.now().month 
                year = datetime.now().year
                for i in Movimiento.objects.values('fecha') \
                        .filter(cliente=2,producto=2,fecha__month=month, fecha__year=year)\
                        .annotate(tot_recepcion=Sum('peso_neto')) \
                        .order_by('fecha'):
                        data.append({'name':  i['fecha'],
                                     'data': [i['tot_recepcion']]})     
                        print(data)         
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['current_day'] = datetime.now().strftime("%c")
        context['current_month'] = datetime.now().strftime("%B de %Y")
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
