from django.shortcuts import render, redirect, get_object_or_404
import json
import jwt
from django.http import JsonResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.conf import settings
from .rate_limiter import rate_limit
from django.db.models import Count, Sum
from django.utils import timezone
from datetime import timedelta
from .models import Order, OrderItem, UserProfile, Review, Wishlist, Plant, Cart, CartItem, Notification
from django.core.paginator import Paginator
from django.db.models import Q
from decimal import Decimal

def is_admin(user):
    return user.is_staff or user.is_superuser

def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('shop')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please provide both username and password')
            return render(request, 'auth/login.html')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully logged in!')
            if user.is_staff:
                return redirect('admin_dashboard')
            return redirect('shop')
        else:
            messages.error(request, 'Invalid credentials')
    
    return render(request, 'auth/login.html')

def register_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        return redirect('shop')

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        is_staff = request.POST.get('is_staff') == 'on'
        
        if not all([username, email, password, confirm_password]):
            messages.error(request, 'Please fill in all fields')
            return render(request, 'auth/register.html')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'auth/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'auth/register.html')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=is_staff
        )
        
        # Create a cart for the user
        Cart.objects.create(user=user)
        
        login(request, user)
        messages.success(request, 'Registration successful!')
        if user.is_staff:
            return redirect('admin_dashboard')
        return redirect('shop')
    
    return render(request, 'auth/register.html')

@login_required
def dashboard(request):
    if request.user.is_staff:
        return admin_dashboard(request)
    return redirect('shop')

@login_required
def user_dashboard(request):
    # Get user's orders
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    orders_count = orders.count()
    recent_orders = orders[:5]

    # Get user's wishlist count
    wishlist_count = request.user.wishlist.count() if hasattr(request.user, 'wishlist') else 0

    # Get user's review count
    reviews_count = request.user.review_set.count() if hasattr(request.user, 'review_set') else 0

    context = {
        'orders_count': orders_count,
        'recent_orders': recent_orders,
        'wishlist_count': wishlist_count,
        'reviews_count': reviews_count,
    }
    return render(request, 'user_dashboard.html', context)

@user_passes_test(is_admin)
def admin_dashboard(request):
    # Get date range for monthly comparisons
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)
    
    # Get orders statistics
    orders = Order.objects.all()
    orders_count = orders.count()
    pending_orders = orders.filter(status='pending').count()
    recent_orders = orders.order_by('-created_at')[:5]

    # Get sales statistics
    total_sales = orders.aggregate(total=Sum('total'))['total'] or 0
    previous_month_sales = orders.filter(
        created_at__lt=thirty_days_ago
    ).aggregate(total=Sum('total'))['total'] or 0
    
    if previous_month_sales > 0:
        sales_growth = ((total_sales - previous_month_sales) / previous_month_sales) * 100
    else:
        sales_growth = 0

    # Get product statistics
    products = Plant.objects.all()
    products_count = products.count()
    low_stock_threshold = 10  # Define what constitutes "low stock"
    low_stock = products.filter(stock__lte=low_stock_threshold).count()
    low_stock_products = products.filter(stock__lte=low_stock_threshold)[:5]

    # Get customer statistics
    customers_count = User.objects.filter(is_staff=False).count()
    new_customers = User.objects.filter(
        date_joined__gte=thirty_days_ago,
        is_staff=False
    ).count()

    context = {
        'total_sales': total_sales,
        'sales_growth': round(sales_growth, 1),
        'orders_count': orders_count,
        'pending_orders': pending_orders,
        'products_count': products_count,
        'low_stock': low_stock,
        'customers_count': customers_count,
        'new_customers': new_customers,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
    }
    return render(request, 'admin_dashboard.html', context)

def api_home(request):
    """
    API home endpoint that lists available endpoints
    """
    api_endpoints = {
        'endpoints': {
            'home': '/',
            'register': '/api/register/',
            'login': '/api/login/',
            'protected': '/api/protected/',
        },
        'documentation': 'Available API endpoints and their methods',
        'version': '1.0'
    }
    return JsonResponse(api_endpoints)

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

# Admin Views
@user_passes_test(is_admin)
def admin_orders(request):
    query = request.GET.get('q', '')
    status = request.GET.get('status', '')
    sort = request.GET.get('sort', 'date_desc')
    
    orders = Order.objects.all()
    
    # Filter by search query
    if query:
        orders = orders.filter(
            Q(id__icontains=query) | 
            Q(user__username__icontains=query) |
            Q(user__email__icontains=query)
        )
    
    # Filter by status
    if status:
        orders = orders.filter(status=status)
    
    # Sort results
    if sort == 'date_asc':
        orders = orders.order_by('created_at')
    elif sort == 'total_desc':
        orders = orders.order_by('-total')
    elif sort == 'total_asc':
        orders = orders.order_by('total')
    else:  # default to date descending
        orders = orders.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(orders, 10)  # Show 10 orders per page
    page = request.GET.get('page')
    orders = paginator.get_page(page)
    
    context = {
        'orders': orders,
        'query': query,
        'status': status,
        'sort': sort,
    }
    
    return render(request, 'admin/orders.html', context)

@user_passes_test(is_admin)
def admin_products(request):
    products = Plant.objects.all().order_by('-created_at')
    return render(request, 'admin/products.html', {'products': products})

@user_passes_test(is_admin)
def product_create(request):
    if request.method == 'POST':
        # Handle product creation
        pass
    return render(request, 'admin/product_form.html')

@user_passes_test(is_admin)
def product_edit(request, product_id):
    product = get_object_or_404(Plant, id=product_id)
    if request.method == 'POST':
        # Handle product update
        pass
    return render(request, 'admin/product_form.html', {'product': product})

@user_passes_test(is_admin)
def category_management(request):
    return render(request, 'admin/categories.html')

@user_passes_test(is_admin)
def inventory_management(request):
    return render(request, 'admin/inventory.html')

@user_passes_test(is_admin)
def shipping_management(request):
    return render(request, 'admin/shipping.html')

@user_passes_test(is_admin)
def refund_management(request):
    return render(request, 'admin/refunds.html')

@user_passes_test(is_admin)
def store_settings(request):
    return render(request, 'admin/settings.html')

@user_passes_test(is_admin)
def payment_settings(request):
    return render(request, 'admin/payment_settings.html')

@user_passes_test(is_admin)
def user_management(request):
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    return render(request, 'admin/users.html', {'users': users})

@user_passes_test(is_admin)
def pending_orders(request):
    orders = Order.objects.filter(status='pending').order_by('-created_at')
    return render(request, 'admin/pending_orders.html', {'orders': orders})

@user_passes_test(is_admin)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        old_status = order.status
        
        if status in ['pending', 'processing', 'shipped', 'delivered', 'cancelled']:
            order.status = status
            order.save()
            
            # Create notification for the user
            status_messages = {
                'processing': 'Your order is now being processed.',
                'shipped': 'Your order has been shipped! It\'s on the way to you.',
                'delivered': 'Your order has been delivered. Enjoy your plants!',
                'cancelled': 'Your order has been cancelled. Please contact support for more information.'
            }
            
            if status in status_messages:
                Notification.objects.create(
                    user=order.user,
                    type='order_status',
                    title=f'Order #{order.id} Status Update',
                    message=status_messages[status],
                    order=order
                )
            
            messages.success(request, f'Order #{order.id} status updated to {status.title()}')
        else:
            messages.error(request, 'Invalid status')
    
    return redirect('admin_orders')

# User Views
@login_required
def user_profile(request):
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update user information
        user = request.user
        
        # Check if username is being changed and is already taken
        new_username = request.POST.get('username')
        if new_username != user.username and User.objects.filter(username=new_username).exists():
            messages.error(request, 'Username is already taken.')
            return render(request, 'auth/profile.html')
        
        # Check if email is being changed and is already taken
        new_email = request.POST.get('email')
        if new_email != user.email and User.objects.filter(email=new_email).exists():
            messages.error(request, 'Email is already registered.')
            return render(request, 'auth/profile.html')
        
        # Update user fields
        user.username = new_username
        user.email = new_email
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        
        # Update profile information
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')

        # Handle profile picture upload
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        try:
            user.save()
            profile.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_dashboard')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
    return render(request, 'auth/profile.html')

@login_required
def user_wishlist(request):
    # Get user's wishlist items
    return render(request, 'accounts/wishlist.html')

@login_required
def notification_settings(request):
    if request.method == 'POST':
        # Handle notification settings update
        pass
    return render(request, 'accounts/notifications.html')

@login_required
def manage_addresses(request):
    # Get user's addresses
    return render(request, 'accounts/addresses.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        # Handle password change
        pass
    return render(request, 'accounts/change_password.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Successfully logged out!')
    return redirect('login')

@login_required
def shop_view(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    
    plants = Plant.objects.filter(stock__gt=0)
    
    # Filter by search query
    if query:
        plants = plants.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Sort results
    if sort == 'price_asc':
        plants = plants.order_by('price')
    elif sort == 'price_desc':
        plants = plants.order_by('-price')
    elif sort == 'name_desc':
        plants = plants.order_by('-name')
    else:  # default to name ascending
        plants = plants.order_by('name')
    
    # Pagination
    paginator = Paginator(plants, 12)  # Show 12 plants per page
    page = request.GET.get('page')
    plants = paginator.get_page(page)
    
    context = {
        'plants': plants,
        'query': query,
        'sort': sort,
    }
    
    return render(request, 'shop.html', context)

@login_required
def plant_list(request):
    query = request.GET.get('q', '')
    sort = request.GET.get('sort', 'name')
    
    plants = Plant.objects.all()
    
    # Filter by search query
    if query:
        plants = plants.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )
    
    # Filter by stock for regular users
    if not request.user.is_staff:
        plants = plants.filter(stock__gt=0)
    
    # Sort results
    if sort == 'price_asc':
        plants = plants.order_by('price')
    elif sort == 'price_desc':
        plants = plants.order_by('-price')
    elif sort == 'name_desc':
        plants = plants.order_by('-name')
    else:  # default to name ascending
        plants = plants.order_by('name')
    
    # Pagination
    paginator = Paginator(plants, 12)  # Show 12 plants per page
    page = request.GET.get('page')
    plants = paginator.get_page(page)
    
    context = {
        'plants': plants,
        'query': query,
        'sort': sort,
    }
    
    if request.user.is_staff:
        return render(request, 'admin/plant_list.html', context)
    return render(request, 'plants/plant_list.html', context)

@user_passes_test(is_admin)
def plant_create(request):
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        image = request.FILES.get('image')
        
        plant = Plant.objects.create(
            name=name,
            description=description,
            price=price,
            stock=stock,
            image=image
        )
        
        messages.success(request, 'Plant created successfully!')
        return redirect('plant_detail', plant_id=plant.id)
    
    return render(request, 'admin/plant_form.html')

@user_passes_test(is_admin)
def plant_edit(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    
    if request.method == 'POST':
        # Handle form submission
        plant.name = request.POST.get('name')
        plant.description = request.POST.get('description')
        plant.price = request.POST.get('price')
        plant.stock = request.POST.get('stock')
        
        if 'image' in request.FILES:
            plant.image = request.FILES['image']
        
        plant.save()
        messages.success(request, 'Plant updated successfully!')
        return redirect('plant_detail', plant_id=plant.id)
    
    return render(request, 'admin/plant_form.html', {'plant': plant})

@user_passes_test(is_admin)
def plant_delete(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    
    if request.method == 'POST':
        plant.delete()
        messages.success(request, 'Plant deleted successfully!')
        return redirect('plant_list')
    
    return render(request, 'admin/plant_confirm_delete.html', {'plant': plant})

@login_required
def plant_detail(request, plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
    if not request.user.is_staff and plant.stock <= 0:
        raise Http404("Plant not available")
    
    return render(request, 'plants/plant_detail.html', {'plant': plant})

@login_required
def cart_view(request):
    # Prevent admins from accessing cart
    if request.user.is_staff:
        messages.error(request, 'Admin users cannot access the cart')
        return redirect('admin_dashboard')
        
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    cart_total = sum(item.get_cost() for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'cart.html', context)

@login_required
def add_to_cart(request, product_id):
    # Prevent admins from adding items to cart
    if request.user.is_staff:
        messages.error(request, 'Admin users cannot add items to cart')
        return redirect('plant_detail', plant_id=product_id)
        
    if request.method == 'POST':
        plant = get_object_or_404(Plant, id=product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if plant.stock < quantity:
            messages.error(request, 'Not enough stock available')
            return redirect('plant_detail', plant_id=product_id)
        
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=plant)
        
        if not created:
            cart_item.quantity += quantity
        else:
            cart_item.quantity = quantity
        
        cart_item.save()
        messages.success(request, f'{plant.name} added to cart')
        
        # Redirect based on the referer
        referer = request.META.get('HTTP_REFERER')
        if referer and 'shop' in referer:
            return redirect('shop')
        return redirect('cart')
    
    return redirect('plant_detail', plant_id=product_id)

@login_required
def update_cart(request, item_id):
    # Prevent admins from updating cart
    if request.user.is_staff:
        messages.error(request, 'Admin users cannot update cart items')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 0))
        
        if quantity > 0:
            if quantity > cart_item.product.stock:
                messages.error(request, f'Not enough stock available for {cart_item.product.name}')
            else:
                cart_item.quantity = quantity
                cart_item.save()
                messages.success(request, 'Cart updated')
        else:
            cart_item.delete()
            messages.success(request, 'Item removed from cart')
    
    return redirect('cart')

@login_required
def remove_from_cart(request, item_id):
    # Prevent admins from removing items from cart
    if request.user.is_staff:
        messages.error(request, 'Admin users cannot remove cart items')
        return redirect('admin_dashboard')
        
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        product_name = cart_item.product.name
        cart_item.delete()
        messages.success(request, f'{product_name} removed from cart')
    
    return redirect('cart')

@login_required
def checkout(request):
    # Prevent admins from accessing checkout
    if request.user.is_staff:
        messages.error(request, 'Admin users cannot access the checkout')
        return redirect('admin_dashboard')
        
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.all()
    cart_total = sum(item.get_cost() for item in cart_items)
    
    if request.method == 'POST':
        # Check stock availability
        for item in cart_items:
            if item.quantity > item.product.stock:
                messages.error(request, f'Not enough stock for {item.product.name}')
                return redirect('cart')
        
        # Process the order
        order = Order.objects.create(
            user=request.user,
            total=cart_total,
            status='pending',
            shipping_address=request.POST.get('address'),
            shipping_phone=request.POST.get('phone')
        )
        
        # Create order items and update stock
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
            
            # Update stock
            product = item.product
            product.stock -= item.quantity
            product.save()
        
        # Clear the cart
        cart_items.delete()
        
        messages.success(request, 'Order placed successfully!')
        return redirect('user_dashboard')
    
    context = {
        'cart_items': cart_items,
        'cart_total': cart_total,
    }
    
    return render(request, 'checkout.html', context)

@login_required
def mark_notification_read(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, user=request.user)
    notification.is_read = True
    notification.save()
    
    # If the notification is about an order, redirect to the order detail page
    if notification.order:
        return redirect('user_dashboard')  # We can create an order detail view later
    
    # Otherwise redirect back to the referring page
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('user_dashboard')

@login_required
def mark_all_notifications_read(request):
    if request.method == 'POST':
        Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
        messages.success(request, 'All notifications marked as read')
    
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('user_dashboard')

def notifications_processor(request):
    """Context processor to add notifications to all templates"""
    if request.user.is_authenticated:
        unread_notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-created_at')
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:5]
        return {
            'unread_notifications_count': unread_notifications.count(),
            'notifications': notifications
        }
    return {}

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        user = request.user
        
        # Verify the password
        if user.check_password(password):
            # Delete all related data
            if hasattr(user, 'cart'):
                user.cart.delete()
            
            # Delete orders (will cascade delete order items)
            Order.objects.filter(user=user).delete()
            
            # Delete notifications
            Notification.objects.filter(user=user).delete()
            
            # Delete user profile
            if hasattr(user, 'userprofile'):
                user.userprofile.delete()
            
            # Delete the user
            user.delete()
            
            messages.success(request, 'Your account has been successfully deleted.')
            return redirect('login')
        else:
            messages.error(request, 'Incorrect password. Account deletion failed.')
            return redirect('profile')
    
    return redirect('profile')

# API Endpoints for Postman testing
@csrf_exempt
def api_plants(request):
    """
    API endpoint for plants
    GET: List all plants
    POST: Create a new plant (admin only)
    """
    if request.method == 'GET':
        plants = Plant.objects.all()
        plants_data = []
        for plant in plants:
            plants_data.append({
                'id': plant.id,
                'name': plant.name,
                'description': plant.description,
                'price': str(plant.price),
                'stock': plant.stock,
                'image': request.build_absolute_uri(plant.image.url) if plant.image else None,
                'created_at': plant.created_at.isoformat(),
                'updated_at': plant.updated_at.isoformat()
            })
        return JsonResponse({'plants': plants_data})
    
    elif request.method == 'POST':
        # Check if user is authenticated and is admin
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        try:
            data = json.loads(request.body)
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            stock = data.get('stock', 0)
            
            if not all([name, description, price]):
                return JsonResponse({'error': 'Missing required fields'}, status=400)
            
            plant = Plant.objects.create(
                name=name,
                description=description,
                price=Decimal(price),
                stock=int(stock)
            )
            
            return JsonResponse({
                'message': 'Plant created successfully',
                'plant': {
                    'id': plant.id,
                    'name': plant.name,
                    'price': str(plant.price),
                    'stock': plant.stock
                }
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_plant_detail(request, plant_id):
    """
    API endpoint for a specific plant
    GET: Get plant details
    PUT: Update plant (admin only)
    DELETE: Delete plant (admin only)
    """
    try:
        plant = Plant.objects.get(id=plant_id)
    except Plant.DoesNotExist:
        return JsonResponse({'error': 'Plant not found'}, status=404)
    
    if request.method == 'GET':
        plant_data = {
            'id': plant.id,
            'name': plant.name,
            'description': plant.description,
            'price': str(plant.price),
            'stock': plant.stock,
            'image': request.build_absolute_uri(plant.image.url) if plant.image else None,
            'created_at': plant.created_at.isoformat(),
            'updated_at': plant.updated_at.isoformat()
        }
        return JsonResponse(plant_data)
    
    elif request.method in ['PUT', 'PATCH']:
        # Check if user is authenticated and is admin
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        try:
            data = json.loads(request.body)
            
            if 'name' in data:
                plant.name = data['name']
            if 'description' in data:
                plant.description = data['description']
            if 'price' in data:
                plant.price = Decimal(data['price'])
            if 'stock' in data:
                plant.stock = int(data['stock'])
            
            plant.save()
            
            return JsonResponse({
                'message': 'Plant updated successfully',
                'plant': {
                    'id': plant.id,
                    'name': plant.name,
                    'price': str(plant.price),
                    'stock': plant.stock
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    elif request.method == 'DELETE':
        # Check if user is authenticated and is admin
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({'error': 'Unauthorized'}, status=401)
        
        plant.delete()
        return JsonResponse({'message': 'Plant deleted successfully'})
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_cart(request):
    """
    API endpoint for user's cart
    GET: Get cart contents
    POST: Add item to cart
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    # Prevent admins from accessing cart
    if request.user.is_staff:
        return JsonResponse({'error': 'Admin users cannot access the cart'}, status=403)
    
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    if request.method == 'GET':
        cart_items = []
        for item in cart.items.all():
            cart_items.append({
                'id': item.id,
                'product_id': item.product.id,
                'product_name': item.product.name,
                'price': str(item.product.price),
                'quantity': item.quantity,
                'subtotal': str(item.get_cost())
            })
        
        return JsonResponse({
            'cart_id': cart.id,
            'items': cart_items,
            'total': str(cart.get_total())
        })
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            if not product_id:
                return JsonResponse({'error': 'Product ID is required'}, status=400)
            
            try:
                plant = Plant.objects.get(id=product_id)
            except Plant.DoesNotExist:
                return JsonResponse({'error': 'Plant not found'}, status=404)
            
            if plant.stock < quantity:
                return JsonResponse({'error': 'Not enough stock available'}, status=400)
            
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=plant)
            
            if not created:
                cart_item.quantity += quantity
            else:
                cart_item.quantity = quantity
            
            cart_item.save()
            
            return JsonResponse({
                'message': f'{plant.name} added to cart',
                'cart_item': {
                    'id': cart_item.id,
                    'product_name': plant.name,
                    'quantity': cart_item.quantity,
                    'subtotal': str(cart_item.get_cost())
                }
            })
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def api_orders(request):
    """
    API endpoint for orders
    GET: List user's orders or all orders (admin only)
    POST: Create a new order
    """
    # Check if user is authenticated
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)
    
    if request.method == 'GET':
        # Get orders based on user role
        if request.user.is_staff:
            orders_queryset = Order.objects.all().order_by('-created_at')
        else:
            orders_queryset = Order.objects.filter(user=request.user).order_by('-created_at')
        
        orders_data = []
        for order in orders_queryset:
            order_items = []
            for item in order.items.all():
                order_items.append({
                    'product_name': item.product.name,
                    'price': str(item.price),
                    'quantity': item.quantity,
                    'subtotal': str(item.get_cost())
                })
            
            orders_data.append({
                'id': order.id,
                'status': order.status,
                'total': str(order.total),
                'created_at': order.created_at.isoformat(),
                'items': order_items
            })
        
        return JsonResponse({'orders': orders_data})
    
    elif request.method == 'POST':
        # Prevent admins from creating orders
        if request.user.is_staff:
            return JsonResponse({'error': 'Admin users cannot create orders'}, status=403)
        
        try:
            # Check if cart has items
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.all()
            
            if not cart_items:
                return JsonResponse({'error': 'Cart is empty'}, status=400)
            
            data = json.loads(request.body)
            shipping_address = data.get('shipping_address')
            shipping_phone = data.get('shipping_phone')
            
            if not shipping_address:
                return JsonResponse({'error': 'Shipping address is required'}, status=400)
            
            cart_total = sum(item.get_cost() for item in cart_items)
            
            # Check stock availability
            for item in cart_items:
                if item.quantity > item.product.stock:
                    return JsonResponse({
                        'error': f'Not enough stock for {item.product.name}',
                        'available': item.product.stock
                    }, status=400)
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total=cart_total,
                status='pending',
                shipping_address=shipping_address,
                shipping_phone=shipping_phone
            )
            
            # Create order items and update stock
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                
                # Update stock
                product = item.product
                product.stock -= item.quantity
                product.save()
            
            # Clear the cart
            cart_items.delete()
            
            return JsonResponse({
                'message': 'Order placed successfully',
                'order_id': order.id,
                'total': str(order.total),
                'status': order.status
            }, status=201)
            
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405) 