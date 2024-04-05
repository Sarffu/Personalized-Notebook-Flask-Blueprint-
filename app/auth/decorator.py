from functools import wraps
from app import app
from flask import jsonify, request, session
import jwt
from app.md.model import User


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print(request.headers)
        d = request.headers
        print(type(d))
        if "Authorization" in request.headers:

            token = request.headers["Authorization"].split()[1]
        if not token:
            return jsonify({"Message": "Token is Missing!"})
        try:
            data = jwt.decode(
                token, app.config["SECRET_KEY"], algorithms=["HS256"], options=None
            )
            current_user = User.query.filter_by(id=data["user_id"]).first()
            if current_user.id != session["user_id"]:
                return jsonify({"MEssage": "TOken in Invalid.."})
        except:
            return jsonify({"Message": "Token is invalid.."})
        return f(current_user)

    return decorated
