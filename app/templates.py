# what templates exist
from app.models import *
from app.exercises import *


UPPER_STRENGTH_TEMPLATE = [
    WorkoutSlot(movement_pattern=MovementPattern.HORIZONTAL_PUSH, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.CHEST},
                trainingEmphasis=TrainingGoal.STRENGTH, sets=4, min_reps=4, max_reps=6, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.HORIZONTAL_PULL, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.BACK},
                trainingEmphasis=TrainingGoal.STRENGTH, sets=4, min_reps=4, max_reps=6, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.VERTICAL_PUSH, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.SHOULDERS},
                trainingEmphasis=TrainingGoal.STRENGTH, sets=3, min_reps=6, max_reps=8, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.VERTICAL_PULL, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.BACK},
                trainingEmphasis=TrainingGoal.STRENGTH, sets=3, min_reps=6, max_reps=8, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.ELBOW_FLEXION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.BICEPS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=2, min_reps=8, max_reps=12, rest_seconds=90),
    WorkoutSlot(movement_pattern=MovementPattern.ELBOW_EXTENSION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.TRICEPS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=2, min_reps=8, max_reps=12, rest_seconds=90)
]