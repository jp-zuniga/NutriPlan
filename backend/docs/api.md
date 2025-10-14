# NutriPlan API

Esta guía documenta todos los endpoints existentes del backend actual, su forma de uso, parámetros, cuerpos de petición y respuestas de ejemplo.

---

## Tabla de Contenidos

1. [Convenciones Generales](#convenciones-generales)
2. [Autenticación (`/auth`)](#autenticación)
3. [Usuarios (`/users`)](#usuarios-users)
4. [Categorías (`/categories`)](#categorías-categories)
5. [Ingredientes (`/ingredients`)](#ingredientes-ingredients)
6. [Recetas (`/recipes`)](#recetas-recipes)
7. [Colecciones de Recetas (`/collections`)](#colecciones-de-recetas-collections)
8. [Ejemplos con curl](#ejemplos-con-curl)
---

## Convenciones Generales

- Base URL: `https://api.nutri-plan.net/`
- El router está configurado con `trailing_slash=r"/?"`.
  - Todos los endpoints del router aceptan con o sin slash al final.
  - Ej.: `GET /recipes` y `GET /recipes/` son válidos.
- Formato por defecto: `application/json`.
- Autenticación: **JWT (SimpleJWT)**.
  - Se debe enviar el encabezado `Authorization: Bearer <access-token>` para endpoints protegidos.
- Los errores de validación llegan como JSON con detalles por campo cuando aplica.

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---

## Autenticación (`/auth`)

### POST `/auth/register` — Registrar usuario

**Auth:** Pública
**Body (JSON):**
```json
{
  "full_name": "Ada Lovelace",
  "email": "ada@example.com",
  "phone_number": "+541100000000",
  "password": "supersegura123",
  "password_confirm": "supersegura123"
}
```

- Validaciones notables:
  - `email` único (case-insensitive).
  - `phone_number` opcional.
  - `password` validada con validadores de Django (mínimo 8).
  - `password_confirm` debe coincidir.

**Respuestas**

- `201 Created`
```json
{
  "user": {
    "id": 42,
    "email": "ada@example.com",
    "first_name": "Ada",
    "last_name": "Lovelace",
    "phone_number": "+541100000000",
    "dietary_restrictions": []
  },
  "refresh": "<refresh.jwt>",
  "access": "<access.jwt>"
}
```

- `400 Bad Request` (ejemplos)
```json
{ "password_confirm": "Las contraseñas no coinciden." }
```
```json
{ "email": "Este correo ya está registrado." }
```
```json
{ "password": ["Esta contraseña es demasiado corta.", "..."] }
```

---

### POST `/auth/login` — Iniciar sesión

**Auth:** Pública
**Body (JSON):**
```json
{ "email": "ada@example.com", "password": "supersegura123" }
```

**Respuestas**

- `200 OK`
```json
{
  "user": {
    "id": 42,
    "email": "ada@example.com",
    "first_name": "Ada",
    "last_name": "Lovelace",
    "phone_number": "+541100000000",
    "dietary_restrictions": []
  },
  "refresh": "<refresh.jwt>",
  "access": "<access.jwt>"
}
```
- `400 Bad Request`
```json
{ "error": "Email y contraseña son requeridos." }
```
- `401 Unauthorized`
```json
{ "error": "Credenciales inválidas." }
```

---

### POST `/auth/refresh` — Renovar Access Token

**Auth:** Pública
**Body (JSON):**
```json
{ "refresh": "<refresh.jwt>" }
```

**Respuestas**
- `200 OK`
```json
{ "access": "<nuevo.access.jwt>" }
```
- `401/400` si el refresh es inválido/expirado (formato estándar de SimpleJWT).

---

### POST `/auth/verify` — Verificar un token

**Auth:** Pública
**Body (JSON):**
```json
{ "token": "<access.o.refresh.jwt>" }
```
**Respuestas**
- `200 OK` si es válido.
- `401/400` si no lo es.

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---

## Usuarios (`/users`)

**Modelo expuesto (serializer de perfil):**
```json
{
  "id": 42,
  "email": "ada@example.com",
  "first_name": "Ada",
  "last_name": "Lovelace",
  "phone_number": "+541100000000",
  "dietary_restrictions": [1, 3]
}
```

> **Permisos**
> - `list`, `create`, `destroy`: **solo admin**.
> - `retrieve`, `update`, `partial_update`: **el propio usuario o admin**.
> - Acciones especiales documentadas abajo.

### GET `/users`
Lista de usuarios. **Solo admin.**
**Query params comunes:** paginación por DRF.

**Respuestas**
- `200 OK` lista paginada.

### GET `/users/{id}`
Obtiene un usuario (si eres el dueño o admin).

**Respuestas**
- `200 OK`
- `403 Forbidden` si no tienes permiso.
- `404 Not Found` si no existe.

### PUT/PATCH `/users/{id}`
Actualiza campos permitidos (no `email`).

**Body (ejemplo PATCH):**
```json
{ "first_name": "A.", "dietary_restrictions": [2,5] }
```
**Respuestas**
- `200 OK`
- `400 Bad Request` en validación.
- `403/404` según corresponda.

### DELETE `/users/{id}`
Elimina usuario. **Solo admin.**
**Respuestas:** `204 No Content`, `404 Not Found`.

---

### GET/PUT/PATCH `/users/me`
Obtiene/actualiza tu propio perfil.

**GET → 200 OK** con el perfil.
**PUT/PATCH → Body (ejemplo):**
```json
{
  "first_name": "Ada",
  "last_name": "L.",
  "phone_number": "+54...",
  "dietary_restrictions": [1,2]
}
```
**Respuestas**
- `200 OK`
- `400 Bad Request`

### POST `/users/me/change-password`
Cambia tu contraseña.

**Body:**
```json
{
  "current_password": "actual123",
  "new_password": "NuevaSegura123"
}
```
**Respuestas**
- `204 No Content` si se cambió correctamente.
- `400 Bad Request`
  - `{"current_password": ["Contraseña actual inválida."]}`
  - `{"new_password": ["<mensajes de validación>"]}`

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---

## Categorías (`/categories`)

**Auth:** Pública (solo lectura)
**Endpoints:**
- `GET /categories` — lista
- `GET /categories/{id}` — detalle

**Búsqueda y ordenamiento:**
- `search`: por `name`, `friendly_name`, `description`. Ej.: `?search=veg`
- `ordering`: `friendly_name`, `name`. Ej.: `?ordering=friendly_name`

**Respuestas**
- `200 OK`

**Modelo:**
```json
{ "id": 1, "name": "breakfast", "friendly_name": "Desayuno", "description": "..." }
```

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---

## Ingredientes (`/ingredients`)

**Auth:** Pública (solo lectura)
**Endpoints:**
- `GET /ingredients`
- `GET /ingredients/{id}`

**Búsqueda/ordenamiento:**
- `search` por `name`, `description`
- `ordering`: `name`, `calories_per_100g`, `protein_per_100g`, `carbs_per_100g`, `fat_per_100g`

**Modelo:**
```json
{
  "id": 10,
  "name": "Arroz",
  "description": "",
  "calories_per_100g": "360.00",
  "protein_per_100g": "6.00",
  "carbs_per_100g": "80.00",
  "fat_per_100g": "1.00",
  "sugar_per_100g": "0.10",
  "dietary_restrictions": []
}
```

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---

## Recetas (`/recipes`)

**Auth:** Pública (solo lectura)
**Lookup:** `slug` → `GET /recipes/{slug}`

**Endpoints:**
- `GET /recipes`
- `GET /recipes/{slug}`

**Búsqueda/ordenamiento:**
- `search` en `name`, `description`. Ej.: `?search=pollo`
- `ordering` soporta: `name`, `prep_time`, `cook_time`, `total_time`, `servings`, `calories_per_serving`, `total_calories`, `protein_per_serving`, `carbs_per_serving`, `fat_per_serving`, `sugar_per_serving`, `created_at`, `updated_at`

**Filtros específicos (`GET /recipes`):**
- `category=`
  - ID (`?category=3`) **o** nombre/friendly_name (`?category=desayuno`)
- `time_max=` (minutos totales)
- Rango de macros por porción (usar `*_min` ó `*_max`):
  - `calories_min`, `calories_max`
  - `protein_min`, `protein_max`
  - `carbs_min`, `carbs_max`
  - `fat_min`, `fat_max`
  - `sugar_min`, `sugar_max`
- Inclusión/exclusión por ingredientes (IDs, separados por coma):
  - `include_ingredients=1,2,3` → **debe** contener **todas** las IDs listadas.
  - `exclude_ingredients=4,5`

**Modelo de respuesta (`RecipeSerializer`):**
```json
{
  "id": "c8c67c8c-...-...",
  "slug": "tortilla-de-papas",
  "name": "Tortilla de papas",
  "description": "...",
  "category": { "id": 1, "name": "breakfast", "friendly_name": "Desayuno", "description": "" },
  "ingredients": [
    {
      "ingredient": {
        "id": 10,
        "name": "Huevo",
        "description": "",
        "calories_per_100g": "143.00",
        "protein_per_100g": "13.00",
        "carbs_per_100g": "1.10",
        "fat_per_100g": "10.00",
        "sugar_per_100g": "1.10",
        "dietary_restrictions": []
      },
      "amount": "2.00",
      "unit": "u"
    }
  ],
  "images": [
    { "url": "https://...", "alt_text": "Foto", "order": 0 }
  ],
  "prep_time": 10,
  "cook_time": 15,
  "total_time": 25,
  "servings": 2,
  "calories_per_serving": "250.00",
  "protein_per_serving": "12.00",
  "carbs_per_serving": "20.00",
  "fat_per_serving": "10.00",
  "sugar_per_serving": "2.00",
  "primary_image": "https://.../principal.jpg",
  "main_image_url": "https://.../principal.jpg",
  "created_at": "2025-10-05T18:20:00Z",
  "updated_at": "2025-10-05T18:20:00Z"
}
```

**Códigos**
- `200 OK`
- `404 Not Found` (por `slug` inexistente)

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---

## Colecciones de Recetas (`/collections`)

Recurso **protegido** (JWT). Cada colección pertenece a un usuario; **solo el dueño (o admin)** puede verla/modificarla.

**Lookup:** `slug` → `/collections/{slug}`

**Modelo (`RecipeCollectionSerializer`):**
```json
{
  "id": "8d0f2f0c-...",
  "slug": "favoritas",
  "name": "Favoritas",
  "description": "Mis recetas favoritas",
  "is_public": false,
  "items": [
    {
      "id": 123,
      "order": 1,
      "added_at": "2025-10-05T19:00:00Z",
      "recipe": { "...": "RecipeSerializer" }
    }
  ],
  "created_at": "2025-10-05T18:20:00Z",
  "updated_at": "2025-10-05T18:21:00Z"
}
```

> **Notas de permisos/visibilidad**
> - `GET /collections` devuelve **solo** las colecciones del usuario autenticado (o **todas** si es staff).
> - Los accesos a `/collections/{slug}` y acciones custom validan **dueño o admin** (si no: `403 Forbidden`).

### GET `/collections`
Lista de colecciones del usuario logueado.

**Respuestas:** `200 OK` (lista), paginación DRF si está habilitada globalmente.

### POST `/collections`
Crea una colección.

**Body:**
```json
{ "name": "Favoritas", "description": "Mis recetas favoritas", "is_public": false }
```
- `owner` se infiere de `request.user`
- `name` debe ser único (case-insensitive) **por usuario**

**Respuestas**
- `201 Created` con la colección creada (incluye `slug` autogenerado en el servidor).
- `400 Bad Request` (por ejemplo nombre duplicado para el mismo dueño).

### GET `/collections/{slug}`
Detalle (solo dueño/admin).
**Respuestas:** `200 OK`, `403 Forbidden`, `404 Not Found`.

### PUT/PATCH `/collections/{slug}`
Actualiza nombre/descr/`is_public`.
**Body (ejemplo PATCH):**
```json
{ "name": "Top 2025", "is_public": true }
```
**Respuestas:** `200 OK`, `400 Bad Request`, `403`, `404`.

### DELETE `/collections/{slug}`
Elimina la colección.
**Respuestas:** `204 No Content`, `403`, `404`.

---

### Acciones custom sobre una colección

#### POST `/collections/{slug}/add-recipe`
Agrega una receta a la colección (si no existía). Si es nueva, se coloca al **final** según `order`.

**Body:**
```json
{ "recipe_id": "c8c67c8c-...-..." }  // UUID de Recipe
```
**Respuestas**
- `200 OK` con la colección actualizada.
- `404 Not Found` si la receta no existe.
- `403 Forbidden` si no eres el dueño/admin.

#### POST `/collections/{slug}/remove-recipe`
Quita una receta de la colección.

**Body:**
```json
{ "recipe_id": "c8c67c8c-...-..." }
```
**Respuestas**
- `200 OK` con la colección actualizada.
- `404 Not Found` con `{ "detail": "La receta no estaba en la colección." }` si no estaba.
- `403 Forbidden` si no eres el dueño/admin.

#### POST `/collections/{slug}/reorder`
Reordena ítems de la colección (solo los incluidos en el payload).

**Body:**
```json
{
  "items": [
    { "recipe_id": "c8c67c8c-...-...", "order": 1 },
    { "recipe_id": "2b1a...", "order": 2 }
  ]
}
```
**Validaciones**
- `items` requerido, no vacío, lista.
- `order` debe ser **entero**.
- Todos los `recipe_id` deben **pertenecer a la colección**.

**Respuestas**
- `200 OK` con la colección actualizada.
- `400 Bad Request` con mensajes:
  - `{"detail": "Formato inválido: se espera 'items'."}`
  - `{"detail": "Todos los 'order' deben ser enteros."}`
  - `{"detail": "Falta recipe_id en algún item."}`
  - `{"detail": "Alguna receta no pertenece a la colección."}`
- `403 Forbidden` si no eres dueño/admin.

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---

## Ejemplos con `curl`

### Login

```bash
curl -X POST https://api.nutri-plan.net/auth/login \
-H "Content-Type: application/json" \
-d '{"email":"ada@example.com","password":"supersegura123"}'
```

### Crear Colección

```bash
curl -X POST https://api.nutri-plan.net/collections \
-H "Authorization: Bearer $ACCESS" \
-H "Content-Type: application/json" \
-d '{"name":"Favoritas","description":"Mis recetas favoritas"}'
```

### Agregar Receta a Colección

```bash
curl -X POST https://api.nutri-plan.net/collections/favoritas/add-recipe \
-H "Authorization: Bearer $ACCESS" \
-H "Content-Type: application/json" \
-d '{"recipe_id":"c8c67c8c-..."}'
```

### Reordenar

```bash
curl -X POST https://api.nutri-plan.net/collections/favoritas/reorder \
-H "Authorization: Bearer $ACCESS" \
-H "Content-Type: application/json" \
-d '{"items":[{"recipe_id":"c8c67c8c-...","order":1},{"recipe_id":"2b1a-...","order":2}]}'
```

<div align="right">
  <a href="#tabla-de-contenidos">Volver a Tabla de Contenidos</a>
</div>

---
