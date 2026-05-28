Encore simplifies backend infrastructure by provisioning databases automatically through code using its `SQLDatabase` primitive.

You need to create a simple "Hello World" application with a GET endpoint and a POST endpoint that stores and retrieves simple message data in a PostgreSQL database managed by Encore. 

**Constraints:**
- Create the API endpoints using Encore's type-safe `api` function.
- Define the database using `new SQLDatabase()` and ensure a `.up.sql` migration file is correctly referenced in the constructor's options.
- The POST endpoint must accept a strict TypeScript interface for its JSON body (containing a `message` string) and return the newly inserted record's database ID.