
from datetime import datetime, timezone

from app.extensions import db


class Ticket(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(db.String(150), nullable=False)

    description = db.Column(db.Text, nullable=False)

    priority = db.Column(
        db.String(2),
        nullable=False,
        default="P3"
    )

    status = db.Column(
        db.String(20),
        nullable=False,
        default="Open"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    # Convert database object into JSON-compatible dictionary
    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "created_at": (
                self.created_at.isoformat()
                if self.created_at else None
            )
        }
