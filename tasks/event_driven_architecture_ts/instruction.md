# Event-Driven Order System with Encore.ts

## Background
Create an event-driven order processing system using Encore.ts. The system will demonstrate Encore's built-in Pub/Sub and PostgreSQL primitives by decoupling order creation from email notification.

## Requirements
- Create an Encore application with two services: `orders` and `emails`.
- **Service `orders`**:
  - Provision a PostgreSQL database named `orders_db`.
  - Create a migration to define an `orders` table with columns `id` (TEXT PRIMARY KEY), `item` (TEXT), and `user_email` (TEXT).
  - Define a public API endpoint `POST /orders` that accepts a JSON body with `id`, `item`, and `user_email`. It should insert the order into the database.
  - Define a Pub/Sub Topic named `order-events`.
  - Upon successful database insertion, the `POST /orders` endpoint must publish an event to `order-events` containing the `id`, `item`, and `user_email`.
- **Service `emails`**:
  - Provision a PostgreSQL database named `emails_db`.
  - Create a migration to define a `sent_emails` table with columns `id` (SERIAL PRIMARY KEY), `user_email` (TEXT), and `message` (TEXT).
  - Define a Pub/Sub Subscription to the `order-events` topic.
  - When an event is received, insert a record into the `sent_emails` table where the `message` is formatted as `"Order created for item: " + event.item`.
  - Define a public API endpoint `GET /emails/:user_email` that returns all sent emails for the specified user from the database.

## Implementation Hints
- Use `encore app create` to initialize a new TypeScript project if needed, or set up the structure manually.
- Use `new SQLDatabase` from `encore.dev/storage/sqldb` to declare databases and provide SQL migrations in a `migrations` folder for each service.
- Use `Topic` and `Subscription` from `encore.dev/pubsub` to implement the event-driven communication.
- Remember to create an `encore.service.ts` file in both the `orders` and `emails` directories to define the service boundaries.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: encore run
- Port: 4000
- API Endpoints:
  - `POST /orders`: Accepts JSON with `id`, `item`, and `user_email`, and returns HTTP 200 OK.
  - `GET /emails/:user_email`: Returns HTTP 200 OK and a JSON object containing an array of email records.

    ```json
    // Response
    {
      "emails": [
        {
          "id": number,
          "user_email": string,
          "message": string
        }
      ]
    }
    ```

