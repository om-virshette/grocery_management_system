from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    # Sales Reports
    path('sales/', views.sales_report, name='sales_report'),
    path('sales/daily/', views.daily_sales_report, name='daily_sales_report'),
    path('sales/monthly/', views.monthly_sales_report, name='monthly_sales_report'),
    path('sales/yearly/', views.yearly_sales_report, name='yearly_sales_report'),
    
    # Inventory Reports
    path('inventory/', views.inventory_report, name='inventory_report'),
    path('inventory/low-stock/', views.low_stock_report, name='low_stock_report'),
    path('inventory/out-of-stock/', views.out_of_stock_report, name='out_of_stock_report'),
    
    # Product Performance Reports
    path('products/', views.product_performance, name='product_performance'),
    path('products/top-selling/', views.top_selling_products, name='top_selling_products'),
    path('products/low-performing/', views.low_performing_products, name='low_performing_products'),
    
    
    # Export URLs
    path('export/sales/csv/', views.export_sales_csv, name='export_sales_csv'),
    path('export/sales/excel/', views.export_sales_excel, name='export_sales_excel'),
    path('export/inventory/csv/', views.export_inventory_csv, name='export_inventory_csv'),
    path('export/products/csv/', views.export_product_csv, name='export_product_csv'),
]