from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Optional, List


@dataclass
class User:
    id: str
    email: str
    password_hash: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Note:
    id: str
    user_id: str
    title: str
    content: str
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


class InMemoryDB:
    """A naive, in-memory storage for demo purposes only. Replace with a real DB in production."""
    def __init__(self) -> None:
        self.users_by_email: Dict[str, User] = {}
        self.users_by_id: Dict[str, User] = {}
        self.sessions: Dict[str, str] = {}  # session_token -> user_id
        self.notes_by_id: Dict[str, Note] = {}
        self.user_notes_index: Dict[str, List[str]] = {}  # user_id -> [note_ids]

    # PUBLIC_INTERFACE
    def create_user(self, email: str, password_hash: str) -> User:
        """Create a new user if not exists; raises ValueError if email taken."""
        if email in self.users_by_email:
            raise ValueError("Email already registered")
        user = User(id=str(uuid.uuid4()), email=email, password_hash=password_hash)
        self.users_by_email[email] = user
        self.users_by_id[user.id] = user
        self.user_notes_index[user.id] = []
        return user

    # PUBLIC_INTERFACE
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get a user by email."""
        return self.users_by_email.get(email)

    # PUBLIC_INTERFACE
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by id."""
        return self.users_by_id.get(user_id)

    # PUBLIC_INTERFACE
    def create_session(self, user_id: str) -> str:
        """Create and store a new session token for a user."""
        token = str(uuid.uuid4())
        self.sessions[token] = user_id
        return token

    # PUBLIC_INTERFACE
    def delete_session(self, token: str) -> None:
        """Delete a session token if it exists."""
        if token in self.sessions:
            del self.sessions[token]

    # PUBLIC_INTERFACE
    def get_user_id_by_session(self, token: str) -> Optional[str]:
        """Resolve a session token to a user id."""
        return self.sessions.get(token)

    # PUBLIC_INTERFACE
    def create_note(self, user_id: str, title: str, content: str) -> Note:
        """Create a note for the user."""
        note = Note(id=str(uuid.uuid4()), user_id=user_id, title=title, content=content)
        self.notes_by_id[note.id] = note
        self.user_notes_index[user_id].append(note.id)
        return note

    # PUBLIC_INTERFACE
    def list_notes(self, user_id: str) -> List[Note]:
        """List notes for a user."""
        ids = self.user_notes_index.get(user_id, [])
        return [self.notes_by_id[nid] for nid in ids]

    # PUBLIC_INTERFACE
    def get_note(self, user_id: str, note_id: str) -> Optional[Note]:
        """Get a note by id if it belongs to user."""
        note = self.notes_by_id.get(note_id)
        if note and note.user_id == user_id:
            return note
        return None

    # PUBLIC_INTERFACE
    def update_note(self, user_id: str, note_id: str, title: Optional[str], content: Optional[str]) -> Optional[Note]:
        """Update a note if it belongs to user."""
        note = self.get_note(user_id, note_id)
        if not note:
            return None
        if title is not None:
            note.title = title
        if content is not None:
            note.content = content
        note.updated_at = datetime.utcnow()
        return note

    # PUBLIC_INTERFACE
    def delete_note(self, user_id: str, note_id: str) -> bool:
        """Delete a note if it belongs to user."""
        note = self.get_note(user_id, note_id)
        if not note:
            return False
        del self.notes_by_id[note.id]
        if user_id in self.user_notes_index:
            self.user_notes_index[user_id] = [nid for nid in self.user_notes_index[user_id] if nid != note.id]
        return True


# Singleton for app use
db = InMemoryDB()
