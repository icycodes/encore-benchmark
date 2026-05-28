Encore handles complex service-to-service communication by offering cloud-agnostic Pub/Sub primitives, eliminating the need to manually configure external message brokers.

You need to set up a distributed Pub/Sub system consisting of two services: one service that publishes "Order Created" events, and another service that consumes these events to mock sending a confirmation email.

**Constraints:**
- Define a `Topic` with an "at-least-once" delivery strategy using `encore.dev/pubsub`.
- Define a `Subscription` in a separate logical service (directory) that triggers a handler function whenever the topic receives an event.
- Ensure the event payload is strictly typed using a TypeScript interface shared or imported between the publisher and subscriber.