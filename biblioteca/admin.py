from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Libro, Author, Genero, Tenant, User

class TenantFilteredAdmin(admin.ModelAdmin):
    exclude = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant=request.user.tenant)

    def get_exclude(self, request, obj=None):
        exclude = list(self.exclude) if self.exclude else []
        if not request.user.is_superuser:
            exclude.append('tenant')
        return exclude

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)


admin.site.register(Tenant)

# Formulario personalizado para incluir el campo tenant
class UserChangeForm(BaseUserAdmin.form):
    class Meta(BaseUserAdmin.form.Meta):
        model = User
        fields = '__all__'

class CustomUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Tenant', {'fields': ('tenant',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Tenant', {'fields': ('tenant',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Author, TenantFilteredAdmin)
admin.site.register(Genero, TenantFilteredAdmin)
admin.site.register(Libro, TenantFilteredAdmin)

