# Stale Records Cleanup Cron Job in Encore.go

## Background
You are building a backend for a data processing system using Encore.go. Over time, the database accumulates records that have either been successfully processed or have failed and are no longer needed. You need to implement a database, a REST API, and a cron job to periodically clean up these stale records.

## Requirements
- Initialize an Encore Go application in the `myproject` directory.
- Create a PostgreSQL database named `records_db` using `encore.dev/storage/sqldb` and define its schema.
- Create a table `records` with columns: `id` (serial primary key), `data` (text), `status` (text), and `updated_at` (timestamp).
- Create a public API endpoint `POST /records` that accepts `data`, `status`, and `updated_at` (to allow testing different timestamps). It should insert a new record and return the generated `id`.
- Create a public API endpoint `POST /records/cleanup` that deletes records matching the following criteria:
  - `status` is 'processed' AND `updated_at` is older than 30 days.
  - `status` is 'failed' AND `updated_at` is older than 90 days.
  It should return the number of deleted records.
- Create an Encore Cron Job named `cleanup-stale-records` that executes the cleanup endpoint every 1 hour.

## Implementation Hints
- Use `encore app create` to initialize the project.
- Create a `migrations` folder with a `.up.sql` file to define the database schema.
- Use `encore.dev/storage/sqldb` to connect to the database and perform SQL queries.
- Define the API endpoints using the `//encore:api public` annotation.
- Use `encore.dev/cron` to define the cron job. Ensure the interval divides 24 hours evenly (e.g., `1 * cron.Hour`).
- You can use standard `database/sql` methods like `QueryRow` and `Exec` with the Encore SQL database instance.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: encore run
- Port: 4000
- API Endpoints:
  - `POST /records`: Accepts JSON body `{"data": string, "status": string, "updated_at": string}` (where `updated_at` is an RFC3339 timestamp). Returns status 200 with JSON `{"id": number}`.
  - `POST /records/cleanup`: Deletes stale records based on the rules. Returns status 200 with JSON `{"deleted_count": number}`.
- Cron Job: The codebase must contain a cron job definition named `cleanup-stale-records` that runs every 1 hour and calls the cleanup endpoint.
