from app.models import *
from app.exercises import *
from app.generator import *

# when using Enums in python, use the member itself. only refer to the name when moving outside python
user_profile_1 = UserProfile(
    goal=TrainingGoal.STRENGTH,
    experience=ExperienceLevel.ADVANCED,
    days_per_week=5,
    max_workout_minutes=60,
    available_equipment={Equipment.BENCH, Equipment.DUMBBELL, Equipment.BARBELL, Equipment.SQUAT_RACK},
    excluded_exercise_ids={BACK_SQUAT.id},
    avoided_exercise_ids={BULGARIAN_SPLIT_SQUAT.id},
    preferred_exercise_ids={INCLINE_DUMBBELL_BENCH_PRESS.id}
)

user_profile_2 = UserProfile(
    goal=TrainingGoal.STRENGTH,
    experience=ExperienceLevel.ADVANCED,
    days_per_week=5,
    max_workout_minutes=60,
    available_equipment={Equipment.BODYWEIGHT},
    excluded_exercise_ids={BACK_SQUAT.id},
    avoided_exercise_ids={BULGARIAN_SPLIT_SQUAT.id},
    preferred_exercise_ids={INCLINE_DUMBBELL_BENCH_PRESS.id}
)

# for key, value in EXERCISES.items():
#     print(f"{key}: {value.name}")

# print(get_eligible_exercises(user_profile_1))
eligible_exercises = get_eligible_exercises(user_profile_1)

# use assert for testing. if the condition is false, it will raise an AssertionError
assert "back_squat" not in {e.id for e in eligible_exercises}
assert "bulgarian_split_squat" in {e.id for e in eligible_exercises}
assert "incline_dumbbell_bench_press" in {e.id for e in eligible_exercises}

testSlot = WorkoutSlot(movement_pattern=MovementPattern.HORIZONTAL_PUSH, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.CHEST})
for exercise in get_candidates_for_slot(eligible_exercises, testSlot):
    print(exercise.name)