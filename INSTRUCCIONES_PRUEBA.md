# Instrucciones para Probar el Sistema Multitenant

## 🚀 Pasos para Probar el Sistema

### 1. Preparar el Entorno

Asegúrate de tener el entorno virtual activado:

```bash
# En Windows
venv\Scripts\activate

# En Linux/Mac
source venv/bin/activate
```

### 2. Ejecutar las Migraciones

```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Ejecutar el Script de Prueba

```bash
python test_multitenant.py
```

Este script creará:
- 2 tenants (Empresa A y Empresa B)
- 1 superusuario (admin/admin123)
- 2 usuarios normales (usuario_a/password123, usuario_b/password123)
- Datos de prueba para cada tenant

### 4. Iniciar el Servidor

```bash
python manage.py runserver
```

### 5. Acceder al Admin

Ve a `http://localhost:8000/admin/` y loguéate con:
- **Superusuario**: `admin` / `admin123`
- **Usuario Empresa A**: `usuario_a` / `password123`
- **Usuario Empresa B**: `usuario_b` / `password123`

### 6. Probar el Filtrado por Tenant

#### En el Admin:
1. Logueate con `usuario_a`
2. Verifica que solo veas datos de "Empresa A"
3. Logueate con `usuario_b`
4. Verifica que solo veas datos de "Empresa B"
5. Logueate con `admin`
6. Verifica que veas datos de ambas empresas

#### En los Endpoints de Reportes:

##### Reportes JSON:
```bash
# Citas por terapeuta (requiere autenticación)
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/reports/appointments-per-therapist/?date=2024-01-15"

# Pacientes por terapeuta
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/reports/patients-by-therapist/?date=2024-01-15"

# Resumen de caja diaria
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/reports/daily-cash/?date=2024-01-15"

# Citas entre fechas
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/reports/appointments-between-dates/?start_date=2024-01-01&end_date=2024-01-31"
```

##### Exportación PDF:
```bash
# PDF de citas por terapeuta
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/exports/pdf/citas-terapeuta/?date=2024-01-15" \
     -o citas_terapeuta.pdf

# PDF de pacientes por terapeuta
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/exports/pdf/pacientes-terapeuta/?date=2024-01-15" \
     -o pacientes_terapeuta.pdf

# PDF de resumen de caja
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/exports/pdf/resumen-caja/?date=2024-01-15" \
     -o resumen_caja.pdf
```

##### Exportación Excel:
```bash
# Excel de citas entre fechas
curl -H "Cookie: sessionid=TU_SESSION_ID" \
     "http://localhost:8000/exports/excel/citas-rango/?start_date=2024-01-01&end_date=2024-01-31" \
     -o citas.xlsx
```

### 7. Verificar el Comportamiento

#### Para Usuarios Normales:
- Solo deben ver datos de su tenant
- No pueden acceder a datos de otros tenants
- Reciben error 403 si no tienen tenant asignado

#### Para Superusuarios:
- Ven todos los datos de todos los tenants
- No están limitados por filtros de tenant
- Pueden acceder a todos los endpoints

### 8. Casos de Prueba

#### Caso 1: Usuario sin autenticación
- Intentar acceder a cualquier endpoint
- Debe recibir error 401 (No autenticado)

#### Caso 2: Usuario sin tenant
- Crear un usuario sin asignar tenant
- Intentar acceder a endpoints
- Debe recibir error 403 (Sin tenant asignado)

#### Caso 3: Usuario con tenant
- Loguearse con usuario_a o usuario_b
- Verificar que solo vea datos de su empresa
- Verificar que los reportes estén filtrados correctamente

#### Caso 4: Superusuario
- Loguearse con admin
- Verificar que vea todos los datos
- Verificar que los reportes muestren datos de todas las empresas

### 9. Verificar en la Base de Datos

```sql
-- Verificar tenants
SELECT * FROM multitenant_tenant;

-- Verificar usuarios y sus tenants
SELECT u.username, u.is_superuser, t.name as tenant_name 
FROM multitenant_user u 
LEFT JOIN multitenant_tenant t ON u.tenant_id = t.id;

-- Verificar que los datos tengan tenant asignado
SELECT 'patients' as table_name, COUNT(*) as count, tenant_id 
FROM patients 
GROUP BY tenant_id
UNION ALL
SELECT 'therapists' as table_name, COUNT(*) as count, tenant_id 
FROM therapists 
GROUP BY tenant_id
UNION ALL
SELECT 'appointments' as table_name, COUNT(*) as count, tenant_id 
FROM appointments 
GROUP BY tenant_id;
```

### 10. Solución de Problemas

#### Error: "Usuario no autenticado"
- Verificar que el usuario esté logueado
- Verificar que la sesión sea válida

#### Error: "Usuario sin tenant asignado"
- Verificar que el usuario tenga un tenant asignado
- Verificar que el campo tenant no sea NULL

#### Los reportes no se filtran por tenant
- Verificar que el decorador `@require_tenant_access` esté aplicado
- Verificar que los servicios reciban el parámetro `user`
- Verificar que el método `_filter_by_tenant` esté funcionando

#### El admin no filtra por tenant
- Verificar que `TenantFilteredAdmin` esté configurado correctamente
- Verificar que los modelos tengan el campo `tenant`
- Verificar que las migraciones se hayan ejecutado

## 🎯 Resultado Esperado

Al final de las pruebas, deberías ver:

1. ✅ **Filtrado automático**: Cada usuario solo ve datos de su tenant
2. ✅ **Seguridad**: Endpoints protegidos y validados
3. ✅ **Admin funcional**: Filtrado automático en el admin de Django
4. ✅ **Reportes seguros**: Todos los reportes respetan la separación de tenants
5. ✅ **Superusuario sin límites**: Puede acceder a todos los datos

## 📝 Notas Importantes

- **Nunca** compartas las credenciales de prueba en producción
- Los datos de prueba se pueden eliminar después de las pruebas
- El sistema mantiene la compatibilidad con el código existente
- Todos los endpoints requieren autenticación
- El filtrado por tenant es automático y transparente
