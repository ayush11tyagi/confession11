from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import Confession
from .forms import ConfessionForm

def register_view(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('confession_list')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        
        # Validation
        errors = []
        
        # Check if email is valid
        try:
            validate_email(email)
        except ValidationError:
            errors.append('Please enter a valid email address.')
        
        # Check if email already exists
        if User.objects.filter(email=email).exists():
            errors.append('An account with this email already exists.')
        
        # Check if username (email) already exists
        if User.objects.filter(username=email).exists():
            errors.append('An account with this email already exists.')
        
        # Check password length
        if len(password1) < 6:
            errors.append('Password must be at least 6 characters long.')
        
        # Check if passwords match
        if password1 != password2:
            errors.append('Passwords do not match.')
        
        if not errors:
            # Create user
            try:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password1
                )
                # Auto-login after registration
                login(request, user)
                messages.success(request, 'Account created successfully! Welcome to the Confession Board!')
                return redirect('confession_list')
            except Exception as e:
                errors.append('An error occurred while creating your account. Please try again.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
    
    return render(request, 'board/register.html')

def login_view(request):
    """Custom login view"""
    if request.user.is_authenticated:
        return redirect('confession_list')
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # Try to authenticate with email as username
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('confession_list')
        else:
            messages.error(request, 'Invalid email or password.')
    
    return render(request, 'board/login.html')

@login_required(login_url='/login/')
def confession_list(request):
    """Display all confessions"""
    confessions = Confession.objects.all()
    form = ConfessionForm()
    
    if request.method == 'POST':
        form = ConfessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confession_list')
    
    return render(request, 'board/confession_list.html', {
        'confessions': confessions,
        'form': form,
        'user': request.user
    })

@login_required(login_url='/login/')
def submit_confession(request):
    """Handle confession submission"""
    if request.method == 'POST':
        form = ConfessionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confession_list')
    else:
        form = ConfessionForm()
    
    return render(request, 'board/submit_confession.html', {
        'form': form,
        'user': request.user
    })

def logout_view(request):
    """Handle user logout"""
    logout(request)
    return redirect('login')
