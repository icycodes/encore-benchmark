# Event-Driven Architecture with Encore and Go

## Background
Create an event-driven architecture with a publisher service and a subscriber service using Encore and Go, and deploy it to Encore Cloud.

## Requirements
- Create a Go-based Encore app.
- Implement a publisher service with a REST API endpoint `POST /publish` that accepts a JSON body containing a `message` string.
- The publisher service must publish the message to an Encore Pub/Sub topic.
- Implement a subscriber service that subscribes to the topic and stores the received messages in an Encore SQL Database.
- Implement a REST API endpoint `GET /messages` that returns a list of all received messages from the database.
- Deploy the app to Encore Cloud.

## Implementation Hints
- Use Encore's built-in Pub/Sub primitives to define a topic and a subscription.
- Use Encore's SQL database primitive to provision a database and store the messages.
- Ensure you read the `run-id` from the `ZEALT_RUN_ID` environment variable and use it if you need to name any globally unique resources, though Encore Cloud app IDs are typically unique enough.
- **Deployment Guide**:
  1. Initialize a Git repository with `git init`.
  2. Authenticate using the provided `ENCORE_AUTH_TOKEN_JSON` environment variable:
     `mkdir -p ~/.config/encore && printf '%s' "$ENCORE_AUTH_TOKEN_JSON" > ~/.config/encore/.auth_token`
  3. Initialize the app with `encore app init <app-name> --lang go`. (Remove `encore.app` first if it already exists).
  4. Add the git remote: `git remote add encore encore://<app-id>`. (You can get the app ID from the `encore.app` file).
  5. Commit your code and deploy with `git push encore`.

## Acceptance Criteria
- Project path: /home/user/eda-app
- Ensure the real deployment action is executed and the app is accessible on Encore Cloud.
- The verifier will test the deployed endpoint at `https://staging-<app-id>.encr.app/`.
- API Endpoints (deployed):
  - POST `/publish`: Accepts JSON `{"message": string}` and returns 200 OK.
  - GET `/messages`: Returns 200 OK and a JSON object containing a list of messages, e.g., `{"messages": [{"message": string}]}`.

