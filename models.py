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



class UserReact(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	userId = db.Column('userId', db.Integer, db.ForeignKey('user.id'))
	postId = db.Column('postId', db.Integer, db.ForeignKey('post.id'))
	react = db.Column("react", db.String(10))
	#Look at only storing two possible string values within the attribute. 






class Post(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	userId = db.Column(db.Integer, db.ForeignKey('user.id'))
	text = db.Column('text', db.String(50))
	reacts = db.relationship("UserReact")

	def getTotalLikes(self):
		reacts = UserReact.query.filter(UserReact.postId==self.id).all()
		like = 0
		if reacts:
			for react in reacts: 
				if react.react == "like": 
					like +=1
			return like
		return 0

	def getTotalDislikes(self):
		reacts = UserReact.query.filter(UserReact.postId==self.id).all()
		dislike = 0
		if reacts:
			for react in reacts: 
				if react.react == "dislike": 
					dislike +=1
			return dislike
		return 0



	def toDict(self):

		user = User.query.filter(User.id == self.userId).first()

		return{
			"id": self.id,  
			"userId": self.userId,
			"username": user.username, 
			"text": self.text,
			"likes": self.getTotalLikes(), 
			"dislikes": self.getTotalDislikes()
		}