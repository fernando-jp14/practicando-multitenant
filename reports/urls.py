from django.urls import path, include
from .views import ReportView
from . import views

urlpatterns = [
    path('reportes/', ReportView.as_view(), name='reportes'),
]

reports_urlpatterns = [
    path('reports/appointments-per-therapist/', views.get_number_appointments_per_therapist, name='appointments_per_therapist'),
    path('reports/patients-by-therapist/', views.get_patients_by_therapist, name='patients_by_therapist'),
    path('reports/daily-cash/', views.get_daily_cash, name='daily_cash'),
    path('reports/appointments-between-dates/', views.get_appointments_between_dates, name='appointments_between_dates'),
]

export_urlpatterns = [
    path('exports/pdf/citas-terapeuta/', views.pdf_citas_terapeuta, name='pdf_citas_terapeuta'),#listo
    path('exports/pdf/pacientes-terapeuta/', views.pdf_pacientes_terapeuta, name='pdf_pacientes_terapeuta'),#listo
    path('exports/pdf/resumen-caja/', views.pdf_resumen_caja, name='pdf_resumen_caja'),
    path('exports/excel/citas-rango/', views.exportar_excel_citas, name='exportar_excel_citas'),#listo
]

views_urlpatterns = [
    path('reports/', views.reports_dashboard, name='reports'),
]

urlpatterns.extend(reports_urlpatterns)
urlpatterns.extend(export_urlpatterns)
urlpatterns.extend(views_urlpatterns)