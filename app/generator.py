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
    if slot.training_emphasis == TrainingGoal.STRENGTH:
        return EXERCISES[exercise_id].strength_suitability
    elif slot.training_emphasis == TrainingGoal.HYPERTROPHY:
        return EXERCISES[exercise_id].hypertrophy_suitability

# return True if the user performed at least the recommended number of sets, reps, and weight
# should consider a situation in which the user increases the weight on their own but their reps fall under the max reps
def should_increase_weight(completed_exercise: CompletedExercise) -> bool:
    if len(completed_exercise.completed_sets) < completed_exercise.workout_exercise.sets: return False
    for completed_set in completed_exercise.completed_sets: # a list of CompletedSet objects each containing reps and weight
        if not (completed_set.weight >= completed_exercise.workout_exercise.recommended_weight and completed_set.reps >= completed_exercise.workout_exercise.max_reps):
            return False
    return True

# returns a completedExercise object correspinding to the given exercise_id containing information about the most recent instance of the exercise
def get_latest_completed_exercise(exercise_id: str, training_emphasis: TrainingGoal, workout_history: list[CompletedWorkout]) -> CompletedExercise:
    for completed_workout in reversed(workout_history): # since completed workouts will be appended to the end of the list, more recent
        # workouts are at higher indices. the reversed() function allows us to visit more recent workouts first with O(1) time complexity
        for completed_exercise in completed_workout.completed_exercises: # exercises should not be repeated within any given day so order doesnt matter
            if completed_exercise.workout_exercise.exercise.id == exercise_id and completed_exercise.workout_exercise.emphasis == training_emphasis:
                return completed_exercise
    return None


def calculate_progressed_weight(completed_exercise: CompletedExercise, increase_percentage: float) -> float:
    return completed_exercise.workout_exercise.recommended_weight * (1+increase_percentage)

def get_next_recommended_weight(exercise_id: str, training_emphasis: TrainingGoal, workout_history: list[CompletedWorkout]) -> float | None:
    completed_exercise = get_latest_completed_exercise(exercise_id, training_emphasis, workout_history)
    if not completed_exercise: # will be none if the user has not done this exercise previously
        return None
    # here we can assume the user has completed the exercise at least once before
    if not completed_exercise.workout_exercise.recommended_weight: # will be none if user has only done the exercise once
        # want to return the minimum weight of the sets they did
        return min(completed_exercise.completed_sets).weight
    # here we can assume the user has completed the exercise at least twice and has a recommended weight
    if should_increase_weight(completed_exercise):
        return calculate_progressed_weight(completed_exercise, increase_percentage=0.05)
    else:
        return completed_exercise.workout_exercise.recommended_weight


 # will generate a workout for a single day
 # returns a list of WorkoutExercise objects as well as the exercises that have been selected that week   
def generate_workout(profile: UserProfile, template, exercises_used_this_week_ids: set[str], workout_history: list[CompletedWorkout]) -> list[WorkoutExercise]:

    eligible_exercise_ids = get_eligible_exercises(profile)

    selected_exercises_ids = set()

    full_workout = []
    for slot in template:
        selected_id = select_exercise(profile, get_candidates_for_slot(eligible_exercise_ids, slot), selected_exercises_ids, exercises_used_this_week_ids, slot)
        selected_exercises_ids.add(selected_id)
        full_workout.append(
            WorkoutExercise(
                exercise=EXERCISES[selected_id], emphasis=slot.training_emphasis, sets=slot.sets, min_reps=slot.min_reps, 
                max_reps=slot.max_reps, rest_seconds=slot.rest_seconds, 
                recommended_weight=get_next_recommended_weight(selected_id, slot.training_emphasis, workout_history)
                )
            ) 
    exercises_used_this_week_ids |= selected_exercises_ids # adds all exercises selected for the workout to the set containing exercises done that week
    return full_workout, exercises_used_this_week_ids

# weekly_template is a list of tuples 
def generate_workout_program(profile: UserProfile, weekly_template, workout_history: list[CompletedWorkout]) -> list[list[WorkoutExercise]]:

    exercises_used_this_week_ids = set()

    program = []

    for template in weekly_template: 
        day, exercises_used_this_week_ids = generate_workout(profile, template[1], exercises_used_this_week_ids, workout_history)
        program.append(day) 

    # workout_history list will be updated with completed workouts before this function is called again.
    
    return program

