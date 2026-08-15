# will generate good exercises for user to do
from app.models import *
from app.exercises import *

def get_eligible_exercises(user: UserProfile) -> list[Exercise]:
    valid_exercises = []

    for key, value in EXERCISES.items():
        if value.equipment_required.issubset(user.available_equipment):
            if key not in user.excluded_exercise_ids: valid_exercises.append(key) 
            # adds the id of the exercise if the equipment it needs is available to the user and not in excluded exercises
    return valid_exercises

    