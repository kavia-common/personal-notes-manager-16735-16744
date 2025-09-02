from flask_smorest import Blueprint
from flask.views import MethodView
from app.schemas import UserResponseSchema, MessageSchema, ErrorSchema
from app.storage import db
from app.auth import get_bearer_token

blp = Blueprint(
    "Sessions", "sessions", url_prefix="/api/sessions", description="Session management endpoints"
)


@blp.route("/whoami")
class WhoAmI(MethodView):
    @blp.response(200, UserResponseSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Not authenticated")
    def get(self):
        """Get the current authenticated user based on Bearer token."""
        token = get_bearer_token()
        if not token:
            blp.abort(401, message="Missing Authorization header")
        user_id = db.get_user_id_by_session(token)
        if not user_id:
            blp.abort(401, message="Invalid or expired session")
        user = db.get_user_by_id(user_id)
        if not user:
            blp.abort(401, message="User not found")
        return {"id": user.id, "email": user.email, "created_at": user.created_at}


@blp.route("/revoke")
class RevokeSession(MethodView):
    @blp.response(200, MessageSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Not authenticated")
    def post(self):
        """Revoke the current session token."""
        token = get_bearer_token()
        if not token:
            blp.abort(401, message="Missing Authorization header")
        db.delete_session(token)
        return {"message": "Session revoked"}
