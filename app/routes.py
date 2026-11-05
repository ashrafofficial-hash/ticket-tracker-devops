
from flask import Blueprint, jsonify, request

from app.extensions import db
from app.models import Ticket

api = Blueprint("api", __name__)


# 1. Health Check
@api.route("/health", methods=["GET"])
def health_check():

    return jsonify({
        "status": "healthy",
        "service": "ticket-tracker-api"
    }), 200


# 2. Create Ticket
@api.route("/tickets", methods=["POST"])
def create_ticket():

    data = request.get_json(silent=True) or {}

    title = data.get("title")
    description = data.get("description")
    priority = data.get("priority")

    if not all(
        isinstance(value, str) and value.strip()
        for value in [title, description, priority]
    ):
        return jsonify({
            "error": "Title, description and priority are required"
        }), 400

    title = title.strip()
    description = description.strip()
    priority = priority.strip().upper()

    if len(title) > 150:
        return jsonify({
            "error": "Title cannot exceed 150 characters"
        }), 400

    if priority not in ["P1", "P2", "P3"]:
        return jsonify({
            "error": "Priority must be P1, P2 or P3"
        }), 400

    ticket = Ticket(
        title=title,
        description=description,
        priority=priority
    )

    try:
        db.session.add(ticket)
        db.session.commit()

        return jsonify(ticket.to_dict()), 201

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Unable to create ticket"
        }), 500


# 3. Get All Tickets
@api.route("/tickets", methods=["GET"])
def get_tickets():

    tickets = Ticket.query.order_by(
        Ticket.id.desc()
    ).all()

    return jsonify([
        ticket.to_dict() for ticket in tickets
    ]), 200


# 4. Get Ticket By ID
@api.route("/tickets/<int:ticket_id>", methods=["GET"])
def get_ticket(ticket_id):

    ticket = db.session.get(Ticket, ticket_id)

    if ticket is None:
        return jsonify({
            "error": "Ticket not found"
        }), 404

    return jsonify(ticket.to_dict()), 200


# 5. Update Ticket Status
@api.route("/tickets/<int:ticket_id>", methods=["PUT"])
def update_ticket(ticket_id):

    ticket = db.session.get(Ticket, ticket_id)

    if ticket is None:
        return jsonify({
            "error": "Ticket not found"
        }), 404

    data = request.get_json(silent=True) or {}
    status = data.get("status")

    allowed_statuses = [
        "Open",
        "In Progress",
        "Resolved"
    ]

    if status not in allowed_statuses:
        return jsonify({
            "error": "Status must be Open, In Progress or Resolved"
        }), 400

    ticket.status = status

    try:
        db.session.commit()
        return jsonify(ticket.to_dict()), 200

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Unable to update ticket"
        }), 500


# 6. Delete Ticket
@api.route("/tickets/<int:ticket_id>", methods=["DELETE"])
def delete_ticket(ticket_id):

    ticket = db.session.get(Ticket, ticket_id)

    if ticket is None:
        return jsonify({
            "error": "Ticket not found"
        }), 404

    try:
        db.session.delete(ticket)
        db.session.commit()

        return jsonify({
            "message": "Ticket deleted successfully"
        }), 200

    except Exception:
        db.session.rollback()
        return jsonify({
            "error": "Unable to delete ticket"
        }), 500
