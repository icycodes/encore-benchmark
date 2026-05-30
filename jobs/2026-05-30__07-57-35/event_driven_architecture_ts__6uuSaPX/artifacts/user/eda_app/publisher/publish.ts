import { api } from "encore.dev/api";
import { messageTopic } from "./topic";

interface PublishRequest {
  text: string;
}

interface PublishResponse {
  status: string;
}

export const publish = api<PublishRequest, PublishResponse>(
  { method: "POST", path: "/publish", expose: true },
  async (req) => {
    await messageTopic.publish({ text: req.text });
    return { status: "published" };
  }
);
