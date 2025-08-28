from django.contrib import admin
from .models import DocumentType, Patient, Therapist, PaymentType, Appointment

from biblioteca.admin import TenantFilteredAdmin

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

admin.site.register(DocumentType, TenantFilteredFKAdmin)
admin.site.register(Patient, TenantFilteredFKAdmin)
admin.site.register(Therapist, TenantFilteredFKAdmin)
admin.site.register(Appointment, TenantFilteredFKAdmin)
admin.site.register(PaymentType, TenantFilteredFKAdmin)
