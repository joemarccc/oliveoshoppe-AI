"""
Supabase Authentication Integration for OliveOshoppe
Handles all authentication operations with Supabase backend
"""

from supabase import create_client, Client
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SupabaseAuthManager:
    """
    Manages all Supabase authentication operations.
    Uses Supabase as the authentication backend while keeping Django for app logic.
    """
    
    def __init__(self):
        """Initialize Supabase client"""
        try:
            self.client: Client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_ANON_KEY
            )
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            self.client = None
    
    def signup_email(self, email: str, password: str, phone_number: str = None, full_name: str = None) -> dict:
        """
        Register new user with email and password.
        
        Args:
            email (str): User email address
            password (str): User password (min 6 characters)
            phone_number (str, optional): Phone in +63 format
            full_name (str, optional): User's full name
        
        Returns:
            dict: {
                'success': bool,
                'user': user object or None,
                'error': error message or None,
                'message': confirmation message
            }
        
        Example:
            >>> auth = SupabaseAuthManager()
            >>> result = auth.signup_email(
            ...     'user@example.com',
            ...     'SecurePass123!',
            ...     phone_number='+63 912 345 6789'
            ... )
            >>> if result['success']:
            ...     print(f"User created: {result['user'].email}")
        """
        if not self.client:
            return {
                'success': False,
                'user': None,
                'error': 'Supabase client not initialized',
                'message': None
            }
        
        try:
            # Prepare metadata
            metadata = {
                'phone_number': phone_number or '',
                'full_name': full_name or email.split('@')[0]
            }
            
            # Sign up in Supabase
            response = self.client.auth.sign_up({
                "email": email,
                "password": password,
                "options": {
                    "data": metadata,
                    "redirect_to": f"{settings.SITE_URL}/auth/callback"
                }
            })
            
            logger.info(f"User signup successful: {email}")
            
            return {
                'success': True,
                'user': response.user,
                'error': None,
                'message': 'Account created! Please verify your email.'
            }
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Signup failed for {email}: {error_msg}")
            
            return {
                'success': False,
                'user': None,
                'error': error_msg,
                'message': None
            }
    
    def login_email(self, email: str, password: str) -> dict:
        """
        Login with email and password.
        
        Args:
            email (str): User email
            password (str): User password
        
        Returns:
            dict: {
                'success': bool,
                'session': session object or None,
                'user': user object or None,
                'token': access token or None,
                'error': error message or None
            }
        
        Example:
            >>> auth = SupabaseAuthManager()
            >>> result = auth.login_email('user@example.com', 'password')
            >>> if result['success']:
            ...     token = result['token']
            ...     request.session['supabase_token'] = token
        """
        if not self.client:
            return {
                'success': False,
                'session': None,
                'user': None,
                'token': None,
                'error': 'Supabase client not initialized'
            }
        
        try:
            response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            logger.info(f"User login successful: {email}")
            
            return {
                'success': True,
                'session': response.session,
                'user': response.user,
                'token': response.session.access_token if response.session else None,
                'error': None
            }
        
        except Exception as e:
            error_msg = str(e)
            logger.warning(f"Login failed for {email}: {error_msg}")
            
            return {
                'success': False,
                'session': None,
                'user': None,
                'token': None,
                'error': error_msg
            }
    
    def get_user_profile(self, user_id: str) -> dict:
        """
        Get user profile from Supabase profiles table.
        
        Args:
            user_id (str): Supabase user UUID
        
        Returns:
            dict: Profile data or None if not found
        
        Example:
            >>> profile = auth.get_user_profile(user_id)
            >>> if profile:
            ...     print(f"Phone: {profile['phone_number']}")
        """
        if not self.client:
            logger.error("Supabase client not initialized")
            return None
        
        try:
            response = self.client.table('profiles').select('*').eq('id', user_id).execute()
            
            if response.data and len(response.data) > 0:
                logger.info(f"Profile retrieved for user: {user_id}")
                return response.data[0]
            
            logger.warning(f"No profile found for user: {user_id}")
            return None
        
        except Exception as e:
            logger.error(f"Error getting profile for {user_id}: {str(e)}")
            return None
    
    def update_user_profile(self, user_id: str, phone_number: str = None, full_name: str = None) -> dict:
        """
        Update user profile in Supabase.
        
        Args:
            user_id (str): Supabase user UUID
            phone_number (str, optional): Phone number to update
            full_name (str, optional): Full name to update
        
        Returns:
            dict: {
                'success': bool,
                'data': updated profile data or None,
                'error': error message or None
            }
        
        Example:
            >>> result = auth.update_user_profile(
            ...     user_id='uuid-here',
            ...     phone_number='+63 912 345 6789'
            ... )
            >>> if result['success']:
            ...     print("Profile updated")
        """
        if not self.client:
            return {
                'success': False,
                'data': None,
                'error': 'Supabase client not initialized'
            }
        
        try:
            update_data = {}
            
            if phone_number is not None:
                update_data['phone_number'] = phone_number
            
            if full_name is not None:
                update_data['full_name'] = full_name
            
            if not update_data:
                return {
                    'success': False,
                    'data': None,
                    'error': 'No fields to update'
                }
            
            update_data['updated_at'] = 'now()'
            
            response = self.client.table('profiles').update(update_data).eq('id', user_id).execute()
            
            logger.info(f"Profile updated for user: {user_id}")
            
            return {
                'success': True,
                'data': response.data[0] if response.data else None,
                'error': None
            }
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error updating profile for {user_id}: {error_msg}")
            
            return {
                'success': False,
                'data': None,
                'error': error_msg
            }
    
    def verify_token(self, token: str) -> dict:
        """
        Verify JWT token and get user information.
        
        Args:
            token (str): JWT access token
        
        Returns:
            dict: User information or None if invalid
        
        Example:
            >>> user = auth.verify_token(token)
            >>> if user:
            ...     print(f"Valid token for: {user.email}")
        """
        if not self.client:
            return None
        
        try:
            user = self.client.auth.get_user(token)
            logger.info(f"Token verified for user: {user.id}")
            return user
        
        except Exception as e:
            logger.warning(f"Invalid token: {str(e)}")
            return None
    
    def logout(self) -> dict:
        """
        Logout current user (sign out from all sessions).
        Note: In practice, just clear the session from Django.
        
        Returns:
            dict: Success status
        """
        return {
            'success': True,
            'message': 'Logged out successfully'
        }
    
    def reset_password(self, email: str) -> dict:
        """
        Send password reset email to user.
        
        Args:
            email (str): User email address
        
        Returns:
            dict: {
                'success': bool,
                'error': error message or None,
                'message': confirmation message
            }
        """
        if not self.client:
            return {
                'success': False,
                'error': 'Supabase client not initialized',
                'message': None
            }
        
        try:
            response = self.client.auth.reset_password_email(email)
            
            logger.info(f"Password reset email sent to: {email}")
            
            return {
                'success': True,
                'error': None,
                'message': 'Password reset email sent. Check your inbox.'
            }
        
        except Exception as e:
            error_msg = str(e)
            logger.error(f"Password reset failed for {email}: {error_msg}")
            
            return {
                'success': False,
                'error': error_msg,
                'message': None
            }


# Create a singleton instance
_auth_manager = None


def get_auth_manager() -> SupabaseAuthManager:
    """Get or create Supabase auth manager instance"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = SupabaseAuthManager()
    return _auth_manager


# Convenience functions for easy import
def signup_with_supabase(email: str, password: str, phone_number: str = None, full_name: str = None):
    """Register new user"""
    manager = get_auth_manager()
    return manager.signup_email(email, password, phone_number, full_name)


def login_with_supabase(email: str, password: str):
    """Login with email and password"""
    manager = get_auth_manager()
    return manager.login_email(email, password)


def get_profile(user_id: str):
    """Get user profile"""
    manager = get_auth_manager()
    return manager.get_user_profile(user_id)


def update_profile(user_id: str, phone_number: str = None, full_name: str = None):
    """Update user profile"""
    manager = get_auth_manager()
    return manager.update_user_profile(user_id, phone_number, full_name)


def verify_supabase_token(token: str):
    """Verify JWT token"""
    manager = get_auth_manager()
    return manager.verify_token(token)


def reset_password(email: str):
    """Send password reset email"""
    manager = get_auth_manager()
    return manager.reset_password(email)
