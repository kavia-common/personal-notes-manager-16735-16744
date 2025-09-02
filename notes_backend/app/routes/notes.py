from flask_smorest import Blueprint
from flask.views import MethodView
from app.schemas import NoteCreateSchema, NoteUpdateSchema, NoteResponseSchema, NotesListResponseSchema, ErrorSchema, MessageSchema
from app.storage import db
from app.auth import get_bearer_token

blp = Blueprint(
    "Notes", "notes", url_prefix="/api/notes", description="CRUD operations for user notes"
)


def require_auth():
    token = get_bearer_token()
    if not token:
        blp.abort(401, message="Missing Authorization header")
    user_id = db.get_user_id_by_session(token)
    if not user_id:
        blp.abort(401, message="Invalid or expired session")
    return user_id


@blp.route("/")
class NotesCollection(MethodView):
    @blp.response(200, NotesListResponseSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Not authenticated")
    def get(self):
        """List notes for the authenticated user."""
        user_id = require_auth()
        notes = db.list_notes(user_id)
        items = [
            {
                "id": n.id,
                "user_id": n.user_id,
                "title": n.title,
                "content": n.content,
                "created_at": n.created_at,
                "updated_at": n.updated_at,
            }
            for n in notes
        ]
        return {"items": items}

    @blp.arguments(NoteCreateSchema)
    @blp.response(201, NoteResponseSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Not authenticated")
    def post(self, args):
        """Create a new note for the authenticated user."""
        user_id = require_auth()
        note = db.create_note(user_id=user_id, title=args["title"], content=args["content"])
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }


@blp.route("/<string:note_id>")
class NoteItem(MethodView):
    @blp.response(200, NoteResponseSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Not authenticated")
    @blp.alt_response(404, schema=ErrorSchema, description="Note not found")
    def get(self, note_id: str):
        """Get a single note by id."""
        user_id = require_auth()
        note = db.get_note(user_id, note_id)
        if not note:
            blp.abort(404, message="Note not found")
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }

    @blp.arguments(NoteUpdateSchema)
    @blp.response(200, NoteResponseSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Not authenticated")
    @blp.alt_response(404, schema=ErrorSchema, description="Note not found")
    def put(self, args, note_id: str):
        """Update a note's title/content."""
        user_id = require_auth()
        note = db.update_note(user_id, note_id, title=args.get("title"), content=args.get("content"))
        if not note:
            blp.abort(404, message="Note not found")
        return {
            "id": note.id,
            "user_id": note.user_id,
            "title": note.title,
            "content": note.content,
            "created_at": note.created_at,
            "updated_at": note.updated_at,
        }

    @blp.response(200, MessageSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Not authenticated")
    @blp.alt_response(404, schema=ErrorSchema, description="Note not found")
    def delete(self, note_id: str):
        """Delete a note by id."""
        user_id = require_auth()
        ok = db.delete_note(user_id, note_id)
        if not ok:
            blp.abort(404, message="Note not found")
        return {"message": "Note deleted"}
