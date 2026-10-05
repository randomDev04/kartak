# FastAPI learning notes — Lessons 1–6 recap

Quick-reload notes for picking this back up after a break. Not a tutorial — just the shape of what you already built.

## 1. Hello World
- venv + `pip install fastapi "uvicorn[standard]"`
- `app = FastAPI()`, then `@app.get("/")` on a plain function returning a dict (FastAPI turns it into JSON).
- Run: `uvicorn app.main:app --reload` (must run from `backend/`, not from inside `app/`).
- `/docs` = auto-generated Swagger UI, built from your routes + type hints.

## 2. Routing
- A function parameter that appears in the path (`/items/{item_id}`) → **path param**.
- A parameter that does *not* appear in the path → **query param** (`?query=...`), optional if given a default (`query: str | None = None`).
- Type hints aren't decoration — FastAPI validates against them and auto-rejects bad input with a 422.

## 3. Pydantic request bodies
- `class Item(BaseModel): name: str; price: float; in_stock: bool = True`
- Declare it as a route parameter (`item: Item`) → FastAPI parses + validates the JSON body into it automatically.
- This is the **form**: validates data in transit, lives only for the request, never touches disk.

## 4. `APIRouter` / project structure
- Split routes out of `main.py` into `app/routes/<name>.py`.
- `router = APIRouter(prefix="/items")`, then `@router.get("/{item_id}")` etc. (paths are relative to the prefix).
- In `main.py`: `app.include_router(items.router)`.
- Gotcha: `@router.post("/")` + `prefix="/items"` mounts as `/items/` (trailing slash) — use `@router.post("")` for a clean `/items`.

## 5. Database setup (SQLAlchemy)
- `app/database.py`: `engine` (connection), `SessionLocal` (session factory), `Base` (parent class for models), `get_db()` (yields a session, closes it in `finally` — wired into routes via `Depends(get_db)`).
- `app/models.py`: SQLAlchemy model, e.g. `class Item(Base): __tablename__ = "items"` with `Mapped[...]` columns. This is the **filing cabinet** — an actual DB row, persists across restarts.
- **Two `Item` classes on purpose**: Pydantic `Item` (validates JSON) vs. SQLAlchemy `Item` (the DB row). Import one with an alias to avoid clashing: `from app.models import Item as ItemModel`.
- `Base.metadata.create_all(bind=engine)` in `main.py` creates tables — **but only for models Python has actually imported somewhere**, and **only tables that don't already exist**. Renaming a column later does *not* alter the existing table — you'll get `no such column` errors until you delete the `.db` file and let it regenerate.

## 6. CRUD tied to the database
- **Save pattern:**
  ```python
  db_item = ItemModel(name=item.name, price=item.price, in_stock=item.in_stock)  # build DB row from validated Pydantic fields
  db.add(db_item)
  db.commit()
  db.refresh(db_item)   # pulls back the auto-assigned id
  return db_item
  ```
- **Read pattern:** `db.get(ItemModel, item_id)` → `None` if missing → `raise HTTPException(status_code=404, detail="...")`.
- ⚠️ **Import `HTTPException` from `fastapi`**, not `http.client` — the latter exists, looks plausible, and will crash instead of returning a clean 404.
- ⚠️ Field names must match when building the DB row — a Pydantic field named `in_stock` won't auto-map to a SQLAlchemy column named `is_in_stock`; either rename to match or map manually field-by-field.

## Where you left off
- Lesson 6 core task: **done** (`POST /items` saves, `GET /items/{id}` reads + 404s).
- Optional bonus not yet done: `GET /items` (list all, `db.query(ItemModel).all()`).
- **Not started: Lesson 7 — auth** (password hashing with `passlib`, JWTs with `python-jose`, register/login endpoints). That's the natural next step.
