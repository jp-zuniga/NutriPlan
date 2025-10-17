# Ejecución Local de Backend

## Requisitos

- Git
- PostgreSQL (v16+)

---

## Instalar `uv`

### macOS / Linux

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# luego reabrí tu terminal
uv --version
```

### Windows (PowerShell)

```powershell
irm https://astral.sh/uv/install.ps1 | iex
uv --version
```

---

## Clonar repositorio

```bash
git clone https://github.com/jp-zuniga/NutriPlan.git
cd NutriPlan
git switch backend-dev
cd backend
```

## Sincronizar ambiente

Este comando instala todas las dependencias (incluyendo las de desarrollo) y crea un ambiente virtual con ellas. Si no tienes la versión de Python necesaria para NutriPlan (3.13.5), `uv` la instalará automáticamente a la hora de crear el ambiente virtual.

```bash
NutriPlan/backend $  uv sync --all-groups
```

De ahora en adelante, aseguráte de ejecutar todos los comandos de Python con `uv run`, para que siempre se utilize el ambiente virtual creado por `uv`.

---

## Configurar `.env`

El proyecto **exige** estas variables o fallará al iniciar.

Creá `backend/.env` con algo así:

```dotenv
# DB
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/nutriplan
TESTING_DATABASE_URL=postgresql://postgres:postgres@localhost:5433/nutriplan_test

# Django
SECRET_KEY=llave-muy-muy-secreta
DEBUG=True

# Google / Gemini
GOOGLE_API_KEY=tu-api-key
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-google-client-secret
```

> `settings.py` carga `.env` con `python-dotenv` automáticamente.

---

## Crear DB

Si no tenés PostgreSQL instalado, ejemplo rápido con Docker:

```bash
# Base para app
$ docker run --name np-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d postgres:15

# Base para pruebas unitarias (opcional)
$ docker run --name np-pg-test -e POSTGRES_PASSWORD=postgres -p 5433:5432 -d postgres:15
```

Ahora, crea las bases de datos si no existen:

```bash
# crear DBs si no existen
$ createdb -h localhost -p 5432 -U postgres nutriplan
$ createdb -h localhost -p 5433 -U postgres nutriplan_test
```

## Migrar DB

```bash
# crear tablas
NutriPlan/backend/src $ uv run manage.py makemigrations nutriplan
NutriPlan/backend/src $ uv run manage.py migrate
```

---

## Creación de Admin

```bash
# crear superusuario
NutriPlan/backend/src $ uv run manage.py createsuperuser
```

## Ejecutar Servidor de Desarrollo

```bash
NutriPlan/backend/src $ uv run manage.py runserver
```

---
