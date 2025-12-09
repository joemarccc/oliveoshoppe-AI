"""
Authentication Middleware for OliveOshoppe
Redirects unauthenticated users to login for protected actions
while allowing them to view the homepage
"""
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
import re


class LoginRequiredForActionsMiddleware:
    """
    Middleware that allows unauthenticated users to view the homepage
    but redirects them to login when they try to perform actions like:
    - Adding to cart
    - Viewing product details
    - Checkout
    - Profile access
    - Any POST requests on protected paths
    """
    
    # Paths that don't require authentication (can be viewed by anyone)
    PUBLIC_PATHS = [
        r'^/$',                          # Homepage / Shop
        r'^/shop/',                      # Shop page
        r'^/api/$',                      # API shop home
        r'^/accounts/login/',            # Login page
        r'^/accounts/register/',         # Registration pages
        r'^/accounts/password_reset/',   # Password reset
        r'^/auth/confirm/',              # Email confirmation
        r'^/static/',                    # Static files
        r'^/media/',                     # Media files
        r'^/admin/login/',               # Admin login
        r'^/chatbot/',                   # Chatbot (optional - remove if needs auth)
        r'^/plants/$',                   # Plant list view (read-only)
        r'^/plants/\d+/$',               # Plant detail view (read-only)
    ]
    
    # Paths that require authentication (actions, not viewing)
    PROTECTED_PATHS = [
        r'^/cart/',                      # Cart
        r'^/checkout/',                  # Checkout
        r'^/cart/add/',                  # Add to cart action
        r'^/wishlist/',                  # Wishlist
        r'^/orders/',                    # Orders
        r'^/accounts/profile/',          # Profile
        r'^/accounts/dashboard/',        # Dashboard
        r'^/api/protected/',             # Protected API
        r'^/plants/create/',             # Create plant (admin)
        r'^/plants/\d+/edit/',           # Edit plant (admin)
        r'^/plants/\d+/delete/',         # Delete plant (admin)
    ]
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Compile regex patterns for efficiency
        self.public_patterns = [re.compile(p) for p in self.PUBLIC_PATHS]
        self.protected_patterns = [re.compile(p) for p in self.PROTECTED_PATHS]
    
    def __call__(self, request):
        # Skip if user is authenticated
        if request.user.is_authenticated:
            return self.get_response(request)
        
        path = request.path
        
        # Allow public paths
        for pattern in self.public_patterns:
            if pattern.match(path):
                return self.get_response(request)
        
        # Check if path is explicitly protected
        is_protected = False
        for pattern in self.protected_patterns:
            if pattern.match(path):
                is_protected = True
                break
        
        # If protected or a POST request to non-public path, redirect to login
        if is_protected or (request.method == 'POST' and not self._is_public(path)):
            messages.info(request, 'Please login to continue.')
            login_url = reverse('login')
            next_url = request.get_full_path()
            return redirect(f'{login_url}?next={next_url}')
        
        return self.get_response(request)
    
    def _is_public(self, path):
        """Check if a path is public"""
        for pattern in self.public_patterns:
            if pattern.match(path):
                return True
        return False
