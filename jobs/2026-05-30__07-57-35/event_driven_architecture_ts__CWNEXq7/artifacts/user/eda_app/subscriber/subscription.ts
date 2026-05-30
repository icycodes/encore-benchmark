import { Subscription } from "encore.dev/pubsub";
import { messageTopic, MessageEvent } from "../publisher/topic";
import { messageDB } from "./db";

export const messageSubscription = new Subscription(messageTopic, "message-subscription", {
  handler: async (event: MessageEvent) => {
    await messageDB.exec`
      INSERT INTO messages (text) VALUES (${event.text})
    `;
  },
});