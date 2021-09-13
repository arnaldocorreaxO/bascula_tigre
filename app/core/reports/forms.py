from core.bascula.models import Asociacion, Chofer, Cliente, Movimiento, Producto
from django import forms

class ReportForm(forms.Form):
    # Extra Fields
    date_range = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))

    # Asociaciones
    asociacion = forms.ChoiceField(choices=[
    (item.id, item) for item in Asociacion.objects.filter(activo__exact=True).order_by('denominacion')])
    cliente = forms.ChoiceField(choices=[
    (item.id, item) for item in Cliente.objects.filter(activo__exact=True).order_by('denominacion')])
    producto = forms.ChoiceField(choices=[
    (item.id, item) for item in Producto.objects.filter(activo__exact=True).order_by('denominacion')])
    chofer = forms.ChoiceField(choices=[
    (item.id, item) for item in Chofer.objects.filter(activo__exact=True).order_by('apellido','nombre')])

    asociacion.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    cliente.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    producto.widget.attrs.update({'class': 'form-control select2','multiple':'true'})
    chofer.widget.attrs.update({'class': 'form-control select2','multiple':'true'})    