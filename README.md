# Rentilo

Plataforma inicial para administrar alquileres y directorios inmobiliarios.

## Funcionalidades incluidas
- Inicio de sesión y panel de gestión.
- Directorio de inmuebles con filtros por tipo y estado.
- Registro y consulta de inquilinos y propietarios.
- Seguimiento de contratos, vencimientos, cobros y mantenimiento.
- Indicadores de ocupación y pagos pendientes.

La selección refleja capacidades habituales en plataformas de gestión inmobiliaria (PMS): inventario, contratos, portal/comunicación con inquilinos, pagos, mantenimiento y reportes. La consulta web en esta sesión no estuvo disponible; no se presenta como benchmarking verificado de proveedores concretos.

## Stack
- Python 3.11.8 / FastAPI
- Angular 19 / Tailwind CSS
- PostgreSQL 17 en localhost:15432

## Inicio local
1. Configurar `backend/.env` a partir de `backend/.env.example` y crear la base `rentilo`.
2. Instalar `backend/requirements.txt` en Python 3.11.8 y ejecutar `python run.py` desde `backend`.
3. `npm install` y `npm start` desde `frontend`.

La base de datos y la clave se configuran por entorno; no deben incluirse secretos en el cliente ni en el repositorio.
