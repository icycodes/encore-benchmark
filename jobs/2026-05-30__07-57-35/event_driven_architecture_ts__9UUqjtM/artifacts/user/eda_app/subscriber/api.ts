import { api } from "encore.dev/api";
import { db } from "./db";

interface MessageResponse {
  messages: { text: string }[];
}

export const getMessages = api(
  { expose: true, method: "GET", path: "/messages" },
  async (): Promise<MessageResponse> => {
    const rows = await db.query`SELECT text FROM messages`;
    const messages: { text: string }[] = [];
    for await (const row of rows) {
      messages.push({ text: row.text });
    }
    return { messages };
  }
);
