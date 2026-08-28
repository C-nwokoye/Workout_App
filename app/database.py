import sqlite3
from app.models import *
from app.exercises import *

def get_connection():
    conn = sqlite3.connect("workout_history.db")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON") # ensures that foreign keys reference a record that actually exists
    return conn

def initialize_full_schema(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS completed_workouts (
    id INTEGER PRIMARY KEY,
    workout_type TEXT NOT NULL,
    completed_at TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS completed_exercises (
    id INTEGER PRIMARY KEY,
    completed_workout_id INTEGER NOT NULL,
    exercise_id TEXT NOT NULL,
    min_reps INTEGER NOT NULL,
    max_reps INTEGER NOT NULL,
    rest_seconds INTEGER NOT NULL,
    recommended_weight REAL,
    FOREIGN KEY (completed_workout_id) REFERENCES completed_workouts(id)
    )
    """) # foreign keys reference data in a separate table; similar to a pointer in python
    cur.execute("""
    CREATE TABLE IF NOT EXISTS completed_sets (
    id INTEGER PRIMARY KEY,
    completed_exercise_id INTEGER NOT NULL,
    reps INTEGER NOT NULL,
    weight REAL NOT NULL,
    FOREIGN KEY (completed_exercise_id) REFERENCES completed_exercises(id)
    )
    """)

def _insert_completed_workout(conn: sqlite3.Connection, workout_type: WorkoutType, completed_at: str):
    cur = conn.cursor()
    cur.execute("INSERT INTO completed_workouts (workout_type, completed_at) VALUES (?, ?)", (workout_type, completed_at))
    return cur.lastrowid # contians the auto assigned id of the row we just added. only for INSERT
    

def _insert_completed_exercise(conn: sqlite3.Connection, completed_workout_id: int, exercise_id: str, min_reps: int, max_reps: int, rest_seconds: int, recommended_weight: float | None):
    # want to keep the function "dumb" such that it only needs values and does not need to know the structure of our python objects
    cur = conn.cursor()
    cur.execute("INSERT INTO completed_exercises (completed_workout_id, exercise_id, min_reps, max_reps, rest_seconds, recommended_weight) VALUES (?, ?, ?, ?, ?, ?)",
                (completed_workout_id, exercise_id, min_reps, max_reps, rest_seconds, recommended_weight))
    return cur.lastrowid

def _insert_completed_set(conn: sqlite3.Connection, completed_exercise_id: int, reps: int, weight: float):
    cur = conn.cursor()
    cur.execute("INSERT INTO completed_sets (completed_exercise_id, reps, weight) VALUES (?, ?, ?)", (completed_exercise_id, reps, weight))

def save_completed_workout(completed_workout: CompletedWorkout):
    conn = get_connection()
    with conn:
        workout_id = _insert_completed_workout(conn, completed_workout.workout.workout_type.value, completed_workout.completed_at)
        for ce in completed_workout.completed_exercises:
            task = ce.workout_exercise
            exercise_id = _insert_completed_exercise(conn, workout_id, task.exercise.id, task.min_reps, task.max_reps, task.rest_seconds, task.recommended_weight)
            for cs in ce.completed_sets:
                _insert_completed_set(conn, exercise_id, cs.reps, cs.weight)
    conn.close()
    return workout_id

