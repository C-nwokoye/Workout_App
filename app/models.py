from enum import Enum
from dataclasses import dataclass, field

class TrainingGoal(Enum):
    STRENGTH = "strength" 
    HYPERTROPHY = "hypertrophy" 
    STRENGTH_HYPERTROPHY = "strength_Hypertrophy"

class ExperienceLevel(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"

class Equipment(Enum):
    BARBELL = "barbell"
    DUMBBELL = "dumbbell"
    BENCH = "bench"
    SQUAT_RACK = "squat_rack"
    CABLE = "cable"
    PULL_UP_BAR = "pullup_bar"
    SMITH_MACHINE = "smith_machine"
    LOW_CABLE_ROW_MACHINE = "low_cable_row_machine"
    LAT_PULLDOWN_MACHINE = "lat_pulldown_machine"
    LEG_PRESS_MACHINE = "leg_press_machine"
    LEG_EXTENSION_MACHINE = "leg_extension_machine"
    LEG_CURL_MACHINE = "leg_curl_machine"
    CALF_RAISE_MACHINE = "calf_raise_machine"
    BODYWEIGHT = "bodyweight"

class MuscleGroup(Enum):
    CHEST = "chest"
    BACK = "back"
    QUADRICEP = "quadricep"
    HAMSTRINGS = "hamstrings"
    GLUTES = "glutes"
    SHOULDERS = "shoulders"
    BICEPS = "biceps"
    TRICEPS = "triceps"
    CALVES = "calves"
    CORE = "core"

class MovementPattern(Enum):
    HORIZONTAL_PUSH = "horizontal_push"
    HORIZONTAL_PULL = "horizontal_pull"

    VERTICAL_PUSH = "vertical_push"
    VERTICAL_PULL = "vertical_pull"

    SQUAT = "squat"
    HINGE = "hinge"

    KNEE_FLEXION = "knee_flexion"
    KNEE_EXTENSION = "knee_extension"
    ELBOW_FLEXION = "elbow_flexion"
    ELBOW_EXTENSION = "elbow_extension"

    SHOULDER_ABDUCTION = "shoulder_abduction"

    CALF_RAISE = "calf_raise"
    CORE = "core"

class ExerciseType(Enum):
    ISOLATION = "isolation"
    COMPOUND = "compound"

# dataclass helps us build a class with default values instead of writing the constructor ourselves
# purely for decoration, not enforced at runtime. 
@dataclass
class Exercise:
    id: str
    name: str
    primary_muscle: MuscleGroup
    # will be a set of muscle_groups, field(default_factory = set) just initializes an empty set
    # we use a set not a list because we dont care about order

    exercise_type: ExerciseType

    movement_pattern: MovementPattern

    secondary_muscles: set[MuscleGroup] = field(default_factory=set)

    equipment_required: set[Equipment] = field(default_factory=set)

    
@dataclass
class UserProfile:
    goal: TrainingGoal
    experience: ExperienceLevel
    days_per_week: int
    max_workout_minutes: int
    available_equipment: set[Equipment] = field(default_factory=set)

    excluded_exercise_ids: set[str] = field(default_factory=set)

    avoided_exercise_ids: set[str] = field(default_factory=set)

    preferred_exercise_ids: set[str] = field(default_factory=set)




