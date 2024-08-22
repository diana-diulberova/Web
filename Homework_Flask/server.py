from flask import Flask, jsonify, request, Response
from flask.views import MethodView
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError
from schema import UserCreate, UserUpdate, CreatePost, UpdatePost
import flask_bcrypt
from models import User, Session, Post

app = Flask('app')
bcrypt = flask_bcrypt.Bcrypt(app)


def hash_password(password: str) -> str:
    password = password.encode()
    password = bcrypt.generate_password_hash(password)
    password = password.decode()
    return password


def check_password(user_password: str, db_password: str) -> bool:
    user_password = user_password.encode()
    db_password = db_password.encode()
    return bcrypt.check_password_hash(db_password, user_password)


class ApiError(Exception):
    def __init__(self, status_code, msg):
        self.status_code = status_code
        self.msg = msg


@app.errorhandler(ApiError)
def error_handler(err: ApiError):
    http_response = jsonify({"error": err.msg})
    http_response.status_code = err.status_code
    return http_response


@app.before_request
def before_request():
    session = Session()
    request.session = session


@app.after_request
def after_request(http_response: Response):
    request.session.close()
    return http_response


def validate(json_data, schema_cls):
    try:
        return schema_cls(**json_data).dict(exclude_unset=True)
    except ValidationError as err:
        error = err.errors()[0]
        error.pop('ctx', None)
        raise ApiError(400, error)


def get_user(user_id: int):
    user = request.session.get(User, user_id)
    if user is None:
        raise ApiError(404, "user not found")
    return user


def add_user(user: User):
    try:
        request.session.add(user)
        request.session.commit()
    except IntegrityError:
        raise ApiError(409, "user already exists")
    return user


def add_post(post: Post):
    try:
        request.session.add(post)
        request.session.commit()
    except Exception:
        raise ApiError(400, "post error")
    return post


def get_post(post_id):
    post = request.session.get(Post, post_id)
    if post is None:
        raise ApiError(404, "post not found")
    return post


class UserView(MethodView):
    def get(self, user_id: int):
        user = get_user(user_id)
        return jsonify(user.json())

    def post(self):
        json_data = validate(request.json, UserCreate)
        new_user = User(
            name=json_data["name"],
            password=hash_password(json_data["password"])
        )
        new_user = add_user(new_user)
        return new_user.json()

    def patch(self, user_id: int):
        json_data = validate(request.json, UserUpdate)
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        user = get_user(user_id)
        for field, value in json_data.items():
            setattr(user, field, value)
        user = add_user(user)
        return jsonify(user.json())

    def delete(self, user_id):
        user = get_user(user_id)
        request.session.delete(user)
        request.session.commit()
        return jsonify({"status": "deleted"})


class PostView(MethodView):
    def get(self, post_id):
        post = get_post(post_id)
        return jsonify(post.json())

    def post(self):
        json_data = validate(request.json, CreatePost)
        new_post = Post(
            heading=json_data["heading"],
            description=json_data["description"],
            user_id=json_data["user_id"]
        )
        new_post = add_post(new_post)
        return new_post.json()

    def patch(self, post_id: int):
        json_data = validate(request.json, UpdatePost)
        post = get_post(post_id)
        for field, value in json_data.items():
            setattr(post, field, value)
        post = add_post(post)
        return jsonify(post.json())

    def delete(self, post_id):
        post = get_post(post_id)
        request.session.delete(post)
        request.session.commit()
        return jsonify({'status': 'deleted'})


user_view = UserView.as_view("user")
app.add_url_rule("/user/<int:user_id>", view_func=user_view, methods=["GET", "PATCH", "DELETE"])
app.add_url_rule("/user", view_func=user_view, methods=["POST"])

post_view = PostView.as_view("post")
app.add_url_rule("/post/<int:post_id>", view_func=post_view, methods=["GET", "PATCH", "DELETE"])
app.add_url_rule("/post", view_func=post_view, methods=["POST"])

app.run()
