# Kartak — Project Requirements

Kartak is a small e-commerce app: user auth, a product catalog, and orders. This doc is the shared contract between the frontend and backend so both sides agree on exactly what the API looks like.

**Repo layout:**
- `backend/` — the backend implementation, being built by hand as a learning exercise.
- `backend_reference/` — a complete, working reference implementation of everything in this doc. Use it to check your work, not to copy-paste from.
- `frontend/` — a complete React app already built against the contract below. It expects the backend to match this doc exactly.

---

## 1. Architecture

| Piece | Tech | Default address |
|---|---|---|
| Frontend | React + Vite | `http://localhost:5173` |
| Backend | FastAPI | `http://127.0.0.1:8000` |
| Database | SQLite (dev) | `backend/kartak.db` |
| Auth | JWT bearer tokens | — |

- The backend **must** enable CORS for `http://localhost:5173`, or the browser will block every request from the frontend.
- Auth is stateless JWT: the backend issues a signed token on login; the frontend sends it back on every protected request as `Authorization: Bearer <token>`.

---

## 2. Data models (backend)

### User
| Field | Type | Notes |
|---|---|---|
| `id` | int | primary key |
| `email` | string | unique, indexed |
| `hashed_password` | string | never returned in any response |
| `created_at` | datetime | UTC |

### Product
| Field | Type | Notes |
|---|---|---|
| `id` | int | primary key |
| `name` | string | required |
| `description` | string | default `""` |
| `price` | float | required |
| `stock` | int | default `0` |

### Order
| Field | Type | Notes |
|---|---|---|
| `id` | int | primary key |
| `user_id` | int | FK → User, owner of the order |
| `created_at` | datetime | UTC |
| `items` | list of OrderItem | see below |

### OrderItem
| Field | Type | Notes |
|---|---|---|
| `product_id` | int | FK → Product |
| `quantity` | int | default `1` |
| `unit_price` | float | price of the product **at time of order** (copied from `Product.price`, not looked up live later) |

---

## 3. API contract

All request/response bodies are JSON **except** `/auth/login`, which is form-encoded (see below). All errors return `{"detail": "<message>"}` with a 4xx/5xx status code.

### Auth

#### `POST /auth/register`
- Auth required: no
- Request body (JSON):
  ```json
  { "email": "user@example.com", "password": "secret123" }
  ```
- Success: `201 Created`
  ```json
  { "id": 1, "email": "user@example.com", "created_at": "2026-07-25T10:00:00" }
  ```
- Errors: `400` if email is already registered.

#### `POST /auth/login`
- Auth required: no
- Request body: **form-encoded**, not JSON (`application/x-www-form-urlencoded`), fields `username` (the email) and `password`. This matches FastAPI's standard `OAuth2PasswordRequestForm` and is what the frontend sends.
- Success: `200 OK`
  ```json
  { "access_token": "<jwt>", "token_type": "bearer" }
  ```
- Errors: `401` if email/password is wrong.

### Products

#### `GET /products`
- Auth required: no
- Success: `200 OK` — array of Product objects:
  ```json
  [{ "id": 1, "name": "Widget", "description": "A nice widget", "price": 9.99, "stock": 10 }]
  ```

#### `GET /products/{product_id}`
- Auth required: no
- Success: `200 OK` — single Product object (same shape as above).
- Errors: `404` if not found.

#### `POST /products`
- Auth required: **yes**
- Request body (JSON):
  ```json
  { "name": "Widget", "description": "A nice widget", "price": 9.99, "stock": 10 }
  ```
  (`description` and `stock` are optional, default `""` / `0`.)
- Success: `201 Created` — the created Product object, including its new `id`.

### Orders

#### `GET /orders`
- Auth required: **yes**
- Success: `200 OK` — array of the **current user's own orders only**, each with nested items:
  ```json
  [{
    "id": 1,
    "created_at": "2026-07-25T10:00:00",
    "items": [{ "product_id": 1, "quantity": 2, "unit_price": 9.99 }]
  }]
  ```

#### `POST /orders`
- Auth required: **yes**
- Request body (JSON):
  ```json
  { "items": [{ "product_id": 1, "quantity": 2 }] }
  ```
- Behavior: for each item, decrement `Product.stock` by `quantity` and snapshot the current price into `unit_price`.
- Success: `201 Created` — the created Order object (same shape as in `GET /orders`).
- Errors: `400` if `items` is empty or a product doesn't have enough stock; `404` if a `product_id` doesn't exist.

---

## 4. Backend requirements

- **Env vars** (see `.env.example`):
  - `SECRET_KEY` — used to sign JWTs. Must be set to a real random value outside of local dev.
  - `ACCESS_TOKEN_EXPIRE_MINUTES` — token lifetime (default `60`).
  - `DATABASE_URL` — optional, defaults to local SQLite (`sqlite:///./kartak.db`).
- **Password hashing**: bcrypt via `passlib`. Known pitfall — `passlib` 1.7.4 is incompatible with `bcrypt` ≥ 4.1 (raises `ValueError: password cannot be longer than 72 bytes` even for short passwords, due to an internal self-test bug). Pin `bcrypt==4.0.1`.
- **JWT**: signed with `SECRET_KEY`, algorithm `HS256`, `sub` claim = user's email.
- **Run it**:
  ```bash
  cd backend
  python3 -m venv venv && source venv/bin/activate
  pip install -r requirements.txt
  cp .env.example .env
  uvicorn app.main:app --reload
  ```

---

## 5. Frontend requirements

- **Pages**: `Login`, `Register`, `Products` (public, but shows a "Buy" button only when logged in), `Orders` (requires login, redirects to `/login` otherwise).
- **Token storage**: JWT stored in `localStorage` under the key `"token"`; attached as `Authorization: Bearer <token>` on authenticated requests.
- **Config**: `VITE_API_URL` env var sets the backend base URL; defaults to `http://127.0.0.1:8000` if unset.
- **Run it**:
  ```bash
  cd frontend
  npm install
  npm run dev
  ```

---

## 6. Non-functional notes

- Timestamps are ISO 8601 datetime strings (UTC, no timezone suffix in the current implementation).
- All authenticated endpoints expect the header `Authorization: Bearer <token>` — missing/invalid tokens return `401`.
- Request bodies are JSON (`Content-Type: application/json`) everywhere except `/auth/login`, which is form-encoded.
