# fitbit_user.py

from flask import url_for, request, redirect, session
import requests
from dotenv import load_dotenv
from requests_oauthlib import OAuth2Session
import base64
import json
import os

load_dotenv()
FITBIT_CLIENT_ID = os.getenv('FITBIT_CLIENT_ID', '23QZ6Y')
FITBIT_CLIENT_SECRET = os.getenv('FITBIT_CLIENT_SECRET', '0ab29d7e9a448844b4bfb0c889e56cd9')
FITBIT_AUTH_URL = 'https://www.fitbit.com/oauth2/authorize'
FITBIT_TOKEN_URL = 'https://api.fitbit.com/oauth2/token'
FITBIT_REDIRECT_URL = os.getenv('FITBIT_REDIRECT_URI', 'https://fitbitdataincorporation.simonlizhm.repl.co/callback/fitbit')


class FitbitUser:
    def __init__(self, app):
        self.app = app
        self.client_id = FITBIT_CLIENT_ID
        self.client_secret = FITBIT_CLIENT_SECRET
        self.redirect_uri = FITBIT_REDIRECT_URL
        self.scope = ['activity', 'heartrate', 'sleep', 'profile']

    def _get_oauth_session(self):
        oauth = OAuth2Session(
            self.client_id,
            redirect_uri=self.redirect_uri,
            scope=self.scope,
            token=session.get('fitbit_token')
        )
        return oauth

    def logout(self):
        session.pop('fitbit_token', None)

    def fitbit_login(self):
        auth_url = f"{FITBIT_AUTH_URL}?response_type=code&client_id={FITBIT_CLIENT_ID}&redirect_uri={url_for('callback_fitbit', _external=True, _scheme='https')}&scope=activity%20nutrition%20heartrate%20location%20nutrition%20profile%20settings%20sleep%20social%20weight&prompt=login"
        return redirect(auth_url)

    def callback_fitbit(self):
        code = request.args.get('code')
        if code:
            token = self.fetch_fitbit_token(code)
            session['fitbit_token'] = token
        return redirect(url_for('dashboard'))

    def fetch_fitbit_token(self, code):
        headers = {
            'Authorization': 'Basic ' + base64.b64encode(f"{FITBIT_CLIENT_ID}:{FITBIT_CLIENT_SECRET}".encode('utf-8')).decode('utf-8'),
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        data = {
            'client_id': FITBIT_CLIENT_ID,
            'grant_type': 'authorization_code',
            'redirect_uri': url_for('callback_fitbit', _external=True, _scheme='https'),
            'code': code
        }
        response = requests.post(FITBIT_TOKEN_URL, headers=headers, data=data)
        token_data = response.json()
        return token_data

    def get_fitbit_data(self, endpoint_url, access_token):
        headers = {"Authorization": f"Bearer {access_token}"}
        data = requests.get(endpoint_url, headers=headers).json()
        return data

    def get_weekly_data(self):
        access_token = session['fitbit_token']['access_token']
        steps_weekly = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/steps/date/today/1w.json', access_token)
        sleep_weekly = self.get_fitbit_data('https://api.fitbit.com/1.2/user/-/sleep/date/today/1w.json', access_token)
        heart_rate_weekly = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/heart/date/today/1w.json', access_token)
        exercise_weekly = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/list.json?afterDate=today&offset=0&limit=7&sort=desc', access_token)
        return {"steps": steps_weekly, "sleep": sleep_weekly, "heart_rate": heart_rate_weekly, "exercise": exercise_weekly}

    def get_monthly_data(self):
        access_token = session['fitbit_token']['access_token']
        steps_monthly = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/steps/date/today/1m.json', access_token)
        sleep_monthly = self.get_fitbit_data('https://api.fitbit.com/1.2/user/-/sleep/date/today/1m.json', access_token)
        heart_rate_monthly = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/heart/date/today/1m.json', access_token)
        exercise_monthly = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/list.json?afterDate=today&offset=0&limit=30&sort=desc', access_token)
        return {"steps": steps_monthly, "sleep": sleep_monthly, "heart_rate": heart_rate_monthly, "exercise": exercise_monthly}


  
    def get_all_data(self):
        access_token = session['fitbit_token']['access_token']
        user_info = self.get_fitbit_data('https://api.fitbit.com/1/user/-/profile.json', access_token)
        daily_activity = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/date/today.json', access_token)
        sleep_data = self.get_fitbit_data('https://api.fitbit.com/1.2/user/-/sleep/date/today.json', access_token)
        heart_rate_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json', access_token)
        exercise_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/list.json?afterDate=today&offset=0&limit=20&sort=desc', access_token)
        weight_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/body/log/weight/date/today/1d.json', access_token)
    
        if 'user' not in user_info:
            user_info['user'] = {}
    
        summary = daily_activity.get('summary', {})
        distances = summary.get('distances', [{}])
        activities_heart = heart_rate_data.get('activities-heart', [{}])
        value = activities_heart[0].get('value', {})
    
        data = {
            "encodedId": user_info['user'].get('encodedId', 'N/A'),
            "full_name": user_info['user'].get('fullName', 'N/A'),
            "steps_today": summary.get('steps', 0),
            "total_minutes_asleep": sleep_data['summary'].get('totalMinutesAsleep', 0),
            "active_minutes": summary.get('fairlyActiveMinutes', 0) + summary.get('veryActiveMinutes', 0),
            "calories_burned": summary.get('caloriesOut', 0),
            "distance_covered": distances[0].get('distance', 0),
            "floors_climbed": summary.get('floors', 0),
            "resting_heart_rate": value.get('restingHeartRate', 0),
            "total_calories_intake": summary.get('caloriesIn', 0),
            "weight": weight_data.get('weight', [{}])[0].get('weight', 0),
            "exercise": exercise_data.get('activities', [{}])[0]
        }
        print(json.dumps(data))
    
        return json.dumps(data)
    

    # def get_all_data(self):
    #     access_token = session['fitbit_token']['access_token']
    #     user_info = self.get_fitbit_data('https://api.fitbit.com/1/user/-/profile.json', access_token)
    #     daily_activity = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/date/today.json', access_token)
    #     sleep_data = self.get_fitbit_data('https://api.fitbit.com/1.2/user/-/sleep/date/today.json', access_token)
    #     heart_rate_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json', access_token)
    #     exercise_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/activities/list.json?afterDate=today&offset=0&limit=20&sort=desc', access_token)
    #     weight_data = self.get_fitbit_data('https://api.fitbit.com/1/user/-/body/log/weight/date/today/1d.json', access_token)

    #     if 'user' not in user_info:
    #         user_info['user'] = {}

    #     summary = daily_activity.get('summary', {})
    #     distances = summary.get('distances', [{}])
    #     activities_heart = heart_rate_data.get('activities-heart', [{}])
    #     value = activities_heart[0].get('value', {})

    #     # return {
    #     #     "encodedId": user_info['user'].get('encodedId', 'N/A'),
    #     #     "full_name": user_info['user'].get('fullName', 'N/A'),
    #     #     "steps_today": summary.get('steps', 0),
    #     #     "total_minutes_asleep": sleep_data['summary'].get('totalMinutesAsleep', 0),
    #     #     "active_minutes": summary.get('fairlyActiveMinutes', 0) + summary.get('veryActiveMinutes', 0),
    #     #     "calories_burned": summary.get('caloriesOut', 0),
    #     #     "distance_covered": distances[0].get('distance', 0),
    #     #     "floors_climbed": summary.get('floors', 0),
    #     #     "resting_heart_rate": value.get('restingHeartRate', 0),
    #     #     "total_calories_intake": summary.get('caloriesIn', 0),
    #     #     "weight": weight_data.get('weight', [{}])[0].get('weight', 0),
    #     #     "exercise": exercise_data.get('activities', [{}])[0]
    #     # }
    #     data = {
    #     "encodedId": user_info['user'].get('encodedId', 'N/A'),
    #     "full_name": user_info['user'].get('fullName', 'N/A'),
    #     "steps_today": summary.get('steps', 0),
    #     "total_minutes_asleep": sleep_data['summary'].get('totalMinutesAsleep', 0),
    #     "active_minutes": summary.get('fairlyActiveMinutes', 0) + summary.get('veryActiveMinutes', 0),
    #     "calories_burned": summary.get('caloriesOut', 0),
    #     "distance_covered": distances[0].get('distance', 0),
    #     "floors_climbed": summary.get('floors', 0),
    #     "resting_heart_rate": value.get('restingHeartRate', 0),
    #     "total_calories_intake": summary.get('caloriesIn', 0),
    #     "weight": weight_data.get('weight', [{}])[0].get('weight', 0),
    #     "exercise": exercise_data.get('activities', [{}])[0]
    # }
    #     print(json.dumps(data))

    #     return json.dumps(data)
