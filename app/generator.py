# will generate good exercises for user to do
from app.models import *
from app.exercises import *
from app.templates import *

def get_eligible_exercises(user: UserProfile) -> set[str]:
    eligible_exercise_ids = []

    for key, value in EXERCISES.items():
        if value.equipment_required.issubset(user.available_equipment):
            if key not in user.excluded_exercise_ids: eligible_exercise_ids.append(key) 
            # adds the exercise id if the equipment it needs is available to the user and not in excluded exercises
    return set(eligible_exercise_ids) # a set of exercise ids

# given exercises user can perform, what exercises can fit this slot
def get_candidates_for_slot(eligible_exercise_ids: set[str], slot: WorkoutSlot) -> set[str]:
    candidate_ids = set()
    for id in eligible_exercise_ids:
        exercise = EXERCISES[id]
        if (exercise.movement_pattern == slot.movement_pattern) and (exercise.exercise_type == slot.exercise_type):
            if exercise.primary_muscle in slot.primary_muscles: candidate_ids.add(id)
    return candidate_ids

# returns three lists of exercise object ids
# ranks exercises based off of what is in the users preferred and avoided list
def rank_by_preference(user: UserProfile, candidate_ids: set[str]) -> list[str]:
    preferred = []
    neutral = []
    avoided = []
    for id in candidate_ids:
        if id in user.preferred_exercise_ids: preferred.append(id)
        elif id in user.avoided_exercise_ids: avoided.append(id)
        else: neutral.append(id)
    return preferred, neutral, avoided

# will return None if no exercises are available
# selects an exercise from available candidates for a slot
def select_exercise(user: UserProfile, candidate_ids: set[str], already_selected: set[str]) -> str:
    candidate_ids -= already_selected # checks the what exercises are in both sets and removes those from candidates
    preferred, neutral, avoided = rank_by_preference(user, candidate_ids)
    choice = None
    if preferred: choice = preferred[0]
    elif neutral: choice = neutral[0]
    elif avoided: choice = avoided[0]
    return choice # the id of the exercise we have chosen

def generate_workout(profile: UserProfile, template) -> list[WorkoutExercise]:

    eligible_exercise_ids = get_eligible_exercises(profile)

    selected_exercises = set()

    full_workout = []

    for slot in template:
        selected = select_exercise(profile, get_candidates_for_slot(eligible_exercise_ids, slot), selected_exercises)
        selected_exercises.add(selected)
        full_workout.append(
            WorkoutExercise(exercise=EXERCISES[selected], sets=slot.sets, min_reps=slot.min_reps, max_reps=slot.max_reps, rest_seconds=slot.rest_seconds)
            )
    return full_workout

