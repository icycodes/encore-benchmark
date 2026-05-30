import { Topic } from "encore.dev/pubsub";

export interface Message {
  text: string;
}

export const messages = new Topic<Message>("messages", {
  deliveryGuarantee: "at-least-once",
});
