from django import forms
from .models import Product
from .models import Return
class MyForm(forms.ModelForm):
  class Meta:
    model = Product
    fields = ["name", "price","stock","image","slug"]
    labels = {'name': "Phone Name", "price": "Phone price","stock": "Phone stock","image": "Phone image","slug":"slug"}
    
class Detailsform(forms.ModelForm):
    class Meta:
        model=Product
        fields = ["name", "price","stock","image"]
        
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
