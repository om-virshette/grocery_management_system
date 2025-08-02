from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from .models import Order, OrderItem
from products.models import Product
from .forms import OrderForm, OrderItemForm

@login_required
def order_list(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(request, 'orders/list.html', {'orders': orders})

@login_required
def order_add_items(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.price = order_item.product.price
            order_item.save()
            messages.success(request, 'Item added to order!')
            return redirect('orders:order_add_items', order_id=order.id)
    else:
        form = OrderItemForm()
    
    order_items = order.items.all()
    products = Product.objects.filter(stock__gt=0)
    
    return render(request, 'orders/add_items.html', {
        'order': order,
        'form': form,
        'order_items': order_items,
        'products': products,
    })

@login_required
def order_complete(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if order.items.count() == 0:
        messages.error(request, 'Cannot complete an empty order!')
        return redirect('order_add_items', order_id=order.id)
    
    order.status = 'completed'
    order.save()
    messages.success(request, 'Order marked as completed!')
    return redirect('order_list')

@login_required
def order_cancel(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        # Restore stock for each item
        for item in order.items.all():
            product = item.product
            product.stock += item.quantity
            product.save()
        
        order.status = 'cancelled'
        order.save()
        messages.success(request, 'Order cancelled and stock restored!')
        return redirect('order_list')
    return render(request, 'orders/confirm_cancel.html', {'order': order})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/detail.html', {'order': order})

@login_required
def generate_invoice_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Add store information (you can move this to settings or database)
    store = {
        'name': 'Grocery Store',
        'address': 'Pimpri, Pune, Maharashtra 411017',
        'phone': '9699970785',
        'email': 'omvirshette@gmail.com'
    }
    
    template_path = 'orders/invoice_pdf.html'
    context = {
        'order': order,
        'store': store
    }
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Invoice_{order.order_number}.pdf"'
    
    template = get_template(template_path)
    html = template.render(context)
    
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@login_required
def order_item_delete(request, order_id, item_id):
    order = get_object_or_404(Order, pk=order_id)
    item = get_object_or_404(OrderItem, pk=item_id, order=order)
    
    if request.method == 'POST':
        # Restore product stock before deletion
        product = item.product
        product.stock += item.quantity
        product.save()
        
        # Delete the item
        item.delete()
        
        # Update order total
        order.total_amount = sum(item.total for item in order.items.all())
        order.save()
        
        messages.success(request, 'Order item removed successfully!')
        return redirect('orders:order_add_items', order_id=order.id)
    
    return render(request, 'orders/order_item_confirm_delete.html', {
        'order': order,
        'item': item
    })
@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, 'Order created successfully!')
            return redirect('orders:order_add_items', order_id=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'orders/order_create.html', {
        'form': form,
        'title': 'Create New Order'
    })