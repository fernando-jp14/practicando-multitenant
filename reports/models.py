from django.db import models
from django.utils import timezone
from multitenant.models import Tenant
#===============tipo de documento================
class DocumentType(models.Model):
    name = models.CharField(max_length=255)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "document_types"

#===============pacientes================
class Patient(models.Model):
    # Información personal
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    document_number = models.CharField(max_length=20, unique=True)
    paternal_lastname = models.CharField(max_length=100)
    maternal_lastname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    sex = models.CharField(max_length=10, choices=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro')
    ])
    primary_phone = models.CharField(max_length=15)
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'patients'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ['-created_at']
    
    def get_full_name(self):
        """Obtiene el nombre completo del paciente."""
        return f"{self.name} {self.paternal_lastname} {self.maternal_lastname}"
    
    def __str__(self):
        return self.get_full_name()

#=================terapeutas=================================
class Therapist(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    GENDERS = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]

    # Datos personales
    document_type = models.ForeignKey(DocumentType, on_delete=models.PROTECT)
    document_number = models.CharField(max_length=20, unique=True)
    last_name_paternal = models.CharField(max_length=100)
    last_name_maternal = models.CharField(max_length=100, blank=True, null=True)
    first_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=1, choices=GENDERS)

    # Información de contacto
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)


    def get_full_name(self):
        """Obtiene el nombre completo del terapeuta."""
        return f"{self.first_name} {self.last_name_paternal} {self.last_name_maternal or ''}"
    
    def __str__(self):
        return self.get_full_name()

#===============tipos de pago================
class PaymentType(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        db_table = "payment_types"

#===============citas================
class Appointment(models.Model):
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE, null=True, blank=True)
    
    # Relaciones con otros módulos
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Paciente")
    therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, verbose_name="Terapeuta")

    # Campos principales de la cita
    appointment_date = models.DateField(verbose_name="Fecha de la cita")
    appointment_hour = models.TimeField(verbose_name="Hora de la cita")
    
    # Fechas de tratamiento
    initial_date = models.DateField(blank=True, null=True, verbose_name="Fecha inicial")
    final_date = models.DateField(blank=True, null=True, verbose_name="Fecha final")
    
    # Configuración de la cita
    appointment_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de cita")
    payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Pago")

    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo de pago")

    # Campos de auditoría
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")
    
    class Meta:
        db_table = 'appointments'
        verbose_name = "Cita"
        verbose_name_plural = "Citas"
        ordering = ['-appointment_date', '-appointment_hour']
        indexes = [
            models.Index(fields=['appointment_date', 'appointment_hour']),
        ]
    
    def __str__(self):
        return f"Cita - {self.appointment_date} {self.appointment_hour}"
    
    @property
    def is_completed(self):
        """Verifica si la cita está completada basándose en la fecha"""
        if self.appointment_date is None:
            return False  # Si no hay fecha, consideramos que la cita no está completada
        return self.appointment_date < timezone.now().date()



