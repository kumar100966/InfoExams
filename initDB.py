from main import app
from models import db, User


db.create_all(app=app)

user1 = User(username="bob", email="bob@mail.com")
user1.set_password("bobpass")
user2 = User(username="alice",  email="alice@mail.com")
user2.set_password("alicepass")
db.session.add(user1)
db.session.add(user2)
db.session.commit()
print('database initialized!')