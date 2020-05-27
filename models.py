from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


db = SQLAlchemy()

#Code imported from assignment 2

#Class to model User
class User(db.Model):
	id = db.Column('id', db.Integer, primary_key=True) 
	username = db.Column("username", db.String(50), unique=True, nullable=False) 
	email = db.Column("email", db.String(50), unique=True, nullable=False) 
	password = db.Column("password", db.String(50)) 

	def toDict(self): 
		return {
			"id": self.id, 
			"username": self.username, 
			"email": self.email, 
			"password": self.password
		}

	def set_password(self, password): 
		self.password = generate_password_hash(password, method="sha256")

	def check_password(self, password): 
		return check_password_hash(self.password, password) 





class Post(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))
    text = db.Column('text', db.String(50))
    reacts = db.relationship("UserReact")
    likes = 0 
    dislikes = 0



    def toDict(self):
        return{
            "id": self.id,  
            "userId": self.userId,
            "text": self.text,
            "defense": self.defense, 
            
        }