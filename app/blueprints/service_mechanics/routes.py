from app.blueprints.service_mechanics import service_mechanics_bp
from .schemas import service_mechanic_schema, service_mechanics_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import ServiceMechanics, db
from app.util.auth import encode_token, token_required

# Assignment
# PUT '/<ticket_id>/assign-mechanic/<mechanic-id>: Adds a relationship between a service ticket and the mechanics. (Reminder: use your relationship attributes! They allow you the treat the relationship like a list, able to append a Mechanic to the mechanics list).
@service_mechanics_bp.route('<int:ticket_id>/assign-mechanic/<int:mechanic_id>', methods=['POST'])
def create_service_mechanic(ticket_id, mechanic_id):
    try:
        print(f"{ticket_id} and {mechanic_id}")
        new_service_mechanic = ServiceMechanics(ticket_id=ticket_id, mechanic_id=mechanic_id)
        db.session.add(new_service_mechanic)
        db.session.commit()
        return service_mechanic_schema.jsonify(new_service_mechanic), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# PUT '/<ticket_id>/remove-mechanic/<mechanic-id>: Removes the relationship from the service ticket and the mechanic.
@service_mechanics_bp.route('<int:ticket_id>/remove-mechanic/<int:mechanic_id>', methods=['DELETE'])
def delete_service_mechanic(ticket_id,mechanic_id):
    # service_mechanic = db.session.get(ServiceMechanics, service_mechanic_id)
    try:
        service_mechanic = db.session.query(ServiceMechanics).filter_by(ticket_id=ticket_id,mechanic_id=mechanic_id).first()
        db.session.delete(service_mechanic)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted service_mechanic "}), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# # return all service mechanics
# @service_mechanics_bp.route('', methods=['GET']) 
# def read_service_mechanics():
#     service_mechanics = db.session.query(ServiceMechanics).all()
#     return service_mechanics_schema.jsonify(service_mechanics), 200


# # return service mechanic at given id
# @service_mechanics_bp.route('<int:service_mechanic_id>', methods=['GET'])
# def read_service_mechanic(service_mechanic_id):
#     service_mechanic = db.session.get(ServiceMechanics, service_mechanic_id)
#     return service_mechanic_schema.jsonify(service_mechanic), 200



# # update service mechanic at given id
# @service_mechanics_bp.route('<int:service_mechanic_id>', methods=['PUT'])
# def update_service_mechanic(service_mechanic_id):
#     service_mechanic = db.session.get(ServiceMechanics, service_mechanic_id) 

#     if not service_mechanic: 
#         return jsonify({"message": "service_mechanic not found"}), 404  
    
#     try:
#         service_mechanic_data = service_mechanic_schema.load(request.json)  # type: ignore
#     except ValidationError as e:
#         return jsonify({"message": e.messages}), 400
    
#     for key, value in service_mechanic_data.items(): 
#         if value: #blank fields will not be updated
#             setattr(service_mechanic, key, value) 

#     db.session.commit()
#     return service_mechanic_schema.jsonify(service_mechanic), 200
    
