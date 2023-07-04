from .models import User

## URL to view all users: https://fitbitdataincorporation.simonlizhm.repl.co/print_users 

def print_all_users():
    all_users = User.query.all()  # Fetch all users from the database
    for user in all_users:
        print_user_info(user)

def print_user_info(user):
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
    print("\n")