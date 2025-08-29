from functools import wraps
from django.http import JsonResponse

def require_tenant_access(view_func):
    """
    Decorador que verifica que el usuario esté autenticado y tenga acceso al tenant.
    - Superusuarios pueden acceder a todo
    - Usuarios normales deben tener tenant asignado
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Usuario no autenticado'}, status=401)
        
        # Superusuarios pueden acceder a todo
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        
        # Usuarios normales deben tener tenant asignado
        if not hasattr(request.user, 'tenant') or not request.user.tenant:
            return JsonResponse({'error': 'Usuario sin tenant asignado'}, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper
