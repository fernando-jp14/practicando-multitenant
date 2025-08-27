from django.contrib import admin
from .models import Libro, Author, Genero, Tenant, User

class LibroAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # ve todo
        return qs.filter(tenant=request.user.tenant)

admin.site.register(Tenant)
admin.site.register(User)
admin.site.register(Author)
admin.site.register(Genero)
admin.site.register(Libro, LibroAdmin)

