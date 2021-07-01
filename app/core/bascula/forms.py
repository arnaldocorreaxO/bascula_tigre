import datetime

from django import forms
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Max
from django.forms import ModelForm
from core.base.forms import readonly_fields

from core.bascula.models import Movimiento, Transportista, Vehiculo, Cliente



''' 
====================
===   SHEARCH    ===
==================== '''
class ShearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)        
        self.fields['term'].widget.attrs['autofocus'] = True
    # Rango de fechas 
    date_range = forms.CharField()

''' 
====================
===    CLIENTE    ===
==================== '''
class ClienteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Cliente
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Cliente'}),
        }

    def save(self, commit=True):
        data = {}
        try:
            if self.is_valid():
                super().save()
            else:
                data['error'] = self.errors
        except Exception as e:
            data['error'] = str(e)
        return data
    

"""FORMULARIO DE VEHICULO"""
class VehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Vehiculo
        fields =['matricula','marca',]
   
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data

"""FORMULARIO DE CHOFER"""
class ChoferForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = Transportista
        fields =['codigo','nombre','apellido']
                   
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


"""FORMULARIO PARA MOVIMIENTO DE ENTRADA"""
class MovimientoEntradaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['vehiculo'].queryset = Vehiculo.objects.none()
        # '''MAX NRO. TICKET'''
        # max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
        # if max_nro_ticket is None:
        #     max_nro_ticket = 0  

        # '''VALORES INICIALES'''
        self.initial['fecha'] = datetime.date.today
        self.initial['nro_ticket'] = 0
        
        '''ATRIBUTOS'''
        for form in self.visible_fields():
            pass
            # form.field.widget.attrs['readonly'] = 'readonly'
            # form.field.widget.attrs['class'] = 'form-control'
            # form.field.widget.attrs['autocomplete'] = 'off'
       
    class Meta:
        model = Movimiento
        fields =['fecha','nro_ticket','vehiculo','chofer',
                 'nro_mic','nro_remision','peso_embarque',
                 'cliente','producto','peso_entrada']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'chofer': forms.Select(attrs={
                'class': 'custom-select select2',
                #  'style': 'width: 100%'
                }
            ),
            'cliente': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'producto': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'fecha': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'nro_ticket': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
            'peso_entrada': forms.TextInput(attrs={
                'readonly': True,
                # 'style': 'width: 100%'
                }
            ),
        }

        
   
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


"""FORMULARIO PARA MOVIMIENTO DE SALIDA"""  
class MovimientoSalidaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
        if max_nro_ticket is None:
            max_nro_ticket = 0  

        '''VALORES INICIALES'''
        # self.initial['fecha'] = datetime.date.today
        self.initial['nro_ticket'] = max_nro_ticket + 1

        for form in self.visible_fields():
            form.field.widget.attrs['readonly'] = 'readonly'
            form.field.widget.attrs['class'] = 'form-control'
            # form.field.widget.attrs['autocomplete'] = 'off'
      
    class Meta:
        model = Movimiento
        fields =['fecha','nro_ticket','vehiculo','chofer',
                 'nro_mic','nro_remision','peso_embarque',
                 'cliente','producto','peso_salida']
        # widgets = {
        #     'vehiculo': forms.Select(attrs={
        #         'class': 'custom-select select2',
        #         # 'style': 'width: 100%'
        #     }),
        #  }
   
    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
