"""
Simple AWS IoT Core Connection Module
Handles basic connection and data transmission to AWS IoT Core
"""

import json
import boto3
from datetime import datetime, timezone
from typing import Dict
import logging
from botocore.exceptions import NoCredentialsError


class AWSIoTConnection:
    """
    Simple AWS IoT Core connection class for soil moisture data
    """

    def __init__(self, region_name: str, thing_name: str):
        """
        Initialize AWS IoT Core connection

        Args:
            region_name (str): AWS region (e.g., 'us-east-1', 'us-west-2')
            thing_name (str): IoT Thing name for device identification
        """
        self.region_name = region_name
        self.thing_name = thing_name

        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize AWS IoT client
        self._init_iot_client()

    def _init_iot_client(self):
        """Initialize single AWS IoT client"""
        try:
            # Single IoT client for all interactions
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

    def test_connection(self) -> bool:
        """
        Test the AWS IoT Core connection

        Returns:
            bool: True if connection successful, False otherwise
        """
        try:
            # Test connection by attempting to publish to a test topic
            test_payload = {"test": "connection"}
            test_topic = f"soil-moisture/{self.thing_name}/test"

            self.iot_client.publish(
                topic=test_topic, qos=0, payload=json.dumps(test_payload)
            )

            self.logger.info("AWS IoT Core connection test successful")
            return True
        except Exception as e:
            self.logger.error(f"AWS IoT Core connection test failed: {e}")
            return False

    def send_sensor_data(self, sensor_data: Dict) -> bool:
        """
        Send sensor data to AWS IoT Core

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
            # Create payload with timestamp and device info
            payload = {
                "device_id": self.thing_name,
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "data": sensor_data,
            }

            # Define IoT Core topic
            topic = f"soil-moisture/{self.thing_name}/data"

            # Publish to IoT Core
            response = self.iot_client.publish(
                topic=topic,
                qos=1,  # At least once delivery
                payload=json.dumps(payload),
            )

            self.logger.info(f"Data sent to IoT topic: {topic}")
            return True

        except Exception as e:
            self.logger.error(f"Failed to send sensor data: {e}")
            return False

    def get_status(self) -> Dict:
        """
        Get connection status and configuration info

        Returns:
            dict: Status information
        """
        return {
            "region": self.region_name,
            "thing_name": self.thing_name,
            "connected": self.test_connection(),
            "topic": f"soil-moisture/{self.thing_name}/data",
        }
