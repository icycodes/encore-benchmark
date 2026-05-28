While Encore provides a native `SQLDatabase` primitive for executing raw SQL queries, developers often prefer integrating modern ORMs like Drizzle to handle complex database schemas and type-safe query building.

You need to integrate Drizzle ORM into an Encore project, ensuring that the ORM is correctly initialized to query the infrastructure provisioned by Encore.

**Constraints:**
- Use the connection string provided by Encore's `SQLDatabase.connectionString` property to securely configure the Drizzle ORM client.
- Implement a GET endpoint that fetches a list of records using a Drizzle query rather than Encore's raw `db.query` tagged template literal.
- Do NOT bypass Encore's automated database provisioning; Drizzle must connect strictly to the PostgreSQL instance automatically managed by the Encore runtime.