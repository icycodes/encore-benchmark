# Multi-Service E-commerce Backend with Encore.ts

## Background
Build a multi-service e-commerce backend using Encore.ts. The application must include an `inventory` service to manage product stock and an `orders` service to handle customer orders. This task demonstrates Encore's automatic database provisioning and seamless service-to-service communication.

## Requirements
- Create an `inventory` service with a PostgreSQL database.
  - Implement `POST /inventory`: Add a new product with an initial stock.
  - Implement `POST /inventory/:id/reserve`: Reserve stock for a product. It must decrease the stock by the requested quantity. If the stock is insufficient, it must fail with an HTTP 400 error.
- Create an `orders` service with a PostgreSQL database.
  - Implement `POST /orders`: Create a new order. It must call the `inventory` service's reserve endpoint to secure the stock. If the reservation succeeds, the order is saved to the database. If it fails, the order creation must be aborted and an HTTP 400 error returned.
- Both services must use Encore's `SQLDatabase` primitive with proper migration files to define their database schemas.

## Implementation Hints
- Initialize an Encore application and create separate directories for the `inventory` and `orders` services, each with an `encore.service.ts` file.
- Define databases using `new SQLDatabase("name", { migrations: "./migrations" })` from `encore.dev/storage/sqldb`.
- Write SQL migration files (e.g., `1_create_tables.up.sql`) in the corresponding `migrations` folders to create the necessary tables.
- For service-to-service communication, simply import the API endpoint function from the `inventory` service into the `orders` service and call it as a normal asynchronous function. Encore automatically handles the internal network call.
- Use `HttpStatus` from `encore.dev/api` or throw an `APIError` to return custom HTTP status codes (e.g., 400 Bad Request) when stock is insufficient.
- Note: Encore's API server runs on port 4000 by default.

## Acceptance Criteria
- Project path: /home/user/myproject
- Start command: encore run
- Port: 4000
- API Endpoints:
  - POST `/inventory`: Accepts JSON body `{"name": string, "stock": number}`, returns 200 OK with `{"id": number, "name": string, "stock": number}`.
  - POST `/inventory/:id/reserve`: Accepts JSON body `{"quantity": number}`. If sufficient stock exists, it returns 200 OK. If insufficient, it returns 400 Bad Request.
  - POST `/orders`: Accepts JSON body `{"product_id": number, "quantity": number}`. It calls the inventory reserve endpoint. If successful, returns 200 OK with `{"id": number, "product_id": number, "quantity": number, "status": "created"}`. If reservation fails, returns 400 Bad Request and does not create the order.

