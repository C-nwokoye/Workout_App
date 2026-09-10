from pydantic import BaseModel
from app.models import *
from app.exercises import *

class CompletedSetSchema(BaseModel):
    reps: int
    weight: float

class ExerciseSchema(BaseModel):
    id: str
    name: str
    primary_muscle: MuscleGroup
    strength_suitability: SuitabilityLevel
    hypertrophy_suitability: SuitabilityLevel
    exercise_type: ExerciseType
    movement_pattern: MovementPattern
    # Pydantic doesnt know what python sets are so everything is automatically converted into an array
    secondary_muscles: set[MuscleGroup] 
    equipment_required: set[Equipment]

class WorkoutExerciseSchema(BaseModel):
    exercise: ExerciseSchema
    emphasis: TrainingGoal
    sets: int
    min_reps: int
    max_reps: int
    rest_seconds: int
    recommended_weight: float | None

class CompletedExerciseSchema(BaseModel):
    workout_exercise: WorkoutExerciseSchema
    completed_sets: list[CompletedSetSchema]

class WorkoutSchema(BaseModel):
    workout_type: WorkoutType
    exercises: list[WorkoutExerciseSchema]

class CompletedWorkoutSchema(BaseModel):
    workout: WorkoutSchema
    completed_exercises: list[CompletedExerciseSchema]
    completed_at: str
