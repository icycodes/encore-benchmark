import { Topic } from "encore.dev/pubsub";

export interface MessageEvent {
  text: string;
}

export const messageTopic = new Topic<MessageEvent>("message-topic", {
  deliveryGuarantee: "at-least-once",
});