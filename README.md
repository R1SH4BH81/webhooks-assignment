# GitHub Webhook Receiver & UI

## Overview
This project implements a minimal system to receive GitHub webhook events (Push, Pull Request, Merge), store them in MongoDB, and display them in a clean UI that polls for updates every 15 seconds.

## Project Structure
- `webhook_receiver.py`: Flask backend that receives webhook events and stores them in MongoDB
- `ui.html`: Frontend UI that displays GitHub actions
- `test_webhook.py`: Test script to generate sample webhook events
- `serve_ui.py`: Simple HTTP server to serve the UI file
- `requirements.txt`: Python dependencies

## Backend (Flask Webhook Receiver)
- Receives POST requests at `/webhook` with the following JSON schema:
  - `request_id` (string): Git commit hash or PR ID
  - `author` (string): GitHub username
  - `action` (string): One of `PUSH`, `PULL_REQUEST`, `MERGE`
  - `from_branch` (string): Source branch
  - `to_branch` (string): Target branch
  - `timestamp` (string, datetime): UTC ISO format
- Stores events in MongoDB (`github_webhooks.actions` collection)
- Provides `/actions` endpoint to fetch all actions sorted by timestamp (desc)

### Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start MongoDB locally or set `MONGO_URI` env variable.
3. Run the Flask app:
   ```bash
   python webhook_receiver.py
   ```

## Frontend (Minimal UI)
1. Serve the UI using the included HTTP server:
   ```bash
   python serve_ui.py
   ```
2. Open `http://localhost:8000/ui.html` in your browser.
3. The UI polls the `/actions` endpoint every 15 seconds and displays events in the required format.

## Testing
To test the system without setting up actual GitHub webhooks:

1. Start the Flask backend:
   ```bash
   python webhook_receiver.py
   ```
2. Run the test script to generate sample webhook events:
   ```bash
   python test_webhook.py
   ```
3. View the results in the UI.

## Webhook Setup for GitHub
1. Go to your GitHub repository settings
2. Navigate to Webhooks > Add webhook
3. Set Payload URL to `http://<your-server>:5000/webhook`
4. Set Content type to `application/json`
5. Select events: Push, Pull Requests, and Merge
6. Save the webhook

## Example Event Formats
- **PUSH:** `"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC`
- **PULL_REQUEST:** `"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC`
- **MERGE:** `"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC`

## Architecture
- GitHub events trigger webhooks to the Flask backend
- Flask backend validates and stores events in MongoDB
- UI polls MongoDB every 15 seconds for updates
- See the included diagrams for schema and flow

## Best Practices & Improvements

### Code Quality
- Use environment variables for configuration (MongoDB URI, ports, etc.)
- Add proper error handling and logging
- Implement input validation and sanitization
- Add unit and integration tests

### Security
- Add webhook secret validation
- Implement rate limiting
- Use HTTPS for production
- Sanitize user inputs

### Scalability
- Use a production-ready web server (Gunicorn, uWSGI)
- Implement connection pooling for MongoDB
- Consider using a message queue for webhook processing

---

**Note:** For production, secure the webhook endpoint and sanitize inputs as needed.