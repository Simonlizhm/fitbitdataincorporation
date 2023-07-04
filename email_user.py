from flask import request, flash, redirect, url_for
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

class EmailUser:
    def __init__(self, app, db, User):
        self.app = app
        self.db = db
        self.User = User

    def register(self, email, password):
        user = self.User.query.filter_by(email=email).first()
        if user:
            flash('Email address already registered.')
            return redirect(url_for('register'))

        new_user = self.User(email=email)
        new_user.set_password(password)
        self.db.session.add(new_user)
        self.db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))

    def login(self, email, password):
        user = self.User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login'))
