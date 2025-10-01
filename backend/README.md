# Backend

```bash
# Instalar uv
# -------------------------------------------------------
# https://docs.astral.sh/uv/getting#started/installation/
# -------------------------------------------------------

# Clonar repo
git clone https://github.com/jp-zuniga/NutriPlan

# Navegar al backend
cd NutriPlan
git switch backend-dev
cd backend

# Crear ambiente virtual e instalar dependencias
uv sync

# Navegar a folder de proyecto
cd src

#################################
### Comandos de Django con uv ###
#################################

# Correr servidor
uv run manage.py runserver

# Crear migraciones de DB
uv run manage.py makemigrations

# Aplicar migraciones a DB
uv run manage.py migrate
```
