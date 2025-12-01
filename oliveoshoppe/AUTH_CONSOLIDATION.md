# Authentication Consolidation

## Summary
All authentication (login, register, logout) has been consolidated to use the **accounts app only**. The old API authentication routes have been removed.

## Changes Made

### 1. Removed API Auth Routes
**File: `api/urls.py`**
- Removed `path('login/', views.login_view, name='login')`
- Removed `path('register/', views.register_view, name='register')`
- Removed `path('logout/', views.logout_view, name='logout')`
- Removed `path('profile/', views.user_profile, name='profile')`

### 2. Removed Staff/Admin Registration
**File: `api/views.py` - `register_view()`**
- Removed `is_staff = request.POST.get('is_staff') == 'on'` parameter handling
- Removed `is_staff=is_staff` from user creation
- Removed conditional admin dashboard redirect
- All registered users now only redirect to shop

**File: `templates/auth/register.html`**
- Removed "Register as staff/admin" checkbox

## Auth URLs (Accounts App)

The following endpoints are now the **only** authentication routes:

```
/accounts/register/    → Register a new user (with Google OAuth + phone number)
/accounts/login/       → Login (with Google OAuth)
/accounts/logout/      → Logout
/accounts/profile/     → User profile (edit phone number)
```

## Registration Form Features

✅ **Username** - Required
✅ **Email** - Required
✅ **Phone Number** - Optional, for order updates
✅ **Password** - Required with validation
✅ **Confirm Password** - Required match verification
✅ **Google Sign-Up** - Optional OAuth button (when configured)

## User Registration Flow

1. User visits `/accounts/register/`
2. Fills in username, email, optional phone number, password
3. Optionally uses Google Sign-Up button
4. Account created as **regular user only** (no staff/admin option)
5. Auto-logged in after registration
6. Redirected to shop page

## Staff/Admin Registration

Staff and admin accounts can **only** be created via:
- Django admin panel (`/admin/`)
- Manual creation using `python manage.py createsuperuser`

This prevents unauthorized staff registration.

## Template Structure

### Primary Auth Templates (Used by Accounts App)
- `accounts/templates/registration/register.html` - Registration with Google OAuth + phone field
- `accounts/templates/registration/login.html` - Login with Google OAuth
- `accounts/templates/auth/profile.html` - User profile management

### Legacy Templates (No Longer Active Routes)
- `templates/auth/register.html` - Backup (old API route removed)
- `templates/auth/login.html` - Backup (old API route removed)
- `templates/auth/base_auth.html` - Base styling

## URL Resolution

All templates use non-namespaced URL names:
- `{% url 'register' %}` → Resolves to `/accounts/register/` (accounts app)
- `{% url 'login' %}` → Resolves to `/accounts/login/` (accounts app)
- `{% url 'logout' %}` → Resolves to `/accounts/logout/` (accounts app)

Since accounts app URLs are loaded **first** in main `urls.py`, these names are unique and consistent.

## Settings Configuration

**File: `oliveoshoppe/settings.py`**
- `LOGIN_URL = 'login'` - Redirects to `/accounts/login/`
- `LOGIN_REDIRECT_URL = 'home'` - Redirects to shop after login
- `ACCOUNT_AUTHENTICATION_METHOD = 'email'` - Google OAuth uses email
- `SOCIALACCOUNT_PROVIDERS` - Google OAuth configured (when credentials added)

## Testing Registration

To verify consolidation works:

1. Start server: `python manage.py runserver`
2. Visit `/accounts/register/` - Should show:
   - Registration form with phone number field
   - "Sign up with Google" button
   - **No** staff/admin checkbox
3. Visit `/register/` - Should **404 Not Found** (old route removed)
4. Register a user - Should:
   - Create account as regular user
   - Auto-login
   - Redirect to shop
5. Check user in admin - `is_staff=False`

## Summary

✅ Single authentication system (accounts app)
✅ Phone number field in registration
✅ Google OAuth integration ready
✅ Staff/admin registration removed from public endpoint
✅ Server running with no errors
