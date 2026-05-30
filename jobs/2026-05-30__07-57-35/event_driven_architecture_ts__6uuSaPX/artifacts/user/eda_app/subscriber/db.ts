import { SQLDatabase } from "encore.dev/storage/sqldb";

export const messageDB = new SQLDatabase("messages", {
  migrations: "./migrations",
});
