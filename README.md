# Depth Monitor with WhatsApp Alert

This application monitors depth and sends a WhatsApp alert when the depth exceeds 13cm.

## Setup Instructions

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file based on `.env.example` and fill in your Twilio credentials:
   - Get your Twilio credentials from https://www.twilio.com/console
   - Enable WhatsApp sandbox in your Twilio account
   - Add the target phone number (+91904339525259) to your WhatsApp sandbox

3. Run the application:
```bash
python depth_monitor.py
```

## Features

- Monitors depth continuously
- Sends WhatsApp alert when depth exceeds 13cm
- Configurable threshold
- Simulated depth reading (replace with actual sensor in production)

## Note

This is a basic implementation. In production, you would need to:
1. Replace the simulated depth reading with actual sensor data
2. Add proper error handling and logging
3. Consider adding configuration options for threshold and monitoring interval
