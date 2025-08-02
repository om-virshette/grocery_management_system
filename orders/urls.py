from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    # Order URLs
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('<int:order_id>/add-items/', views.order_add_items, name='order_add_items'),
    path('<int:order_id>/complete/', views.order_complete, name='order_complete'),
    path('<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    path('<int:order_id>/invoice/', views.generate_invoice_pdf, name='generate_invoice_pdf'),
    
    # Order Item URLs
    path('<int:order_id>/items/<int:item_id>/delete/', views.order_item_delete, name='order_item_delete'),
]