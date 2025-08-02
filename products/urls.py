from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product URLs
    path('', views.product_list, name='product_list'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    
    # Category URLs
    path('categories/', views.category_list, name='category_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
    
    # Barcode URLs
    path('barcode/scan/', views.barcode_scan, name='barcode_scan'),
    path('barcode/generate/', views.barcode_generate, name='barcode_generate'),
    path('barcode/generate/<int:product_id>/', views.barcode_generate, name='barcode_generate_for_product'),
    path('export/', views.product_export, name='product_export')
]