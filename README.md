# personal-notes-manager-16735-16744

Notes Backend (Flask) provides:
- Health check: GET /
- Users: POST /api/users/register, POST /api/users/login
- Sessions: GET /api/sessions/whoami, POST /api/sessions/revoke
- Notes: GET/POST /api/notes/, GET/PUT/DELETE /api/notes/{note_id}

Run locally:
- pip install -r notes_backend/requirements.txt
- cd notes_backend && python run.py
- Open docs at /docs (Swagger UI)

Auth:
- Use Authorization: Bearer <token> returned by login for protected endpoints.

Env:
- FLASK_SECRET_KEY (optional but recommended)
- SESSION_COOKIE_NAME (optional)
- CORS_ORIGINS (optional)
