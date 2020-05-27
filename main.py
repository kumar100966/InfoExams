import json
from flask_cors import CORS
from flask import Flask, request, render_template, redirect, flash, url_for
from flask_jwt import JWT, jwt_required, current_identity
from sqlalchemy.exc import IntegrityError
from datetime import timedelta 

from models import db, User, UserReact, Post

''' Begin boilerplate code '''

def create_app():
  app = Flask(__name__, static_url_path='')
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
  app.config['SECRET_KEY'] = "MYSECRET"
  app.config['JWT_EXPIRATION_DELTA'] = timedelta(days = 7) 
  CORS(app)

  db.init_app(app)
  return app

app = create_app()

app.app_context().push()

''' End Boilerplate Code '''

''' Set up JWT here (if using flask JWT)'''

#imported JWT code from assignment 2
def authenticate(username, password): 
	user = User.query.filter(User.username == username).first() 
	if user.check_password(password): 
		return user

def identity(payload): 
	return User.query.get(payload["identity"])

jwt = JWT(app, authenticate, identity)
''' End JWT Setup '''

@app.route('/app')
def client_app():
  return app.send_static_file('app.html')

@app.route('/')
def index():
  return app.send_static_file('index.html')


@app.route('/createPost', methods=["POST"]) 
@jwt_required()
def createPost(): 
	try: 
		post_data = request.get_json()
		post = Post(userId=current_identity.id, text=post_data["text"])
		db.session.add(post)
		db.session.commit()
	except IntegrityError: 
		return "post already exists", 409
	
	return "post created", 201


@app.route("/posts", methods=["GET"])
@jwt_required()
def list_posts(): 
  post = Post.query.all()
  list_of_post = [each.toDict() for each in post] 

  for post in list_of_post: 

    # Identifying if a post belongs to the logged in user.
    if post["userId"]==current_identity.id: 
      post["owner"] = True
    else: 
      post["owner"] = False

    # Identifying if the user had reacted to the post. 
    user_react = UserReact.query.filter(UserReact.userId == current_identity.id, UserReact.postId == post["id"]).first()
    if user_react:
      post["react"] = user_react.react
    else: 
      post["react"] = None 

  return json.dumps(list_of_post), 200 



@app.route('/reactToPost', methods=["POST"]) 
@jwt_required()
def reactToPost(): 
  try: 
    post_data = request.get_json()
    user_react = UserReact(userId=current_identity.id, postId=post_data["postId"], react=post_data["react"])

    db.session.add(user_react)
    db.session.commit()
  except IntegrityError: 
    return "user react already exists", 409

  return "user react created", 201


@app.route("/changeReact", methods=["PUT"])
@jwt_required()
def changeReact():
	post_data = request.get_json()
	user_react = UserReact.query.filter(UserReact.userId==current_identity.id, UserReact.postId==post_data["postId"]).first()

	if user_react == []: 
		return "You do not have any reacts to this post", 200

	user_react.react = post_data["react"] 
	db.session.add(user_react)
	db.session.commit() 
	return "Updated", 200 


@app.route("/mypost/<id>", methods=["DELETE"])
@jwt_required()
def delete_pokemon(id):

  my_post = Post.query.filter(Post.id==id).first()

  if my_post == []: 
    return "You do not have any Posts", 200


  db.session.delete(my_post)
  db.session.commit() 
  return "No content", 204




if __name__ == '__main__':
  app.run(host='127.0.0.1', port=8080, debug=True)
