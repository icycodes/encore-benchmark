import { api } from "encore.dev/api";
import { messageDB } from "./db";

interface MessageRow {
  text: string;
}

interface ListMessagesResponse {
  messages: { text: string }[];
}

export const listMessages = api<void, ListMessagesResponse>(
  { method: "GET", path: "/messages", expose: true },
  async () => {
    const rows = await messageDB.queryAll<MessageRow>`SELECT text FROM messages ORDER BY id`;
    return { messages: rows.map((row) => ({ text: row.text })) };
  }
);
