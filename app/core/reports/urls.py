from django.urls import path
# from .views.electoral.views import (RptElectoral001ReportView, 
#                                     RptElectoral002ReportView,
#                                     RptEstadistica001ReportView, 
#                                     RptPadron001ReportView)
from .views.bascula.views import RptBascula001ReportView

urlpatterns = [    
    # REPORTES ELECTORAL    
    path('rpt_bascula001/', RptBascula001ReportView.as_view(), name='rpt_bascula001'),

]
