from counterfit_connection import CounterFitConnection
import requests
import time
from counterfit_shims_grove.adc import ADC

# Initialize the connection
CounterFitConnection.init("127.0.0.1", 8080)


# Create soil moisture sensors programmatically
def create_soil_sensor(pin):
    url = "http://127.0.0.1:8080/create_sensor"
    sensor_config = {
        "type": "Soil Moisture",
        "pin": pin,
        "i2c_pin": 0,
        "port": "/dev/ttyAMA0",
        "name": f"sensor_{pin + 1}",
        "unit": "NoUnits",
        "i2c_unit": "NoUnits",
    }
    try:
        print(f"Creating sensor on pin {pin} with config: {sensor_config}")
        response = requests.post(url, json=sensor_config)
        print(f"Create sensor response: {response.status_code} - {response.text}")
        response.raise_for_status()
        return True
    except requests.HTTPError as e:
        print(f"Error creating sensor on pin {pin}: {e}")
        return False


def set_sensor_value(pin, value):
    """Set a specific value for a sensor"""
    url = "http://127.0.0.1:8080/integer_sensor_settings"
    payload = {
        "port": pin,
        "value": value,
        "is_random": True,
        "random_min": 0,
        "random_max": 1023,
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        return True
    except requests.HTTPError as e:
        print(f"Error setting value for sensor on pin {pin}: {e}")
        return False


# Create 3 soil moisture sensors on pins 0, 1, and 2
for pin in range(3):
    if create_soil_sensor(pin):
        print(f"Created soil moisture sensor on pin {pin}")

        print(f"Setting initial value for sensor on pin {pin}")
        set_sensor_value(str(pin), 0)  # Set initial value to 0
    else:
        print(f"Failed to create sensor on pin {pin}")

adc = ADC()

while True:
    # Read from all three sensors
    for pin in range(3):
        try:
            soil_moisture = adc.read(pin)
            print(f"Soil moisture (pin {pin}): {soil_moisture}")
        except Exception as e:
            print(f"Error reading from pin {pin}: {e}")

    print("-" * 40)  # Separator line
    time.sleep(10)
