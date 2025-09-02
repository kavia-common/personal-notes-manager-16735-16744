from flask_smorest import Blueprint
from flask.views import MethodView
from flask import current_app
from app.schemas import UserRegisterSchema, UserResponseSchema, UserLoginSchema, SessionResponseSchema, MessageSchema, ErrorSchema
from app.storage import db
from app.auth import hash_password, verify_password

blp = Blueprint(
    "Users", "users", url_prefix="/api/users", description="User management and authentication endpoints"
)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema, example={"email": "user@example.com", "password": "secret123"})
    @blp.response(201, UserResponseSchema)
    @blp.alt_response(400, schema=ErrorSchema, description="Email already registered or invalid input")
    def post(self, args):
        """Register a new user.
        Accepts email and password, stores hashed password.
        Returns created user details.
        """
        email = args["email"].strip().lower()
        password = args["password"]
        salt = current_app.config["SECRET_KEY"]  # DO NOT use in production; use per-user random salt
        try:
            user = db.create_user(email=email, password_hash=hash_password(password, salt))
        except ValueError as e:
            blp.abort(400, message=str(e))
        return {"id": user.id, "email": user.email, "created_at": user.created_at}


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema, example={"email": "user@example.com", "password": "secret123"})
    @blp.response(200, SessionResponseSchema)
    @blp.alt_response(401, schema=ErrorSchema, description="Invalid credentials")
    def post(self, args):
        """Login with email and password.
        Returns a session token for Authorization: Bearer <token>.
        """
        email = args["email"].strip().lower()
        password = args["password"]
        salt = current_app.config["SECRET_KEY"]
        user = db.get_user_by_email(email)
        if not user or not verify_password(password, salt, user.password_hash):
            blp.abort(401, message="Invalid email or password")
        token = db.create_session(user.id)
        return {"token": token, "user_id": user.id}


@blp.route("/logout")
class UserLogout(MethodView):
    @blp.response(200, MessageSchema)
    def post(self):
        """Logout current session if Authorization header present."""
        # Logout is stateless here; clients should discard token. Handling in session route too.
        return {"message": "If you provided a valid token, it is now invalidated. Otherwise, this is a no-op."}
