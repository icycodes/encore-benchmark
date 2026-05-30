import { api, API } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("book", {
  migrations: "./migrations",
});

interface Book {
  id: number;
  title: string;
  author: string;
}

interface BookParams {
  title: string;
  author: string;
}

// POST /book - Add a new book
export const addBook = api(
  { method: "POST", path: "/book", expose: true },
  async (params: BookParams): Promise<Book> => {
    const row = await db.queryRow`
      INSERT INTO books (title, author)
      VALUES (${params.title}, ${params.author})
      RETURNING id, title, author
    `;
    return row as Book;
  }
);

// GET /book/:id - Get a book by ID
export const getBook = api(
  { method: "GET", path: "/book/:id", expose: true },
  async (params: { id: number }): Promise<Book> => {
    const row = await db.queryRow`
      SELECT id, title, author FROM books WHERE id = ${params.id}
    `;
    if (!row) {
      throw API.notFound("book not found");
    }
    return row as Book;
  }
);

// GET /book - List all books
export const listBooks = api(
  { method: "GET", path: "/book", expose: true },
  async (): Promise<{ books: Book[] }> => {
    const rows = await db.query`
      SELECT id, title, author FROM books ORDER BY id
    `;
    const books: Book[] = [];
    for await (const row of rows) {
      books.push(row as Book);
    }
    return { books };
  }
);
// v2
// v3
