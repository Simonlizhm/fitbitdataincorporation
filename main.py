from flask import Flask, render_template, session, redirect, url_for, request,jsonify
from flask_sqlalchemy import SQLAlchemy
from fitbit_user import FitbitUser
from numpy import ndarray
from flask_login import LoginManager


from google_account_user import GoogleAccountUser
from email_user import EmailUser
import matplotlib.pyplot as plt

import requests, os
import openai


openai.api_key = "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"

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

fitbit_user = FitbitUser(app)
# # Get all data
# data_string = fitbit_user.get_all_data()

# # Print the data
# print(data_string)
# print(type(data_string))

class User(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    full_name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    steps_today = db.Column(db.Integer)
    total_minutes_asleep = db.Column(db.Integer)
    active_minutes = db.Column(db.Integer)
    calories_burned = db.Column(db.Integer)
    distance_covered = db.Column(db.Float)
    floors_climbed = db.Column(db.Integer)
    sedentary_minutes = db.Column(db.Integer)
    resting_heart_rate = db.Column(db.Integer)
    time_in_bed = db.Column(db.Integer)
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    is_active = db.Column(db.Boolean, default=True) 
    def get_id(self):
      return str(self.id)
  
email_user = EmailUser(app, db, User)
google_account_user = GoogleAccountUser(app, db, User)

@app.route('/chat', methods=['GET'])
def chat_get():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat_post():
    user_message = request.form['message']
    session['conversation'].append({
        "role": "user",
        "content": user_message
    })
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=session['conversation']
    )
    assistant_message = response.choices[0].message['content']
    session['conversation'].append({
        "role": "assistant",
        "content": assistant_message
    })
    return render_template('chat.html', assistant_message=assistant_message)

  
@app.route('/print_users')
def print_users():
    users = User.query.all()
    return render_template('users.html', users=users)


def print_all_users():
    users = User.query.all()
    for user in users:
        print(f"User ID: {user.id}")
        print(f"Full Name: {user.full_name}")
        print(f"Steps Today: {user.steps_today}")
        print(f"Total Minutes Asleep: {user.total_minutes_asleep}")
        print(f"Active Minutes: {user.active_minutes}")
        print(f"Calories Burned: {user.calories_burned}")
        print(f"Distance Covered: {user.distance_covered}")
        print(f"Floors Climbed: {user.floors_climbed}")
        print(f"Sedentary Minutes: {user.sedentary_minutes}")
        print(f"Resting Heart Rate: {user.resting_heart_rate}")
        print(f"Time in Bed: {user.time_in_bed}")
        print(f"Age: {user.age}")
        print(f"Gender: {user.gender}")
        print(f"Height: {user.height}")
        print(f"Weight: {user.weight}")
        print("------")
  
@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/user_profile/<string:user_id>')
def user_profile(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user_profile.html', user=user)
  
@app.route('/edit_user/<string:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        return redirect(url_for('update_user', user_id=user.id))
    return render_template('edit_user.html', user=user)

@app.route('/update_user/<string:user_id>', methods=['POST'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    resting_heart_rate = request.form['resting_heart_rate']
    if resting_heart_rate != '':
        user.resting_heart_rate = int(resting_heart_rate)
    else:
        user.resting_heart_rate = None
    user.steps_today = int(request.form['steps_today'])
    user.total_minutes_asleep = int(request.form['total_minutes_asleep'])
    user.active_minutes = int(request.form['active_minutes'])
    user.calories_burned = int(request.form['calories_burned'])
    user.distance_covered = float(request.form['distance_covered'])
    user.floors_climbed = int(request.form['floors_climbed'])
    user.sedentary_minutes = int(request.form['sedentary_minutes'])
    # user.resting_heart_rate = int(request.form['resting_heart_rate'])  # Remove this line
    user.time_in_bed = int(request.form['time_in_bed'])
    user.age = int(request.form['age'])
    user.gender = request.form['gender']
    user.height = float(request.form['height'])
    user.weight = float(request.form['weight'])
    db.session.commit()
    return redirect(url_for('dashboard'))



@app.route('/callback/google')
def google_callback():
    # Get the authorization code from the request
    auth_code = request.args.get('code')
    
    # Define the token endpoint and the data for the token request
    token_endpoint = 'https://oauth2.googleapis.com/token'
    token_data = {
        'client_id': os.environ['GOOGLE_CLIENT_ID'],
        'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
        'code': auth_code,
        'grant_type': 'authorization_code',
        'redirect_uri': 'https://fitbitdataincorporation.simonlizhm.repl.co/callback/google',
    }
    
    # Exchange the authorization code for an access token
    response = requests.post(token_endpoint, data=token_data)
    token_response = response.json()
    
    # Get the access token and id_token from the response
    access_token = token_response['access_token']
    id_token = token_response['id_token']
    
    # Define the userinfo endpoint and the headers for the request
    userinfo_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    
    # Get the user's information
    response = requests.get(userinfo_endpoint, headers=headers)
    userinfo = response.json()
    
    # Return the user's information as a JSON response
    return jsonify(userinfo)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return email_user.register(email, password)
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        return email_user.login(email, password)
    return render_template('login.html')


@app.route('/google_login')
def google_login():
    return google_account_user.google_login()

@app.route('/callback/google')
def callback_google():
    return google_account_user.google_auth()

@app.route('/google_auth')
def google_auth():
    return google_account_user.google_auth()

@app.route('/')
def index():
    if 'fitbit_token' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')
  
# @app.route('/get_user_data')
# def get_user_data():
#     fitbit_user = FitbitUser(app)
#     user_data = fitbit_user.get_all_data()
#     print(user_data)  
#     return "User data printed in console."


# @app.route('/dashboard')
# def dashboard():
#     if 'fitbit_token' not in session:
#         return redirect(url_for('index'))

#     user_id = session['fitbit_token']['user_id']
#     user = User.query.get(user_id)

#     if not user:
#         user_data = fitbit_user.get_all_data()
#         user = User(id=user_data['encodedId'], email=user_data.get('email', 'default@email.com'))
#         db.session.add(user)
#         user.full_name = user_data['full_name']
#         user.steps_today = user_data['steps_today']
#         user.total_minutes_asleep = user_data['total_minutes_asleep']
#         user.active_minutes = user_data['active_minutes']
#         user.calories_burned = user_data['calories_burned']
#         user.distance_covered = user_data['distance_covered']
#         user.floors_climbed = user_data['floors_climbed']
#         user.sedentary_minutes = user_data['sedentary_minutes']
#         user.resting_heart_rate = user_data['resting_heart_rate']
#         user.time_in_bed = user_data['time_in_bed']
#         user.age = user_data['age']
#         user.gender = user_data['gender']
#         user.height = user_data['height']
#         user.weight = user_data['weight']
#         db.session.commit()

#     weekly_data = fitbit_user.get_weekly_data()
#     monthly_data = fitbit_user.get_monthly_data()

#     return render_template('dashboard.html',
#                            dashboard_data=user,
#                            weekly_data=weekly_data,
#                            monthly_data=monthly_data)







# functional version
@app.route('/dashboard')
def dashboard():
    if 'fitbit_token' not in session:
        return redirect(url_for('index'))

    user_id = session['fitbit_token']['user_id']
    user = User.query.get(user_id)
    
    if not user:
        user_data = fitbit_user.get_all_data()
        user = User(id=user_data['encodedId'], email=user_data.get('email', 'default@email.com'))
        db.session.add(user)
        user.full_name = user_data['full_name']
        user.steps_today = user_data['steps_today']
        user.total_minutes_asleep = user_data['total_minutes_asleep']
        user.active_minutes = user_data['active_minutes']
        user.calories_burned = user_data['calories_burned']
        user.distance_covered = user_data['distance_covered']
        user.floors_climbed = user_data['floors_climbed']
        user.sedentary_minutes = user_data['sedentary_minutes']
        user.resting_heart_rate = user_data['resting_heart_rate']
        user.time_in_bed = user_data['time_in_bed']
        user.age = user_data['age']
        user.gender = user_data['gender']
        user.height = user_data['height']
        user.weight = user_data['weight']
        db.session.commit()

    # Assuming you have functions get_weekly_data and get_monthly_data
    # which return dictionaries of relevant data for the given user_id
    weekly_data = fitbit_user.get_weekly_data()

    monthly_data = fitbit_user.get_monthly_data()

    return render_template('dashboard.html', dashboard_data=user, weekly_data=weekly_data, monthly_data=monthly_data)

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/chat')
def chat():
    return render_template('chat.html')



@app.route('/callback/fitbit')
def callback_fitbit():
    return fitbit_user.callback_fitbit()


@app.route('/fitbit-login')
def fitbit_login():
    return fitbit_user.fitbit_login()
  
@app.route('/logout')
def logout():
  session.pop('fitbit_token', None)
  return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
