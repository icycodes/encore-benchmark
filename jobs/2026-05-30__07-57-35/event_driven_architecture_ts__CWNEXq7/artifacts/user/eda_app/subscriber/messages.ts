import { api } from "encore.dev/api";
import { messageDB } from "./db";

interface Message {
  text: string;
}

interface MessagesResponse {
  messages: Message[];
}

export const getMessages = api(
  { expose: true, method: "GET", path: "/messages" },
  async (): Promise<MessagesResponse> => {
    const rows = await messageDB.query`SELECT text FROM messages ORDER BY id ASC`;
    const messages: Message[] = [];
    for await (const row of rows) {
      messages.push({ text: row.text });
    }
    return { messages };
  }
);