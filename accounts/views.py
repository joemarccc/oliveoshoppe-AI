from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .forms import CustomUserCreationForm, UserProfileForm
from .models import UserProfile
from .supabase_auth import signup_with_supabase, send_confirmation_email, verify_confirmation_token, verify_access_token
from decouple import config
import logging
import json

logger = logging.getLogger(__name__)

def register_step1_email(request):
    """Step 1: User enters email and agrees to T&C"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'auth/register_step1.html')
        
        # Build callback URL for Supabase email link - use production URL
        # Check if we're in production (Render) or local
        if request.get_host() and 'onrender.com' in request.get_host():
            callback_url = f"https://{request.get_host()}/auth/confirm/"
        elif request.get_host() and 'localhost' not in request.get_host() and '127.0.0.1' not in request.get_host():
            callback_url = request.build_absolute_uri('/auth/confirm/')
        else:
            # Local development - still use the proper confirm endpoint
            callback_url = request.build_absolute_uri('/auth/confirm/')
        
        # Send confirmation email with magic link
        email_result = send_confirmation_email(email, redirect_url=callback_url)
        
        if email_result['success']:
            # Store email in session for later
            request.session['registration_email'] = email
            request.session['registration_step'] = 1
            messages.success(request, f'Confirmation email sent to {email}. Please check your email.')
            return redirect('register_step2_email_check')
        else:
            error_msg = email_result.get('error', 'Failed to send confirmation email')
            messages.error(request, f'Error: {error_msg}')
            return render(request, 'auth/register_step1.html', {'email': email})
    
    return render(request, 'auth/register_step1.html')


def register_step2_email_check(request):
    """Step 2: User checks email and clicks confirmation link"""
    if request.user.is_authenticated:
        return redirect('home')
    
    email = request.session.get('registration_email')
    if not email:
        messages.error(request, 'Please start from the beginning.')
        return redirect('register_step1_email')
    
    # If already verified, redirect to step 3
    if request.session.get('email_verified'):
        return redirect('register_step3_details')
    
    # Development mode: Allow skipping email verification
    if request.method == 'POST' and request.POST.get('skip_email'):
        if config('DEBUG', default=False, cast=bool):
            # In development, auto-verify and go to step 3
            request.session['email_verified'] = True
            request.session['registration_step'] = 2
            return redirect('register_step3_details')
    
    debug = config('DEBUG', default=False, cast=bool)
    return render(request, 'auth/register_step2_email_check.html', {'email': email, 'debug': debug})


@require_http_methods(["GET"])
def check_email_verification(request):
    """API endpoint to check if email has been verified (for polling from step 2)"""
    if request.session.get('email_verified'):
        return JsonResponse({
            'verified': True,
            'redirect_url': '/accounts/register/step3/'
        })
    return JsonResponse({'verified': False})


def register_callback(request):
    """
    Callback handler for confirmation link from email
    Processes token and automatically redirects to Step 3
    """
    token = request.GET.get('token')
    token_hash = request.GET.get('token_hash')
    email = request.GET.get('email')
    token_to_verify = token_hash or token
    
    if not token_to_verify:
        messages.error(request, 'Invalid confirmation link.')
        return redirect('register_step1_email')
    
    # Verify the confirmation token
    verify_result = verify_confirmation_token(token_to_verify, email=email)
    
    if verify_result['success']:
        # Extract email from the verified user
        user_email = verify_result['user'].email if hasattr(verify_result['user'], 'email') else email
        
        # Store verified state in session
        request.session['registration_email'] = user_email
        request.session['email_verified'] = True
        request.session['registration_step'] = 2
        
        # Auto-redirect to Step 3
        return redirect('register_step3_details')
    else:
        error_msg = verify_result.get('error', 'Email verification failed')
        messages.error(request, error_msg)
        return redirect('register_step1_email')


def register_step3_details(request):
    """Step 3: User enters username, password, and phone number"""
    if request.user.is_authenticated:
        return redirect('home')
    
    # Check if email was verified via link
    if not request.session.get('email_verified'):
        messages.error(request, 'Please verify your email first.')
        return redirect('register_step1_email')
    
    email = request.session.get('registration_email')
    if not email:
        messages.error(request, 'Session expired. Please start over.')
        return redirect('register_step1_email')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            phone_number = form.cleaned_data.get('phone_number', '')
            
            # Create user in Supabase using the email-verified email
            supabase_result = signup_with_supabase(
                email=email,
                password=password,
                full_name=username,
                phone_number=phone_number
            )
            
            if supabase_result['success']:
                # Also create Django user for compatibility
                try:
                    # Create user with the provided email (form should have this field)
                    user = form.save(commit=False)
                    user.email = email
                    user.save()
                    
                    # Create UserProfile linked to Supabase user
                    UserProfile.objects.get_or_create(
                        user=user,
                        defaults={'phone_number': phone_number}
                    )
                    
                    # Clear registration session data
                    if 'registration_email' in request.session:
                        del request.session['registration_email']
                    if 'email_verified' in request.session:
                        del request.session['email_verified']
                    if 'registration_step' in request.session:
                        del request.session['registration_step']
                    
                    messages.success(request, 'Account created successfully! Please login to continue.')
                    return redirect('login')
                except Exception as e:
                    logger.error(f"Error creating Django user: {str(e)}")
                    messages.error(request, 'Error creating local account. Please try again.')
            else:
                error_msg = supabase_result.get('error', 'Unknown error')
                if 'already exists' in error_msg.lower():
                    messages.error(request, 'This email is already registered. Please login instead.')
                else:
                    messages.error(request, f'Registration failed: {error_msg}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{error}')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'auth/register_step3.html', {'form': form, 'email': email})


def register(request):
    """Redirect to step 1 (kept for backwards compatibility)"""
    return redirect('register_step1_email')


def resend_otp(request):
    """Resend confirmation email to user"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    
    email = request.session.get('registration_email')
    if not email:
        return JsonResponse({'success': False, 'error': 'No email in session'}, status=400)
    
    # Build callback URL for Supabase email link
    callback_url = request.build_absolute_uri('/accounts/register/callback/')
    
    # Send confirmation email again
    email_result = send_confirmation_email(email, redirect_url=callback_url)
    
    if email_result['success']:
        return JsonResponse({'success': True, 'message': 'Confirmation email resent'})
    else:
        error_msg = email_result.get('error', 'Failed to send email')
        return JsonResponse({'success': False, 'error': error_msg}, status=400)


def dashboard(request):
    """Redirect to profile page"""
    return redirect('profile')

def login_view(request):
    """Login with Supabase"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        if not username or not password:
            messages.error(request, 'Please enter username and password')
            return render(request, 'auth/login.html')
        
        # Try to login with Supabase using email or username
        from .supabase_auth import login_with_supabase
        
        # First try as email
        supabase_result = login_with_supabase(username, password)
        
        # If failed and username doesn't look like email, try to find user by username
        if not supabase_result['success'] and '@' not in username:
            try:
                user = authenticate(request, username=username, password=password)
                if user:
                    login(request, user)
                    messages.success(request, f'Welcome back!')
                    return redirect('home')
            except:
                pass
        
        if supabase_result['success']:
            # Store Supabase token in session
            request.session['supabase_token'] = supabase_result.get('token')
            request.session['supabase_user_id'] = str(supabase_result['user'].id)
            
            # Also login to Django for compatibility
            try:
                django_user = authenticate(request, username=username, password=password)
                if django_user:
                    login(request, django_user)
            except:
                pass
            
            messages.success(request, 'Welcome back!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email/username or password')
    
    return render(request, 'auth/login.html')

@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'auth/profile.html', {'form': form, 'user_profile': user_profile})


# ============================================
# AUTH CONFIRM VIEWS (Supabase Email Confirmation)
# ============================================

def auth_confirm(request):
    """
    Display the email confirmation page
    This page handles the Supabase redirect with hash parameters
    """
    return render(request, 'auth/auth_confirm.html')


@require_http_methods(["POST"])
def auth_confirm_verify(request):
    """
    API endpoint to verify Supabase tokens from the confirmation page
    Handles access_token, token_hash, or session check
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
    
    # Check if just verifying session
    if data.get('check_session'):
        if request.session.get('email_verified'):
            return JsonResponse({
                'success': True,
                'session_verified': True,
                'email': request.session.get('registration_email')
            })
        return JsonResponse({'success': False, 'error': 'No verified session'})
    
    access_token = data.get('access_token')
    token_hash = data.get('token_hash')
    token_type = data.get('type', 'signup')
    
    # Try to verify access token first
    if access_token:
        result = verify_access_token(access_token)
        if result['success']:
            user_email = result['user'].email if hasattr(result['user'], 'email') else None
            
            # Store in session
            if user_email:
                request.session['registration_email'] = user_email
            request.session['email_verified'] = True
            request.session['registration_step'] = 2
            
            return JsonResponse({
                'success': True,
                'message': 'Email verified successfully',
                'email': user_email
            })
        else:
            return JsonResponse({'success': False, 'error': result.get('error', 'Token verification failed')})
    
    # Try token_hash verification
    if token_hash:
        email = request.session.get('registration_email')
        result = verify_confirmation_token(token_hash, email=email)
        
        if result['success']:
            user_email = result['user'].email if hasattr(result['user'], 'email') else email
            
            if user_email:
                request.session['registration_email'] = user_email
            request.session['email_verified'] = True
            request.session['registration_step'] = 2
            
            return JsonResponse({
                'success': True,
                'message': 'Email verified successfully',
                'email': user_email
            })
        else:
            return JsonResponse({'success': False, 'error': result.get('error', 'Verification failed')})
    
    return JsonResponse({'success': False, 'error': 'No token provided'}, status=400)

