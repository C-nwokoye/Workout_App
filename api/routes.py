from fastapi import FastAPI, HTTPException
from app.database import load_full_history, save_completed_workout
from api.schemas import *

app = FastAPI()

@app.get("/health") # decorator
# when there is a GET request at /health endpoint, call this function and return the result
# fastAPI automatically converts the returned dict into JSON
def health_check():
    return {"status": "ok"}

@app.get("/workout-history", response_model=list[CompletedWorkoutSchema])
# response model defines the exact schema the connected function should return
# response model requires each schema to specifically allow reading from non-dict objects
def get_workout_history():
    return load_full_history()
# FastAPI runs model_validate automatically using this return value based on what is passed to response_model
# after all model_validate calls run FastAPI serializes result and sends it to http as JSON

@app.post("/completed-workouts")
def create_completed_workout(payload: CompletedWorkoutInputSchema):
    try:
        completed_workout = completed_workout_to_domain(payload)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    workout_id = save_completed_workout(completed_workout)
    return {"id": workout_id, "status": "saved"}