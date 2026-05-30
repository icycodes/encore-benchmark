# Encore REST API with PostgreSQL

## Background
Encore is a backend framework for building type-safe distributed systems with declarative infrastructure. In this task, you will build a REST API using Encore.ts with a PostgreSQL database and deploy it to Encore Cloud.

## Requirements
- Create a new Encore.ts app named `helloworld-${run-id}` where `run-id` is read from the `ZEALT_RUN_ID` environment variable.
- Implement a REST API with CRUD operations for "books" (fields: `id`, `title`, `author`).
  - POST `/book`: Add a new book.
  - GET `/book/:id`: Get a book by ID.
  - GET `/book`: List all books.
- Store data using Encore's built-in `SQLDatabase` (PostgreSQL).
- Deploy the app to Encore Cloud. The task executor must deploy the app to Encore Cloud for testing since Docker is NOT available in the execution environment.

## Implementation Hints
1. Authenticate with Encore using the provided `ENCORE_AUTH_TOKEN_JSON`. Run `mkdir -p ~/.config/encore && printf '%s' "$ENCORE_AUTH_TOKEN_JSON" > ~/.config/encore/.auth_token` and verify with `encore auth whoami`.
2. Read the current `run-id` from the `ZEALT_RUN_ID` environment variable.
3. Create the app using `encore app init helloworld-${run-id} --lang ts`.
4. Use `SQLDatabase` from `encore.dev/storage/sqldb` for the database and create a migration file in a `migrations` folder (e.g. `1_create_tables.up.sql`).
5. Implement the API endpoints using `api` from `encore.dev/api`.
6. Deploy to Encore Cloud:
   - Navigate into the app directory.
   - Extract the App ID from `encore.app`.
   - Add the remote: `git remote add encore encore://<app-id>`.
   - Commit and push: `git add -A . && git commit -m "init" && git push encore`.

## Acceptance Criteria
- Project path: /home/user/helloworld-${run-id}
- Ensure the real app deployment is executed and the app is deployed to Encore Cloud.
- The deployed endpoint must be accessible at `https://staging-<app-id>.encr.app/` (where `<app-id>` is the Encore App ID from `encore.app`).
- API Endpoints (all accessible via the deployed URL):
  - POST `/book`: Accepts JSON `{"title": string, "author": string}` and returns `{"id": number, "title": string, "author": string}`.
  - GET `/book/:id`: Returns the book object `{"id": number, "title": string, "author": string}`.
  - GET `/book`: Returns a JSON array of book objects.

