from app.models import *
from app.exercises import *
from app.generator import *
from app.database import *


def print_workout_history(history: list[CompletedWorkout]) -> None:
    """Pretty-print a full workout history for debugging/sanity-checking."""
    if not history:
        print("No workout history found.")
        return

    for cw in history:
        print("=" * 60)
        print(f"{cw.workout.workout_type.value.upper()}  —  {cw.completed_at}")
        print("=" * 60)

        for ce in cw.completed_exercises:
            we = ce.workout_exercise
            print(f"\n{we.exercise.name}  ({we.emphasis.value})")
            print(f"  Prescribed: {we.sets} x {we.min_reps}-{we.max_reps}, "
                  f"rest {we.rest_seconds}s, recommended weight: {we.recommended_weight}")
            print("  Actual sets:")
            for i, cs in enumerate(ce.completed_sets, start=1):
                print(f"    Set {i}: {cs.reps} reps @ {cs.weight}")
        print()

def main():
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

    initialize_full_schema() # ensures a database exists
    workout_history = load_full_history() # gets the workout history from our SQL database

    program = generate_workout_program(profile=user_profile_1, weekly_template=FIVE_DAY_TEMPLATE, workout_history=workout_history)

    for i, day in enumerate(program):
        print(FIVE_DAY_TEMPLATE[i][0])
        for workout in day:
            print(workout)
            print()

    

    

if __name__ == "__main__":
    main()

