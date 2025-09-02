from marshmallow import Schema, fields, validate


class MessageSchema(Schema):
    message = fields.String(required=True, description="Informational message")


class ErrorSchema(Schema):
    code = fields.Integer(required=True, description="Error code")
    status = fields.String(required=True, description="Error name")
    message = fields.String(required=True, description="Error message")
    errors = fields.Dict(required=False, description="Validation or contextual errors")


class UserRegisterSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, validate=validate.Length(min=6), description="User password")


class UserLoginSchema(Schema):
    email = fields.Email(required=True, description="User email")
    password = fields.String(required=True, description="User password")


class SessionResponseSchema(Schema):
    token = fields.String(required=True, description="Session token (Bearer)")
    user_id = fields.String(required=True, description="User identifier")


class UserResponseSchema(Schema):
    id = fields.String(required=True)
    email = fields.Email(required=True)
    created_at = fields.DateTime(required=True)


class NoteCreateSchema(Schema):
    title = fields.String(required=True, validate=validate.Length(min=1, max=200), description="Note title")
    content = fields.String(required=True, validate=validate.Length(min=1), description="Note content")


class NoteUpdateSchema(Schema):
    title = fields.String(required=False, validate=validate.Length(min=1, max=200), description="Note title")
    content = fields.String(required=False, validate=validate.Length(min=1), description="Note content")


class NoteResponseSchema(Schema):
    id = fields.String(required=True)
    user_id = fields.String(required=True)
    title = fields.String(required=True)
    content = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(required=True)


class NotesListResponseSchema(Schema):
    items = fields.List(fields.Nested(NoteResponseSchema), required=True)
