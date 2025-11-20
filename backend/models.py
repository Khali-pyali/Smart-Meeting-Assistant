from database import db
from datetime import datetime, timezone
import json

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    datetime = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    participants = db.Column(db.Text, default="[]") # Stored as JSON string
    raw_notes = db.Column(db.Text, default="")
    ai_summary = db.Column(db.Text, default="")
    tags = db.Column(db.Text, default="[]") # Stored as JSON string
    meeting_link = db.Column(db.String(500), default="") # Video call link
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "datetime": self.datetime.isoformat() if self.datetime else None,
            "participants": json.loads(self.participants) if self.participants else [],
            "raw_notes": self.raw_notes,
            "ai_summary": self.ai_summary,
            "tags": json.loads(self.tags) if self.tags else [],
            "meeting_link": self.meeting_link,
            "created_at": self.created_at.isoformat()
        }

class ActionItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    owner = db.Column(db.String(100), default="Unassigned")
    due_date = db.Column(db.DateTime, nullable=True)
    status = db.Column(db.String(20), default="pending") # pending, in-progress, completed

    def to_dict(self):
        return {
            "id": self.id,
            "meeting_id": self.meeting_id,
            "description": self.description,
            "owner": self.owner,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "status": self.status
        }
