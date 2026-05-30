import { Subscription } from "encore.dev/pubsub";
import { messages, Message } from "../publisher/pubsub";
import { db } from "./db";

const _ = new Subscription(messages, "message-subscriber", {
  handler: async (event: Message) => {
    await db.exec`INSERT INTO messages (text) VALUES (${event.text})`;
  },
});
