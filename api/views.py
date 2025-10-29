from django.shortcuts import render, redirect
import json
import jwt
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.conf import settings
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from .rate_limiter import rate_limit

# Create your views here.

# API Views
@csrf_exempt
@rate_limit(requests_per_minute=5)
def register_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')

        if not all([username, password, email]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        user = User.objects.create(
            username=username,
            password=make_password(password),
            email=email
        )

        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'username': user.username,
                'email': user.email
            }
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@rate_limit(requests_per_minute=5)
def login_api(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not all([username, password]):
            return JsonResponse({'error': 'Missing required fields'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        if not check_password(password, user.password):
            return JsonResponse({'error': 'Invalid credentials'}, status=401)

        token = jwt.encode(
            {'user_id': user.id, 'username': user.username},
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM
        )

        return JsonResponse({'token': token})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

@csrf_exempt
@rate_limit(requests_per_minute=10)
def protected_api(request):
    if request.method != 'GET':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    return JsonResponse({
        'message': 'You have access to protected data',
        'user': request.user.username
    })

# Template Views
def register_view(request):
    if request.user.is_authenticated:
        return redirect('api:user_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields')
            return render(request, 'register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'register.html')
        
        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Registration successful!')
        return redirect('api:user_dashboard')
    
    return render(request, 'register.html')

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('api:admin_dashboard')
        return redirect('api:user_dashboard')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password')
            return render(request, 'login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            if user.is_staff:
                return redirect('api:admin_dashboard')
            return redirect('api:user_dashboard')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'login.html')

@login_required
def user_dashboard(request):
    context = {
        'featured_plants': [],  # You'll need to add your plant model
        'care_tips': [],        # You'll need to add your care tips model
        'orders': []           # You'll need to add your orders model
    }
    return render(request, 'user_dashboard.html', context)

@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    context = {
        'total_orders': 0,     # Add real data when you have the models
        'pending_orders': 0,
        'total_products': 0,
        'out_of_stock': 0,
        'total_users': User.objects.count(),
        'new_users': User.objects.filter(date_joined__month=timezone.now().month).count(),
        'products': [],        # You'll need to add your product model
        'care_tips': []        # You'll need to add your care tips model
    }
    return render(request, 'admin_dashboard.html', context)

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('api:login')

def home_view(request):
    """
    Home view that redirects to dashboard if authenticated, otherwise to login
    """
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('api:admin_dashboard')
        return redirect('api:user_dashboard')
    return redirect('api:login')
