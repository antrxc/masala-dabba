import requests

# ThingSpeak Channel Info
channel_id = "2971630"
field_number = 1
read_api_key = "CXMQZB0SQRA73H80"  # Leave empty if public; otherwise paste your Read API Key

# URL to get latest entry
url = f"https://api.thingspeak.com/channels/{channel_id}/fields/{field_number}/last.json"

params = {}
if read_api_key:
    params["api_key"] = read_api_key

response = requests.get(url, params=params)

if response.status_code == 200:
    data = response.json()
    value = data.get("field1")
    print(f"📏 Latest Distance: {value} cm")
else:
    print(f"❌ Failed to fetch data. HTTP {response.status_code}")

