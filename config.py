# Simple AWS IoT Core Configuration
# Update these values for your AWS account

AWS_CONFIG = {
    # AWS Region - change to your preferred region
    "region": "us-east-1",
    # IoT Thing name - unique identifier for your device
    "thing_name": "my-soil-monitor",
    # Topic for publishing sensor data
    "topic": "soil-moisture/data",
    # Custom CloudWatch namespace for metrics
    "namespace": "IoT/SoilMoisture"
}
