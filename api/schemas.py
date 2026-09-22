from pydantic import BaseModel, ConfigDict
from app.models import *
from app.exercises import *

class CompletedSetSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    # explicitly allows the schema to read from non-dict objects. 
    reps: int
    weight: float

class ExerciseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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

class WorkoutExerciseBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    emphasis: TrainingGoal
    sets: int
    min_reps: int
    max_reps: int
    rest_seconds: int
    recommended_weight: float | None = None

# These schemas are separate so as not to have conflicting data with requests and not rewrite existing dataclasses to include exercise_id
class WorkoutExerciseSchema(WorkoutExerciseBase):
    exercise: ExerciseSchema          # for responses

class WorkoutExerciseInputSchema(WorkoutExerciseBase):
    exercise_id: str                  # for requests

def workout_exercise_to_domain(schema: WorkoutExerciseInputSchema) -> WorkoutExercise:
    if schema.exercise_id not in EXERCISES:
        raise ValueError(f"Unknown exercise_id: {schema.exercise_id}")
    return WorkoutExercise(
        exercise=EXERCISES[schema.exercise_id],
        emphasis=schema.emphasis,
        sets=schema.sets,
        min_reps=schema.min_reps,
        max_reps=schema.max_reps,
        rest_seconds=schema.rest_seconds,
        recommended_weight=schema.recommended_weight,
    )

class CompletedExerciseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workout_exercise: WorkoutExerciseSchema
    completed_sets: list[CompletedSetSchema]

class CompletedExerciseInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workout_exercise: WorkoutExerciseInputSchema
    completed_sets: list[CompletedSetSchema]

def completed_exercise_to_domain(schema: CompletedExerciseInputSchema) -> CompletedExercise:
    return CompletedExercise(
        workout_exercise=workout_exercise_to_domain(schema.workout_exercise),
        completed_sets=[CompletedSet(reps=cs.reps, weight=cs.weight) for cs in schema.completed_sets]
    )

class WorkoutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workout_type: WorkoutType
    exercises: list[WorkoutExerciseSchema]

class WorkoutInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workout_type: WorkoutType
    exercises: list[WorkoutExerciseInputSchema]

def workout_to_domain(schema: WorkoutInputSchema) -> Workout:
    return Workout(
        workout_type=schema.workout_type,
        exercises=[workout_exercise_to_domain(ex) for ex in schema.exercises],
    )

class CompletedWorkoutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workout: WorkoutSchema
    completed_exercises: list[CompletedExerciseSchema]
    completed_at: str

class CompletedWorkoutInputSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    workout: WorkoutInputSchema
    completed_exercises: list[CompletedExerciseInputSchema]

def completed_workout_to_domain(schema: CompletedWorkoutInputSchema) -> CompletedWorkout:
    return CompletedWorkout(
        workout=workout_to_domain(schema.workout),
        completed_exercises=[completed_exercise_to_domain(ce) for ce in schema.completed_exercises],
    )


