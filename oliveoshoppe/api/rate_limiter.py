from django.core.cache import cache
from django.http import JsonResponse
from functools import wraps
import time

def rate_limit(requests_per_minute=5):
    """
    Rate limiting decorator that limits the number of requests per minute per client IP.
    
    Args:
        requests_per_minute (int): Maximum number of requests allowed per minute
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Get client IP
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR'))
            
            # Create a unique cache key for this IP and endpoint
            cache_key = f"rate_limit:{client_ip}:{request.path}"
            
            # Get the list of request timestamps for this IP
            request_timestamps = cache.get(cache_key, [])
            now = time.time()
            
            # Remove timestamps older than 1 minute
            request_timestamps = [ts for ts in request_timestamps if now - ts < 60]
            
            # Check if request limit is exceeded
            if len(request_timestamps) >= requests_per_minute:
                response_data = {
                    "error": "Too many requests",
                    "message": f"Request limit of {requests_per_minute} per minute exceeded. Please try again later.",
                    "retry_after": "60 seconds"
                }
                return JsonResponse(response_data, status=429)
            
            # Add current timestamp and update cache
            request_timestamps.append(now)
            cache.set(cache_key, request_timestamps, timeout=60)
            
            # Process the request
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator 