from fastapi import APIRouter
from models.schemas import SensorData, IntensityRecommendation

# Module 3: Smart Gym Assistant (AI + IoT Integration)
# Receives sensor data via MQTT and exposes REST endpoints
# MQTT integration: use paho-mqtt library, subscribe to gym/# topics
# This REST layer acts as the bridge between MQTT and the frontend

router = APIRouter()

# heart rate zone thresholds (% of max HR, assuming max = 220 - age)
# using generic thresholds for now
HR_ZONES = {
    "Zone 1": (0, 115),      # very light
    "Zone 2": (115, 130),    # light / fat burn
    "Zone 3": (130, 145),    # moderate / aerobic
    "Zone 4": (145, 160),    # hard / anaerobic
    "Zone 5": (160, 999),    # maximum
}


def classify_hr_zone(bpm: int) -> str:
    for zone, (low, high) in HR_ZONES.items():
        if low <= bpm < high:
            return zone
    return "Zone 5"


def get_recommendation(sensor: SensorData) -> IntensityRecommendation:
    hr = sensor.heart_rate or 120
    zone = classify_hr_zone(hr)

    alert = None
    if hr > 155:
        alert = f"Heart rate at {hr} BPM — approaching Zone 4/5. Consider slowing down or resting."

    # resistance recommendation logic
    current_resistance = sensor.cable_resistance or 40.0
    if zone in ["Zone 4", "Zone 5"]:
        suggested = max(current_resistance - 5, 10)
        rest_in = 2.0
    elif zone == "Zone 3":
        suggested = current_resistance
        rest_in = 4.0
    else:
        suggested = min(current_resistance + 2.5, 100)
        rest_in = 6.0

    return IntensityRecommendation(
        recommended_zone="Zone 3" if zone in ["Zone 4", "Zone 5"] else zone,
        suggested_resistance=suggested,
        next_rest_in_mins=rest_in,
        alert=alert,
    )


@router.post("/sensor-data", response_model=IntensityRecommendation)
def receive_sensor_data(data: SensorData):
    """
    Receive real-time sensor data from IoT equipment and return AI recommendation.
    In production: this would also be triggered by MQTT messages via paho-mqtt.
    
    MQTT setup example:
        import paho.mqtt.client as mqtt
        client = mqtt.Client()
        client.connect("192.168.1.100", 1883)
        client.subscribe("gym/#")
        client.on_message = lambda c, u, msg: process_sensor(msg)
    """
    return get_recommendation(data)


@router.get("/live/{device_id}")
def get_live_stats(device_id: str):
    """
    Get latest sensor readings for a device.
    TODO: pull from Redis cache (MQTT publishes → Redis → this endpoint).
    Returns mock data for now.
    """
    import random
    bpm = random.randint(118, 155)
    return {
        "device_id": device_id,
        "heart_rate": bpm,
        "hr_zone": classify_hr_zone(bpm),
        "treadmill_speed_kmh": round(random.uniform(6.0, 9.0), 1),
        "treadmill_incline_deg": round(random.uniform(2.0, 5.0), 1),
        "cable_resistance_kg": random.choice([35, 40, 42.5, 45, 47.5, 50]),
        "calories_burned": random.randint(280, 380),
        "session_duration_mins": random.randint(30, 55),
    }


@router.get("/zones")
def get_hr_zones():
    """Return heart rate zone definitions."""
    return {
        zone: {"min_bpm": low, "max_bpm": high if high != 999 else "max"}
        for zone, (low, high) in HR_ZONES.items()
    }
