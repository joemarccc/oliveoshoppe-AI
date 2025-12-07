"""
Supabase Database Helper Module
Handles all Supabase database operations for plants, orders, wishlist, etc.
"""

from supabase import create_client
from decouple import config
import logging

logger = logging.getLogger(__name__)

# Initialize Supabase client
SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_SERVICE_ROLE_KEY = config('SUPABASE_SERVICE_ROLE_KEY', default='')

supabase = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# ============================================
# PLANTS OPERATIONS
# ============================================

def get_all_plants():
    """Get all plants"""
    try:
        response = supabase.table('plants').select('*').execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error fetching plants: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_plant(plant_id):
    """Get a single plant by ID"""
    try:
        response = supabase.table('plants').select('*').eq('id', plant_id).single().execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error fetching plant {plant_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def create_plant(name, price, description=None, stock=0, image_url=None):
    """Create a new plant"""
    try:
        response = supabase.table('plants').insert({
            'name': name,
            'price': price,
            'description': description,
            'stock': stock,
            'image_url': image_url
        }).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error creating plant: {str(e)}")
        return {'success': False, 'error': str(e)}

def update_plant(plant_id, **kwargs):
    """Update a plant"""
    try:
        response = supabase.table('plants').update(kwargs).eq('id', plant_id).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error updating plant {plant_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def delete_plant(plant_id):
    """Delete a plant"""
    try:
        response = supabase.table('plants').delete().eq('id', plant_id).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error deleting plant {plant_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

# ============================================
# ORDERS OPERATIONS
# ============================================

def create_order(user_id, total_price, shipping_address=None, phone=None):
    """Create a new order"""
    try:
        response = supabase.table('orders').insert({
            'user_id': user_id,
            'total_price': total_price,
            'shipping_address': shipping_address,
            'phone': phone,
            'status': 'pending'
        }).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error creating order: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_user_orders(user_id):
    """Get all orders for a user"""
    try:
        response = supabase.table('orders').select('*').eq('user_id', user_id).order('created_at', desc=True).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error fetching orders for user {user_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_order(order_id):
    """Get a single order with items"""
    try:
        order_response = supabase.table('orders').select('*').eq('id', order_id).single().execute()
        items_response = supabase.table('order_items').select('*').eq('order_id', order_id).execute()
        
        return {
            'success': True,
            'order': order_response.data,
            'items': items_response.data
        }
    except Exception as e:
        logger.error(f"Error fetching order {order_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

def update_order(order_id, **kwargs):
    """Update an order"""
    try:
        response = supabase.table('orders').update(kwargs).eq('id', order_id).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error updating order {order_id}: {str(e)}")
        return {'success': False, 'error': str(e)}

# ============================================
# ORDER ITEMS OPERATIONS
# ============================================

def add_order_item(order_id, plant_id, quantity, price):
    """Add an item to an order"""
    try:
        response = supabase.table('order_items').insert({
            'order_id': order_id,
            'plant_id': plant_id,
            'quantity': quantity,
            'price': price
        }).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error adding order item: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_order_items(order_id):
    """Get all items in an order"""
    try:
        response = supabase.table('order_items').select('*').eq('order_id', order_id).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error fetching order items: {str(e)}")
        return {'success': False, 'error': str(e)}

# ============================================
# WISHLIST OPERATIONS
# ============================================

def add_to_wishlist(user_id, plant_id):
    """Add a plant to user's wishlist"""
    try:
        response = supabase.table('wishlist').insert({
            'user_id': user_id,
            'plant_id': plant_id
        }).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error adding to wishlist: {str(e)}")
        return {'success': False, 'error': str(e)}

def remove_from_wishlist(user_id, plant_id):
    """Remove a plant from user's wishlist"""
    try:
        response = supabase.table('wishlist').delete().eq('user_id', user_id).eq('plant_id', plant_id).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error removing from wishlist: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_user_wishlist(user_id):
    """Get user's wishlist with plant details"""
    try:
        response = supabase.table('wishlist').select('*, plants(*)').eq('user_id', user_id).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error fetching wishlist: {str(e)}")
        return {'success': False, 'error': str(e)}

def is_in_wishlist(user_id, plant_id):
    """Check if plant is in user's wishlist"""
    try:
        response = supabase.table('wishlist').select('id').eq('user_id', user_id).eq('plant_id', plant_id).execute()
        return {'success': True, 'in_wishlist': len(response.data) > 0}
    except Exception as e:
        logger.error(f"Error checking wishlist: {str(e)}")
        return {'success': False, 'error': str(e)}

# ============================================
# NOTIFICATIONS OPERATIONS
# ============================================

def create_notification(user_id, message):
    """Create a notification for a user"""
    try:
        response = supabase.table('notifications').insert({
            'user_id': user_id,
            'message': message,
            'is_read': False
        }).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error creating notification: {str(e)}")
        return {'success': False, 'error': str(e)}

def get_user_notifications(user_id, unread_only=False):
    """Get user's notifications"""
    try:
        query = supabase.table('notifications').select('*').eq('user_id', user_id)
        if unread_only:
            query = query.eq('is_read', False)
        response = query.order('created_at', desc=True).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error fetching notifications: {str(e)}")
        return {'success': False, 'error': str(e)}

def mark_notification_read(notification_id):
    """Mark a notification as read"""
    try:
        response = supabase.table('notifications').update({'is_read': True}).eq('id', notification_id).execute()
        return {'success': True, 'data': response.data}
    except Exception as e:
        logger.error(f"Error marking notification read: {str(e)}")
        return {'success': False, 'error': str(e)}
