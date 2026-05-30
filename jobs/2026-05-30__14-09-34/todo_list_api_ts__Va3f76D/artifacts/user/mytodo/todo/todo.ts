import { api } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

// Define a database named 'todos'
const db = new SQLDatabase("todos", {
  migrations: "./migrations",
});

interface Todo {
  id: number;
  title: string;
  done: boolean;
}

interface CreateTodoParams {
  title: string;
  done?: boolean;
}

interface UpdateTodoParams {
  title?: string;
  done?: boolean;
}

// POST /todos
export const create = api(
  { expose: true, method: "POST", path: "/todos" },
  async (params: CreateTodoParams): Promise<Todo> => {
    const done = params.done ?? false;
    const row = await db.queryRow`
      INSERT INTO todos (title, done)
      VALUES (${params.title}, ${done})
      RETURNING id, title, done
    `;
    if (!row) throw new Error("Could not create todo");
    return {
      id: row.id,
      title: row.title,
      done: row.done,
    };
  }
);

// GET /todos
export const list = api.raw(
  { expose: true, method: "GET", path: "/todos" },
  async (req, res) => {
    const rows = await db.query`
      SELECT id, title, done
      FROM todos
      ORDER BY id ASC
    `;
    const todos: Todo[] = [];
    for await (const row of rows) {
      todos.push({
        id: row.id,
        title: row.title,
        done: row.done,
      });
    }
    
    res.writeHead(200, { "Content-Type": "application/json" });
    res.end(JSON.stringify(todos));
  }
);

// PUT /todos/:id
export const update = api(
  { expose: true, method: "PUT", path: "/todos/:id" },
  async (params: UpdateTodoParams & { id: number }): Promise<void> => {
    const { id, title, done } = params;
    
    // Fetch existing
    const existing = await db.queryRow`SELECT title, done FROM todos WHERE id = ${id}`;
    if (!existing) {
      throw new Error("Todo not found");
    }
    
    const newTitle = title !== undefined ? title : existing.title;
    const newDone = done !== undefined ? done : existing.done;
    
    await db.exec`
      UPDATE todos
      SET title = ${newTitle}, done = ${newDone}
      WHERE id = ${id}
    `;
  }
);

// DELETE /todos/:id
export const remove = api(
  { expose: true, method: "DELETE", path: "/todos/:id" },
  async (params: { id: number }): Promise<void> => {
    await db.exec`
      DELETE FROM todos
      WHERE id = ${params.id}
    `;
  }
);
// dummy 2
