import json
import os
from datetime import datetime, timedelta

import requests
from flask import Flask, render_template, redirect, url_for, flash, abort, request, current_app, jsonify, make_response, \
    Response
from flask_admin import Admin
from markupsafe import Markup

from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app= Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

with app.app_context():

    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_name = db.Column(db.String(1000))
        user_email = db.Column(db.String(1000))
        user_password = db.Column(db.String(1000))
        user_number = db.Column(db.String(1000))
    db.create_all()


    class MyModelView(ModelView):
        def is_accessible(self):
            return True

admin = Admin(app)
admin.add_view(MyModelView(User, db.session))

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about_us")
def about_us():
    return render_template("about.html")

@app.route("/classes")
def classes():
    return render_template("classes.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/login")
def login():

    if request.method == "POST":
        user_name = request.form.get("user_name")
        user_password = request.form.get("user_password")

        user = User(
            user_name=user_name,
            user_password=user_password
        )
        db.session.add(user)
        db.session.commit()

    return render_template("login.html")


if __name__ =="__main__":
    app.run(debug=True)