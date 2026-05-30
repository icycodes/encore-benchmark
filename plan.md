# Encore Research Plan

## 1. Library Overview

* **Description**: Encore is an open-source backend framework for building type-safe distributed systems. It uses a declarative "Infrastructure from Code" approach, allowing developers to define infrastructure (databases, pub/sub, cron jobs) directly in their application code using TypeScript or Go. Encore automatically provisions the infrastructure, wires up services, and generates API documentation and distributed traces.
* **Ecosystem Role**: Encore replaces the traditional combination of a web framework (like Express or Gin), an infrastructure-as-code tool (like Terraform), and observability pipelines. It acts as an end-to-end backend platform that integrates tightly with cloud providers (AWS, GCP) and its own Encore Cloud platform.
* **Project Setup**:
  1. **Install Encore CLI**: Use the `curl`-based install method:
     ```bash
     curl -L https://encore.dev/install.sh | bash
     ```
  2. **Create a new app**:
     ```bash
     encore app create
     ```
     (Select TypeScript or Go, choose a template like "Hello World", and provide an app name).
  3. **Run locally**:
     ```bash
     cd your-app-name
     encore run
     ```
     This starts the local development environment, automatically spinning up required infrastructure (like PostgreSQL via Docker) and providing a local dashboard at `http://localhost:9400`.

## 2. Core Primitives & APIs

### Encore.ts SDK

* **Services**: Defined by creating an `encore.service.ts` file in a directory and exporting a `Service` instance.
  ```typescript
  import { Service } from "encore.dev/service";
  export default new Service("hello");
  ```
  [Documentation: Services](https://encore.dev/docs/ts/primitives/services)
* **APIs**: Defined by wrapping an async function with the `api` function from `encore.dev/api`.
  ```typescript
  import { api } from "encore.dev/api";

  export const world = api(
    { method: "GET", path: "/hello/:name", expose: true },
    async ({ name }: { name: string }): Promise<{ message: string }> => {
      return { message: `Hello ${name}!` };
    }
  );
  ```
  [Documentation: Defining APIs](https://encore.dev/docs/ts/primitives/defining-apis)

### Encore.go SDK

* **Services**: Defined simply by creating a Go package. Encore automatically identifies packages with API endpoints as services.
* **APIs**: Defined using the `//encore:api` annotation above a standard Go function.
  ```go
  package hello

  import "context"

  type Response struct {
      Message string
  }

  //encore:api public path=/hello/:name
  func World(ctx context.Context, name string) (*Response, error) {
      return &Response{Message: "Hello, " + name + "!"}, nil
  }
  ```
  [Documentation: Defining APIs](https://encore.dev/docs/go/primitives/defining-apis)

### Databases (Cross-SDK)
Encore automatically provisions databases when declared in code.
* **TypeScript**:
  ```typescript
  import { SQLDatabase } from "encore.dev/storage/sqldb";
  export const db = new SQLDatabase("users", { migrations: "./migrations" });
  ```
* **Go**:
  ```go
  import "encore.dev/storage/sqldb"
  var db = sqldb.NewDatabase("users", sqldb.DatabaseConfig{
      Migrations: "./migrations",
  })
  ```

## 3. Real-World Use Cases & Templates

* **Event-Driven Systems**: Using Encore's built-in Pub/Sub primitives to build asynchronous workflows (e.g., Uptime Monitors).
  * *Template*: [Event-Driven System Starter](https://encore.dev/templates/eda)
* **REST APIs with PostgreSQL**: Building robust APIs with automated database provisioning and migrations.
  * *Template*: [REST API Starter](https://encore.dev/templates/rest-api)
* **SaaS Boilerplates**: Integrating third-party authentication (Clerk, Auth0), billing (Stripe), and frontend frameworks (Next.js) with an Encore backend.
  * *Template*: [SaaS Starter](https://encore.dev/templates/saas-starter)
* **Microservices Architecture**: Splitting monolithic applications into independently scalable services with automatic service-to-service communication.

## 4. Developer Friction Points

* **Custom Infrastructure Integration**: Since Encore abstracts infrastructure provisioning, developers often face friction when trying to integrate custom infrastructure or services not natively supported by Encore's declarative model.
* **Authentication Middleware**: Implementing complex, custom authentication flows can be tricky, as developers must adapt to Encore's specific `authHandler` patterns rather than using standard Express/Gin middleware.
* **Migration from Existing Frameworks**: Refactoring an existing Express.js or Go/Gin application into Encore requires a significant paradigm shift to adopt Encore's service boundaries and API annotations.
* **Testing with Infrastructure**: Setting up integration tests that require the automated infrastructure (like Pub/Sub or Databases) can be challenging for developers unfamiliar with Encore's internal testing utilities.

## 5. Evaluation Ideas

* Create a simple REST API with a PostgreSQL database and CRUD operations.
* Implement an event-driven architecture with a publisher service and a subscriber service.
* Set up a cron job that periodically cleans up stale database records.
* Build a multi-service application demonstrating service-to-service API calls.
* Migrate a simple Express.js endpoint to an Encore.ts endpoint.

## 6. Sources

1. [Encore Documentation (llms.txt)](https://encore.dev/llms.txt) - Official full site map and resources overview.
2. [Encore.ts Quick Start](https://encore.dev/docs/ts/quick-start) - Official guide for setting up and deploying TypeScript applications.
3. [Encore.go Quick Start](https://encore.dev/docs/go/quick-start) - Official guide for setting up and deploying Go applications.
4. [Deploying Applications with Encore Cloud](https://encore.dev/docs/platform/deploy/deploying) - Documentation on git-push deployments to Encore Cloud.

## Integration

### Install Encore CLI

1. Run `curl -L https://encore.dev/install.sh | bash`.
2. Create a symlink for each binary in `~/.encore/bin` under `/usr/local/bin/`:
   `ln -s ~/.encore/bin/encore /usr/local/bin/encore`
   `ln -s ~/.encore/bin/git-remote-encore /usr/local/bin/git-remote-encore`
   `ln -s ~/.encore/bin/tsbundler-encore /usr/local/bin/tsbundler-encore`
   `ln -s ~/.encore/bin/tsparser-encore /usr/local/bin/tsparser-encore`
3. Install `ssh`, which is required by `git-remote-encore`:
   `apt-get update && apt-get install ssh -y`

### Task Execution Environment

Docker is NOT available in the task execution environment, even though some Encore commands require it.
Commands such as `encore run` (which use Docker to start local databases) are NEVER available in this environment.
The task executor must deploy the app to Encore Cloud for testing.


To deploy an Encore app to Encore Cloud:

1. Initialize a Git repository:
  1. Run `git init`.
2. Authenticate Encore by writing the provided `ENCORE_AUTH_TOKEN_JSON` value to `~/.config/encore/.auth_token`, then verify:
  1. Run `mkdir -p ~/.config/encore && printf '%s' "$ENCORE_AUTH_TOKEN_JSON" > ~/.config/encore/.auth_token`.
  2. Run `encore auth whoami` to confirm authentication.
3. Initialize an Encore app (example: a TypeScript app named `helloworld`):
  1. Remove `encore.app` first if it already exists.
  2. Run `encore app init helloworld --lang ts`.
  3. Get the app ID from the command output. The app ID can also be read from `encore.app`, in the following format:
    ```encore.app
    {
      "id": "helloworld-f3z2",
      "lang": "typescript"
    }
    ```
  **NOTE:** If you need to extract the app ID with pytest code, use a regex instead of a JSON parser, because `encore.app` is not strict JSON.
  Example regex: `"id"\s*:\s*"([^\"]+)"` (capture group 1 is the app ID, e.g., `helloworld-f3z2`).
4. Add the Encore Git remote:
  1. Run `git remote add encore encore://<app-id>`.
5. Push to the Encore remote and wait for deployment (this may take about 2 minutes):
  1. Run `git push encore`.
6. Access the deployed endpoint at: `https://staging-<app-id>.encr.app/`

### Task Generation Rules

**IMPORTANT:** When generating the `task.json`:
1. Clearly state that the task executor is expected to deploy the app to Encore Cloud.
2. The verifier should test only against the deployed endpoint.
3. Ensure you include the usage of `ENCORE_AUTH_TOKEN_JSON` in the `Implementation Hints`.
4. Add a simple guide to deploy an Encore app to Encore Cloud in the `Implementation Hints`.

After executing `07_postgen_script.sh` and the `task.toml` is created, modify the `task.toml` to update the agent timeout from `600` to `1200`:
```
[agent]
timeout_sec = 1200.0
```
