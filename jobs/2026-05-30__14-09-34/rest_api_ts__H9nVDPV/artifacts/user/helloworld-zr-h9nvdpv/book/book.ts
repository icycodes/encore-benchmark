import { api, APIError } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("books", { migrations: "migrations" });

interface Book {
  id: number;
  title: string;
  author: string;
}

interface CreateBookRequest {
  title: string;
  author: string;
}

interface GetBookRequest {
  id: number;
}

export const addBook = api(
  { method: "POST", path: "/book", expose: true },
  async ({ title, author }: CreateBookRequest): Promise<Book> => {
    const created = await db.queryRow<Book>
      `INSERT INTO books (title, author) VALUES (${title}, ${author}) RETURNING id, title, author`;

    if (!created) {
      throw APIError.internal("Failed to create book");
    }

    return created;
  }
);

export const getBook = api(
  { method: "GET", path: "/book/:id", expose: true },
  async ({ id }: GetBookRequest): Promise<Book> => {
    const book = await db.queryRow<Book>
      `SELECT id, title, author FROM books WHERE id = ${id}`;

    if (!book) {
      throw APIError.notFound(`Book ${id} not found`);
    }

    return book;
  }
);

export const listBooks = api(
  { method: "GET", path: "/book", expose: true },
  async (): Promise<Book[]> => {
    return db.queryAll<Book>`SELECT id, title, author FROM books ORDER BY id`;
  }
);
