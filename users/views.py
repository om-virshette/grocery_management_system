from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from products.models import Product
from orders.models import Order
from django.utils import timezone
from django.db.models import F
from .forms import (
    UserRegistrationForm, 
    StaffRegistrationForm, 
    UserLoginForm,
    ProfileUpdateForm,
    PasswordChangeForm
)
from django.contrib.auth import get_user_model

User = get_user_model()

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def register_staff(request):
    if not request.user.is_admin:
        messages.error(request, 'You are not authorized to perform this action!')
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = StaffRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            messages.success(request, 'Staff member added successfully!')
            return redirect('staff_list')
    else:
        form = StaffRegistrationForm()
    return render(request, 'users/register_staff.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect('login')

@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})

@login_required
def password_change(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'users/password_change.html', {'form': form})

@login_required
def staff_list(request):
    if not request.user.is_admin:
        messages.error(request, 'You are not authorized to perform this action!')
        return redirect('dashboard')
    
    staff_members = User.objects.filter(is_staff=True)
    return render(request, 'users/staff_list.html', {'staff_members': staff_members})

def dashboard(request):
    context = {
        'product_count': Product.objects.count(),
        'todays_orders': Order.objects.filter(
            created_at__date=timezone.now().date()
        ).count(),
        'low_stock_count': Product.objects.filter(
            stock__lt=F('min_stock_level')
        ).count(),
        'recent_orders': Order.objects.all().order_by('-created_at')[:5]
    }
    return render(request, 'dashboard.html', context)