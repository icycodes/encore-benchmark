import { APIError, API } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("userdb", {
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

// POST /users - Create a new user
export const create = API({
  method: "POST",
  path: "/users",
}, async (req: CreateUserRequest): Promise<User> => {
  const row = await db.queryRow`
    INSERT INTO users (name, email)
    VALUES (${req.name}, ${req.email})
    RETURNING id, name, email
  ` as User | null;

  if (!row) {
    throw APIError.internal("failed to create user");
  }

  return row;
});

// GET /users/:id - Get a user by ID
export const get = API({
  method: "GET",
  path: "/users/:id",
}, async (req: { id: number }): Promise<User> => {
  const row = await db.queryRow`
    SELECT id, name, email FROM users WHERE id = ${req.id}
  ` as User | null;

  if (!row) {
    throw APIError.notFound("user not found");
  }

  return row;
});

// GET /users - List all users
export const list = API({
  method: "GET",
  path: "/users",
}, async (): Promise<{ users: User[] }> => {
  const rows: User[] = [];

  const cursor = await db.query`
    SELECT id, name, email FROM users ORDER BY id
  `;

  for await (const row of cursor) {
    rows.push(row as User);
  }

  return { users: rows };
});