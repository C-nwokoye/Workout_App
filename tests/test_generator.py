# tests/test_generator.py
import pytest
from app.models import *
import app.generator as generator


# --- small, controlled exercise set, isolated from the real registry ---

FAKE_BENCH = Exercise(
    id="fake_bench", name="Fake Bench", primary_muscle=MuscleGroup.CHEST,
    strength_suitability=Suitability_Level.HIGH, hypertrophy_suitability=Suitability_Level.HIGH,
    exercise_type=ExerciseType.COMPOUND, movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    equipment_required={Equipment.BARBELL, Equipment.BENCH},
)

FAKE_BENCH_2 = Exercise(
    id="fake_bench_2", name="Fake Bench 2", primary_muscle=MuscleGroup.CHEST,
    strength_suitability=Suitability_Level.HIGH, hypertrophy_suitability=Suitability_Level.HIGH,
    exercise_type=ExerciseType.COMPOUND, movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    equipment_required={Equipment.BARBELL, Equipment.BENCH},
)

FAKE_INCLINE = Exercise(
    id="fake_incline", name="Fake Incline", primary_muscle=MuscleGroup.CHEST,
    strength_suitability=Suitability_Level.MEDIUM, hypertrophy_suitability=Suitability_Level.HIGH,
    exercise_type=ExerciseType.COMPOUND, movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    equipment_required={Equipment.DUMBBELL, Equipment.BENCH},
)

FAKE_FLY = Exercise(
    id="fake_fly", name="Fake Fly", primary_muscle=MuscleGroup.CHEST,
    strength_suitability=Suitability_Level.LOW, hypertrophy_suitability=Suitability_Level.HIGH,
    exercise_type=ExerciseType.COMPOUND, movement_pattern=MovementPattern.HORIZONTAL_PUSH,
    equipment_required={Equipment.CABLE},
)

FAKE_EXERCISES = {e.id: e for e in [FAKE_BENCH, FAKE_BENCH_2, FAKE_INCLINE, FAKE_FLY]}


@pytest.fixture
def fake_registry(monkeypatch):
    monkeypatch.setattr(generator, "EXERCISES", FAKE_EXERCISES)


@pytest.fixture
def strength_chest_slot():
    return WorkoutSlot(
        movement_pattern=MovementPattern.HORIZONTAL_PUSH, exercise_type=ExerciseType.COMPOUND,
        primary_muscles={MuscleGroup.CHEST}, training_emphasis=TrainingGoal.STRENGTH,
        sets=4, min_reps=4, max_reps=6, rest_seconds=180,
    )

def test_suitability_checker_raises_for_unsupported_emphasis(fake_registry, strength_chest_slot):
    unsupported_slot = WorkoutSlot(
        movement_pattern=strength_chest_slot.movement_pattern,
        exercise_type=strength_chest_slot.exercise_type,
        primary_muscles=strength_chest_slot.primary_muscles,
        training_emphasis=TrainingGoal.STRENGTH_HYPERTROPHY,
        sets=4, min_reps=4, max_reps=6, rest_seconds=180,
    )
    with pytest.raises(ValueError):
        generator.suitability_checker(unsupported_slot, "fake_bench")

def make_profile(**overrides):
    defaults = dict(
        goal=TrainingGoal.STRENGTH_HYPERTROPHY, experience=ExperienceLevel.ADVANCED,
        days_per_week=5, max_workout_minutes=60,
        available_equipment={Equipment.BARBELL, Equipment.DUMBBELL, Equipment.BENCH, Equipment.CABLE},
        excluded_exercise_ids=set(), avoided_exercise_ids=set(), preferred_exercise_ids=set(),
    )
    defaults.update(overrides)
    return UserProfile(**defaults)


# --- eligibility filtering ---

def test_equipment_filtering_excludes_missing_equipment(fake_registry):
    profile = make_profile(available_equipment={Equipment.DUMBBELL, Equipment.BENCH})
    eligible = generator.get_eligible_exercises(profile)
    assert "fake_bench" not in eligible  # requires barbell, not available
    assert "fake_incline" in eligible


def test_excluded_exercise_is_hard_filtered(fake_registry):
    profile = make_profile(excluded_exercise_ids={"fake_bench"})
    eligible = generator.get_eligible_exercises(profile)
    assert "fake_bench" not in eligible
    assert "fake_incline" in eligible


# --- selection / ranking ---

def test_avoided_exercise_loses_to_neutral_alternative(fake_registry, strength_chest_slot):
    profile = make_profile(avoided_exercise_ids={"fake_bench"})
    candidates = {"fake_bench", "fake_incline"}
    chosen = generator.select_exercise(profile, candidates, set(), set(), strength_chest_slot)
    assert chosen == "fake_incline"


def test_avoided_exercise_selected_when_only_candidate(fake_registry, strength_chest_slot):
    profile = make_profile(avoided_exercise_ids={"fake_bench"})
    candidates = {"fake_bench"}
    chosen = generator.select_exercise(profile, candidates, set(), set(), strength_chest_slot)
    assert chosen == "fake_bench"


def test_preferred_wins_with_equal_suitability(fake_registry, strength_chest_slot):
    profile = make_profile(preferred_exercise_ids={"fake_bench_2"})
    candidates = {"fake_bench", "fake_bench_2"}
    chosen = generator.select_exercise(profile, candidates, set(), set(), strength_chest_slot)
    assert chosen == "fake_bench_2"


def test_suitability_overrides_preference(fake_registry, strength_chest_slot):
    profile = make_profile(preferred_exercise_ids={"fake_fly"})  # LOW strength suitability
    candidates = {"fake_bench", "fake_fly"}  # fake_bench: HIGH, not preferred
    chosen = generator.select_exercise(profile, candidates, set(), set(), strength_chest_slot)
    assert chosen == "fake_bench"


def test_repeated_exercise_prohibited_within_workout(fake_registry, strength_chest_slot):
    profile = make_profile()
    candidates = {"fake_bench"}
    already_selected = {"fake_bench"}
    with pytest.raises(ValueError):
        generator.select_exercise(profile, candidates, already_selected, set(), strength_chest_slot)


def test_weekly_variety_breaks_tie(fake_registry, strength_chest_slot):
    profile = make_profile()
    candidates = {"fake_bench", "fake_bench_2"}
    used_this_week = {"fake_bench"}
    chosen = generator.select_exercise(profile, candidates, set(), used_this_week, strength_chest_slot)
    assert chosen == "fake_bench_2"


def test_get_candidates_for_slot_raises_when_no_match(fake_registry):
    slot = WorkoutSlot(
        movement_pattern=MovementPattern.SQUAT, exercise_type=ExerciseType.COMPOUND,
        primary_muscles={MuscleGroup.QUADRICEP}, training_emphasis=TrainingGoal.STRENGTH,
        sets=4, min_reps=4, max_reps=6, rest_seconds=180,
    )
    with pytest.raises(ValueError):
        generator.get_candidates_for_slot(set(FAKE_EXERCISES.keys()), slot)


# --- historical lookup / progression (no registry dependency) ---

def _completed_exercise(exercise, emphasis, recommended_weight, sets_data):
    workout_exercise = WorkoutExercise(
        exercise=exercise, emphasis=emphasis, sets=len(sets_data),
        min_reps=8, max_reps=10, rest_seconds=90, recommended_weight=recommended_weight,
    )
    completed_sets = [CompletedSet(reps=r, weight=w) for r, w in sets_data]
    return CompletedExercise(workout_exercise=workout_exercise, completed_sets=completed_sets)


def _workout_with(completed_exercise, completed_at="2026-01-01T00:00:00"):
    workout = Workout(workout_type=None, exercises=[completed_exercise.workout_exercise.exercise])
    return CompletedWorkout(
        workout=workout, completed_exercises=[completed_exercise], completed_at=completed_at,
    )


def test_no_history_returns_none_recommended_weight():
    result = generator.get_next_recommended_weight("fake_bench", TrainingGoal.STRENGTH, [])
    assert result is None


def test_different_emphasis_not_matched():
    ce = _completed_exercise(FAKE_BENCH, TrainingGoal.HYPERTROPHY, 100.0, [(10, 100.0)] * 3)
    history = [_workout_with(ce)]
    result = generator.get_latest_completed_exercise("fake_bench", TrainingGoal.STRENGTH, history)
    assert result is None


def test_first_completion_uses_min_completed_weight_as_reference():
    ce = _completed_exercise(FAKE_BENCH, TrainingGoal.STRENGTH, None, [(10, 95.0), (9, 100.0), (8, 90.0)])
    history = [_workout_with(ce)]
    result = generator.get_next_recommended_weight("fake_bench", TrainingGoal.STRENGTH, history)
    assert result == 90.0


def test_successful_progression_increases_weight():
    ce = _completed_exercise(FAKE_BENCH, TrainingGoal.STRENGTH, 100.0, [(10, 100.0)] * 3)
    history = [_workout_with(ce)]
    result = generator.get_next_recommended_weight("fake_bench", TrainingGoal.STRENGTH, history)
    assert result == pytest.approx(105.0)


def test_dropping_below_recommended_weight_does_not_progress():
    ce = _completed_exercise(FAKE_BENCH, TrainingGoal.STRENGTH, 100.0, [(10, 100.0), (10, 100.0), (10, 90.0)])
    history = [_workout_with(ce)]
    result = generator.get_next_recommended_weight("fake_bench", TrainingGoal.STRENGTH, history)
    assert result == 100.0  # unchanged, not progressed