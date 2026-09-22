# tests/test_api.py
import os
import pytest
from fastapi.testclient import TestClient

from app.database import initialize_full_schema, load_full_history, save_completed_workout
from app.models import WorkoutType
import api.routes as routes_module

TEST_DB_PATH = "test_workout_history.db"

@pytest.fixture
def test_db(monkeypatch):
    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)
    initialize_full_schema(db_path=TEST_DB_PATH)

    # redirect the route module's calls to the test database
    monkeypatch.setattr(routes_module, "load_full_history",
                         lambda: load_full_history(db_path=TEST_DB_PATH))
    monkeypatch.setattr(routes_module, "save_completed_workout",
                         lambda cw: save_completed_workout(cw, db_path=TEST_DB_PATH))

    yield TEST_DB_PATH

    if os.path.exists(TEST_DB_PATH):
        os.remove(TEST_DB_PATH)

@pytest.fixture
def client(test_db):
    return TestClient(routes_module.app)


VALID_PAYLOAD = {
    "workout": {
        "workout_type": "upper_strength",
        "exercises": [{
            "exercise_id": "barbell_bench_press",
            "emphasis": "strength",
            "sets": 4, "min_reps": 4, "max_reps": 6, "rest_seconds": 180,
            "recommended_weight": 185.0,
        }],
    },
    "completed_exercises": [{
        "workout_exercise": {
            "exercise_id": "barbell_bench_press",
            "emphasis": "strength",
            "sets": 4, "min_reps": 4, "max_reps": 6, "rest_seconds": 180,
            "recommended_weight": 185.0,
        },
        "completed_sets": [
            {"reps": 6, "weight": 185.0},
            {"reps": 6, "weight": 185.0},
        ],
    }],
}


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_workout_history_empty(client):
    response = client.get("/workout-history")
    assert response.status_code == 200
    assert response.json() == []


def test_post_completed_workout_persists(client):
    response = client.post("/completed-workouts", json=VALID_PAYLOAD)
    assert response.status_code == 200

    history = load_full_history(db_path=TEST_DB_PATH)
    assert len(history) == 1
    assert history[0].workout.workout_type == WorkoutType.UPPER_STRENGTH
    assert history[0].completed_exercises[0].completed_sets[0].reps == 6


def test_post_completed_workout_malformed_body(client):
    bad_payload = {"workout": {"workout_type": "upper_strength", "exercises": []}}
    response = client.post("/completed-workouts", json=bad_payload)
    assert response.status_code == 422  # missing completed_exercises entirely


def test_post_completed_workout_unknown_exercise_id(client):
    bad_payload = {
        "workout": {"workout_type": "upper_strength", "exercises": [{
            "exercise_id": "not_a_real_exercise",
            "emphasis": "strength", "sets": 3, "min_reps": 8, "max_reps": 12,
            "rest_seconds": 90, "recommended_weight": None,
        }]},
        "completed_exercises": [],
    }
    response = client.post("/completed-workouts", json=bad_payload)
    assert response.status_code == 422