from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

default_photo = "https://tinyurl.com/demo-cupcake"

class Cupcake(db.Model):
    """Model for Cupcake"""
    __tablename__ = 'cupcakes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    flavor = db.Column(db.Text, nullable=False)
    size = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.Text, nullable=False, default=default_photo)

    def __repr__(self):
        return f"#{self.id} - {self.flavor} - {self.size} - {self.rating} - {self.image}"
        
    def serialize_cupcake(self):
        return {
            'id': self.id,
            'flavor': self.flavor,
            'size': self.size,
            'rating': self.rating,
            'image': self.image
        }
    
