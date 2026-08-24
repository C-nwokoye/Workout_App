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

LOWER_STRENGTH_TEMPLATE = [
    WorkoutSlot(movement_pattern=MovementPattern.HINGE, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.HAMSTRINGS, MuscleGroup.GLUTES},
                trainingEmphasis=TrainingGoal.STRENGTH, sets=4, min_reps=4, max_reps=6, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.SQUAT, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.QUADRICEP},
                trainingEmphasis=TrainingGoal.STRENGTH, sets=4, min_reps=6, max_reps=8, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.KNEE_FLEXION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.HAMSTRINGS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.KNEE_EXTENSION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.QUADRICEP},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.CALF_RAISE, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.CALVES},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=90)
]

PUSH_HYPERTROPHY_TEMPLATE = [
    WorkoutSlot(movement_pattern=MovementPattern.HORIZONTAL_PUSH, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.CHEST},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.VERTICAL_PUSH, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.SHOULDERS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.HORIZONTAL_PUSH, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.CHEST},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.SHOULDER_ABDUCTION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.SHOULDERS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=90),
    WorkoutSlot(movement_pattern=MovementPattern.ELBOW_EXTENSION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.TRICEPS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=90)
]

PULL_HYPERTROPHY_TEMPLATE = [
    WorkoutSlot(movement_pattern=MovementPattern.VERTICAL_PULL, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.BACK},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.HORIZONTAL_PULL, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.BACK},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.HORIZONTAL_PULL, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.BACK},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.ELBOW_FLEXION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.BICEPS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=90),
    WorkoutSlot(movement_pattern=MovementPattern.ELBOW_FLEXION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.BICEPS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=90)
]

LEGS_HYPERTROPHY_TEMPLATE = [
    WorkoutSlot(movement_pattern=MovementPattern.SQUAT, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.QUADRICEP},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.HINGE, exercise_type=ExerciseType.COMPOUND, primary_muscles={MuscleGroup.HAMSTRINGS, MuscleGroup.GLUTES},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=8, max_reps=12, rest_seconds=180),
    WorkoutSlot(movement_pattern=MovementPattern.KNEE_EXTENSION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.QUADRICEP},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.KNEE_FLEXION, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.HAMSTRINGS},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=120),
    WorkoutSlot(movement_pattern=MovementPattern.CALF_RAISE, exercise_type=ExerciseType.ISOLATION, primary_muscles={MuscleGroup.CALVES},
                trainingEmphasis=TrainingGoal.HYPERTROPHY, sets=3, min_reps=12, max_reps=15, rest_seconds=90)
]

# consider renaming
# using tuples to make clear what workout type each workout represents
FIVE_DAY_TEMPLATE = [
    (WorkoutType.UPPER_STRENGTH, UPPER_STRENGTH_TEMPLATE),
    (WorkoutType.LOWER_STRENGTH, LOWER_STRENGTH_TEMPLATE),
    (WorkoutType.PUSH_HYPERTROPHY, PUSH_HYPERTROPHY_TEMPLATE),
    (WorkoutType.PULL_HYPERTROPHY, PULL_HYPERTROPHY_TEMPLATE),
    (WorkoutType.LEGS_HYPERTROPHY, LEGS_HYPERTROPHY_TEMPLATE)
]