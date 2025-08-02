from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Product, Category
from django.http import HttpResponse, JsonResponse
from .forms import ProductForm, CategoryForm
import barcode
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File
import base64
import csv

@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/list.html', {'products': products})

@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            
            # Generate numeric barcode if not provided or invalid
            if not product.barcode or not product.barcode.isdigit():
                # Create a temporary product to get ID
                product.save()
                product.barcode = f"{product.id:012d}"  # 12-digit zero-padded ID
                product.save()
            
            try:
                # Generate barcode image
                ean = barcode.get('ean13', product.barcode, writer=ImageWriter())
                buffer = BytesIO()
                ean.write(buffer)
                product.barcode_image.save(f'barcode_{product.barcode}.png', File(buffer), save=False)
                product.save()
                
                messages.success(request, 'Product created successfully!')
                return redirect('products:product_list')
            except Exception as e:
                # If barcode generation fails, still save the product
                product.save()
                messages.warning(request, f'Product created but barcode generation failed: {str(e)}')
                return redirect('products:product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/form.html', {'form': form})

@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully!')
        return redirect('product_list')
    return render(request, 'products/confirm_delete.html', {'product': product})

@login_required
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/detail.html', {'product': product})

@login_required
def category_update(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('products:category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'products/category_form.html', {
        'form': form,
        'title': 'Update Category'
    })

@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        # Check if any products are using this category
        if Product.objects.filter(category=category).exists():
            messages.error(request, 'Cannot delete category with associated products!')
        else:
            category.delete()
            messages.success(request, 'Category deleted successfully!')
        return redirect('products:category_list')
    return render(request, 'products/category_confirm_delete.html', {
        'category': category
    })

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'products/category_list.html', {'categories': categories})

@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Category created successfully!')
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'products/category_form.html', {'form': form})

@login_required
def barcode_scan(request):
    if request.method == 'POST':
        barcode_data = request.POST.get('barcode')
        try:
            product = Product.objects.get(barcode=barcode_data)
            return JsonResponse({
                'success': True,
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': str(product.price),
                    'stock': product.stock
                }
            })
        except Product.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Product not found'
            }, status=404)
    return render(request, 'products/barcode_scan.html')

@login_required
def barcode_generate(request, product_id=None):
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        if not product.barcode:
            product.barcode = str(product.id).zfill(12)  # Generate a simple barcode
            product.save()
        
        # Generate barcode image
        code = barcode.get('ean13', product.barcode, writer=ImageWriter())
        buffer = BytesIO()
        code.write(buffer)
        image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
        
        return JsonResponse({
            'barcode': product.barcode,
            'image': image_base64,
            'product_name': product.name
        })
    
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        return redirect('products:barcode_generate', product_id=product_id)
    
    products = Product.objects.all()
    return render(request, 'products/barcode_generate.html', {
        'products': products
    })

def product_export(request):
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products_export.csv"'

    # Create a CSV writer
    writer = csv.writer(response)
    
    # Write headers
    writer.writerow(['Barcode', 'Name', 'Category', 'Price', 'Stock', 'Min Stock', 'Status'])
    
    # Get all products
    products = Product.objects.all()
    
    # Write product data
    for product in products:
        if product.is_out_of_stock():
            status = "Out of Stock"
        elif product.is_low_stock():
            status = "Low Stock"
        else:
            status = "In Stock"
            
        writer.writerow([
            product.barcode,
            product.name,
            product.category.name if product.category else '',
            product.price,
            product.stock,
            product.min_stock_level,
            status
        ])
    
    return response