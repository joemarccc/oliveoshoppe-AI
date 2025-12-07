import jwt
from django.http import JsonResponse
from django.conf import settings
from django.contrib.auth.models import User

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/protected/'):
            auth_header = request.headers.get('Authorization')
            if not auth_header or not auth_header.startswith('Bearer '):
                return JsonResponse({'error': 'Invalid or missing token'}, status=401)
            
            token = auth_header.split(' ')[1]
            try:
                payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
                user = User.objects.get(id=payload['user_id'])
                request.user = user
            except (jwt.InvalidTokenError, User.DoesNotExist):
                return JsonResponse({'error': 'Invalid token'}, status=401)
            
        response = self.get_response(request)
        return response 