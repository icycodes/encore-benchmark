import { api } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

export const db = new SQLDatabase("users", {
  migrations: "./migrations",
});

interface User {
  id: number;
  name: string;
  email: string;
}

interface CreateUserRequest {
  name: string;
  email: string;
}

export const createUser = api(
  { method: "POST", path: "/users" },
  async (req: CreateUserRequest): Promise<User> => {
    const row = await db.queryRow<User>`
      INSERT INTO users (name, email)
      VALUES (${req.name}, ${req.email})
      RETURNING id, name, email
    `;

    if (!row) {
      throw new Error("Failed to create user");
    }

    return row;
  }
);

export const getUser = api(
  { method: "GET", path: "/users/:id" },
  async (req: { id: number }): Promise<User> => {
    const row = await db.queryRow<User>`
      SELECT id, name, email
      FROM users
      WHERE id = ${req.id}
    `;

    if (!row) {
      throw new Error("User not found");
    }

    return row;
  }
);

export const listUsers = api(
  { method: "GET", path: "/users" },
  async (): Promise<User[]> => {
    const rows = await db.query<User>`
      SELECT id, name, email
      FROM users
      ORDER BY id
    `;

    return rows;
  }
);
