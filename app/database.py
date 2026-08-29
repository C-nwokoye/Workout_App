import sqlite3
from app.models import *
from app.exercises import EXERCISES
from itertools import groupby

DEFAULT_DB_PATH = "workout_history.db"

def get_connection(db_path=DEFAULT_DB_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON") # ensures that foreign keys reference a record that actually exists
    return conn

def initialize_full_schema(db_path=DEFAULT_DB_PATH) -> None:
    conn = get_connection(db_path)
    with conn:
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
        emphasis TEXT NOT NULL,
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
    conn.close()

def _insert_completed_workout(conn: sqlite3.Connection, workout_type: WorkoutType, completed_at: str) -> int:
    cur = conn.cursor()
    cur.execute("INSERT INTO completed_workouts (workout_type, completed_at) VALUES (?, ?)", (workout_type, completed_at))
    return cur.lastrowid # contians the auto assigned id of the row we just added. only for INSERT
    

def _insert_completed_exercise(conn: sqlite3.Connection, completed_workout_id: int, exercise_id: str, emphasis: str, min_reps: int, max_reps: int, rest_seconds: int, recommended_weight: float | None) -> int:
    # want to keep the function "dumb" such that it only needs values and does not need to know the structure of our python objects
    cur = conn.cursor()
    cur.execute("INSERT INTO completed_exercises (completed_workout_id, exercise_id, emphasis, min_reps, max_reps, rest_seconds, recommended_weight) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (completed_workout_id, exercise_id, emphasis, min_reps, max_reps, rest_seconds, recommended_weight))
    return cur.lastrowid

def _insert_completed_set(conn: sqlite3.Connection, completed_exercise_id: int, reps: int, weight: float) -> int:
    cur = conn.cursor()
    cur.execute("INSERT INTO completed_sets (completed_exercise_id, reps, weight) VALUES (?, ?, ?)", (completed_exercise_id, reps, weight))

def save_completed_workout(completed_workout: CompletedWorkout, db_path=DEFAULT_DB_PATH) -> int:
    conn = get_connection(db_path)
    with conn:
        workout_id = _insert_completed_workout(conn, completed_workout.workout.workout_type.value, completed_workout.completed_at)
        for ce in completed_workout.completed_exercises:
            task = ce.workout_exercise
            exercise_id = _insert_completed_exercise(conn, workout_id, task.exercise.id, task.emphasis.value, task.min_reps, task.max_reps, task.rest_seconds, task.recommended_weight)
            for cs in ce.completed_sets:
                _insert_completed_set(conn, exercise_id, cs.reps, cs.weight)
    conn.close()
    return workout_id

def _load_workout(conn, workout_id):
    cur = conn.cursor()
    cur.execute("""
    SELECT
    completed_workouts.id AS workout_id,
    completed_workouts.workout_type,
    completed_workouts.completed_at,
    completed_exercises.id AS exercise_row_id,
    completed_exercises.exercise_id,
    completed_exercises.emphasis,
    completed_exercises.min_reps,
    completed_exercises.max_reps,
    completed_exercises.rest_seconds,
    completed_exercises.recommended_weight,
    completed_sets.reps,
    completed_sets.weight
    FROM completed_workouts
    JOIN completed_exercises ON completed_exercises.completed_workout_id = completed_workouts.id
    JOIN completed_sets ON completed_sets.completed_exercise_id = completed_exercises.id
    WHERE completed_workouts.id = ?
    ORDER BY completed_exercises.id, completed_sets.id
    """, (workout_id,))
    return cur.fetchall()

def _reconstruct_completed_workout(rows):
    if not rows:
        return None

    first = rows[0]
    workout_type = WorkoutType(first["workout_type"])
    completed_at = first["completed_at"]

    completed_exercises = []

    for exercise_row_id, group in groupby(rows, key=lambda r: r["exercise_row_id"]):
        group = list(group)  # groupby gives you a one-time-use iterator; materialize it into a list
        first_row_in_group = group[0]

        workout_exercise = WorkoutExercise(
            exercise=EXERCISES[first_row_in_group["exercise_id"]],
            emphasis=TrainingGoal(first_row_in_group["emphasis"]),
            sets=len(group),
            min_reps=first_row_in_group["min_reps"],
            max_reps=first_row_in_group["max_reps"],
            rest_seconds=first_row_in_group["rest_seconds"],
            recommended_weight=first_row_in_group["recommended_weight"],
        )

        completed_sets = [
            CompletedSet(reps=row["reps"], weight=row["weight"])
            for row in group
        ]

        completed_exercises.append(
            CompletedExercise(
                workout_exercise=workout_exercise,
                completed_sets=completed_sets,
            )
        )

    workout = Workout(
        workout_type=workout_type,
        exercises=[ce.workout_exercise.exercise for ce in completed_exercises],
    )

    return CompletedWorkout(
        workout=workout,
        completed_exercises=completed_exercises,
        completed_at=completed_at,
    )


def load_full_history(db_path=DEFAULT_DB_PATH) -> list[CompletedWorkout]:
    conn = get_connection(db_path)
    workout_history = []
    with conn:
        cur = conn.cursor()
        cur.execute("SELECT id FROM completed_workouts")
        cw_ids = {item["id"] for item in cur.fetchall()} # gives us a set of all the workout ids
        for cw_id in cw_ids:
            rows = _load_workout(conn, cw_id) # loads a single completed_workout object
            cw = _reconstruct_completed_workout(rows)
            workout_history.append(cw)
    conn.close()
    return workout_history




