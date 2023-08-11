from models import db, Cupcake
from app import app

db.drop_all()
db.create_all()

c1 = Cupcake(flavor="vanilla", size="large", rating=4.6)
c2 = Cupcake(flavor="chocolate", size="large", rating=4.8)
c3 = Cupcake(flavor="strawberry", size="medium", rating=3.9)
c4 = Cupcake(flavor="red velvet", size="small", rating=5.0)

db.session.add_all([c1, c2, c3, c4])
db.session.commit()