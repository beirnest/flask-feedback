from models import db
from app import app

app = app

with app.app_context():
    db.drop_all()
    db.create_all()