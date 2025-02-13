from kafka import KafkaConsumer
from sqlalchemy import create_engine, Column, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense

Base = declarative_base()

class HealthData(Base):
    __[tablename](pplx://action/followup)__ = 'health_data'
    
    id = Column(Integer, primary_key=True)
    GlucoseLevel = Column(Float)
    Cholesterol = Column(Float)
    Triglycerides = Column(Float)
    HDL = Column(Float)
    LDL = Column(Float)
    HemoglobinA1c = Column(Float)

# Set up Kafka consumer
consumer = KafkaConsumer('health_data_topic', bootstrap_servers=['localhost:9092'])

# Set up database connection
engine = create_engine('postgresql://username:password@localhost:5432/healthdb')
Session = sessionmaker(bind=engine)
session = Session()

# LSTM model setup
model = Sequential([
    LSTM(64, input_shape=(6, 1), return_sequences=True),
    LSTM(32),
    Dense(1)
])
model.compile(optimizer='adam', loss='mse')

# Process incoming data
for message in consumer:
    data = message.value
    
    # Store data in database
    health_data = HealthData(**data)
    session.add(health_data)
    session.commit()
    
    # Prepare data for LSTM model
    X = np.array([data['GlucoseLevel'], data['Cholesterol'], data['Triglycerides'],
                  data['HDL'], data['LDL'], data['HemoglobinA1c']]).reshape(1, 6, 1)
    
    # Train LSTM model
    model.fit(X, y, epochs=1, verbose=0)

# Close database session
session.close()
