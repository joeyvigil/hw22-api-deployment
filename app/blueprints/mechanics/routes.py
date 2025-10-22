from app.blueprints.mechanics import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema,login_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Mechanics, ServiceMechanics, ServiceTickets, db
from app.extensions import limiter
from werkzeug.security import generate_password_hash, check_password_hash
from app.util.auth import encode_token, token_required



@mechanics_bp.route('/login', methods=['POST']) 
def login():
    try:
        data = login_schema.load(request.json) # type: ignore
        mechanic = db.session.query(Mechanics).where(Mechanics.email==data['email']).first()
        
        if mechanic and check_password_hash(mechanic.password, data['password']): 
            token = encode_token(mechanic.id) 
            return jsonify({
                "message": f'Hello There {mechanic.first_name}',
                "token" : token
            }), 200
        
        return jsonify({"message": "invalid email or password"}), 401
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# Assignment
# POST '/' : Creates a new Mechanic
@mechanics_bp.route('', methods=['POST']) 
def create_mechanic():
    try:
        data = mechanic_schema.load(request.json) # type: ignore
        data['password'] = generate_password_hash(data['password']) #encrypts password
        new_mechanic = Mechanics(**data) 
        db.session.add(new_mechanic)
        db.session.commit()
        return jsonify(mechanic_schema.dump(new_mechanic)), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400

# Assignment
# GET '/': Retrieves all Mechanics
@mechanics_bp.route('', methods=['GET']) 
def read_mechanics():
    try: 
        mechanics = db.session.query(Mechanics).all()
        return mechanics_schema.jsonify(mechanics), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400


@mechanics_bp.route('/profile', methods=['GET'])
@token_required
def read_user():
    try:
        mechanic_id = request.mechanic_id # type: ignore 
        #wow, the encoded request token contains the ID for the user?
        mechanic = db.session.get(Mechanics, mechanic_id)
        return mechanic_schema.jsonify(mechanic), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400


# gets all tickets assigned to the logged-in mechanic based on the token provided in the request header
@mechanics_bp.route('my-tickets', methods=['GET'])
@token_required
def mechanic_tickets():
    try:
        mechanic_id = request.mechanic_id  # type: ignore
        service_tickets = db.session.query(ServiceMechanics).filter(ServiceMechanics.mechanic_id == mechanic_id).all()
        tickets_list = [ticket.id for ticket in service_tickets]  # or serialize as needed
        return jsonify({"tickets": tickets_list}), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400



# GET at id
@mechanics_bp.route('<int:mechanic_id>', methods=['GET'])
def read_mechanic(mechanic_id):
    try:
        mechanic = db.session.get(Mechanics, mechanic_id)
        return mechanic_schema.jsonify(mechanic), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# DELETE '/<int:id'>: Deletes a specific Mechanic based on the id passed in through the url.
@mechanics_bp.route('<int:mechanic_id>', methods=['DELETE'])
@token_required
def delete_mechanic(mechanic_id):
    try:
        mechanic = db.session.get(Mechanics, mechanic_id)
        db.session.delete(mechanic)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted mechanic {mechanic_id}"}), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400

# Assignment
# PUT '/<int:id>':  Updates a specific Mechanic based on the id passed in through the url.
@mechanics_bp.route('<int:mechanic_id>', methods=['PUT'])
@token_required
def update_mechanic(mechanic_id):
    try:
        mechanic = db.session.get(Mechanics, mechanic_id) 
        if not mechanic: 
            return jsonify({"message": "mechanic not found"}), 404  
        
        mechanic_data = mechanic_schema.load(request.json)  # type: ignore

        for key, value in mechanic_data.items():
            if value: #blank fields will not be updated
                if key !="password":
                    # print(f"mechanic {mechanic} key {key} value {value}")
                    setattr(mechanic, key, value) 
                else:
                    setattr(mechanic, key, generate_password_hash(value)) 
                    
        db.session.commit()
        return mechanic_schema.jsonify(mechanic), 200
    except ValidationError as e:
        return jsonify(e.messages), 400 
    except Exception as e:
        return jsonify(str(e)), 400
    