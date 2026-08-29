import os
import pytest

from app.database import save_completed_workout, load_full_history

def test_save_and_load_round_trip(initialized_db, sample_completed_workouts):
    for cw in sample_completed_workouts:
        save_completed_workout(cw, db_path=initialized_db)

    loaded_history = load_full_history(db_path=initialized_db)

    # same number of workouts saved as loaded back
    assert len(loaded_history) == len(sample_completed_workouts)

    # spot-check the first workout matches what we saved
    original = sample_completed_workouts[0]
    loaded = loaded_history[0]

    assert loaded.workout.workout_type == original.workout.workout_type
    assert loaded.completed_at == original.completed_at
    assert len(loaded.completed_exercises) == len(original.completed_exercises)

    original_exercise = original.completed_exercises[0]
    loaded_exercise = loaded.completed_exercises[0]

    assert loaded_exercise.workout_exercise.exercise.id == original_exercise.workout_exercise.exercise.id
    assert loaded_exercise.workout_exercise.emphasis == original_exercise.workout_exercise.emphasis
    assert len(loaded_exercise.completed_sets) == len(original_exercise.completed_sets)

def test_none_recommended_weight_round_trips(initialized_db, sample_completed_workouts):
    # sample_data.py's workout_1 bench press has recommended_weight=None (first encounter)
    save_completed_workout(sample_completed_workouts[0], db_path=initialized_db)
    loaded = load_full_history(db_path=initialized_db)

    bench_exercise = loaded[0].completed_exercises[0]
    assert bench_exercise.workout_exercise.recommended_weight is None


def test_emphasis_enum_round_trips_correctly(initialized_db, sample_completed_workouts):
    from app.models import TrainingGoal

    save_completed_workout(sample_completed_workouts[0], db_path=initialized_db)
    loaded = load_full_history(db_path=initialized_db)

    emphasis = loaded[0].completed_exercises[0].workout_exercise.emphasis
    assert isinstance(emphasis, TrainingGoal)
    assert emphasis == TrainingGoal.STRENGTH