import { api } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("bookstore", {
  migrations: "./migrations",
});

interface Book {
  id: number;
  title: string;
  author: string;
}

interface CreateBookRequest {
  title: string;
  author: string;
}

export const addBook = api(
  { method: "POST", path: "/books", expose: true },
  async (req: CreateBookRequest): Promise<Book> => {
    const book = await db.queryRow<Book>`
      INSERT INTO books (title, author)
      VALUES (${req.title}, ${req.author})
      RETURNING id, title, author
    `;

    if (!book) {
      throw new Error("Failed to create book");
    }

    return book;
  }
);

export const listBooks = api(
  { method: "GET", path: "/books", expose: true },
  async (): Promise<Book[]> => {
    return db.query<Book>`
      SELECT id, title, author
      FROM books
      ORDER BY id
    `;
  }
);

export const deleteBook = api(
  { method: "DELETE", path: "/books/:id", expose: true },
  async (req: { id: number }): Promise<void> => {
    await db.exec`
      DELETE FROM books
      WHERE id = ${req.id}
    `;
  }
);
