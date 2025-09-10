from flask import Blueprint

ticket_inventory_bp = Blueprint('ticket_inventory_bp', __name__)

from . import routes