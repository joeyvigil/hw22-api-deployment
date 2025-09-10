from app.extensions import ma
from app.models import Inventory, db


class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory 
        include_fk=True

inventory_schema = InventorySchema() 
inventorys_schema = InventorySchema(many=True) 