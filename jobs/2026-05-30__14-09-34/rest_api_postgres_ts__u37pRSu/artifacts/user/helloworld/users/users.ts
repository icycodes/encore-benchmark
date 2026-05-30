import { api } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";
import type { IncomingMessage, ServerResponse } from "node:http";

const db = new SQLDatabase("users", {
    migrations: "./migrations",
});

export interface User {
    id: number;
    name: string;
    email: string;
}

export interface CreateUserParams {
    name: string;
    email: string;
}

export const createUser = api(
    { expose: true, method: "POST", path: "/users" },
    async (params: CreateUserParams): Promise<User> => {
        const row = await db.queryRow`
            INSERT INTO users (name, email)
            VALUES (${params.name}, ${params.email})
            RETURNING id, name, email
        `;
        if (!row) throw new Error("Failed to create user");
        return {
            id: row.id,
            name: row.name,
            email: row.email
        };
    }
);

export const getUser = api(
    { expose: true, method: "GET", path: "/users/:id" },
    async ({ id }: { id: number }): Promise<User> => {
        const row = await db.queryRow`
            SELECT id, name, email FROM users WHERE id = ${id}
        `;
        if (!row) throw new Error("User not found");
        return {
            id: row.id,
            name: row.name,
            email: row.email
        };
    }
);

export const listUsers = api.raw(
    { expose: true, method: "GET", path: "/users" },
    async (req: IncomingMessage, res: ServerResponse) => {
        const rows: User[] = [];
        for await (const row of db.query`SELECT id, name, email FROM users`) {
            rows.push({
                id: row.id,
                name: row.name,
                email: row.email
            });
        }
        res.setHeader("Content-Type", "application/json");
        res.end(JSON.stringify(rows));
    }
);
