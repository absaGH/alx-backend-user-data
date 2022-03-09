#!/usr/bin/env python3
"""
Flask app module
"""
from flask import Flask, escape, request, jsonify, abort, redirect
from auth import Auth
from sqlalchemy.orm.exc import NoResultFound

app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def welcome() -> str:
    """ Welcome Json
    """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def register_user() -> str:
    """ end-point to register user
    """

    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": "{}".format(user.email),
                        "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@ app.route('/sessions', methods=['POST'])
def login() -> str:
    """ Login User session"""
    try:
        email = request.form['email']
        pwd = request.form['password']
    except KeyError:
        abort(401)

    if (AUTH.valid_login(email, pwd)):
        session_id = AUTH.create_session(email)
        if session_id is not None:
            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie("session_id", session_id)
            return response

    abort(401)


@ app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """ Destroye session using session_id
    """
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)
        if user:
            AUTH.destroy_session(user.id)
            return redirect("http://0.0.0.0:5000/")
    abort(403)


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """ takes session_id & respond with profile Json
    """
    sessionID = request.cookies.get('session_id')
    if sessionID:
        user = AUTH.get_user_from_session_id(sessionID)
        if user:
            return jsonify({"email": user.email})
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
