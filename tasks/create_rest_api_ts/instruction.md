# Encore REST API with PostgreSQL

## Background
Create a simple REST API for managing a list of books using Encore.ts and its built-in PostgreSQL database support. Encore automatically provisions the database when declared in code.

## Requirements
- Create an Encore.ts application named `helloworld`.
- Implement a RESTful API with the following endpoints:
  - GET `/books`: List all books.
  - POST `/books`: Add a new book (fields: `title`, `author`).
  - DELETE `/books/:id`: Remove a book by ID.
- Store data in a PostgreSQL database managed by Encore.
- Deploy the application to Encore Cloud.
- Write the app ID to `app_id.txt` after deployment.

## Implementation Hints
- The task execution environment does NOT have Docker available, so you cannot run `encore run` locally. You must deploy the app to Encore Cloud for testing.
- Use `SQLDatabase` from `encore.dev/storage/sqldb` to define the database.
- Write SQL migrations in the `migrations` directory to create the `books` table.
- To deploy to Encore Cloud:
  1. Initialize a Git repository with `git init`.
  2. Authenticate Encore by writing the provided `ENCORE_AUTH_TOKEN_JSON` value to `~/.config/encore/.auth_token` (e.g., `mkdir -p ~/.config/encore && printf '%s' "$ENCORE_AUTH_TOKEN_JSON" > ~/.config/encore/.auth_token`), then verify with `encore auth whoami`.
  3. Initialize the Encore app with `encore app init helloworld --lang ts`.
  4. Get the app ID from the output or `encore.app` file.
  5. Add the Encore Git remote: `git remote add encore encore://<app-id>`.
  6. Commit your code and push: `git push encore`.
  7. The deployment may take about 2 minutes. The deployed endpoint will be `https://staging-<app-id>.encr.app/`.
- Write the app ID to `/home/user/helloworld/app_id.txt` in the format `App ID: <app_id>`.

## Acceptance Criteria
- Project path: /home/user/helloworld
- Ensure the app is deployed to Encore Cloud and the log artifact exists.
- Log file: /home/user/helloworld/app_id.txt
- The log file must contain the app ID in the format: `App ID: <app_id>`.
- API Endpoints (accessed via `https://staging-<app_id>.encr.app/`):
  - GET `/books`: Returns status 200 and a JSON array of book objects.

    ```json
    // Response
    [
      {
        "id": number,
        "title": string,
        "author": string
      }
    ]
    ```

  - POST `/books`: Accepts book object JSON and returns 200 OK with the new book object.

    ```json
    // Request
    {
      "title": string,
      "author": string
    }
    ```
    ```json
    // Response
    {
      "id": number,
      "title": string,
      "author": string
    }
    ```

  - DELETE `/books/:id`: Deletes the book with the given ID and returns 200 OK.

