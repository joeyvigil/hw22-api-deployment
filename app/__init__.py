from flask import Flask
from app.blueprints import inventory
from .models import db
from .extensions import ma, limiter, cache
from .blueprints.customers import customers_bp
from .blueprints.mechanics import mechanics_bp
from .blueprints.service_mechanics import service_mechanics_bp
from .blueprints.service_tickets import service_tickets_bp
from .blueprints.inventory import inventory_bp
from .blueprints.ticket_inventory import ticket_inventory_bp
from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = '/static/swagger.yaml'  # Our API URL (can of course be a local resource)

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Mechanic Shop API - Joseph Vigil"
    }
)

def create_app(config_name):

    app = Flask(__name__) #Creating base app
    app.config.from_object(f'config.{config_name}')


    #initialize extensions (plugging them in)
    db.init_app(app)
    ma.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    
    #Register blueprints 
    app.register_blueprint(customers_bp, url_prefix='/customers')
    app.register_blueprint(mechanics_bp, url_prefix='/mechanics')
    app.register_blueprint(service_mechanics_bp, url_prefix='/service_mechanics')
    app.register_blueprint(service_tickets_bp, url_prefix='/service_tickets')
    app.register_blueprint(inventory_bp, url_prefix='/inventory')
    app.register_blueprint(ticket_inventory_bp, url_prefix='/ticket_inventory')
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL) #Registering our swagger blueprint

    return app