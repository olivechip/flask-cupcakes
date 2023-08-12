from models import db, Cupcake
from app import app

db.drop_all()
db.create_all()

c1 = Cupcake(flavor="vanilla", size="large", rating=4.6, image="https://tinyurl.com/5fez7t2d")
c2 = Cupcake(flavor="chocolate", size="large", rating=4.8)
c3 = Cupcake(flavor="strawberry", size="medium", rating=3.9, image="https://tinyurl.com/c46pr9xa")
c4 = Cupcake(flavor="red velvet", size="small", rating=5.0, image="https://tinyurl.com/3f2y3v3t")

db.session.add_all([c1, c2, c3, c4])
db.session.commit()