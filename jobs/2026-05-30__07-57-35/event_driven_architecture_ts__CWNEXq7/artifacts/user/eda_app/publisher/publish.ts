import { api } from "encore.dev/api";
import { messageTopic, MessageEvent } from "./topic";

interface PublishRequest {
  text: string;
}

export const publish = api(
  { expose: true, method: "POST", path: "/publish" },
  async (body: PublishRequest): Promise<{ message: string }> => {
    await messageTopic.publish({ text: body.text });
    return { message: "Published!" };
  }
);