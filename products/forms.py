from django import forms
from .models import Product, Category
from django.core.validators import MinValueValidator

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['barcode', 'name', 'category', 'description', 
                 'price', 'stock', 'min_stock_level', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    def clean_barcode(self):
        barcode = self.cleaned_data.get('barcode', '').strip()
        if barcode and not barcode.isdigit():
            raise forms.ValidationError("Barcode must contain only numbers.")
        return barcode    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].validators = [MinValueValidator(0.01)]
        self.fields['stock'].validators = [MinValueValidator(0)]
        self.fields['min_stock_level'].validators = [MinValueValidator(0)]

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }