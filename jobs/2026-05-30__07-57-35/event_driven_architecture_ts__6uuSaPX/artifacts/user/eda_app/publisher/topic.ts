import { Topic } from "encore.dev/pubsub";

export interface MessageEvent {
  text: string;
}

export const messageTopic = new Topic<MessageEvent>("messages", {
  deliveryGuarantee: "at-least-once",
});
