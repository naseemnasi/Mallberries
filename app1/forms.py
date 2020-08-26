from django import forms
from app1.models import product

class productForm(forms.ModelForm):
    class Meta:
        model = product
        fields = '__all__'
