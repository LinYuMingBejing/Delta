from app import db
from datetime import datetime

EXCLUDED_FIELDS = ['category_id', 'creation_date', 'modified_date']


class BaseModel():
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creation_date = db.Column(db.DateTime, default=datetime.now, nullable=False)
    modified_date = db.Column(db.DateTime, onupdate=datetime.now, default=datetime.now, nullable=False)
    
    def to_dict(self):
        return {column.name: getattr(self, column.name, None) for column in self.__table__.columns if column.name not in EXCLUDED_FIELDS}
        
    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Size(BaseModel, db.Model):
    __tablename__ = 'size'
    __bind_key__  = 'external_database'

    name = db.Column(db.String(30), unique=True, nullable=False)

    clothes = db.relationship('Inventory', backref=db.backref('sizes', ))
    

class Color(BaseModel, db.Model):
    __tablename__ = 'color'

    name = db.Column(db.String(30), unique=True, nullable=False)

    clothes = db.relationship('Inventory', backref=db.backref('colors'))


class Category(BaseModel, db.Model):
    __tablename__ = 'category'

    name = db.Column(db.String(30), unique=True, nullable=False)

    clothes = db.relationship('ClothInfo', backref=db.backref('category'))

    def find(self):
        return self.query.first()
    

class Inventory(BaseModel, db.Model):
    __tablename__ = 'inventory'

    cloth_id = db.Column(db.Integer, db.ForeignKey('cloth.id'), nullable=False)
    color_id = db.Column(db.Integer, db.ForeignKey('color.id'), nullable=False)
    size_id = db.Column(db.Integer, db.ForeignKey('size.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    meta = {
        'indexes': [
            'inventory',
            ('cloth_id', 'color_id', 'size_id',),
        ]
    }


class ClothInfo(BaseModel, db.Model):
    __tablename__ = 'cloth'

    code = db.Column(db.String(30), unique=True, nullable=False)
    name = db.Column(db.String(30), nullable=False)
    unit_price = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    cloth_info = db.relationship('Inventory', backref=db.backref('info'))

    def to_dict(self):
        base_dict = super().to_dict()
        base_dict['category'] = self.category.name
        return base_dict