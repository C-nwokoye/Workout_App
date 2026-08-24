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
    if not candidate_ids: raise ValueError(f"No exercises valid for {slot.primary_muscles}, {slot.exercise_type}, {slot.movement_pattern} slot")
    return candidate_ids

# helper function for select_exercise
# creates tuples to be used within a max function
def rank_by_preference(user: UserProfile, candidate_ids: set[str], exercises_used_this_week_ids: set[str], slot: WorkoutSlot) -> set[str]:
    options = set()
    for id in candidate_ids:
        options.add(
            (id not in user.avoided_exercise_ids, suitability_checker(slot, id).value, id in user.preferred_exercise_ids, id not in exercises_used_this_week_ids, id)
            )
    return options

# selects an exercise from available candidates for a slot
# will raise an error if there are no available candidates for a given slot
def select_exercise(user: UserProfile, candidate_ids: set[str], already_selected: set[str], exercises_used_this_week_ids: set[str], slot: WorkoutSlot) -> str:
    candidate_ids -= already_selected # checks the what exercises are in both sets and removes those from candidates
    # already_selected only includes exercises previously selected for that day
    if not candidate_ids: raise ValueError("No valid exercise candidates remaining")
    options = rank_by_preference(user, candidate_ids, exercises_used_this_week_ids, slot)

    choice = max(options)

    return choice[-1] # the id associated with the ranking

# returns either the strength or hypertrophy suitability level depending upon what the slot requires
def suitability_checker(slot: WorkoutSlot, exercise_id: str) -> int: 
    if slot.trainingEmphasis == TrainingGoal.STRENGTH:
        return EXERCISES[exercise_id].strength_suitability
    elif slot.trainingEmphasis == TrainingGoal.HYPERTROPHY:
        return EXERCISES[exercise_id].hypertrophy_suitability

 # will generate a workout for a single day
 # returns a list of WorkoutExercise objects as well as the exercises that have been selected that week   
def generate_workout(profile: UserProfile, template, exercises_used_this_week_ids: set[str]) -> list[WorkoutExercise]:

    eligible_exercise_ids = get_eligible_exercises(profile)

    selected_exercises_ids = set()

    full_workout = []
    for slot in template:
        selected_id = select_exercise(profile, get_candidates_for_slot(eligible_exercise_ids, slot), selected_exercises_ids, exercises_used_this_week_ids, slot)
        selected_exercises_ids.add(selected_id)
        full_workout.append(
            WorkoutExercise(exercise=EXERCISES[selected_id], sets=slot.sets, min_reps=slot.min_reps, max_reps=slot.max_reps, rest_seconds=slot.rest_seconds)
            )
    exercises_used_this_week_ids |= selected_exercises_ids # adds all exercises selected to the workout to the set containing exercises done that week
    return full_workout, exercises_used_this_week_ids

# weekly_template is a list of tuples 
def generate_workout_program(profile: UserProfile, weekly_template):

    exercises_used_this_week_ids = set()

    program = []

    for template in weekly_template: 
        day, exercises_used_this_week_ids = generate_workout(profile, template[1], exercises_used_this_week_ids)
        program.append(day)
    return program

