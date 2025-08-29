#!/usr/bin/env python
"""
Script de prueba para el sistema multitenant de reportes
Ejecutar desde la raíz del proyecto Django
"""

import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth import get_user_model
from multitenant.models import Tenant
from reports.models import DocumentType, Patient, Therapist, PaymentType, Appointment
from reports.reports_services import ReportService

User = get_user_model()

def crear_datos_prueba():
    """Crea datos de prueba para el sistema multitenant"""
    print("🔧 Creando datos de prueba...")
    
    # Crear tenants
    tenant1, created = Tenant.objects.get_or_create(
        name="Empresa A",
        domain="empresa-a.com"
    )
    if created:
        print(f"✅ Tenant creado: {tenant1.name}")
    
    tenant2, created = Tenant.objects.get_or_create(
        name="Empresa B", 
        domain="empresa-b.com"
    )
    if created:
        print(f"✅ Tenant creado: {tenant2.name}")
    
    # Crear superusuario si no existe
    superuser, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@example.com',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        superuser.set_password('admin123')
        superuser.save()
        print("✅ Superusuario creado: admin/admin123")
    
    # Crear usuarios para cada tenant
    user1, created = User.objects.get_or_create(
        username='usuario_a',
        defaults={
            'email': 'usuario_a@empresa-a.com',
            'tenant': tenant1,
            'is_staff': True
        }
    )
    if created:
        user1.set_password('password123')
        user1.save()
        print(f"✅ Usuario creado: {user1.username} para {tenant1.name}")
    
    user2, created = User.objects.get_or_create(
        username='usuario_b',
        defaults={
            'email': 'usuario_b@empresa-b.com',
            'tenant': tenant2,
            'is_staff': True
        }
    )
    if created:
        user2.set_password('password123')
        user2.save()
        print(f"✅ Usuario creado: {user2.username} para {tenant2.name}")
    
    # Crear tipos de documento
    doc_type1, created = DocumentType.objects.get_or_create(
        name="DNI",
        tenant=tenant1
    )
    doc_type2, created = DocumentType.objects.get_or_create(
        name="DNI",
        tenant=tenant2
    )
    
    # Crear pacientes para tenant1
    patient1, created = Patient.objects.get_or_create(
        document_number="12345678",
        defaults={
            'tenant': tenant1,
            'paternal_lastname': 'García',
            'maternal_lastname': 'López',
            'name': 'Juan',
            'sex': 'M',
            'primary_phone': '123456789',
            'document_type': doc_type1
        }
    )
    if created:
        print(f"✅ Paciente creado: {patient1.get_full_name()} para {tenant1.name}")
    
    patient2, created = Patient.objects.get_or_create(
        document_number="87654321",
        defaults={
            'tenant': tenant1,
            'paternal_lastname': 'Martínez',
            'maternal_lastname': 'Rodríguez',
            'name': 'María',
            'sex': 'F',
            'primary_phone': '987654321',
            'document_type': doc_type1
        }
    )
    if created:
        print(f"✅ Paciente creado: {patient2.get_full_name()} para {tenant1.name}")
    
    # Crear pacientes para tenant2
    patient3, created = Patient.objects.get_or_create(
        document_number="11111111",
        defaults={
            'tenant': tenant2,
            'paternal_lastname': 'Pérez',
            'maternal_lastname': 'González',
            'name': 'Carlos',
            'sex': 'M',
            'primary_phone': '111111111',
            'document_type': doc_type2
        }
    )
    if created:
        print(f"✅ Paciente creado: {patient3.get_full_name()} para {tenant2.name}")
    
    # Crear terapeutas
    therapist1, created = Therapist.objects.get_or_create(
        document_number="T001",
        defaults={
            'tenant': tenant1,
            'last_name_paternal': 'Hernández',
            'last_name_maternal': 'Díaz',
            'first_name': 'Ana',
            'gender': 'F',
            'phone': '555555555',
            'email': 'ana@empresa-a.com',
            'document_type': doc_type1
        }
    )
    if created:
        print(f"✅ Terapeuta creado: {therapist1.get_full_name()} para {tenant1.name}")
    
    therapist2, created = Therapist.objects.get_or_create(
        document_number="T002",
        defaults={
            'tenant': tenant2,
            'last_name_paternal': 'Sánchez',
            'last_name_maternal': 'Fernández',
            'first_name': 'Luis',
            'gender': 'M',
            'phone': '666666666',
            'email': 'luis@empresa-b.com',
            'document_type': doc_type2
        }
    )
    if created:
        print(f"✅ Terapeuta creado: {therapist2.get_full_name()} para {tenant2.name}")
    
    # Crear tipos de pago
    payment_type1, created = PaymentType.objects.get_or_create(
        name="Efectivo",
        tenant=tenant1
    )
    payment_type2, created = PaymentType.objects.get_or_create(
        name="Efectivo",
        tenant=tenant2
    )
    
    # Crear citas
    today = date.today()
    
    appointment1, created = Appointment.objects.get_or_create(
        patient=patient1,
        therapist=therapist1,
        appointment_date=today,
        appointment_hour='09:00:00',
        defaults={
            'tenant': tenant1,
            'payment': 50.00,
            'payment_type': payment_type1
        }
    )
    if created:
        print(f"✅ Cita creada para {patient1.get_full_name()} con {therapist1.get_full_name()}")
    
    appointment2, created = Appointment.objects.get_or_create(
        patient=patient2,
        therapist=therapist1,
        appointment_date=today,
        appointment_hour='10:00:00',
        defaults={
            'tenant': tenant1,
            'payment': 60.00,
            'payment_type': payment_type1
        }
    )
    if created:
        print(f"✅ Cita creada para {patient2.get_full_name()} con {therapist1.get_full_name()}")
    
    appointment3, created = Appointment.objects.get_or_create(
        patient=patient3,
        therapist=therapist2,
        appointment_date=today,
        appointment_hour='11:00:00',
        defaults={
            'tenant': tenant2,
            'payment': 70.00,
            'payment_type': payment_type2
        }
    )
    if created:
        print(f"✅ Cita creada para {patient3.get_full_name()} con {therapist2.get_full_name()}")
    
    print("✅ Datos de prueba creados exitosamente!")
    return {
        'tenant1': tenant1,
        'tenant2': tenant2,
        'user1': user1,
        'user2': user2,
        'superuser': superuser
    }

def probar_filtrado_tenant():
    """Prueba el filtrado por tenant en los reportes"""
    print("\n🧪 Probando filtrado por tenant...")
    
    report_service = ReportService()
    today = date.today()
    
    # Datos de prueba
    test_data = {'date': today}
    
    # Probar con superusuario (debe ver todos los datos)
    print("\n👑 Probando con superusuario...")
    try:
        data = report_service.get_appointments_count_by_therapist(test_data, User.objects.get(username='admin'))
        print(f"   Citas por terapeuta: {data['total_appointments_count']} citas totales")
        print(f"   Terapeutas con citas: {len(data['therapists_appointments'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Probar con usuario de tenant1
    print("\n👤 Probando con usuario de Empresa A...")
    try:
        data = report_service.get_appointments_count_by_therapist(test_data, User.objects.get(username='usuario_a'))
        print(f"   Citas por terapeuta: {data['total_appointments_count']} citas totales")
        print(f"   Terapeutas con citas: {len(data['therapists_appointments'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Probar con usuario de tenant2
    print("\n👤 Probando con usuario de Empresa B...")
    try:
        data = report_service.get_appointments_count_by_therapist(test_data, User.objects.get(username='usuario_b'))
        print(f"   Citas por terapeuta: {data['total_appointments_count']} citas totales")
        print(f"   Terapeutas con citas: {len(data['therapists_appointments'])}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

def mostrar_resumen():
    """Muestra un resumen de los datos creados"""
    print("\n📊 Resumen de datos creados:")
    
    print(f"\n🏢 Tenants:")
    for tenant in Tenant.objects.all():
        print(f"   - {tenant.name} ({tenant.domain})")
    
    print(f"\n👥 Usuarios:")
    for user in User.objects.all():
        tenant_name = user.tenant.name if user.tenant else "Sin tenant"
        superuser_text = " (Superusuario)" if user.is_superuser else ""
        print(f"   - {user.username} -> {tenant_name}{superuser_text}")
    
    print(f"\n👨‍⚕️ Terapeutas:")
    for therapist in Therapist.objects.all():
        print(f"   - {therapist.get_full_name()} -> {therapist.tenant.name}")
    
    print(f"\n👤 Pacientes:")
    for patient in Patient.objects.all():
        print(f"   - {patient.get_full_name()} -> {patient.tenant.name}")
    
    print(f"\n📅 Citas:")
    for appointment in Appointment.objects.all():
        print(f"   - {appointment.patient.get_full_name()} con {appointment.therapist.get_full_name()} -> {appointment.tenant.name}")

if __name__ == "__main__":
    print("🚀 Iniciando pruebas del sistema multitenant...")
    
    try:
        # Crear datos de prueba
        datos = crear_datos_prueba()
        
        # Mostrar resumen
        mostrar_resumen()
        
        # Probar filtrado por tenant
        probar_filtrado_tenant()
        
        print("\n✅ Todas las pruebas completadas exitosamente!")
        print("\n🔑 Credenciales de acceso:")
        print("   Superusuario: admin / admin123")
        print("   Usuario Empresa A: usuario_a / password123")
        print("   Usuario Empresa B: usuario_b / password123")
        
    except Exception as e:
        print(f"\n❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()
