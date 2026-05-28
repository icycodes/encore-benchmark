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

When generating a task that requires deployment to Encore Cloud, the `ENCORE_AUTH_KEY` environment variable will be provided in the task execution environment to authenticate the Encore CLI for Encore Cloud deployment.
