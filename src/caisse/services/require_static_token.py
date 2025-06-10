from django.conf import settings
from django.http import JsonResponse


def require_static_token(view_func):
    def wrapper(request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        expected = f"Token {settings.AUTH_STATIC_TOKEN}"

        if auth_header != expected:
            return JsonResponse({'detail': 'Unauthorized'}, status=401)

        return view_func(request, *args, **kwargs)

    return wrapper