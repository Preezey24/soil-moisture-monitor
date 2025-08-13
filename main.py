"""
Main Application - Soil Moisture Monitoring System
Orchestrates the soil moisture monitoring using CounterFit sensors
"""

import time
from counterfit_api import CounterFitAPI
from soil_sensor import SoilMoistureSensor


def main():
    """Main application function"""
    print("=== Soil Moisture Monitoring System ===")
    print("Initializing system...")
    
    # Initialize the CounterFit API
    api = CounterFitAPI()
    
    # Create 3 soil moisture sensors
    sensors = []
    num_sensors = 3
    
    print(f"\nCreating {num_sensors} soil moisture sensors...")
    
    for pin in range(num_sensors):
        # Create sensor via API
        if api.create_soil_sensor(pin):
            print(f"✓ Created soil moisture sensor on pin {pin}")
            
            # Set initial value
            print(f"Setting initial value for sensor on pin {pin}")
            if api.set_sensor_value(str(pin), 0):
                print(f"✓ Set initial value for sensor on pin {pin}")
            else:
                print(f"✗ Failed to set initial value for sensor on pin {pin}")
            
            # Create sensor object for reading
            sensor = SoilMoistureSensor(pin)
            sensors.append(sensor)
            
        else:
            print(f"✗ Failed to create sensor on pin {pin}")
    
    if not sensors:
        print("No sensors were created successfully. Exiting.")
        return
    
    print(f"\n✓ Successfully initialized {len(sensors)} sensors")
    print("Starting monitoring loop...\n")
    
    # Main monitoring loop
    try:
        while True:
            print(f"=== Reading at {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
            
            # Read from all sensors
            for sensor in sensors:
                try:
                    # Get raw moisture value
                    moisture_raw = sensor.read_moisture()
                    
                    if moisture_raw is not None:
                        print(f"{sensor.name} (pin {sensor.pin}): {moisture_raw}")
                    else:
                        print(f"{sensor.name} (pin {sensor.pin}): ERROR - Could not read value")
                        
                except Exception as e:
                    print(f"Error reading from {sensor.name}: {e}")
            
            print("-" * 50)  # Separator line
            time.sleep(10)  # Wait 10 seconds before next reading
            
    except KeyboardInterrupt:
        print("\n\n=== Monitoring stopped by user ===")
        print("Shutting down gracefully...")
    except Exception as e:
        print(f"\nUnexpected error in main loop: {e}")
    finally:
        print("System shutdown complete.")


if __name__ == "__main__":
    main()
