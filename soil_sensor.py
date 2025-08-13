"""
Soil Moisture Sensor Class
Represents and manages individual soil moisture sensors
"""

from counterfit_shims_grove.adc import ADC


class SoilMoistureSensor:
    """Represents a soil moisture sensor"""
    
    def __init__(self, pin, name=None):
        """
        Initialize a soil moisture sensor
        
        Args:
            pin (int): The pin number for this sensor
            name (str, optional): Custom name for the sensor
        """
        self.pin = pin
        self.name = name or f"sensor_{pin + 1}"
        self.adc = ADC()
        
        print(f"Initialized {self.name} on pin {pin}")
    
    def read_moisture(self):
        """
        Read the current soil moisture value
        
        Returns:
            int: The moisture reading (0-1023), or None if error
        """
        try:
            moisture_value = self.adc.read(self.pin)
            return moisture_value
        except Exception as e:
            print(f"Error reading from {self.name} (pin {self.pin}): {e}")
            return None
    
    def __str__(self):
        """String representation of the sensor"""
        return f"SoilMoistureSensor(name='{self.name}', pin={self.pin})"
    
    def __repr__(self):
        """Detailed string representation"""
        return self.__str__()
