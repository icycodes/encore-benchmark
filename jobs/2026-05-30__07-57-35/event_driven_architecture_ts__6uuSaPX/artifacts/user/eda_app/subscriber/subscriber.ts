import { Subscription } from "encore.dev/pubsub";
import { messageTopic } from "../publisher/topic";
import { messageDB } from "./db";

new Subscription(messageTopic, "store-messages", {
  handler: async (event) => {
    await messageDB.exec`INSERT INTO messages (text) VALUES (${event.text})`;
  },
});
