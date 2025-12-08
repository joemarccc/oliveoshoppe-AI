"""
Supabase Authentication Module
Handles user signup, login, profile management with Supabase
"""
import httpx
from supabase import ClientOptions, create_client
from decouple import config
import logging

logger = logging.getLogger(__name__)

# Initialize Supabase client
SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_ANON_KEY = config('SUPABASE_ANON_KEY', default='')
SUPABASE_SERVICE_ROLE_KEY = config('SUPABASE_SERVICE_ROLE_KEY', default='')

def _make_supabase_client(key: str):
    """Create a Supabase client with a prebuilt httpx client to avoid proxy kwarg issues."""
    if not SUPABASE_URL or not key:
        logger.warning("Supabase URL or key missing; skipping client bootstrap")
        return None

    http_client = httpx.Client(http2=True, timeout=30.0)
    options = ClientOptions(httpx_client=http_client)

    try:
        return create_client(SUPABASE_URL, key, options=options)
    except TypeError as exc:
        logger.error("Supabase client init failed (proxy/httpx mismatch): %s", exc)
        raise


supabase = _make_supabase_client(SUPABASE_ANON_KEY)
supabase_admin = _make_supabase_client(SUPABASE_SERVICE_ROLE_KEY)


def _require_supabase():
    if supabase is None:
        raise RuntimeError("Supabase client not initialized. Check SUPABASE_URL and SUPABASE_ANON_KEY.")
    return supabase


def _require_supabase_admin():
    if supabase_admin is None:
        raise RuntimeError(
            "Supabase admin client not initialized. Check SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY."
        )
    return supabase_admin

# ============================================
# EMAIL VERIFICATION (Registration - Confirmation Link)
# ============================================

def send_confirmation_email(email, redirect_url=None):
    """
    Send confirmation email with magic link for registration
    User clicks link in email to verify and proceed to step 3
    """
    try:
        supabase_client = _require_supabase()
        import uuid
        # Generate a temporary password (user will set real password in step 3)
        temp_password = str(uuid.uuid4())[:16]
        
        # Prepare signup options with redirect URL
        signup_options = {
            'email': email,
            'password': temp_password,
        }
        
        if redirect_url:
            signup_options['options'] = {
                'redirect_to': redirect_url
            }
        
        print(f"[DEBUG] Attempting to sign_up with email: {email}")
        print(f"[DEBUG] Supabase URL: {SUPABASE_URL}")
        
        # Supabase sign_up sends a confirmation email with magic link
        response = supabase_client.auth.sign_up(signup_options)
        
        print(f"[DEBUG] Sign_up response: {response}")
        logger.info(f"Confirmation email sent to {email}")
        return {
            'success': True,
            'message': f'Confirmation email sent to {email}. Please check your email to verify.'
        }
    except Exception as e:
        error_str = str(e)
        print(f"[ERROR] Failed to send confirmation email: {error_str}")
        logger.error(f"Error sending confirmation email to {email}: {error_str}")
        return {
            'success': False,
            'error': error_str
        }


def verify_confirmation_token(token):
    """
    Verify confirmation token from email link
    """
    try:
        supabase_client = _require_supabase()
        response = supabase_client.auth.verify_otp({
            'token': token,
            'type': 'signup'
        })
        
        if response.user:
            logger.info(f"Email verified for user: {response.user.email}")
            return {
                'success': True,
                'user': response.user,
                'message': 'Email verified successfully!'
            }
        else:
            return {
                'success': False,
                'error': 'Email verification failed'
            }
    
    except Exception as e:
        error_str = str(e)
        logger.error(f"Email verification error: {error_str}")
        
        if 'invalid' in error_str.lower() or 'expired' in error_str.lower():
            error_msg = 'Verification link expired or invalid. Please sign up again.'
        else:
            error_msg = 'Email verification failed.'
        
        return {
            'success': False,
            'error': error_msg
        }


# ============================================
# SIGNUP / REGISTRATION
# ============================================

def signup_with_supabase(email, password, full_name=None, phone_number=None):
    """
    Sign up a new user with Supabase
    Creates user in auth.users and creates profile entry
    """
    try:
        supabase_client = _require_supabase()
        supabase_admin_client = _require_supabase_admin()
        # Create user in Supabase Auth
        auth_response = supabase_client.auth.sign_up({
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "full_name": full_name or email.split('@')[0],
                    "phone_number": phone_number
                }
            }
        })
        
        if auth_response.user:
            user_id = str(auth_response.user.id)
            
            # Create profile in profiles table
            try:
                profile_response = supabase_admin_client.table('profiles').insert({
                    'id': user_id,
                    'email': email,
                    'full_name': full_name or email.split('@')[0],
                    'phone_number': phone_number
                }).execute()
                
                logger.info(f"User {email} registered successfully with profile created")
                return {
                    'success': True,
                    'user': auth_response.user,
                    'profile': profile_response.data
                }
            except Exception as profile_error:
                logger.warning(f"User created but profile creation failed: {str(profile_error)}")
                # User was created even if profile fails
                return {
                    'success': True,
                    'user': auth_response.user,
                    'warning': f"Profile creation failed: {str(profile_error)}"
                }
        else:
            logger.error(f"Signup failed for {email}: No user returned")
            return {
                'success': False,
                'error': 'No user returned from signup'
            }
    
    except Exception as e:
        logger.error(f"Signup error for {email}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# ============================================
# LOGIN
# ============================================

def login_with_supabase(email, password):
    """
    Login user with email and password
    Returns user and session token
    """
    try:
        supabase_client = _require_supabase()
        auth_response = supabase_client.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        if auth_response.user and auth_response.session:
            logger.info(f"User {email} logged in successfully")
            return {
                'success': True,
                'user': auth_response.user,
                'session': auth_response.session,
                'token': auth_response.session.access_token
            }
        else:
            logger.error(f"Login failed for {email}: Invalid credentials")
            return {
                'success': False,
                'error': 'Invalid email or password'
            }
    
    except Exception as e:
        logger.error(f"Login error for {email}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# ============================================
# PROFILE MANAGEMENT
# ============================================

def get_profile(user_id):
    """Get user profile from Supabase"""
    try:
        supabase_client = _require_supabase()
        response = supabase_client.table('profiles').select('*').eq('id', user_id).single().execute()
        return response.data if response.data else None
    except Exception as e:
        logger.error(f"Error fetching profile for {user_id}: {str(e)}")
        return None

def update_profile(user_id, **kwargs):
    """Update user profile"""
    try:
        supabase_admin_client = _require_supabase_admin()
        response = supabase_admin_client.table('profiles').update(kwargs).eq('id', user_id).execute()
        return {
            'success': True,
            'data': response.data
        }
    except Exception as e:
        logger.error(f"Error updating profile for {user_id}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# ============================================
# PASSWORD RESET
# ============================================

def reset_password(email):
    """Send password reset email"""
    try:
        supabase_client = _require_supabase()
        response = supabase_client.auth.reset_password_for_email(email)
        logger.info(f"Password reset email sent to {email}")
        return {
            'success': True,
            'message': 'Check your email for password reset link'
        }
    except Exception as e:
        logger.error(f"Password reset error for {email}: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# ============================================
# VERIFY TOKEN
# ============================================

def verify_token(token):
    """Verify a JWT token"""
    try:
        supabase_client = _require_supabase()
        response = supabase_client.auth.get_user(token)
        return {
            'success': True,
            'user': response.user
        }
    except Exception as e:
        logger.error(f"Token verification failed: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }

# ============================================
# LOGOUT
# ============================================

def logout():
    """Logout current user"""
    try:
        supabase_client = _require_supabase()
        supabase_client.auth.sign_out()
        logger.info("User logged out successfully")
        return {
            'success': True,
            'message': 'Logged out successfully'
        }
    except Exception as e:
        logger.error(f"Logout error: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }
