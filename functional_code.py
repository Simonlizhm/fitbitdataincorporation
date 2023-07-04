# class FitbitAssistant:
#     def __init__(self, api_key):
#         self.examples = [
#             {
#         "query": "Why am I not seeing improvements in my running distance?",
#         "data": "steps_today: 5000, total_minutes_asleep: 360, active_minutes: 30, calories_burned: 1800, distance_covered: 2.5, floors_climbed: 10, sedentary_minutes: 1000, resting_heart_rate: 68, time_in_bed: 390, age: 35, gender: 'Female', height: 165, weight: 65",
#         "recommendation": "You seem to be leading a sedentary lifestyle with only 30 active minutes per day. To improve your running distance, try increasing your active minutes gradually, focusing particularly on cardio exercises. This could help improve your stamina and endurance over time."
#     },
#     {
#         "query": "I've been feeling unusually tired recently. Can you suggest why?",
#         "data": "steps_today: 4000, total_minutes_asleep: 240, active_minutes: 50, calories_burned: 2000, distance_covered: 3.0, floors_climbed: 5, sedentary_minutes: 1200, resting_heart_rate: 76, time_in_bed: 300, age: 45, gender: 'Male', height: 175, weight: 78",
#         "recommendation": "Your data suggests that you're not getting enough sleep - the total minutes asleep is only 240, which is less than the recommended 7-9 hours per night for adults. Lack of sufficient sleep could be contributing to your feelings of tiredness."
#     },
#     {
#         "query": "I am not losing weight despite regular exercise. What could be the reason?",
#         "data": "steps_today: 8000, total_minutes_asleep: 420, active_minutes: 120, calories_burned: 2500, distance_covered: 6.0, floors_climbed: 10, sedentary_minutes: 800, resting_heart_rate: 72, time_in_bed: 450, age: 30, gender: 'Female', height: 170, weight: 80",
#         "recommendation": "You are burning 2500 calories per day which is commendable, however, weight management isn't solely about exercise. The other crucial component is diet. If you're consuming more calories than you're burning, you may not see a weight loss even with regular exercise. Try to maintain a balanced diet and consider speaking to a dietitian if needed."
#     },
#     {
#         "query": "I'm finding it hard to catch my breath during workouts. Could it be something serious?",
#         "data": "steps_today: 6000, total_minutes_asleep: 450, active_minutes: 100, calories_burned: 2200, distance_covered: 4.0, floors_climbed: 30, sedentary_minutes: 800, resting_heart_rate: 85, time_in_bed: 500, age: 38, gender: 'Female', height: 170, weight: 68",
#         "recommendation": "Your resting heart rate is a bit on the higher side, which might be contributing to your breathlessness. Also, climbing 30 floors is strenuous and can result in breathlessness especially if you're not conditioned for it. However, if this is a recent development and/or the breathlessness is severe, it's advised to consult with a healthcare professional."
#     },
#         ]
#         self.example_formatter_template = """
#             Query: {query}
#             Data: {data}
#             Recommendation: {recommendation}
#             """
#         self.example_prompt = PromptTemplate(
#             input_variables=["query", "data"],
#             template=self.example_formatter_template,
#         )
#         openai.api_key = "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"
      
#     # def setup_routes(self):
#     #     @self.app.route('/', methods=['GET', 'POST'])
#     #     def chat():
#     #         if request.method == 'POST':
#     #             user_query = request.form['query']
#     #             ai_response = ai_model.generate_recommendations(user_query)
#     #             return jsonify(ai_response)
#     #         else:
#     #             return render_template('chat.html')
#     def load_fitbit_data(self):
#         return "steps_today: 5000, total_minutes_asleep: 360, active_minutes: 30, calories_burned: 1800, distance_covered: 2.5, floors_climbed: 10, sedentary_minutes: 1000, resting_heart_rate: 68, time_in_bed: 390, age: 35, gender: 'Female', height: 165, weight: 65"

#     def generate_recommendations(self, query): 
#         data = self.load_fitbit_data()
#         llm_complete = OpenAI(model_name="gpt-3.5-turbo", n=1, best_of=1)
#         example_prompt = PromptTemplate(
#             input_variables = ["query", "data", "recommendation"],
#             template = self.example_formatter_template,
#         )
#         few_shot_prompt = FewShotPromptTemplate(
#             examples = self.examples, 
#             example_prompt = example_prompt,
#             prefix = "You are a health assistant. Given the user query related to health and data points steps_today, total_minutes_asleep, active_minutes, calories_burned, distance_covered, floors_climbed, sedentary_minutes, resting_heart_rate, time_in_bed, age, gender, height and weight, provide a relevant medical recommendation. If the data points don't suggest a clear recommendation, advise to consult with a healthcare professional.",
#             suffix = "Query: {query}\nData: {data}\nRecommendation:", 
#             input_variables = ["query", "data"]
#         )
#         final_prompt= few_shot_prompt.format(
#             query = query.strip(), 
#             data = data.strip(),
#         )
#         return llm_complete(final_prompt)


# if __name__ == '__main__':
#   fitbit_user = FitbitUser()
#   assistant = FitbitAssistant('your-api-key')
#   query = input("Please enter your health query: ") 
#   print(assistant.generate_recommendations(query))

<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Dashboard</title>
</head>
<body>
    <a href="{{ url_for('chatbot') }}">Go to Chatbot</a>
    <h1>Welcome, {{ dashboard_data.full_name }}!</h1>
    <h2>Today's Stats</h2>
    <ul>
        <li>Steps Today: {{ dashboard_data.steps_today }}</li>
        <li>Total Minutes Asleep: {{ dashboard_data.total_minutes_asleep }}</li>
        <li>Active Minutes: {{ dashboard_data.active_minutes }}</li>
        <li>Calories Burned: {{ dashboard_data.calories_burned }}</li>
        <li>Distance Covered: {{ dashboard_data.distance_covered }}</li>
        <li>Floors Climbed: {{ dashboard_data.floors_climbed }}</li>
        <li>Sedentary Minutes: {{ dashboard_data.sedentary_minutes }}</li>
        <li>Resting Heart Rate: {{ dashboard_data.resting_heart_rate }}</li>
        <li>Time in Bed: {{ dashboard_data.time_in_bed }}</li>
    </ul>

    <h2>Profile Information</h2>
    <ul>
        <li>Age: {{ dashboard_data.age }}</li>
        <li>Gender: {{ dashboard_data.gender }}</li>
        <li>Height: {{ dashboard_data.height }}</li>
        <li>Weight: {{ dashboard_data.weight }}</li>
    </ul>

    <h2>Weekly Data</h2>
    <ul>
        <li>Weekly Steps: {{ weekly_data.steps }}</li>
        <li>Weekly Sleep: {{ weekly_data.sleep }}</li>
        <li>Weekly Heart Rate: {{ weekly_data.heart_rate }}</li>
        <li>Weekly Exercise: {{ weekly_data.exercise }}</li>
    </ul>

    <h2>Monthly Data</h2>
    <ul>
        <li>Monthly Steps: {{ monthly_data.steps }}</li>
        <li>Monthly Sleep: {{ monthly_data.sleep }}</li>
        <li>Monthly Heart Rate: {{ monthly_data.heart_rate }}</li>
        <li>Monthly Exercise: {{ monthly_data.exercise }}</li>
    </ul>

    <a href="{{ url_for('edit_user', user_id=dashboard_data.id) }}">Edit Your Information</a><br>
    <a href="{{ url_for('logout') }}">Logout</a>

</body>
</html>



<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Dashboard</title>
</head>
<body>
    <h1>Welcome, {{ dashboard_data.full_name }}!</h1>
    <h2>Today's Stats</h2>
    <ul>
        <li>Steps Today: {{ dashboard_data.steps_today }}</li>
        <li>Total Minutes Asleep: {{ dashboard_data.total_minutes_asleep }}</li>
        <li>Active Minutes: {{ dashboard_data.active_minutes }}</li>
        <li>Calories Burned: {{ dashboard_data.calories_burned }}</li>
        <li>Distance Covered: {{ dashboard_data.distance_covered }}</li>
        <li>Floors Climbed: {{ dashboard_data.floors_climbed }}</li>
        <li>Sedentary Minutes: {{ dashboard_data.sedentary_minutes }}</li>
        <li>Resting Heart Rate: {{ dashboard_data.resting_heart_rate }}</li>
        <li>Time in Bed: {{ dashboard_data.time_in_bed }}</li>
    </ul>

    <h2>Profile Information</h2>
    <ul>
        <li>Age: {{ dashboard_data.age }}</li>
        <li>Gender: {{ dashboard_data.gender }}</li>
        <li>Height: {{ dashboard_data.height }}</li>
        <li>Weight: {{ dashboard_data.weight }}</li>
    </ul>

    <h2>Weekly Data</h2>
    <ul>
        <li>Weekly Steps: {{ weekly_data.steps }}</li>
        <li>Weekly Sleep: {{ weekly_data.sleep }}</li>
        <li>Weekly Heart Rate: {{ weekly_data.heart_rate }}</li>
        <li>Weekly Exercise: {{ weekly_data.exercise }}</li>
    </ul>

    <h2>Monthly Data</h2>
    <ul>
        <li>Monthly Steps: {{ monthly_data.steps }}</li>
        <li>Monthly Sleep: {{ monthly_data.sleep }}</li>
        <li>Monthly Heart Rate: {{ monthly_data.heart_rate }}</li>
        <li>Monthly Exercise: {{ monthly_data.exercise }}</li>
    </ul>

    <a href="{{ url_for('edit_user', user_id=dashboard_data.id) }}">Edit Your Information</a><br>
    <a href="{{ url_for('logout') }}">Logout</a>
</body>
</html>




# 1. display the trend for users' data in the past week and try to acquire the data from fitbit API
# 2. collect the data and organize it into a csv

# from flask import Flask, render_template, session, redirect, url_for, request,jsonify
# from flask_sqlalchemy import SQLAlchemy
# from fitbit_user import FitbitUser
# from google_account_user import GoogleAccountUser
# from email_user import EmailUser
# import requests, os
# from flask_login import LoginManager, login_required, current_user, logout_user, UserMixin

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user_data.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

# fitbit_user = FitbitUser(app)

# class User(db.Model):
#     id = db.Column(db.String(10), primary_key=True)
#     full_name = db.Column(db.String(100))
#     email = db.Column(db.String(100), unique=True, nullable=False)
#     steps_today = db.Column(db.Integer)
#     total_minutes_asleep = db.Column(db.Integer)
#     active_minutes = db.Column(db.Integer)
#     calories_burned = db.Column(db.Integer)
#     distance_covered = db.Column(db.Float)
#     floors_climbed = db.Column(db.Integer)
#     sedentary_minutes = db.Column(db.Integer)
#     resting_heart_rate = db.Column(db.Integer)
#     time_in_bed = db.Column(db.Integer)
#     age = db.Column(db.Integer)
#     gender = db.Column(db.String(10))
#     height = db.Column(db.Float)
#     weight = db.Column(db.Float)
#     is_active = db.Column(db.Boolean, default=True) 
#     def get_id(self):
#       return str(self.id)
  
# email_user = EmailUser(app, db, User)
# google_account_user = GoogleAccountUser(app, db, User)

  
# @app.route('/print_users')
# def print_users():
#     users = User.query.all()
#     return render_template('users.html', users=users)


# def print_all_users():
#     users = User.query.all()
#     for user in users:
#         print(f"User ID: {user.id}")
#         print(f"Full Name: {user.full_name}")
#         print(f"Steps Today: {user.steps_today}")
#         print(f"Total Minutes Asleep: {user.total_minutes_asleep}")
#         print(f"Active Minutes: {user.active_minutes}")
#         print(f"Calories Burned: {user.calories_burned}")
#         print(f"Distance Covered: {user.distance_covered}")
#         print(f"Floors Climbed: {user.floors_climbed}")
#         print(f"Sedentary Minutes: {user.sedentary_minutes}")
#         print(f"Resting Heart Rate: {user.resting_heart_rate}")
#         print(f"Time in Bed: {user.time_in_bed}")
#         print(f"Age: {user.age}")
#         print(f"Gender: {user.gender}")
#         print(f"Height: {user.height}")
#         print(f"Weight: {user.weight}")
#         print("------")
  
# @app.before_first_request
# def create_tables():
#     db.create_all()

# @app.route('/user_profile/<string:user_id>')
# def user_profile(user_id):
#     user = User.query.get_or_404(user_id)
#     return render_template('user_profile.html', user=user)
  
# @app.route('/edit_user/<string:user_id>', methods=['GET', 'POST'])
# def edit_user(user_id):
#     user = User.query.get_or_404(user_id)
#     if request.method == 'POST':
#         return redirect(url_for('update_user', user_id=user.id))
#     return render_template('edit_user.html', user=user)

# @app.route('/update_user/<string:user_id>', methods=['POST'])
# def update_user(user_id):
#     user = User.query.get_or_404(user_id)
#     resting_heart_rate = request.form['resting_heart_rate']
#     if resting_heart_rate != '':
#         user.resting_heart_rate = int(resting_heart_rate)
#     else:
#         user.resting_heart_rate = None
#     user.steps_today = int(request.form['steps_today'])
#     user.total_minutes_asleep = int(request.form['total_minutes_asleep'])
#     user.active_minutes = int(request.form['active_minutes'])
#     user.calories_burned = int(request.form['calories_burned'])
#     user.distance_covered = float(request.form['distance_covered'])
#     user.floors_climbed = int(request.form['floors_climbed'])
#     user.sedentary_minutes = int(request.form['sedentary_minutes'])
#     # user.resting_heart_rate = int(request.form['resting_heart_rate'])  # Remove this line
#     user.time_in_bed = int(request.form['time_in_bed'])
#     user.age = int(request.form['age'])
#     user.gender = request.form['gender']
#     user.height = float(request.form['height'])
#     user.weight = float(request.form['weight'])
#     db.session.commit()
#     return redirect(url_for('dashboard'))



# @app.route('/callback/google')
# def google_callback():
#     # Get the authorization code from the request
#     auth_code = request.args.get('code')
    
#     # Define the token endpoint and the data for the token request
#     token_endpoint = 'https://oauth2.googleapis.com/token'
#     token_data = {
#         'client_id': os.environ['GOOGLE_CLIENT_ID'],
#         'client_secret': os.environ['GOOGLE_CLIENT_SECRET'],
#         'code': auth_code,
#         'grant_type': 'authorization_code',
#         'redirect_uri': 'https://fitbitdataincorporation.simonlizhm.repl.co/callback/google',
#     }
    
#     # Exchange the authorization code for an access token
#     response = requests.post(token_endpoint, data=token_data)
#     token_response = response.json()
    
#     # Get the access token and id_token from the response
#     access_token = token_response['access_token']
#     id_token = token_response['id_token']
    
#     # Define the userinfo endpoint and the headers for the request
#     userinfo_endpoint = 'https://www.googleapis.com/oauth2/v1/userinfo'
#     headers = {'Authorization': f'Bearer {access_token}'}
    
#     # Get the user's information
#     response = requests.get(userinfo_endpoint, headers=headers)
#     userinfo = response.json()
    
#     # Return the user's information as a JSON response
#     return jsonify(userinfo)


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         return email_user.register(email, password)
#     return render_template('register.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['password']
#         return email_user.login(email, password)
#     return render_template('login.html')


# @app.route('/google_login')
# def google_login():
#     return google_account_user.google_login()

# @app.route('/callback/google')
# def callback_google():
#     return google_account_user.google_auth()

# @app.route('/google_auth')
# def google_auth():
#     return google_account_user.google_auth()

# @app.route('/')
# def index():
#     if 'fitbit_token' in session:
#         return redirect(url_for('dashboard'))
#     return render_template('index.html')


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

#     return render_template('dashboard.html', dashboard_data=user)


# @app.route('/callback/fitbit')
# def callback_fitbit():
#     return fitbit_user.callback_fitbit()


# @app.route('/fitbit-login')
# def fitbit_login():
#     return fitbit_user.fitbit_login()
  
# @app.route('/logout')
# def logout():
#   session.pop('fitbit_token', None)
#   return redirect(url_for('index'))



# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0')


## fitbit_user.py

# from flask import url_for, request, redirect, session
# import requests
# from dotenv import load_dotenv
# from requests_oauthlib import OAuth2Session
# import base64
# import os

# FITBIT_CLIENT_ID = '23QZ6Y'
# FITBIT_CLIENT_SECRET = '0ab29d7e9a448844b4bfb0c889e56cd9'
# FITBIT_AUTH_URL = 'https://www.fitbit.com/oauth2/authorize'
# FITBIT_TOKEN_URL = 'https://api.fitbit.com/oauth2/token'
# FITBIT_REDIRECT_URL = 'https://fitbitdataincorporation.simonlizhm.repl.co/callback/fitbit'


# class FitbitUser:
#     def __init__(self, app):
#         load_dotenv()
#         self.app = app
#         self.client_id = os.environ['FITBIT_CLIENT_ID']
#         self.client_secret = os.environ['FITBIT_CLIENT_SECRET']
#         self.redirect_uri = os.environ['FITBIT_REDIRECT_URI']
#         self.scope = ['activity', 'heartrate', 'sleep', 'profile']

#     def _get_oauth_session(self):
#         oauth = OAuth2Session(
#             self.client_id,
#             redirect_uri=self.redirect_uri,
#             scope=self.scope,
#             token=session.get('fitbit_token')
#         )
#         return oauth

#     def logout(self):
#         session.pop('fitbit_token', None)

#     def fitbit_login(self):
#       auth_url = f"{FITBIT_AUTH_URL}?response_type=code&client_id={FITBIT_CLIENT_ID}&redirect_uri={url_for('callback_fitbit', _external=True, _scheme='https')}&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&prompt=login"
#       return redirect(auth_url)


#     def callback_fitbit(self):
#         code = request.args.get('code')
#         if code:
#             token = self.fetch_fitbit_token(code)
#             session['fitbit_token'] = token
#         return redirect(url_for('dashboard'))

#     def fetch_fitbit_token(self, code):
#         headers = {
#             'Authorization': 'Basic ' + base64.b64encode(f"{FITBIT_CLIENT_ID}:{FITBIT_CLIENT_SECRET}".encode('utf-8')).decode('utf-8'),
#             'Content-Type': 'application/x-www-form-urlencoded'
#         }
#         data = {
#             'client_id': FITBIT_CLIENT_ID,
#             'grant_type': 'authorization_code',
#             'redirect_uri': url_for('callback_fitbit', _external=True, _scheme='https'),
#             'code': code
#         }
#         response = requests.post(FITBIT_TOKEN_URL, headers=headers, data=data)
#         token_data = response.json()
#         return token_data

#     def get_fitbit_data(self, endpoint_url, access_token):
#         headers = {"Authorization": f"Bearer {access_token}"}
#         data = requests.get(endpoint_url, headers=headers).json()
#         return data

#     def get_all_data(self):
#         access_token = session['fitbit_token']['access_token']
#         user_info = self.get_fitbit_data('https://api.fitbit.com/1/user/-/profile.json', access_token)
#         daily_activity = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/date/today.json', access_token)
#         sleep_data = self.get_fitbit_data('https://api.fitbit.com/1.2/user/-/sleep/date/today.json', access_token)
#         heart_rate_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json', access_token)
#         exercise_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/list.json?afterDate=today&offset=0&limit=20&sort=desc', access_token)
#         weight_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/body/log/weight/date/today/1d.json', access_token)
    
#         if 'user' not in user_info:
#             user_info['user'] = {}
      
#         summary = daily_activity.get('summary', {})
#         distances = summary.get('distances', [{}])
#         activities_heart = heart_rate_data.get('activities-heart', [{}])
#         value = activities_heart[0].get('value', {})
    
#         return {
#             "encodedId": user_info['user'].get('encodedId', 'N/A'),
#             "full_name": user_info['user'].get('fullName', 'N/A'),
#             "steps_today": summary.get('steps', 0),
#             "total_minutes_asleep": sleep_data['summary'].get('totalMinutesAsleep', 0),
#             "active_minutes": summary.get('fairlyActiveMinutes', 0) + summary.get('veryActiveMinutes', 0),
#             "calories_burned": summary.get('caloriesOut', 0),
#             "distance_covered": distances[0].get('distance', 0),
#             "floors_climbed": summary.get('floors', 0),
#             "sedentary_minutes": summary.get('sedentaryMinutes', 0),
#             "resting_heart_rate": value.get('restingHeartRate', None),
#             "time_in_bed": sleep_data['summary'].get('totalTimeInBed', 0),
#             "age": user_info['user'].get('age', None),
#             "gender": user_info['user'].get('gender', None),
#             "height": user_info['user'].get('height', None),
#             "weight": weight_data.get('weight', [])[0].get('weight', None) if weight_data.get('weight') else user_info['user'].get('weight', None),
#             "user_info": user_info,
#             "daily_activity": daily_activity,
#             "sleep_data": sleep_data,
#             "heart_rate_data": heart_rate_data,
#             "exercise_data": exercise_data,
#             "weight_data": weight_data
#         }
# import os
# from flask import url_for, request, redirect, session
# from flask_login import login_user
# from authlib.integrations.flask_client import OAuth

# class GoogleAccountUser:
#     def __init__(self, app, db, User):
#         self.app = app
#         self.db = db
#         self.User = User
#         self.oauth = OAuth(app)
#         self.google = self.create_google_oauth_client()

#     def create_google_oauth_client(self):
#         google = self.oauth.register(
#             name='google',
#             client_id=os.environ['GOOGLE_CLIENT_ID'],
#             client_secret=os.environ['GOOGLE_CLIENT_SECRET'],
#             access_token_url='https://accounts.google.com/o/oauth2/token',
#             access_token_params=None,
#             authorize_url='https://accounts.google.com/o/oauth2/auth',
#             authorize_params=None,
#             api_base_url='https://www.googleapis.com/oauth2/v1/',
#             userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#             client_kwargs={'scope': 'openid email profile'},
#         )
#         return google



#     def google_login(self):
#         google = self.google
#         redirect_uri = url_for('callback_google', _external=True, _scheme='https')
#         return google.authorize_redirect(redirect_uri)

#     def google_auth(self):
#         google = self.google
#         token = google.authorize_access_token()
#         resp = google.get('userinfo')
#         user_info = resp.json()

#         user = self.User.query.filter_by(email=user_info['email']).first()

#         if not user:
#             user = self.User()
#             user.email = user_info['email']
#             user.full_name = user_info['name']
#             user.id = user_info['id']
#             self.db.session.add(user)
#             self.db.session.commit()

#         login_user(user)
#         return redirect(url_for('dashboard'))

# <!doctype html>
# <html lang="en">
# <head>
#     <meta charset="utf-8">
#     <title>Dashboard</title>
# </head>
# <body>
#     <h1>Welcome, {{ dashboard_data.full_name }}!</h1>
#     <h2>Today's Stats</h2>
#     <ul>
#         <li>Steps Today: {{ dashboard_data.steps_today }}</li>
#         <li>Total Minutes Asleep: {{ dashboard_data.total_minutes_asleep }}</li>
#         <li>Active Minutes: {{ dashboard_data.active_minutes }}</li>
#         <li>Calories Burned: {{ dashboard_data.calories_burned }}</li>
#         <li>Distance Covered: {{ dashboard_data.distance_covered }}</li>
#         <li>Floors Climbed: {{ dashboard_data.floors_climbed }}</li>
#         <li>Sedentary Minutes: {{ dashboard_data.sedentary_minutes }}</li>
#         <li>Resting Heart Rate: {{ dashboard_data.resting_heart_rate }}</li>
#         <li>Time in Bed: {{ dashboard_data.time_in_bed }}</li>
#     </ul>

#     <h2>Profile Information</h2>
#     <ul>
#         <li>Age: {{ dashboard_data.age }}</li>
#         <li>Gender: {{ dashboard_data.gender }}</li>
#         <li>Height: {{ dashboard_data.height }}</li>
#         <li>Weight: {{ dashboard_data.weight }}</li>
#     </ul>

#     <a href="{{ url_for('edit_user', user_id=dashboard_data.id) }}">Edit Your Information</a><br>
#     <a href="{{ url_for('logout') }}">Logout</a>
# </body>
# </html>



## login.html
# <!doctype html>
# <html lang="en">
# <head>
#     <meta charset="utf-8">
#     <title>Login</title>
# </head>
# <body>
#     <h1>Login</h1>
#     <form method="POST" action="{{ url_for('login') }}">
#         {{ form.hidden_tag() }}
#         <p>Email: {{ form.email.label }} {{ form.email() }}</p>
#         <p>Password: {{ form.password.label }} {{ form.password() }}</p>
#         <input type="submit" value="Login">
#     </form>
#     <h2>Or</h2>
#     <p>Login with Google</p>
#     <a href="{{ url_for('google_login') }}"><img src="https://developers.google.com/identity/images/btn_google_signin_dark_normal_web.png" alt="Login with Google"></a>
#     <p>Login with Fitbit</p>
#     <a href="{{ url_for('fitbit_login') }}"><img src="https://upload.wikimedia.org/wikipedia/commons/thumb/a/a3/Fitbit_logo16.svg/1280px-Fitbit_logo16.svg.png" alt="Login with Fitbit" width="120"></a>
# </body>
# </html>
