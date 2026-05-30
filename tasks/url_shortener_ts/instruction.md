# URL Shortener REST API with Encore.ts

## Background
Create a URL Shortener REST API using Encore.ts and its built-in PostgreSQL database provisioning. The API will allow users to submit a long URL and receive a shortened ID, and then retrieve the original URL using that ID.

## Requirements
- Implement a RESTful API with the following endpoints:
  - POST `/url`: Shorten a URL. Accepts a JSON body with a `url` string. Generates a unique short ID (e.g., a random string) and stores it in the database.
  - GET `/url/:id`: Retrieve the original URL by its short ID.
- Use Encore's `SQLDatabase` to store the URL mappings.
- Provide a database migration file to create the necessary table.
- The application must be deployed to Encore Cloud.

## Implementation Hints
- Use `api` from `encore.dev/api` to define the endpoints.
- Use `SQLDatabase` from `encore.dev/storage/sqldb` to define the database.
- Create a `migrations` directory with a SQL file (e.g., `1_create_tables.up.sql`) to define the table schema.
- To deploy an Encore app to Encore Cloud:
  1. Initialize a Git repository (`git init`).
  2. Authenticate Encore by writing the provided `ENCORE_AUTH_TOKEN_JSON` value to `~/.config/encore/.auth_token`: `mkdir -p ~/.config/encore && printf '%s' "$ENCORE_AUTH_TOKEN_JSON" > ~/.config/encore/.auth_token`.
  3. Verify authentication with `encore auth whoami`.
  4. Initialize an Encore app (e.g., `encore app init myapp --lang ts`).
  5. Add the Encore Git remote: `git remote add encore encore://<app-id>`.
  6. Commit your code and push to the Encore remote: `git push encore`.
  7. The deployed endpoint will be available at `https://staging-<app-id>.encr.app/`.

## Acceptance Criteria
- Project path: /home/user/url-shortener
- Start command: The app must be deployed to Encore Cloud via `git push encore`.
- Port: N/A (Deployed to Encore Cloud)
- API Endpoints:
  - POST `/url`: Accepts a URL and returns the created short ID.

    ```json
    // Request
    {
      "url": string
    }
    ```
    ```json
    // Response
    {
      "id": string,
      "url": string
    }
    ```

  - GET `/url/:id`: Returns the URL object for the given short ID.

    ```json
    // Response
    {
      "id": string,
      "url": string
    }
    ```

