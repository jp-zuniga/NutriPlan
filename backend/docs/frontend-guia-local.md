# Ejecución Local de Frontend

## Requisitos

- Git
- Node.js (22+)
- `npm` (10+)
- [Django API](./backend-guia-local.md) corriendo localmente

---

## Instalar Node.js

### macOS / Linux (con nvm)

```bash
# instalar nvm si no lo tenés
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash

# reiniciá la terminal y luego:
nvm install --lts
nvm use --lts
node -v
npm -v
```

### Windows

Usá el **Node.js LTS** desde [nodejs.org](nodejs.org) o [`nvm-windows`](https://github.com/coreybutler/nvm-windows).

Verifica la instalación:

```powershell
node -v
npm -v
```

---

## Clonar repositorio

```bash
git clone https://github.com/jp-zuniga/NutriPlan.git
cd NutriPlan
git switch frontend-dev
cd frontend
```

## Instalar dependencias

```bash
NutriPlan/frontend $ npm install
```

---

## Configurar `.env`

```dotenv
# Apuntar al backend local
PUBLIC_API_URL=http://localhost:<port>

# Google / Gemini
GOOGLE_API_KEY=tu-api-key
GOOGLE_CLIENT_ID=tu-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=tu-google-client-secret
```

---

## Levantar servidor de desarrollo

```bash
npm run dev
# o a veces:
# npm run dev -- --open
```

---
