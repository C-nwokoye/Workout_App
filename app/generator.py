# will generate good exercises for user to do
from app.models import *
from app.exercises import *

def get_eligible_exercises(user: UserProfile) -> list[Exercise]:
    valid_exercises = []

    for key, value in EXERCISES.items():
        if value.equipment_required.issubset(user.available_equipment):
            if key not in user.excluded_exercise_ids: valid_exercises.append(value) 
            # adds the exercise object if the equipment it needs is available to the user and not in excluded exercises
    return valid_exercises

# given exercises user can perform, what exercises can fit this slot
def get_candidates_for_slot(eligible_exercises: set[Exercise], slot: WorkoutSlot) -> list[Exercise]:
    candidates = []
    for exercise in eligible_exercises:
        if (exercise.movement_pattern == slot.movement_pattern) and (exercise.exercise_type == slot.exercise_type):
            if exercise.primary_muscle in slot.primary_muscles: candidates.append(exercise)
    return candidates
