import { SQLDatabase } from "encore.dev/storage/sqldb";

export const messageDB = new SQLDatabase("message-db", {
  migrations: "./migrations",
});