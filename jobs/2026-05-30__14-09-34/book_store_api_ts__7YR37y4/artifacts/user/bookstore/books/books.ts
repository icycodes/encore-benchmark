import { api } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("bookstore", {
  migrations: "./migrations",
});

export interface Book {
  id: number;
  title: string;
  author: string;
}

export interface AddBookParams {
  title: string;
  author: string;
}

export const addBook = api(
  { expose: true, method: "POST", path: "/books" },
  async (params: AddBookParams): Promise<Book> => {
    const row = await db.queryRow`
      INSERT INTO books (title, author)
      VALUES (${params.title}, ${params.author})
      RETURNING id, title, author
    `;
    if (!row) throw new Error("Failed to insert book");
    return {
      id: row.id,
      title: row.title,
      author: row.author,
    };
  }
);

export const listBooks = api.raw(
  { expose: true, method: "GET", path: "/books" },
  async (req, res) => {
    try {
      const rows = await db.query`SELECT id, title, author FROM books ORDER BY id ASC`;
      const books: Book[] = [];
      for await (const row of rows) {
        books.push({
          id: row.id,
          title: row.title,
          author: row.author,
        });
      }
      res.writeHead(200, { "Content-Type": "application/json" });
      res.end(JSON.stringify(books));
    } catch (err) {
      res.writeHead(500, { "Content-Type": "application/json" });
      res.end(JSON.stringify({ error: "Internal Server Error" }));
    }
  }
);

export const deleteBook = api(
  { expose: true, method: "DELETE", path: "/books/:id" },
  async (params: { id: number }): Promise<void> => {
    await db.exec`DELETE FROM books WHERE id = ${params.id}`;
  }
);
