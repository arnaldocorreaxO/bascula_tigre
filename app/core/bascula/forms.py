import datetime

from django import forms
from django.db.models import Max
from django.forms import ModelForm
from core.base.forms import readonly_fields

from core.bascula.models import *


''' 
====================
===   SHEARCH    ===
==================== '''
# Tiene problemas de rendimiento VEHICULOS tiene asignada MARCAS y hace un producto cartesiano
# se soluciona con select_related: ejemplo queryset=Vehiculo.objects.select_related('marca').all()
# class SearchForm(forms.ModelForm):
#     # Extra Fields
#     date_range = forms.CharField(widget=forms.TextInput(attrs={
#         'class': 'form-control',
#         'autocomplete': 'off'
#     }))

#     class Meta:
#         model = Asociacion
#         fields = '__all__'
#         widgets = {
#             'cliente': forms.Select(attrs={'class': 'form-control select2', }),
#             'producto': forms.Select(attrs={'class': 'form-control select2', }),
#             #'vehiculo': forms.Select(attrs={'class': 'form-control select2', }),
#             'chofer': forms.Select(attrs={'class': 'form-control select2', }),
#             # 'tipo_voto': forms.Select(attrs={'class': 'form-control select2', }),
#         }

class SearchForm(forms.Form):
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    fecha_fin = forms.DateField(widget=forms.DateInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.select_related('asociacion').all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
    }))
    producto = forms.ModelChoiceField(queryset=Producto.objects.select_related('categoria').all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
    }))
    vehiculo = forms.ModelChoiceField(queryset=Vehiculo.objects.select_related('marca').all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
    }))
    chofer = forms.ModelChoiceField(queryset=Chofer.objects.all(), widget=forms.Select(attrs={
        'class': 'form-control select2',
    }))
      

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

''' 
==========================
===    ASOCIACIONES    ===
========================== '''
class AsociacionForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Asociacion
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Asociacion'}),
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
''' 
======================
=== MARCA VEHICULO ===
====================== '''
class MarcaVehiculoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = MarcaVehiculo
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Marca Vehiculo'}),
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
''' 
====================
===   CATEGORIA   ===
==================== '''
class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['denominacion'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese una Categoria'}),
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

''' 
====================
===   PRODUCTO   ===
==================== '''
class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'denominacion': forms.TextInput(attrs={'placeholder': 'Ingrese un Producto'}),
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
        fields =['matricula','marca','activo']    
        widgets = {
            'marca': forms.Select(attrs={'class': 'form-control select2', 'style': 'width: 100%;'}),
        }
    
    '''Eliminamos espacios de la matricula '''
    def clean_matricula(self):
        data = self.cleaned_data['matricula']
        data = data.replace(" ","")
        return data
    
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
        model = Chofer
        fields =['codigo','nombre','apellido','activo']
                   
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

"""FORMULARIO DE CLIENTE PRODUCTO"""
class ClienteProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    class Meta:
        model = ClienteProducto
        fields = '__all__'
        exclude = readonly_fields
        widgets = {
            'cliente': forms.Select(attrs={
                'class': 'custom-select select2',
                # 'style': 'width: 100%'
                }
            ),
            'producto': forms.SelectMultiple(
                attrs={'class': 'form-control select2', 'multiple': 'multiple', 'style': 'width:100%'}),
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


"""FORMULARIO PARA MOVIMIENTO DE ENTRADA"""
class MovimientoEntradaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.select_related('categoria').filter(activo__exact=True)
        self.fields['cliente'].queryset = Cliente.objects.select_related('asociacion').filter(activo__exact=True).order_by('denominacion')
        self.fields['chofer'].queryset = Chofer.objects.filter(activo__exact=True)
        self.fields['vehiculo'].queryset = Vehiculo.objects.select_related('marca').filter(activo__exact=True)
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
                 'cliente','producto','peso_entrada','sucursal']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 90%'
                }
            ),
            'chofer': forms.Select(attrs={
                'class': 'custom-select select2',
                 'style': 'width: 90%',
                 'required': True
                }
            ),
            'cliente': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%',
                'required': True
                }
            ),
            'producto': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%',
                'required': True
            }
            ),
            'fecha': forms.TextInput(attrs={
                'readonly': True,
            }
            ),
            'nro_ticket': forms.TextInput(attrs={
                'readonly': True,
            }
            ),
            'peso_entrada': forms.TextInput(attrs={
                'readonly': True,
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
        self.fields['producto'].queryset = Producto.objects.select_related('categoria').filter(activo__exact=True)
        self.fields['cliente'].queryset = Cliente.objects.select_related('asociacion').filter(activo__exact=True)
        self.fields['chofer'].queryset = Chofer.objects.filter(activo__exact=True)
        self.fields['vehiculo'].queryset = Vehiculo.objects.select_related('marca').filter(activo__exact=True)
        
        '''NUMERACION TICKET'''
        max_nro_ticket = Movimiento.objects.aggregate(Max('nro_ticket'))['nro_ticket__max']
        if max_nro_ticket is None:
            max_nro_ticket = 0 

        '''NUMERACION REMISION'''
        import datetime
        year = datetime.datetime.now().year 
        if not self.instance.nro_remision:
            max_nro_remision = Movimiento.objects.filter(fecha__year=year).aggregate(Max('nro_remision'))['nro_remision__max']
            if max_nro_remision==0:
                max_nro_remision = year * 100000000
            max_nro_remision += 1
        else:
            max_nro_remision = self.instance.nro_remision 

        '''VALORES INICIALES'''
        self.initial['nro_ticket'] = max_nro_ticket + 1
        self.initial['nro_remision'] = max_nro_remision

        for form in self.visible_fields():
            pass
            # form.field.widget.attrs['readonly'] = 'readonly'
            # form.field.widget.attrs['class'] = 'form-control'
            # form.field.widget.attrs['autocomplete'] = 'off'
      
    class Meta:
        model = Movimiento
        fields =['fecha','nro_ticket','vehiculo','chofer',
                 'nro_mic','nro_remision','peso_embarque',
                 'cliente','producto','peso_entrada','peso_salida','sucursal']
        widgets = {
            'vehiculo': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%',
                'disabled': True,
            }
            ),
            'chofer': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%',
                'disabled': True,
            }
            ),
            'cliente': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%',
            }
            ),
            'producto': forms.Select(attrs={
                'class': 'custom-select select2',
                'style': 'width: 100%',
            }
            ),
            'fecha': forms.TextInput(attrs={
                'readonly': True,
                'style': 'width: 100%',
            }
            ),
            'nro_ticket': forms.TextInput(attrs={
                'readonly': True,
                'style': 'width: 100%',

            }
            ),
            'peso_entrada': forms.TextInput(attrs={
                'readonly': True,
                'type': 'hidden',
            }
            ),
            'peso_salida': forms.TextInput(attrs={
                'readonly': True,
            }
            ),
            'nro_mic': forms.TextInput(attrs={
                'readonly': True,
            }
            ),
            'nro_remision': forms.TextInput(attrs={
                'readonly': True,
            }
            ),
            'peso_embarque': forms.TextInput(attrs={
                'readonly': True,
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
