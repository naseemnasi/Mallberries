from django import forms
from app1.models import Register,payment,product

#
# class regForm(forms.ModelForm):
#     class Meta:
#         model = Register
#
#         fields = '__all__'
class payForm(forms.ModelForm):
    class Meta:
        model = payment
        fields = '__all__'

class productForm(forms.ModelForm):
    class Meta:
        model = product
        fields = '__all__'
