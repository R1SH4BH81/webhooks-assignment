import requests
import json
from datetime import datetime, timezone
import time
import sys

# URL of the webhook receiver
webhook_url = 'http://localhost:5000/webhook'

# Sample data for testing different actions
test_actions = [
    {
        'request_id': 'commit123',
        'author': 'Travis',
        'action': 'PUSH',
        'from_branch': '',  # Not needed for PUSH
        'to_branch': 'staging',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'request_id': 'pr456',
        'author': 'Travis',
        'action': 'PULL_REQUEST',
        'from_branch': 'staging',
        'to_branch': 'master',
        'timestamp': datetime.now(timezone.utc).isoformat()
    },
    {
        'request_id': 'merge789',
        'author': 'Travis',
        'action': 'MERGE',
        'from_branch': 'dev',
        'to_branch': 'master',
        'timestamp': datetime.now(timezone.utc).isoformat()
    }
]

# Check if Flask server is running
def check_server():
    try:
        response = requests.get('http://localhost:5000/actions', timeout=2)
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the Flask server at http://localhost:5000")
        print("Please make sure webhook_receiver.py is running first.")
        print("\nRun the following command in a separate terminal:")
        print("python webhook_receiver.py")
        return False

# Main execution
if not check_server():
    sys.exit(1)

# Send each test action to the webhook
for action in test_actions:
    print(f"Sending {action['action']} action...")
    try:
        response = requests.post(webhook_url, json=action)
        print(f"Response: {response.status_code} - {response.text}\n")
        # Add a small delay between requests
        time.sleep(0.5)
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}\n")

print("Test complete! Open ui.html in your browser to see the results.")
print("\nTo view the UI, run the following command in a separate terminal:")
print("python serve_ui.py")
print("Then open http://localhost:8000/ui.html in your browser.")