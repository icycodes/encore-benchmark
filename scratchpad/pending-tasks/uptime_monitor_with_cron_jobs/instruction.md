Combining scheduled tasks, pub/sub communication, and database storage allows for robust distributed workflows like uptime monitoring.

You need to build an event-driven uptime monitor that uses an Encore `CronJob` to trigger a periodic website health check, publishes the success/failure result to a Topic, and stores the historical results in an Encore-managed database.

**Constraints:**
- The `CronJob` must be imported from `encore.dev/cron` and scheduled to run exactly every 5 minutes.
- The event subscriber must write the health check result (URL, timestamp, and status) into the database.
- Do NOT use external third-party scheduling libraries (e.g., node-cron); you must strictly use Encore's native Cron Job primitive.