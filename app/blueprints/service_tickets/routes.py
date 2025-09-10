from app.blueprints.service_tickets import service_tickets_bp
from .schemas import service_ticket_schema, service_tickets_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import ServiceTickets, db

# Assignment
# POST '/': Pass in all the required information to create the service_ticket.
@service_tickets_bp.route('', methods=['POST']) 
def create_service_ticket():
    try:
        data = service_ticket_schema.load(request.json) # type: ignore
        new_service_ticket = ServiceTickets(**data) 
        db.session.add(new_service_ticket)
        db.session.commit()
        return service_ticket_schema.jsonify(new_service_ticket), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# GET '/': Retrieves all service tickets.
@service_tickets_bp.route('', methods=['GET']) 
def read_service_tickets():
    try:
        service_tickets = db.session.query(ServiceTickets).all()
        return service_tickets_schema.jsonify(service_tickets), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# GET at ID
@service_tickets_bp.route('<int:service_ticket_id>', methods=['GET'])
def read_service_ticket(service_ticket_id):
    try:
        service_ticket = db.session.get(ServiceTickets, service_ticket_id)
        return service_ticket_schema.jsonify(service_ticket), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# Delete at ID
@service_tickets_bp.route('<int:service_ticket_id>', methods=['DELETE'])
def delete_service_ticket(service_ticket_id):
    try:
        service_ticket = db.session.get(ServiceTickets, service_ticket_id)
        db.session.delete(service_ticket)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted service_ticket {service_ticket_id}"}), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# PUT at id
@service_tickets_bp.route('<int:service_ticket_id>', methods=['PUT'])
def update_service_ticket(service_ticket_id):
    try:
        service_ticket = db.session.get(ServiceTickets, service_ticket_id) 
        if not service_ticket: 
            return jsonify({"message": "service_ticket not found"}), 404  
        service_ticket_data = service_ticket_schema.load(request.json)  # type: ignore
        for key, value in service_ticket_data.items(): 
            if value: #blank fields will not be updated
                setattr(service_ticket, key, value) 
        db.session.commit()
        return service_ticket_schema.jsonify(service_ticket), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400
    