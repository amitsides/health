from models.sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'Users'
    
    UserID = Column(Integer, primary_key=True)
    Name = Column(String(100))
    DateOfBirth = Column(Date)
    Gender = Column(String(10))
    Height = Column(Float)
    Weight = Column(Float)
    
    physical_activities = relationship("PhysicalActivity", back_populates="user")
    sleep_activities = relationship("SleepActivity", back_populates="user")
    blood_tests = relationship("BloodTest", back_populates="user")

class PhysicalActivity(Base):
    __tablename__ = 'PhysicalActivity'
    
    ActivityID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    Date = Column(Date)
    StepCount = Column(Integer)
    ActiveMinutes = Column(Integer)
    CaloriesBurned = Column(Float)
    HeartRate = Column(Integer)
    
    user = relationship("User", back_populates="physical_activities")

class SleepActivity(Base):
    __tablename__ = 'SleepActivity'
    
    SleepID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    Date = Column(Date)
    SleepDuration = Column(Float)
    SleepQuality = Column(Integer)
    DeepSleepMinutes = Column(Integer)
    REMSleepMinutes = Column(Integer)
    LightSleepMinutes = Column(Integer)
    WakeMinutes = Column(Integer)
    
    user = relationship("User", back_populates="sleep_activities")

class BloodTest(Base):
    __tablename__ = 'BloodTests'
    
    TestID = Column(Integer, primary_key=True)
    UserID = Column(Integer, ForeignKey('Users.UserID'))
    Date = Column(Date)
    GlucoseLevel = Column(Float)
    Cholesterol = Column(Float)
    Triglycerides = Column(Float)
    HDL = Column(Float)
    LDL = Column(Float)
    HemoglobinA1c = Column(Float)
    
    user = relationship("User", back_populates="blood_tests")

# Database connection setup
DATABASE_URL = "sqlite:///./health_database.db"  # Change this to your preferred database URL
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)

# Function to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
