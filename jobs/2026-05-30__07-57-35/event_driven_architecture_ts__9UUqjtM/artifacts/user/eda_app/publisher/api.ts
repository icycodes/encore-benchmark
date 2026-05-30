import { api } from "encore.dev/api";
import { messages } from "./pubsub";

export interface PublishRequest {
  text: string;
}

export interface PublishResponse {
  success: boolean;
}

export const publishMessage = api(
  { expose: true, method: "POST", path: "/publish" },
  async (req: PublishRequest): Promise<PublishResponse> => {
    await messages.publish({ text: req.text });
    return { success: true };
  }
);
