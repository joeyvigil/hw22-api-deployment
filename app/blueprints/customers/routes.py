from app.blueprints.customers import customers_bp
from .schemas import customer_schema, customers_schema
from flask import request, jsonify
from marshmallow import ValidationError
from app.models import Customers, db
from app.extensions import limiter, cache


# POST '/' : Creates a new Customer
@customers_bp.route('/', methods=['POST']) 
def create_customer():
    try:
        data = customer_schema.load(request.json) # type: ignore
        new_customer = Customers(**data) 
        db.session.add(new_customer)
        db.session.commit()
        return customer_schema.jsonify(new_customer), 200
    except ValidationError as e:
        return jsonify(e.messages), 400
    except Exception as e:
        return jsonify(str(e)), 400
    



# GET '/': Retrieves all Customers
@customers_bp.route('/', methods=['GET']) 
@cache.cached(timeout=30)
def read_customers():
    try:
        customers = db.session.query(Customers).all()
        return customers_schema.jsonify(customers), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400

# GET '/<int:id>': Get Customer at ID
@customers_bp.route('/<int:customer_id>', methods=['GET'])
def read_customer(customer_id):
    try:
        customer = db.session.get(Customers, customer_id)
        return customer_schema.jsonify(customer), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400

# DELETE '/<int:id'>: Deletes a specific Customer based on the id passed in through the url.
@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        customer = db.session.get(Customers, customer_id)
        db.session.delete(customer)
        db.session.commit()
        return jsonify({"message": f"Successfully deleted customer {customer_id}"}), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400


# PUT '/<int:id>':  Updates a specific Customer based on the id passed in through the url.
@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@limiter.limit("30 per hour")
def update_customer(customer_id):
    try:
        customer = db.session.get(Customers, customer_id) 
        if not customer: 
            return jsonify({"message": "customer not found"}), 404  
        customer_data = customer_schema.load(request.json)  # type: ignore

        for key, value in customer_data.items():
            if value:
                setattr(customer, key, value) 

        db.session.commit()
        return customer_schema.jsonify(customer), 200

    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400


#-   Search for a Customer using there email as a Query Parameter.
@customers_bp.route('/search', methods=['GET'])
@limiter.limit("300 per hour")
def search_customer():
    try:
        email = request.args.get('email')
        print("this",email)
        customer = db.session.query(Customers).where(Customers.email.ilike(f"%{email}%")).first()
        return customer_schema.jsonify(customer), 200
    except ValidationError as e:
        return jsonify({"ValidationError": e.messages}), 400
    except Exception as e:
        return jsonify({"Exception": str(e)}), 400

    
