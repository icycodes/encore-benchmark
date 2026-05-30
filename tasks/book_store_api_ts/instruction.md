# Book Store REST API with Encore.ts

## Background
Create a REST API for managing a list of books using Encore.ts and a PostgreSQL database, then deploy it to Encore Cloud.

## Requirements
- Implement a RESTful API with the following endpoints in a `books` service:
  - `POST /books`: Add a new book (fields: `title`, `author`).
  - `GET /books`: List all books.
  - `DELETE /books/:id`: Remove a book by ID.
- Store data in an Encore PostgreSQL database named `bookstore`.
- Deploy the app to Encore Cloud.

## Implementation Hints
- Use `encore.dev/api` to define API endpoints and `encore.dev/storage/sqldb` to define the database.
- Write database migrations in a `migrations` folder (e.g. `1_create_books_table.up.sql`) to create a `books` table with `id` (serial/auto-increment), `title` (text), and `author` (text).
- Since Docker is not available in the execution environment, you cannot use `encore run` to test locally. You must deploy to Encore Cloud to verify your code.
- **Encore Cloud Deployment Guide**:
  1. Initialize a Git repository with `git init`.
  2. Authenticate Encore by writing the `ENCORE_AUTH_TOKEN_JSON` environment variable value to `~/.config/encore/.auth_token`.
  3. Run `encore auth whoami` to confirm authentication.
  4. Initialize the Encore app using `encore app init bookstore --lang ts` (remove `encore.app` first if it exists).
  5. Add the Git remote: `git remote add encore encore://<app-id>`.
  6. Commit your code and push: `git push encore`.
  7. The deployed app will be accessible at `https://staging-<app-id>.encr.app/`.

## Acceptance Criteria
- Project path: `/home/user/bookstore`
- Ensure the app is successfully deployed to Encore Cloud.
- The `encore.app` file must exist in the project directory and contain the valid app ID.
- API Endpoints (deployed at `https://staging-<app-id>.encr.app/`):
  - `POST /books`: Accepts a JSON body with `title` and `author`, returns 200 OK with the created book object (including `id`).
  - `GET /books`: Returns 200 OK and a JSON array of book objects.
  - `DELETE /books/:id`: Deletes the book and returns 200 OK.
