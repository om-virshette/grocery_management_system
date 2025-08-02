from django.contrib import admin
from .models import Product, Category
from django.utils.html import format_html

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'min_stock_level', 'stock_status')
    list_filter = ('category', 'stock')
    search_fields = ('name', 'barcode')
    list_editable = ('price', 'stock', 'min_stock_level')
    
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: red; font-weight: bold;">Out of Stock</span>')
        elif obj.stock < obj.min_stock_level:
            return format_html('<span style="color: orange; font-weight: bold;">Low Stock ({} left)</span>', obj.stock)
        return format_html('<span style="color: green;">In Stock ({} available)</span>', obj.stock)
    stock_status.short_description = 'Inventory Status'
    stock_status.admin_order_field = 'stock'



@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','description')
    search_fields = ('name',)