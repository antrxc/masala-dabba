import os
from twilio.rest import Client
from dotenv import load_dotenv
import time
import requests

class DepthMonitor:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        
        # Initialize Twilio client
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.twilio_phone = os.getenv('TWILIO_PHONE_NUMBER')
        
        if not all([self.account_sid, self.auth_token, self.twilio_phone]):
            raise ValueError("Please set TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, and TWILIO_PHONE_NUMBER in .env file")
        
        self.client = Client(self.account_sid, self.auth_token)
        self.target_number = '+91904339525259'
        self.depth_threshold = 13  # in cm
        self.thingspeak_channel_id = "2971630"
        self.thingspeak_field_number = 1
        self.thingspeak_read_api_key = "CXMQZB0SQRA73H80"
        
    def send_whatsapp_message(self, depth):
        message = f"Alert: Depth has exceeded 13cm! Current depth: {depth}cm"
        try:
            self.client.messages.create(
                from_='whatsapp:' + self.twilio_phone,
                body=message,
                to='whatsapp:' + self.target_number
            )
            print(f"WhatsApp message sent successfully: {message}")
        except Exception as e:
            print(f"Error sending WhatsApp message: {str(e)}")

    def fetch_depth_from_thingspeak(self):
        """Fetch the latest depth reading from ThingSpeak"""
        try:
            url = f"https://api.thingspeak.com/channels/{self.thingspeak_channel_id}/fields/{self.thingspeak_field_number}/last.json"
            params = {}
            if self.thingspeak_read_api_key:
                params["api_key"] = self.thingspeak_read_api_key
            
            response = requests.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                depth = float(data.get("field1", 0))
                print(f"Current depth: {depth:.2f}cm")
                return depth
            else:
                print(f"Error fetching data from ThingSpeak: HTTP {response.status_code}")
                return None
        except Exception as e:
            print(f"Error fetching data from ThingSpeak: {str(e)}")
            return None

    def monitor_depth(self):
        while True:
            depth = self.fetch_depth_from_thingspeak()
            if depth is not None and depth > self.depth_threshold:
                self.send_whatsapp_message(depth)
            
            time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    try:
        monitor = DepthMonitor()
        print("Starting depth monitoring from ThingSpeak...")
        monitor.monitor_depth()
    except KeyboardInterrupt:
        print("\nMonitoring stopped")
