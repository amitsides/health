# Additional SQLAlchemy models
sleep_activity = sqlalchemy.Table(
    "SleepActivity",
    metadata,
    sqlalchemy.Column("SleepID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("UserID", sqlalchemy.Integer),
    sqlalchemy.Column("Date", sqlalchemy.Date),
    sqlalchemy.Column("SleepDuration", sqlalchemy.Float),
    sqlalchemy.Column("SleepQuality", sqlalchemy.Integer),
    sqlalchemy.Column("DeepSleepMinutes", sqlalchemy.Integer),
    sqlalchemy.Column("REMSleepMinutes", sqlalchemy.Integer),
    sqlalchemy.Column("LightSleepMinutes", sqlalchemy.Integer),
    sqlalchemy.Column("WakeMinutes", sqlalchemy.Integer),
)

blood_tests = sqlalchemy.Table(
    "BloodTests",
    metadata,
    sqlalchemy.Column("TestID", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("UserID", sqlalchemy.Integer),
    sqlalchemy.Column("Date", sqlalchemy.Date),
    sqlalchemy.Column("GlucoseLevel", sqlalchemy.Float),
    sqlalchemy.Column("Cholesterol", sqlalchemy.Float),
    sqlalchemy.Column("Triglycerides", sqlalchemy.Float),
    sqlalchemy.Column("HDL", sqlalchemy.Float),
    sqlalchemy.Column("LDL", sqlalchemy.Float),
    sqlalchemy.Column("HemoglobinA1c", sqlalchemy.Float),
)