"""
CounterFit API Handler
Manages all interactions with the CounterFit simulation API
"""

import requests
from counterfit_connection import CounterFitConnection


class CounterFitAPI:
    """Handles all CounterFit API interactions"""
    
    def __init__(self, host="127.0.0.1", port=8080):
        """Initialize the CounterFit API connection"""
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        
        # Initialize the CounterFit connection
        CounterFitConnection.init(host, port)
        print(f"Initialized CounterFit connection to {host}:{port}")
    
    def create_soil_sensor(self, pin):
        """
        Create a soil moisture sensor programmatically
        
        Args:
            pin (int): The pin number for the sensor
            
        Returns:
            bool: True if sensor created successfully, False otherwise
        """
        url = f"{self.base_url}/create_sensor"
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
            response = requests.post(url, json=sensor_config)
            response.raise_for_status()
            return True
        except requests.HTTPError as e:
            print(f"Error creating sensor on pin {pin}: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error creating sensor on pin {pin}: {e}")
            return False
    
    def set_sensor_value(self, pin, value):
        """
        Set a specific value for a sensor
        
        Args:
            pin (str): The pin identifier for the sensor
            value (int): The value to set
            
        Returns:
            bool: True if value set successfully, False otherwise
        """
        url = f"{self.base_url}/integer_sensor_settings"
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
        except Exception as e:
            print(f"Unexpected error setting value for sensor on pin {pin}: {e}")
            return False
