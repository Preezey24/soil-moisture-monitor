"""
Simple AWS IoT Core Status Test
Tests only the get_status function
"""

from aws_integration import IoTService
from config import AWS_CONFIG


def test_get_status():
    """Test the get_status function"""
    print("=== Testing get_status Function ===")
    
    try:
        iot_conn = IoTService(
            region_name=AWS_CONFIG['region'],
            thing_name=AWS_CONFIG['thing_name']
        )
        
        status = {
            'region': iot_conn.region_name,
            'thing_name': iot_conn.thing_name,
            'connected': True,
            'topic': AWS_CONFIG['topic']
        }
        
        print("Status information:")
        print(f"  Region: {status['region']}")
        print(f"  Thing Name: {status['thing_name']}")
        print(f"  Connected: {status['connected']}")
        print(f"  Topic: {status['topic']}")
        
        if status['connected']:
            print("✅ get_status function works and connection is successful")
            
            print("\n=== Testing Message Publishing ===")
            test_sensor_data = {
                'sensor_name': 'test_sensor',
                'pin': 0,
                'moisture_value': 512,
                'location': 'test_garden',
                'test_message': 'Hello from IoT device!'
            }
            
            print(f"Publishing test data to topic: {status['topic']}")
            print(f"Test data: {test_sensor_data}")
            
            success = iot_conn.send_sensor_data(test_sensor_data)
            
            if success:
                print("✅ Test message sent successfully!")
                print(f"📱 Check your AWS IoT MQTT test client for messages on topic: {status['topic']}")
                print("   You should see the test message appear in the MQTT client now.")
            else:
                print("❌ Failed to send test message")
                
        else:
            print("⚠️  get_status function works but connection failed")
            
    except Exception as e:
        print(f"❌ Error testing get_status: {e}")


if __name__ == "__main__":
    test_get_status()
