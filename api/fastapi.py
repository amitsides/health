from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import date
import databases
import sqlalchemy
from sqlalchemy import create_engine

# Initialize FastAPI app
app = FastAPI()

# Database URL - Replace with your actual database URL
DATABASE_URL = "sqlite:///./health_data.db"

# Database connection
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()

# Define SQLAlchemy models
physical_activity = sqlalchemy.Table(
    "PhysicalActivity",
    metadata,
    sqlalchemy.Column("ActivityID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("UserID", sqlalchemy.Integer),
    sqlalchemy.Column("Date", sqlalchemy.Date),
    sqlalchemy.Column("StepCount", sqlalchemy.Integer),
    sqlalchemy.Column("ActiveMinutes", sqlalchemy.Integer),
    sqlalchemy.Column("CaloriesBurned", sqlalchemy.Float),
    sqlalchemy.Column("HeartRate", sqlalchemy.Integer),
)

# Pydantic models for request/response
class PhysicalActivityBase(BaseModel):
    UserID: int
    Date: date
    StepCount: int
    ActiveMinutes: int
    CaloriesBurned: float
    HeartRate: int

class PhysicalActivityCreate(PhysicalActivityBase):
    pass

class PhysicalActivity(PhysicalActivityBase):
    ActivityID: int

    class Config:
        orm_mode = True

# Database events
@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

# API endpoints
@app.get("/api/PhysicalActivity", response_model=List[PhysicalActivity])
async def get_all_physical_activities():
    query = physical_activity.select()
    return await database.fetch_all(query)

@app.post("/api/PhysicalActivity", response_model=PhysicalActivity)
async def create_physical_activity(activity: PhysicalActivityCreate):
    # Get the next ActivityID
    query = "SELECT MAX(ActivityID) FROM PhysicalActivity"
    last_id = await database.fetch_val(query) or 0
    new_id = last_id + 1
    
    # Create new activity record
    query = physical_activity.insert().values(
        ActivityID=new_id,
        UserID=activity.UserID,
        Date=activity.Date,
        StepCount=activity.StepCount,
        ActiveMinutes=activity.ActiveMinutes,
        CaloriesBurned=activity.CaloriesBurned,
        HeartRate=activity.HeartRate
    )
    
    try:
        await database.execute(query)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Return the created activity
    return {**activity.dict(), "ActivityID": new_id}