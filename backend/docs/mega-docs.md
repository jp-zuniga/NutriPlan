<div align="center">
  <img src="./logo.png" size=600x600 alt="Logo de NutriPlan."/>
</div>

<div align="right">
  <a>16 de octubre de 2025.</a>
</div>

---

# Documentación

## Resumen Técnico

NutriPlan es la plataforma que personaliza al 100% tu alimentación: recomenda planes y recetas a tu medida según objetivos, condiciones, restricciones de salud, tipo de dieta, tiempo disponible e inventario real de tu cocina. Nuestra diferencia clave es la integración exclusiva de ingredientes y recetas nicaragüenses, respetando sabores y técnicas locales para que comás variado, saludable y accesible con lo que se consigue aquí. Todo en una interfaz simple, con criterios nutricionales claros y ajustes dinámicos según tu avance y feedback. En pocas palabras: personalización total con identidad nica.

---

## Tech Stack

- **Frontend**: SvelteKit y Node.js.
- **Backend**: Django + REST API (Django REST Framework).
- **Base de Datos**: PostgreSQL.

---

## Despliegue

Estamos utilizando la plataforma [`Railway`](https://railway.com) para desplegar todos los componentes de NutriPlan.

- Frontend: [`https://nutri-plan.net`](https://nutri-plan.net)
- Backend: [`https://api.nutri-plan.net`](https://api.nutri-plan.net)

### Backend

Tenemos un ambiente dedicado solamente al backend, donde tenemos un deploy para testing y un deploy de producción. El testing es donde ocurre todo el desarrollo, y cuando las nuevas funcionalidades están listas, se pasan a producción donde el usuario las puede visualizar. Adicionalmente, implementamos pruebas unitarias automatizadas utilizando Github Actions, de tal manera que cada vez que subimos un cambio, las pruebas se ejecutan, y solamente se crea un nuevo deploy si las pruebas fueron exitosas. Esto nos permite mantener un control de calidad sobre lo que exponemos a los usuarios,  y asegurarnos de que cualquier error fatal no sea permanente. En este mismo ambiente, tenemos desplegada nuestra base de datos (PostgreSQL), la cual se respalda automáticamente cada 24 horas.

### Frontend

Adicionalmente tenemos un ambiente para el frontend, donde tenemos la misma separación entre deploys de desarrollo y deploys de producción.

---

## Arquitectura e Infraestructura

### Estructura de Carpetas

```dir
backend/
├─ src/
│   ├─ backend/
│   └─ nutriplan/
│      ├─ admin/
│      ├─ models/
│      ├─ serializers/
│      ├─ services/
│      │  └─ auth/
│      ├─ tests/
│      └─ views/
│         ├─ auth/
│         └─ permissions/
│
└── frontend/
    ├── src/
    │   ├── lib/
    │   │   ├── components/
    │   │   │   ├── forms/
    │   │   │   └── welcome/
    │   │   ├── stores/
    │   │   └── utils/
    │   └── routes/
    │       ├── acerca/
    │       ├── api/
    │       │   ├── login/
    │       │   ├── logout/
    │       │   ├── rate/
    │       │   └── register/
    │       ├── chef-ia/
    │       ├── helloworld/
    │       ├── login/
    │       ├── perfil/
    │       ├── planes/
    │       ├── planificador-ia/
    │       ├── receta-rapida/
    │       ├── recetas/
    │       │   └── [slug]/
    │       └── signup/
    └── static/
        └── styles/
```

### Modelo ORM

Todas las entidades heredan de un `BaseModel` con UUID como PK, lo que simplifica referencias entre tablas y evita colisiones. El usuario (`CustomUser`) elimina `username` y autentica únicamente por email con unicidad case-insensitive. Ingredientes modelan macros por 100 g con *check constraints* para valores no negativos y usan índices GIN trigram (`pg_trgm`) sobre `name` y `description` para búsqueda tolerante/autocompletado; categorías también indexan por trigram en `friendly_name`. Las recetas emplean `slug` único (case-insensitive) e índices específicos, relaciones M2M con categorías e ingredientes (a través de `RecipeIngredient`, que almacena cantidad/unidad con unicidad por receta/ingrediente) y un M2M ordenado con imágenes; además usan `GeneratedField` en base de datos para `total_time` y `total_calories`, permitiendo ordenar y filtrar sin recomputar en la aplicación. Colecciones de usuario aseguran unicidad por dueño en `name` y `slug` (case-insensitive) y mantienen orden explícito de ítems; las reseñas imponen una por usuario/receta con rating validado 1–5 e índices en rating y fechas. OAuth social (Google) se liga por `(provider, provider_user_id)` y restringe el proveedor mediante `choices`.

### Microservicios

La capa de API usa DRF con viewsets enfocados y *prefetching* coherente para evitar N+1 (ingredientes a través de la tabla intermedia, imágenes ordenadas, categorías). El `RecipeViewSet` expone búsqueda por nombre/descripcion, filtros por categorías (IDs o nombres/friendly), tiempo máximo y *include/exclude* de ingredientes por UUID (con *match-all* al incluir); anota `rating_avg` y `rating_count` para ordenamientos y ofrece acciones para listar y crear reseñas. Ingredientes y categorías son *read-only*; colecciones ofrecen CRUD más acciones para agregar/quitar/reordenar recetas (y búsqueda por `slug`), y usuarios exponen `me` (GET/PUT/PATCH) y cambio de contraseña. La seguridad se centra en JWT (Simple JWT) servidos en **cookies HTTPOnly** (`np-access` ~60 min y `np-refresh` ~1 día) mediante `CookieJWTAuthentication` que lee el acceso desde cookie (el header Bearer está comentado por defecto); CORS/CSRF están configurados para `localhost:5173` y dominios `nutri-plan.net`/`railway.app`. El *sign-in* con Google valida estrictamente `aud`, `iss` y email verificado antes de crear o vincular cuentas, y el *exception handler* garantiza respuestas de error consistentes. La capa de servicios encapsula la lógica de dominio (`RecipeService`, `UserService`) y la integración con Gemini para *seeders* controlados: un cliente (`GeminiClient`), *prompts* acotados a lo existente (listas permitidas) y *seeders* robustos con manejo de errores, expuestos vía el comando `populate` con `--dry-run`.

Hoy operamos como monolito modular por costo/beneficio: latencia baja, simplicidad operativa y un dominio bien encapsulado que permite extraer piezas si el tráfico o la latencia lo exigen. Candidatos naturales a externalizar en el futuro incluyen la generación LLM (como `worker/batch` con cola), recomendaciones pesadas si evolucionan a modelos específicos, y el asistente `Chefcito` si requiere *streaming*, herramientas externas o orquestación independiente. Mientras tanto, el diseño en capas y los límites de módulo ya trazados facilitan una transición selectiva sin rehacer el dominio.

---

## Guía de Instalación

Debido a que NutriPlan es un sitio web, no se necesita instalar. Nuestros usuarios solamente necesitan un navegador web para utilizar NutriPlan, desde cualquier dispositivo o plataforma compatible con un navegador moderno (Chrome, Firefox, Edge, etc.).

## Guía de Ejecución Local

### [Backend – Django API](./backend-guia-local.md)

### [Frontend – Svelte Site](./backend-guia-local.md)
