import os
from flask import url_for, request, redirect, session
from flask_login import login_user
from authlib.integrations.flask_client import OAuth

class GoogleAccountUser:
    def __init__(self, app, db, User):
        self.app = app
        self.db = db
        self.User = User
        self.oauth = OAuth(app)
        self.google = self.create_google_oauth_client()

    def create_google_oauth_client(self):
        google = self.oauth.register(
            name='google',
            client_id=os.environ['GOOGLE_CLIENT_ID'],
            client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
            access_token_url='https://accounts.google.com/o/oauth2/token',
            access_token_params=None,
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            authorize_params=None,
            api_base_url='https://www.googleapis.com/oauth2/v1/',
            userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
            client_kwargs={'scope': 'openid email profile'},
        )
        return google



    def google_login(self):
        google = self.google
        redirect_uri = url_for('callback_google', _external=True, _scheme='https')
        return google.authorize_redirect(redirect_uri)

    def google_auth(self):
        google = self.google
        token = google.authorize_access_token()
        resp = google.get('userinfo')
        user_info = resp.json()

        user = self.User.query.filter_by(email=user_info['email']).first()

        if not user:
            user = self.User()
            user.email = user_info['email']
            user.full_name = user_info['name']
            user.id = user_info['id']
            self.db.session.add(user)
            self.db.session.commit()

        login_user(user)
        return redirect(url_for('dashboard'))