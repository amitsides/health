-- User table to store basic information about individuals
CREATE TABLE Users (
    UserID INT PRIMARY KEY,
    Name VARCHAR(100),
    DateOfBirth DATE,
    Gender VARCHAR(10),
    Height FLOAT,
    Weight FLOAT
);

-- Physical Activity table
CREATE TABLE PhysicalActivity (
    ActivityID INT PRIMARY KEY,
    UserID INT,
    Date DATE,
    StepCount INT,
    ActiveMinutes INT,
    CaloriesBurned FLOAT,
    HeartRate INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Sleep Activity table
CREATE TABLE SleepActivity (
    SleepID INT PRIMARY KEY,
    UserID INT,
    Date DATE,
    SleepDuration FLOAT,
    SleepQuality INT,
    DeepSleepMinutes INT,
    REMSleepMinutes INT,
    LightSleepMinutes INT,
    WakeMinutes INT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Blood Tests table
CREATE TABLE BloodTests (
    TestID INT PRIMARY KEY,
    UserID INT,
    Date DATE,
    GlucoseLevel FLOAT,
    Cholesterol FLOAT,
    Triglycerides FLOAT,
    HDL FLOAT,
    LDL FLOAT,
    HemoglobinA1c FLOAT,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

-- Index for faster queries
CREATE INDEX idx_user_date ON PhysicalActivity (UserID, Date);
CREATE INDEX idx_sleep_date ON SleepActivity (UserID, Date);
CREATE INDEX idx_blood_date ON BloodTests (UserID, Date);
