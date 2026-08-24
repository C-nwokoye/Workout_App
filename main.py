from app.models import *
from app.exercises import *
from app.generator import *

# when using Enums in python, use the member itself. only refer to the name when moving outside python
user_profile_1 = UserProfile(
    goal=TrainingGoal.STRENGTH,
    experience=ExperienceLevel.ADVANCED,
    days_per_week=5,
    max_workout_minutes=60,
    available_equipment={Equipment.BENCH, Equipment.DUMBBELL, Equipment.BARBELL, Equipment.SQUAT_RACK, Equipment.CABLE,
                         Equipment.CALF_RAISE_MACHINE, Equipment.LAT_PULLDOWN_MACHINE, Equipment.LEG_CURL_MACHINE, Equipment.LEG_EXTENSION_MACHINE,
                         Equipment.LEG_PRESS_MACHINE, Equipment.LOW_CABLE_ROW_MACHINE, Equipment.PULL_UP_BAR, Equipment.SMITH_MACHINE,
                         Equipment.PEC_DECK_MACHINE},
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
assert "back_squat" not in {e for e in eligible_exercises}
assert "bulgarian_split_squat" in {e for e in eligible_exercises}
assert "incline_dumbbell_bench_press" in {e for e in eligible_exercises}

workout = generate_workout(user_profile_1, UPPER_STRENGTH_TEMPLATE, set())

# for item in workout:
#     print(item)
#     print()

program = generate_workout_program(user_profile_1, FIVE_DAY_TEMPLATE)
for i, day in enumerate(program):

    print(FIVE_DAY_TEMPLATE[i][0])
    for item in day:
        print(item)
        print()