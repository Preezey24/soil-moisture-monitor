"""
IoT-Only AWS Integration Module
Handles AWS IoT Core connection with rules-based CloudWatch routing
"""

import json
import boto3
from datetime import datetime, timezone
from typing import Dict, List
import logging
from botocore.exceptions import NoCredentialsError
from config import AWS_CONFIG


class IoTService:
    """
    Simplified AWS IoT service class for soil moisture data
    """

    def __init__(self, region_name: str, thing_name: str):
        """
        Initialize AWS IoT Core

        Args:
            region_name (str): AWS region (e.g., 'us-east-1', 'us-west-2')
            thing_name (str): IoT Thing name for device identification
        """
        self.region_name = region_name
        self.thing_name = thing_name

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize IoT client only
        self._init_iot_client()

    def _init_iot_client(self):
        """Initialize AWS IoT client"""
        try:
            # IoT client for device communication
            self.iot_client = boto3.client("iot-data", region_name=self.region_name)

            self.logger.info(
                f"AWS IoT client initialized for region: {self.region_name}"
            )

        except NoCredentialsError:
            self.logger.error("AWS credentials not found. Please run 'aws configure'")
            raise
        except Exception as e:
            self.logger.error(f"Error initializing AWS IoT client: {e}")
            raise

    def send_sensor_data(self, sensor_data: Dict) -> bool:
        """
        Send sensor data to IoT Core

        Args:
            sensor_data (dict): Dictionary containing sensor data
                Example: {
                    'sensor_name': 'sensor_1',
                    'pin': 0,
                    'moisture_value': 512,
                    'location': 'garden'
                }

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create IoT payload with sensor data
            # IoT Rules will extract the necessary fields for CloudWatch
            payload = {
                "device_id": self.thing_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "sensor_data": sensor_data
            }

            # Define IoT Core topic
            topic = AWS_CONFIG["topic"]
            
            response = self.iot_client.publish(
                topic=topic,
                qos=1,  # At least once delivery
                payload=json.dumps(payload),
            )

            self.logger.info(f"Data sent to IoT topic: {topic}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send sensor data to IoT Core: {e}")
            return False

    def send_multiple_sensor_data(self, sensor_data_list: List[Dict]) -> bool:
        """
        Send multiple sensor readings to IoT Core in efficient batches
        
        Args:
            sensor_data_list (List[Dict]): List of sensor data dictionaries
            
        Returns:
            bool: True if all successful, False otherwise
        """
        try:
            # Create a single batch payload with all sensor readings
            batch_payload = {
                "device_id": self.thing_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "batch_sensor_data": sensor_data_list,
                "sensor_count": len(sensor_data_list)
            }

            # Send batch to IoT Core
            topic = AWS_CONFIG["topic"]
            
            response = self.iot_client.publish(
                topic=topic,
                qos=1,
                payload=json.dumps(batch_payload),
            )

            self.logger.info(f"Batch of {len(sensor_data_list)} sensor readings sent to IoT Core")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send batch sensor data to IoT Core: {e}")
            return False
