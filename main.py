from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
import models
import schemas
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import pytz


Base.metadata.create_all(bind=engine)


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "¡Bienvenido a tu servidor FastAPI para manejar datos de temperatura y pulso desde tu dispositivo!"


@app.get("/temperatures", response_model=List[schemas.Temperature])
def list_temperatures(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):

    temperatures = session.query(models.Temperature).offset(skip).limit(limit).all()

    return temperatures


@app.get("/pulses", response_model=List[schemas.Pulse])
def list_pulses(skip: int = 0, limit: int = 10, session: Session = Depends(get_session)):

    pulses = session.query(models.Pulse).offset(skip).limit(limit).all()

    return pulses


@app.post("/temperature", response_model=schemas.Temperature, status_code=status.HTTP_201_CREATED)
def create_temperature(temperature: schemas.TemperatureCreate, session: Session = Depends(get_session)):

    local_tz = pytz.timezone("America/Lima")
    

    timestamp_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    timestamp_local = timestamp_utc.astimezone(local_tz)

    temperature_db = models.Temperature(value=temperature.value, timestamp=timestamp_local)


    session.add(temperature_db)
    session.commit()
    session.refresh(temperature_db)

    return temperature_db


@app.get("/temperature/{id}", response_model=schemas.Temperature)
def read_temperature(id: int, session: Session = Depends(get_session)):

    temperature = session.query(models.Temperature).get(id)

    if not temperature:
        raise HTTPException(status_code=404, detail=f"Temperature data with id {id} not found")

    return temperature


@app.post("/pulse", response_model=schemas.Pulse, status_code=status.HTTP_201_CREATED)
def create_pulse(pulse: schemas.PulseCreate, session: Session = Depends(get_session)):
    local_tz = pytz.timezone("America/Lima")
    

    timestamp_utc = datetime.utcnow().replace(tzinfo=pytz.utc)
    timestamp_local = timestamp_utc.astimezone(local_tz)

    pulse_db = models.Pulse(value=pulse.value, timestamp=timestamp_local)

    session.add(pulse_db)
    session.commit()
    session.refresh(pulse_db)

    return pulse_db


@app.get("/pulse/{id}", response_model=schemas.Pulse)
def read_pulse(id: int, session: Session = Depends(get_session)):

    pulse = session.query(models.Pulse).get(id)

    if not pulse:
        raise HTTPException(status_code=404, detail=f"Pulse data with id {id} not found")

    return pulse


@app.delete("/temperatures", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_temperatures(session: Session = Depends(get_session)):
    session.query(models.Temperature).delete()
    session.commit()
    return None


@app.delete("/pulses", status_code=status.HTTP_204_NO_CONTENT)
def delete_all_pulses(session: Session = Depends(get_session)):
    session.query(models.Pulse).delete()
    session.commit()
    return None

