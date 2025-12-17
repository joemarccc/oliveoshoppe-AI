"""
Supabase Storage integration for plant images
"""
import logging
from decouple import config
from supabase import create_client, Client
import uuid
import mimetypes

logger = logging.getLogger(__name__)

SUPABASE_URL = config('SUPABASE_URL', default='')
SUPABASE_SERVICE_ROLE_KEY = config('SUPABASE_SERVICE_ROLE_KEY', default='')

def get_supabase_client() -> Client:
    """Get Supabase client with service role key for storage operations"""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        raise RuntimeError("Supabase credentials not configured")
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


def upload_plant_image(image_file, plant_name=None):
    """
    Upload plant image to Supabase Storage
    
    Args:
        image_file: Django UploadedFile object
        plant_name: Optional plant name for better file naming
    
    Returns:
        dict: {'success': bool, 'url': str, 'error': str}
    """
    try:
        client = get_supabase_client()
        
        # Generate unique filename
        ext = image_file.name.split('.')[-1] if '.' in image_file.name else 'jpg'
        base_name = plant_name.lower().replace(' ', '_') if plant_name else 'plant'
        filename = f"{base_name}_{uuid.uuid4().hex[:8]}.{ext}"
        
        # Get file content
        image_file.seek(0)
        file_content = image_file.read()
        
        # Detect MIME type
        mime_type = mimetypes.guess_type(image_file.name)[0] or 'image/jpeg'
        
        # Upload to Supabase Storage bucket 'plants'
        response = client.storage.from_('plants').upload(
            filename,
            file_content,
            {
                'content-type': mime_type,
                'x-upsert': 'true'  # Overwrite if exists
            }
        )
        
        # Get public URL
        public_url = client.storage.from_('plants').get_public_url(filename)
        
        logger.info(f"Successfully uploaded image to Supabase: {filename}")
        return {
            'success': True,
            'url': public_url,
            'filename': filename
        }
        
    except Exception as e:
        logger.error(f"Error uploading to Supabase Storage: {str(e)}")
        return {
            'success': False,
            'error': str(e)
        }


def delete_plant_image(image_url):
    """
    Delete plant image from Supabase Storage
    
    Args:
        image_url: Full public URL of the image
    
    Returns:
        bool: True if deleted successfully
    """
    try:
        client = get_supabase_client()
        
        # Extract filename from URL
        # URL format: https://xxx.supabase.co/storage/v1/object/public/plants/filename.jpg
        if '/plants/' in image_url:
            filename = image_url.split('/plants/')[-1]
            client.storage.from_('plants').remove([filename])
            logger.info(f"Deleted image from Supabase: {filename}")
            return True
        return False
        
    except Exception as e:
        logger.error(f"Error deleting from Supabase Storage: {str(e)}")
        return False
