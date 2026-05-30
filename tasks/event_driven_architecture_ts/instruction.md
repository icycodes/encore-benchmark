# Event-Driven Architecture with Encore.ts

## Background
Encore is a backend framework that uses a declarative "Infrastructure from Code" approach. You will build an event-driven application using Encore's built-in Pub/Sub primitives and PostgreSQL database, and deploy it to Encore Cloud.

## Requirements
- Create an Encore TypeScript application named `eda_app`.
- Implement a `publisher` service that exposes a REST API to publish messages to a Pub/Sub topic.
- Implement a `subscriber` service that subscribes to the topic and stores received messages in a PostgreSQL database.
- The `subscriber` service must expose a REST API to retrieve the stored messages.
- Deploy the application to Encore Cloud.

## Implementation Hints
- Create an Encore app using `encore app init eda_app --lang ts`.
- In the `publisher` service, define a Topic and an API endpoint `POST /publish` that accepts a JSON body `{"text": string}` and publishes it to the Topic.
- In the `subscriber` service, define an `SQLDatabase` and a Subscription to the publisher's Topic. When an event is received, insert the `text` into the database.
- In the `subscriber` service, define an API endpoint `GET /messages` that returns all stored messages from the database as a JSON array.
- **Authentication**: Write the provided `ENCORE_AUTH_TOKEN_JSON` environment variable to `~/.config/encore/.auth_token` to authenticate the Encore CLI.
- **Deployment**: Docker is NOT available in this environment, so you cannot use `encore run`. You MUST deploy the app to Encore Cloud to test it.
  - To deploy:
    1. Initialize a Git repository (`git init`).
    2. Authenticate Encore.
    3. Remove `encore.app` if it exists, then run `encore app init eda_app --lang ts`.
    4. Extract the app ID from the `encore.app` file.
    5. Add the remote: `git remote add encore encore://<app-id>`.
    6. Commit your code and push: `git push encore`.
    7. The deployed API will be available at `https://staging-<app-id>.encr.app`.

## Acceptance Criteria
- Project path: `/home/user/eda_app`
- Ensure the app is deployed to Encore Cloud.
- The deployed app must have a `POST /publish` endpoint that accepts `{"text": "<message>"}`.
- The deployed app must have a `GET /messages` endpoint that returns a JSON object containing a list of messages, e.g., `{"messages": [{"text": "<message>"}]}`.
- The app must use Encore's Pub/Sub (Topic and Subscription) to pass the message from the publisher to the subscriber.
- The app must use Encore's `SQLDatabase` to store the messages.

