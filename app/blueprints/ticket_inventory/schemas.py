from app.extensions import ma
from app.models import TicketInventory, db


class TicketInventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = TicketInventory 
        include_fk=True

ticket_inventory_schema = TicketInventorySchema() 
ticket_inventorys_schema = TicketInventorySchema(many=True) 
