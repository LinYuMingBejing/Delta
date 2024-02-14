from marshmallow import Schema, fields, ValidationError, validates_schema


class SizeSchema(Schema):
    name = fields.String(required=True)


class ColorSchema(Schema):
    name = fields.String(required=True)


class CategorySchema(Schema):
    name = fields.String(required=True)


class InventorySchema(Schema):
    cloth_id = fields.Integer(required=True)
    color_id = fields.Integer(required=True)
    size_id = fields.Integer(required=True)
    quantity = fields.Integer(required=True)

    @validates_schema
    def validate_inventory(self, data, **kwargs):
        if data['quantity'] > 1000 or data['quantity'] < 0:
            raise ValidationError("The number of inventory is not correct.")


class ClothInfoSchema(Schema):
    code = fields.String(required=True)
    name = fields.String(required=True)
    unit_price = fields.Integer(required=True)
    category_id = fields.Integer(required=True)
