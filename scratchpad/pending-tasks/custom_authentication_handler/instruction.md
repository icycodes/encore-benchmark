While Encore provides built-in mechanisms for API routing, integrating external JWT providers (like Clerk or Auth0) requires injecting custom logic to validate requests before they reach the endpoint.

You need to implement a custom authentication handler that validates JWTs from an external provider and use it to protect a private API endpoint that returns sensitive user data.

**Constraints:**
- Use the `authHandler` primitive from `encore.dev/auth` to define the authentication validation logic and context.
- Create an API endpoint with `{ auth: true }` configured in its route definition to ensure it is protected.
- Extract and return the authenticated user's ID from the injected authentication context in the protected endpoint.