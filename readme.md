# 🏥 Proyecto Multitenancy – Módulo 8: Reportes

Este repositorio forma parte del ejercicio **Practicando Multitenancy**.  
El objetivo del **Módulo 8** es implementar **reportes filtrados por tenant** (ej: Clínica A y Clínica B), asegurando el aislamiento de datos entre diferentes organizaciones.

---

## 📌 Objetivo del módulo
- Generar reportes que muestren información solo del tenant activo.
- Validar que los datos de una clínica no se mezclen con los de otra.
- Ejemplos de reportes:
  - Pacientes por clínica
  - Citas por clínica
  - Diagnósticos por clínica

------

## ⚙️ Instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/usuario/practicando-multitenant.git
   cd practicando-multitenant
---------------
## Crear y activar entorno virtual:
-  python -m venv venv
-  venv\Scripts\activate
## Instalar dependencias:
-  pip install -r requirements.txt
## Aplicar migraciones:
-  python manage.py createsuperuser
## Levantar el servidor:
-  python manage.py runserver

------------
🧪 Pruebas del módulo

Registro de tenants (Clínica A y Clínica B).

-  Crear al menos 2 tenants en el sistema.

-  Generación de datos de prueba.

-  Registrar pacientes, citas y terapeutas en cada tenant.

-  Validación de aislamiento en reportes.

-  Generar un reporte PDF o listado en Django Admin.

Verificar que:

-  Clínica A solo muestra sus pacientes, citas y diagnósticos.

-  Clínica B solo muestra su propia información.

-  No existe cruce de datos entre clínicas.
-----------
