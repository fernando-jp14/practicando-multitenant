from django.contrib import admin
from .models import DocumentType, Patient, Therapist, PaymentType, Appointment
from multitenant.admin import TenantFilteredAdmin

class TenantFilteredFKAdmin(TenantFilteredAdmin):
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Si el usuario no es superusuario, filtra los ForeignKey por tenant
        if not request.user.is_superuser and hasattr(request.user, 'tenant') and request.user.tenant:
            # Ajusta los nombres de los campos según tus modelos
            if db_field.name in ['patient', 'therapist', 'document_type', 'payment_type']:
                model = db_field.related_model
                if hasattr(model, 'tenant'):
                    kwargs['queryset'] = model.objects.filter(tenant=request.user.tenant)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

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

# Registrar modelos con el admin filtrado por tenant
admin.site.register(DocumentType, TenantFilteredFKAdmin)
admin.site.register(Patient, TenantFilteredFKAdmin)
admin.site.register(Therapist, TenantFilteredFKAdmin)
admin.site.register(Appointment, TenantFilteredFKAdmin)
admin.site.register(PaymentType, TenantFilteredFKAdmin)
