from datetime import datetime
from django.utils.timezone import localtime
from django.db.models import Count, Q, Sum
from .models import Appointment, Therapist, Patient
from django.db import models

class ReportService:
    """Responsable exclusivamente de consultas de base de datos para reportes."""
    
    def _filter_by_tenant(self, queryset, user):
        """
        Filtra el queryset por tenant del usuario.
        - Si es superusuario, no filtra (ve todos los datos)
        - Si es usuario normal, solo ve datos de su tenant
        """
        if user.is_superuser:
            return queryset
        return queryset.filter(tenant=user.tenant)
    
    def get_appointments_count_by_therapist(self, validated_data, user):
        """Obtiene el conteo de citas por terapeuta para una fecha dada."""
        query_date = validated_data.get("date")
        
        # Filtrar terapeutas por tenant
        therapists_queryset = Therapist.objects
        therapists_queryset = self._filter_by_tenant(therapists_queryset, user)
        
        # Consultar terapeutas con la cantidad de citas
        therapists = (
            therapists_queryset
            .annotate(
                appointments_count=Count(
                    "appointment",
                    filter=Q(appointment__appointment_date=query_date)
                )
            )
            .filter(appointments_count__gt=0)
            .values("id", "first_name", "last_name_paternal", "last_name_maternal", "appointments_count")
        )
        
        # Sumar el total de citas
        total_appointments = sum(t["appointments_count"] for t in therapists)
        
        return {
            "therapists_appointments": list(therapists),
            "total_appointments_count": total_appointments
        }
    
    def get_patients_by_therapist(self, validated_data, user):
        """Obtiene pacientes agrupados por terapeuta para una fecha dada."""
        query_date = validated_data.get("date")
        
        # Filtrar citas por tenant
        appointments_queryset = Appointment.objects.select_related("patient", "therapist")
        appointments_queryset = self._filter_by_tenant(appointments_queryset, user)
        
        # Consultar citas para la fecha
        appointments = appointments_queryset.filter(
            appointment_date=query_date
        )
        
        # Procesar datos
        report = {}
        sin_terapeuta = {
            "therapist_id": "",
            "therapist": "Sin terapeuta asignado",
            "patients": {}
        }
        
        for appointment in appointments:
            patient = appointment.patient
            therapist = appointment.therapist
            
            if not patient:
                continue
            
            patient_data = {
                "patient_id": patient.id,
                "patient": f"{patient.paternal_lastname} {patient.maternal_lastname or ''} {patient.name}".strip(),
                "appointments": 1
            }
            
            if not therapist:
                # Paciente sin terapeuta
                key = patient.id
                if key not in sin_terapeuta["patients"]:
                    sin_terapeuta["patients"][key] = patient_data
                else:
                    sin_terapeuta["patients"][key]["appointments"] += 1
            else:
                # Paciente con terapeuta
                t_id = therapist.id
                if t_id not in report:
                    report[t_id] = {
                        "therapist_id": t_id,
                        "therapist": f"{therapist.last_name_paternal} {therapist.last_name_maternal or ''} {therapist.first_name}".strip(),
                        "patients": {}
                    }
                key = patient.id
                if key not in report[t_id]["patients"]:
                    report[t_id]["patients"][key] = patient_data
                else:
                    report[t_id]["patients"][key]["appointments"] += 1
        
        # Agregar pacientes sin terapeuta si existen
        if sin_terapeuta["patients"]:
            report["sinTherapist"] = sin_terapeuta
        
        # Convertir diccionarios a listas
        for therapist_id in report:
            report[therapist_id]["patients"] = list(report[therapist_id]["patients"].values())
        
        return list(report.values())
    
    def get_daily_cash(self, validated_data, user):
        """Obtiene el resumen diario de efectivo detallado por cita."""
        query_date = validated_data.get("date")
        
        # Filtrar pagos por tenant
        payments_queryset = Appointment.objects.filter(
            appointment_date=query_date,
            payment__isnull=False,
            payment_type__isnull=False
        )
        payments_queryset = self._filter_by_tenant(payments_queryset, user)
        
        # Consultar pagos del día
        payments = (
            payments_queryset
            .values(
                'id',
                'payment',
                'payment_type',
                'payment_type__name'
            )
            .order_by('-id')  # Ordenar por id descendente para tener las más recientes primero
        )
        
        # Formatear resultado
        result = [
            {
                "id_cita": p['id'],
                "payment": p['payment'],
                "payment_type": p['payment_type'],
                "payment_type_name": p['payment_type__name']
            }
            for p in payments
        ]
        
        return result
    
    def get_appointments_between_dates(self, validated_data, user):
        """Obtiene citas entre dos fechas dadas."""
        start_date = validated_data.get("start_date")
        end_date = validated_data.get("end_date")
        
        # Filtrar citas por tenant
        appointments_queryset = Appointment.objects.select_related("patient", "therapist")
        appointments_queryset = self._filter_by_tenant(appointments_queryset, user)
        
        # Consultar citas
        appointments = (
            appointments_queryset
            .filter(
                appointment_date__gte=start_date,
                appointment_date__lte=end_date
            )
            .order_by("appointment_date", "appointment_hour")
        )
        
        # Formatear resultado
        result = []
        for app in appointments:
            if not app.patient:
                continue
                
            patient_name = " ".join(filter(None, [
                app.patient.paternal_lastname,
                app.patient.maternal_lastname,
                app.patient.name
            ]))
            
            result.append({
                "appointment_id": app.id,
                "patient_id": app.patient.id,
                "document_number_patient": app.patient.document_number,
                "patient": patient_name,
                "primary_phone_patient": app.patient.primary_phone,
                "appointment_date": app.appointment_date.strftime("%Y-%m-%d"),
                "appointment_hour": app.appointment_hour if isinstance(app.appointment_hour, str) else app.appointment_hour.strftime("%H:%M")
            })
        
        return result