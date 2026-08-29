# fixtures to be used in our test file. automatically imported
import os
import pytest

from app.database import get_connection, initialize_full_schema
from app.models import UserProfile, TrainingGoal, ExperienceLevel, Equipment
from sample_data import build_sample_completed_workouts

@pytest.fixture
def test_db_path():
    path = "test_workout_app.db"
    yield path                    # <- test runs here, using this path
    if os.path.exists(path):
        os.remove(path)            # <- cleanup, runs even if the test fails/raises


@pytest.fixture
def initialized_db(test_db_path):
    initialize_full_schema(test_db_path)
    return test_db_path            # <- nothing to clean up here specifically;
                                    #    test_db_path's own yield/cleanup already
                                    #    covers deleting the file afterward


@pytest.fixture
def sample_profile():
    return UserProfile(
        goal=TrainingGoal.STRENGTH_HYPERTROPHY,
        experience=ExperienceLevel.ADVANCED,
        days_per_week=5,
        max_workout_minutes=60,
        available_equipment={Equipment.BARBELL, Equipment.DUMBBELL, Equipment.BENCH},
        excluded_exercise_ids={"back_squat"},
        avoided_exercise_ids={"bulgarian_split_squat"},
        preferred_exercise_ids={"incline_dumbbell_bench_press"},
    )

@pytest.fixture
def sample_completed_workouts():
    return build_sample_completed_workouts()
