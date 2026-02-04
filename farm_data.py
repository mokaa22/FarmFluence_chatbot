# farm_data.py
def get_live_farm_data(user_id: str):
    """
    This will later come from dashboard / DB / IoT / cloud
    """
    return {
        "crop": "Tomato",
        "soil_moisture": 28,      # %
        "temperature": 32,        # °C
        "humidity": 45,           # %
        "rain_forecast": False
    }
