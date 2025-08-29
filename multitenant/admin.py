from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Tenant, User

class TenantFilteredAdmin(admin.ModelAdmin):
    # Lista de campos a excluir del formulario del admin
    exclude = []

    def get_queryset(self, request):
        """
        Filtra los objetos mostrados en el admin según el tenant del usuario logueado.
        - Si es superusuario, ve todos los objetos.
        - Si es usuario normal, solo ve los objetos de su tenant.
        """
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(tenant=request.user.tenant)

    def get_exclude(self, request, obj=None):
        """
        Oculta el campo 'tenant' en el formulario del admin para usuarios normales.
        Solo el superusuario puede ver y editar el campo 'tenant'.
        """
        exclude = list(self.exclude) if self.exclude else []
        if not request.user.is_superuser:
            exclude.append('tenant')
        return exclude

    def save_model(self, request, obj, form, change):
        """
        Asigna automáticamente el tenant del usuario logueado al guardar el objeto,
        solo si no es superusuario. Así se evita que un usuario asigne objetos a otro tenant.
        """
        if not request.user.is_superuser:
            obj.tenant = request.user.tenant
        super().save_model(request, obj, form, change)


admin.site.register(Tenant)

#  para incluir el campo tenant
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


