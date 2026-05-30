import { api, APIError } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

// Define the database
const db = new SQLDatabase("book", {
  migrations: "./migrations",
});

// Define the book interface
export interface Book {
  id: number;
  title: string;
  author: string;
}

export interface ListBooksResponse {
  books: Book[];
}

// POST /book
export const addBook = api(
  { expose: true, method: "POST", path: "/book" },
  async (params: { title: string; author: string }): Promise<Book> => {
    const row = await db.queryRow`
      INSERT INTO books (title, author)
      VALUES (${params.title}, ${params.author})
      RETURNING id, title, author
    `;
    if (!row) throw APIError.internal("Could not insert book");
    return { id: row.id, title: row.title, author: row.author };
  }
);

// GET /book/:id
export const getBook = api(
  { expose: true, method: "GET", path: "/book/:id" },
  async (params: { id: number }): Promise<Book> => {
    const row = await db.queryRow`
      SELECT id, title, author
      FROM books
      WHERE id = ${params.id}
    `;
    if (!row) throw APIError.notFound("Book not found");
    return { id: row.id, title: row.title, author: row.author };
  }
);

// GET /book
export const listBooks = api(
  { expose: true, method: "GET", path: "/book" },
  async (): Promise<ListBooksResponse> => {
    const rows = await db.query`
      SELECT id, title, author
      FROM books
    `;
    const books: Book[] = [];
    for await (const row of rows) {
      books.push({ id: row.id, title: row.title, author: row.author });
    }
    return { books };
  }
);
