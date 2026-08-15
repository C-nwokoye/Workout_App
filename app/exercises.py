# holds all exercises the exercises generator will know about
from enum import Enum
from app.models import *

BARBELL_BENCH_PRESS = Exercise(
    id="barbell_bench_press", 
    name="Barbell Bench Press", 
    primary_muscle=MuscleGroup.CHEST,
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    secondary_muscles={MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS}, 
    equipment_required={Equipment.BARBELL, Equipment.BENCH}
    )

INCLINE_DUMBBELL_BENCH_PRESS = Exercise(
    id="incline_dumbbell_bench_press", 
    name="Incline Dumbbell Bench Press", 
    primary_muscle=MuscleGroup.CHEST, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    secondary_muscles={MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS}, 
    equipment_required={Equipment.DUMBELL, Equipment.BENCH}
    )

DUMBBELL_BENCH_PRESS = Exercise(
    id="dumbbell_bench_press", 
    name="Dumbbell Bench Press", 
    primary_muscle=MuscleGroup.CHEST, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    secondary_muscles={MuscleGroup.TRICEPS, MuscleGroup.SHOULDERS}, 
    equipment_required={Equipment.DUMBELL, Equipment.BENCH}
    )

OVERHEAD_PRESS = Exercise(
    id="overhead_press", 
    name="Overhead Press", 
    primary_muscle=MuscleGroup.SHOULDERS, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.VERTICAL_PUSH,
    secondary_muscles={MuscleGroup.TRICEPS, MuscleGroup.CORE, MuscleGroup.BACK}, 
    equipment_required={Equipment.BARBELL}
    )

CABLE_FLY = Exercise(
    id="cable_fly", 
    name="Cable Fly", 
    primary_muscle=MuscleGroup.CHEST, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    secondary_muscles={MuscleGroup.SHOULDERS, MuscleGroup.BICEPS}, 
    equipment_required={Equipment.CABLE})

BARBELL_ROW = Exercise(
    id="barbell_row", 
    name="Barbell Row", 
    primary_muscle=MuscleGroup.BACK, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.HORIZONTAL_PULL,
    secondary_muscles={MuscleGroup.SHOULDERS, MuscleGroup.BICEPS}, 
    equipment_required={Equipment.BARBELL}
    )

SEATED_CABLE_ROW = Exercise(
    id="seated_cable_row", 
    name="Seated Cable Row", 
    primary_muscle=MuscleGroup.BACK, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.HORIZONTAL_PULL,
    secondary_muscles={MuscleGroup.SHOULDERS, MuscleGroup.BICEPS}, 
    equipment_required={Equipment.LOW_CABLE_ROW_MACHINE}
    )

LAT_PULLDOWN = Exercise(
    id="lat_pulldown", 
    name="Lat Pulldown", 
    primary_muscle=MuscleGroup.BACK, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.VERTICAL_PULL,
    secondary_muscles={MuscleGroup.SHOULDERS, MuscleGroup.BICEPS}, 
    equipment_required={Equipment.LAT_PULLDOWN_MACHINE}
    )

PULL_UP = Exercise(
    id="pull_up", 
    name="Pull Ups", 
    primary_muscle=MuscleGroup.BACK, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.VERTICAL_PULL,
    secondary_muscles={MuscleGroup.SHOULDERS, MuscleGroup.BICEPS}, 
    equipment_required={Equipment.PULL_UP_BAR}
    )

BACK_SQUAT = Exercise(
    id="back_squat", 
    name="Back Squat", 
    primary_muscle=MuscleGroup.QUADRICEP, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.SQUAT,
    secondary_muscles={MuscleGroup.GLUTES, MuscleGroup.CORE}, 
    equipment_required={Equipment.SQUAT_RACK, Equipment.BARBELL}
    )

LEG_PRESS = Exercise( # not finished
    id="leg_press", 
    name="Leg Press", 
    primary_muscle=MuscleGroup.QUADRICEP, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.SQUAT, 
    secondary_muscles={MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS, MuscleGroup.CALVES}, 
    equipment_required={Equipment.LEG_PRESS_MACHINE}
    )

ROMANIAN_DEADLIFT = Exercise(
    id="romanian_deadlift", 
    name="RDL", 
    primary_muscle=MuscleGroup.GLUTES, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.HINGE,
    secondary_muscles={MuscleGroup.HAMSTRINGS}, 
    equipment_required={Equipment.BARBELL}
    )

LEG_EXTENSION = Exercise(
    id="leg_extension", 
    name="Leg Extension", 
    primary_muscle=MuscleGroup.QUADRICEP, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.KNEE_EXTENSION,
    secondary_muscles={}, # empty set, exclusively targets quads
    equipment_required={Equipment.LEG_EXTENSION_MACHINE}
    )

LEG_CURL = Exercise(
    id="leg_curl", 
    name="Leg Curl", 
    primary_muscle=MuscleGroup.HAMSTRINGS, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.KNEE_FLEXION,
    secondary_muscles={}, # empty set, exclusively targets hamstrings (currently) 
    equipment_required={Equipment.LEG_CURL_MACHINE}
    )

BULGARIAN_SPLIT_SQUAT = Exercise(
    id="bulgarian_split_squat", 
    name="Bulgarian Split Squat", 
    primary_muscle=MuscleGroup.QUADRICEP, 
    exercise_type=ExerciseType.COMPOUND, 
    movement_pattern=MovementPattern.SQUAT,
    secondary_muscles={MuscleGroup.GLUTES, MuscleGroup.HAMSTRINGS}, 
    equipment_required={Equipment.BENCH, Equipment.DUMBELL}
    )

STANDING_CALF_RAISE = Exercise(
    id="standing_calf_raise", 
    name="Standing Calf Raise", 
    primary_muscle=MuscleGroup.CALVES, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.CALF_RAISE,
    secondary_muscles={}, 
    equipment_required={Equipment.CALF_RAISE_MACHINE}
    )

DUMBBELL_LATERAL_RAISE = Exercise(
    id="dumbbell_lateral_raise", 
    name="Dumbbell Lat Raise", 
    primary_muscle=MuscleGroup.SHOULDERS, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.SHOULDER_ABDUCTION,
    secondary_muscles={}, 
    equipment_required={Equipment.DUMBELL}
    )

DUMBBELL_BICEP_CURL = Exercise(
    id="dumbbell_bicep_curl", 
    name="Dumbbell Bicep Curl", 
    primary_muscle=MuscleGroup.BICEPS, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.ELBOW_FLEXION,
    secondary_muscles={}, 
    equipment_required={Equipment.DUMBELL}
    )

CABLE_BICEP_CURL = Exercise(
    id="cable_bicep_curl", 
    name="Cable Bicep Curl", 
    primary_muscle=MuscleGroup.BICEPS, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.ELBOW_FLEXION,
    secondary_muscles={MuscleGroup.CORE}, 
    equipment_required={Equipment.CABLE}
    )

TRICEPS_PUSHDOWN = Exercise(
    id="triceps_pushdown", 
    name="Triceps Pushdown", 
    primary_muscle=MuscleGroup.TRICEPS, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.ELBOW_EXTENSION,
    secondary_muscles={}, 
    equipment_required={Equipment.CABLE}
    )

OVERHEAD_TRICEPS_EXTENSION = Exercise(
    id="overhead_triceps_extension", 
    name="Overhead Triceps Extension", 
    primary_muscle=MuscleGroup.TRICEPS, 
    exercise_type=ExerciseType.ISOLATION, 
    movement_pattern=MovementPattern.ELBOW_EXTENSION,
    secondary_muscles={}, 
    equipment_required={Equipment.CABLE}
    )

EXERCISES = {
    BARBELL_BENCH_PRESS.id: BARBELL_BENCH_PRESS,
    INCLINE_DUMBBELL_BENCH_PRESS.id: INCLINE_DUMBBELL_BENCH_PRESS,
    DUMBBELL_BENCH_PRESS.id: DUMBBELL_BENCH_PRESS,
    OVERHEAD_PRESS.id: OVERHEAD_PRESS,
    CABLE_FLY.id: CABLE_FLY,
    BARBELL_ROW.id: BARBELL_ROW,
    SEATED_CABLE_ROW.id: SEATED_CABLE_ROW,
    LAT_PULLDOWN.id: LAT_PULLDOWN,
    PULL_UP.id: PULL_UP,
    BACK_SQUAT.id: BACK_SQUAT,
    LEG_PRESS.id: LEG_PRESS,
    ROMANIAN_DEADLIFT.id: ROMANIAN_DEADLIFT,
    LEG_EXTENSION.id: LEG_EXTENSION,
    LEG_CURL.id: LEG_CURL,
    BULGARIAN_SPLIT_SQUAT.id: BULGARIAN_SPLIT_SQUAT,
    STANDING_CALF_RAISE.id: STANDING_CALF_RAISE,
    DUMBBELL_LATERAL_RAISE.id: DUMBBELL_LATERAL_RAISE,
    DUMBBELL_BICEP_CURL.id: DUMBBELL_BICEP_CURL,
    CABLE_BICEP_CURL.id: CABLE_BICEP_CURL,
    TRICEPS_PUSHDOWN.id: TRICEPS_PUSHDOWN,
    OVERHEAD_TRICEPS_EXTENSION.id: OVERHEAD_TRICEPS_EXTENSION
}

def main():
    for key, value in EXERCISES.items():
        print(f"{key}: {value.name}")

if __name__ =="__main__":
    main()




