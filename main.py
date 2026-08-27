from app.models import *
from app.exercises import *
from app.generator import *
from app.database import *

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

workout = generate_workout(user_profile_1, UPPER_STRENGTH_TEMPLATE, set(), [])

# for item in workout:
#     print(item)
#     print()

# program = generate_workout_program(user_profile_1, FIVE_DAY_TEMPLATE)
# for i, day in enumerate(program):

#     print(FIVE_DAY_TEMPLATE[i][0])
#     for item in day:
#         print(item)
#         print()

completed_exercise_0 = CompletedExercise(
    WorkoutExercise(INCLINE_DUMBBELL_BENCH_PRESS, TrainingGoal.HYPERTROPHY, 3, 8, 10, 90),
    [
        CompletedSet(10, 70),
        CompletedSet(10, 75),
        CompletedSet(10, 80)
    ]
)
completed_exercise_1 = CompletedExercise(
    WorkoutExercise(LEG_PRESS, TrainingGoal.HYPERTROPHY, 3, 8, 10, 90, 90),
    [
        CompletedSet(10, 95),
        CompletedSet(10, 95),
        CompletedSet(10, 90)
    ]
)
completed_exercise_2 = CompletedExercise(
    WorkoutExercise(INCLINE_DUMBBELL_BENCH_PRESS, TrainingGoal.HYPERTROPHY, 3, 8, 10, 90, 75),
    [
        CompletedSet(10, 80),
        CompletedSet(10, 80),
        CompletedSet(10, 80)
    ]
)
completed_exercise_3 = CompletedExercise(
    WorkoutExercise(BARBELL_ROW, TrainingGoal.STRENGTH, 4, 4, 6, 180, 185),
    [
        CompletedSet(6, 200),
        CompletedSet(6, 200),
        CompletedSet(6, 200),
        CompletedSet(6, 200)
    ]
)

CW0  = CompletedWorkout(Workout(
    WorkoutType.PUSH_HYPERTROPHY,
    [INCLINE_DUMBBELL_BENCH_PRESS, LEG_PRESS]
), [completed_exercise_0, completed_exercise_1])

CW1  = CompletedWorkout(Workout(
    WorkoutType.LEGS_STRENGTH,
    [LEG_PRESS, INCLINE_DUMBBELL_BENCH_PRESS]
), [completed_exercise_1, completed_exercise_2])

CW2 = CompletedWorkout(Workout(
    WorkoutType.PULL_STRENGTH,
    [BARBELL_ROW]
), [completed_exercise_3])

# print(should_increase_weight(completed_exercise_0))

# comp = get_latest_completed_exercise(INCLINE_DUMBBELL_BENCH_PRESS.id, TrainingGoal.HYPERTROPHY, [CW0, CW1])

# print(get_next_recommended_weight(INCLINE_DUMBBELL_BENCH_PRESS.id, TrainingGoal.HYPERTROPHY, [CW0, CW1]))

program = generate_workout_program(user_profile_1, FIVE_DAY_TEMPLATE, [CW0, CW1, CW2, CW2])

# for i, day in enumerate(program):

#     print(FIVE_DAY_TEMPLATE[i][0])
#     for item in day:
#         print(item)
#         print()

connection = get_connection()
print(connection)
connection.close()


