# Sample CompletedWorkout objects for testing persistence (save/load) and,
# later, historical lookup / progression logic once connected to the generator.
#
# Workout 1 and Workout 2 both use Barbell Bench Press under STRENGTH emphasis,
# at different dates with an increased weight — useful for testing
# get_latest_completed_exercise() and should_increase_weight() once wired up.

from datetime import datetime, timedelta

from app.models import *

from app.exercises import *


def _days_ago(n: int) -> str:
    return (datetime.now() - timedelta(days=n)).isoformat()


def build_sample_completed_workouts() -> list[CompletedWorkout]:
    workouts = []

    # ---------------------------------------------------------------
    # Workout 1: Upper Strength — 10 days ago
    # ---------------------------------------------------------------
    bench_we_1 = WorkoutExercise(
        exercise=BARBELL_BENCH_PRESS,
        emphasis=TrainingGoal.STRENGTH,
        sets=4, min_reps=4, max_reps=6, rest_seconds=180,
        recommended_weight=None,  # first encounter
    )
    bench_ce_1 = CompletedExercise(
        workout_exercise=bench_we_1,
        completed_sets=[
            CompletedSet(reps=6, weight=185.0),
            CompletedSet(reps=6, weight=185.0),
            CompletedSet(reps=5, weight=185.0),
            CompletedSet(reps=5, weight=185.0),
        ],
    )

    row_we_1 = WorkoutExercise(
        exercise=BARBELL_ROW,
        emphasis=TrainingGoal.STRENGTH,
        sets=4, min_reps=4, max_reps=6, rest_seconds=180,
        recommended_weight=None,
    )
    row_ce_1 = CompletedExercise(
        workout_exercise=row_we_1,
        completed_sets=[
            CompletedSet(reps=6, weight=155.0),
            CompletedSet(reps=6, weight=155.0),
            CompletedSet(reps=6, weight=155.0),
            CompletedSet(reps=5, weight=155.0),
        ],
    )

    workout_1 = CompletedWorkout(
        workout=Workout(
            workout_type=WorkoutType.UPPER_STRENGTH,
            exercises=[BARBELL_BENCH_PRESS, BARBELL_ROW],
        ),
        completed_exercises=[bench_ce_1, row_ce_1],
        completed_at=_days_ago(10),
    )
    workouts.append(workout_1)

    # ---------------------------------------------------------------
    # Workout 2: Upper Strength — 3 days ago
    # Same exercise (bench), same emphasis, higher weight than Workout 1
    # -> useful for testing historical lookup / progression later.
    # ---------------------------------------------------------------
    bench_we_2 = WorkoutExercise(
        exercise=BARBELL_BENCH_PRESS,
        emphasis=TrainingGoal.STRENGTH,
        sets=4, min_reps=4, max_reps=6, rest_seconds=180,
        recommended_weight=185.0,
    )
    bench_ce_2 = CompletedExercise(
        workout_exercise=bench_we_2,
        completed_sets=[
            CompletedSet(reps=6, weight=185.0),
            CompletedSet(reps=6, weight=185.0),
            CompletedSet(reps=6, weight=185.0),
            CompletedSet(reps=6, weight=185.0),
        ],
    )

    overhead_we_2 = WorkoutExercise(
        exercise=OVERHEAD_PRESS,
        emphasis=TrainingGoal.STRENGTH,
        sets=3, min_reps=6, max_reps=8, rest_seconds=120,
        recommended_weight=None,
    )
    overhead_ce_2 = CompletedExercise(
        workout_exercise=overhead_we_2,
        completed_sets=[
            CompletedSet(reps=8, weight=95.0),
            CompletedSet(reps=7, weight=95.0),
            CompletedSet(reps=6, weight=95.0),
        ],
    )

    workout_2 = CompletedWorkout(
        workout=Workout(
            workout_type=WorkoutType.UPPER_STRENGTH,
            exercises=[BARBELL_BENCH_PRESS, OVERHEAD_PRESS],
        ),
        completed_exercises=[bench_ce_2, overhead_ce_2],
        completed_at=_days_ago(3),
    )
    workouts.append(workout_2)

    # ---------------------------------------------------------------
    # Workout 3: Push Hypertrophy — 5 days ago
    # Different workout type/emphasis entirely, for variety.
    # ---------------------------------------------------------------
    incline_we = WorkoutExercise(
        exercise=INCLINE_DUMBBELL_BENCH_PRESS,
        emphasis=TrainingGoal.HYPERTROPHY,
        sets=3, min_reps=8, max_reps=12, rest_seconds=180,
        recommended_weight=None,
    )
    incline_ce = CompletedExercise(
        workout_exercise=incline_we,
        completed_sets=[
            CompletedSet(reps=12, weight=60.0),
            CompletedSet(reps=11, weight=60.0),
            CompletedSet(reps=10, weight=60.0),
        ],
    )

    lateral_we = WorkoutExercise(
        exercise=DUMBBELL_LATERAL_RAISE,
        emphasis=TrainingGoal.HYPERTROPHY,
        sets=3, min_reps=12, max_reps=15, rest_seconds=90,
        recommended_weight=None,
    )
    lateral_ce = CompletedExercise(
        workout_exercise=lateral_we,
        completed_sets=[
            CompletedSet(reps=15, weight=20.0),
            CompletedSet(reps=14, weight=20.0),
            CompletedSet(reps=13, weight=20.0),
        ],
    )

    workout_3 = CompletedWorkout(
        workout=Workout(
            workout_type=WorkoutType.PUSH_HYPERTROPHY,
            exercises=[INCLINE_DUMBBELL_BENCH_PRESS, DUMBBELL_LATERAL_RAISE],
        ),
        completed_exercises=[incline_ce, lateral_ce],
        completed_at=_days_ago(5),
    )
    workouts.append(workout_3)

    return workouts


def main():
    from app.database import save_completed_workout, initialize_full_schema

    for cw in build_sample_completed_workouts():
        initialize_full_schema(db_name="test.db")
        workout_id = save_completed_workout(cw, db_name="test.db")
        print(f"Saved workout_id={workout_id} ({cw.workout.workout_type.value}, {cw.completed_at})")


if __name__ == "__main__":
    main()