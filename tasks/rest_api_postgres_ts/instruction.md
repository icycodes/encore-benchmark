# Create a REST API with PostgreSQL using Encore.ts

## Background
Encore is an open-source backend framework for building type-safe distributed systems with automatic infrastructure provisioning. In this task, you will create a REST API with a PostgreSQL database and deploy it to Encore Cloud.

## Requirements
- Initialize a new Encore application named `helloworld` using TypeScript.
- Implement a REST API for managing users with the following endpoints:
  - POST `/users`: Create a new user (fields: `name`, `email`).
  - GET `/users/:id`: Get a user by ID.
  - GET `/users`: List all users.
- Use Encore's built-in PostgreSQL database primitive (`SQLDatabase`) to store the users.
- Deploy the app to Encore Cloud.

## Implementation Hints
- The task executor is expected to deploy the app to Encore Cloud. Docker is NOT available in the task execution environment.
- To deploy an Encore app to Encore Cloud:
  1. Initialize a Git repository with `git init`.
  2. Authenticate Encore by writing the provided `ENCORE_AUTH_TOKEN_JSON` environment variable value to `~/.config/encore/.auth_token`.
     `mkdir -p ~/.config/encore && printf '%s' "$ENCORE_AUTH_TOKEN_JSON" > ~/.config/encore/.auth_token`
  3. Verify with `encore auth whoami`.
  4. Remove `encore.app` first if it already exists.
  5. Initialize the app using `encore app init helloworld --lang ts`.
  6. Add the Encore Git remote: `git remote add encore encore://<app-id>` (extract `<app-id>` from the output or `encore.app`).
  7. Push to the Encore remote: `git push encore`.
- Use `encore.dev/api` to define API endpoints.
- Use `encore.dev/storage/sqldb` to define the PostgreSQL database.
- Create a `migrations` folder with a SQL migration file to create the `users` table.

## Acceptance Criteria
- Project path: /home/user/helloworld
- Ensure the app is deployed to Encore Cloud.
- The deployed API should be accessible at `https://staging-<app-id>.encr.app`.
- API Endpoints:
  - POST `/users`: Accepts `name` and `email`, returns the created user object including an `id`.
  - GET `/users/:id`: Returns the user object for the given ID.
  - GET `/users`: Returns a JSON array of all user objects.

