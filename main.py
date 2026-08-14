from app.models import *

# when using Enums in python, use the member itself. only refer to the name when moving outside python
userP = UserProfile(
    goal=TrainingGoal.STRENGTH,
    experience=ExperienceLevel.ADVANCED,
    days_per_week=5,
    max_workout_minutes=60,
    available_equipment={Equipment.BENCH, Equipment.DUMBELL, Equipment.SMITH_MACHINE},
    excluded_exercise_ids={"back_squat"},
    avoided_exercise_ids={"bulgarian_split_squat"},
    preferred_exercise_ids={"incline_dumbbell_bench"}
)

print(userP.avoided_exercise_ids)
print(userP.goal == "strength")