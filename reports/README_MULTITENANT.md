# Sistema Multitenant para Reportes

## Descripción

Este sistema implementa un filtrado automático por tenant para todos los reportes, asegurando que cada usuario solo vea los datos de su empresa/organización.

## Funcionamiento

### 1. Filtrado Automático por Tenant

- **Superusuarios**: Pueden ver todos los datos de todos los tenants
- **Usuarios normales**: Solo ven datos de su tenant asignado

### 2. Implementación en Servicios

Todos los métodos en `ReportService` ahora incluyen filtrado por tenant:

```python
def _filter_by_tenant(self, queryset, user):
    """
    Filtra el queryset por tenant del usuario.
    - Si es superusuario, no filtra (ve todos los datos)
    - Si es usuario normal, solo ve datos de su tenant
    """
    if user.is_superuser:
        return queryset
    return queryset.filter(tenant=user.tenant)
```

### 3. Seguridad en Vistas

Todas las vistas están protegidas con el decorador `@require_tenant_access` que:

- Verifica que el usuario esté autenticado
- Permite acceso total a superusuarios
- Verifica que usuarios normales tengan tenant asignado
- Retorna errores apropiados (401, 403) si no se cumplen las condiciones

### 4. Endpoints Protegidos

Los siguientes endpoints ahora están protegidos y filtrados por tenant:

#### Reportes JSON:
- `GET /reports/appointments-per-therapist/` - Citas por terapeuta
- `GET /reports/patients-by-therapist/` - Pacientes por terapeuta  
- `GET /reports/daily-cash/` - Resumen de caja diaria
- `GET /reports/appointments-between-dates/` - Citas entre fechas

#### Exportación PDF:
- `GET /exports/pdf/citas-terapeuta/` - PDF de citas por terapeuta
- `GET /exports/pdf/pacientes-terapeuta/` - PDF de pacientes por terapeuta
- `GET /exports/pdf/resumen-caja/` - PDF de resumen de caja

#### Exportación Excel:
- `GET /exports/excel/citas-rango/` - Excel de citas entre fechas

## Uso

### Para Usuarios Normales

1. Deben estar logueados en el sistema
2. Deben tener un tenant asignado
3. Solo verán datos de su empresa

### Para Superusuarios

1. Pueden acceder a todos los endpoints
2. Ven datos de todos los tenants
3. No están limitados por filtros de tenant

## Estructura de Archivos

```
reports/
├── decorators.py          # Decorador de seguridad multitenant
├── models.py             # Modelos con campo tenant
├── reports_services.py   # Servicios con filtrado por tenant
├── views.py              # Vistas protegidas con decoradores
├── admin.py              # Admin configurado para multitenant
└── urls.py               # URLs de los endpoints
```

## Ejemplo de Respuesta de Error

Si un usuario no autenticado o sin tenant intenta acceder:

```json
{
    "error": "Usuario no autenticado"
}
```

```json
{
    "error": "Usuario sin tenant asignado"
}
```

## Configuración del Admin

El admin ya está configurado para filtrar por tenant usando `TenantFilteredAdmin`:

- Usuarios normales solo ven objetos de su tenant
- Superusuarios ven todos los objetos
- El campo tenant se oculta automáticamente para usuarios normales
- Se asigna automáticamente el tenant del usuario al crear/editar objetos

## Notas Importantes

1. **Autenticación requerida**: Todos los endpoints requieren que el usuario esté logueado
2. **Filtrado automático**: No es necesario pasar parámetros de tenant manualmente
3. **Compatibilidad**: El sistema mantiene la compatibilidad con el código existente
4. **Seguridad**: Implementa múltiples capas de seguridad para proteger los datos

## Pruebas

Para probar el sistema:

1. Crear usuarios con diferentes tenants
2. Loguearse con cada usuario
3. Verificar que solo vean datos de su tenant
4. Verificar que superusuarios vean todos los datos
5. Probar todos los endpoints con diferentes usuarios
