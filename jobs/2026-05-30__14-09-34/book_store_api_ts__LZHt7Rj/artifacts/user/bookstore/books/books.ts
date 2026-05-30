import { api, APIError } from "encore.dev/api";
import { SQLDatabase } from "encore.dev/storage/sqldb";

const db = new SQLDatabase("bookstore", {
  migrations: "./migrations",
});

interface Book {
  id: number;
  title: string;
  author: string;
}

interface CreateBookParams {
  title: string;
  author: string;
}

// Add a new book to the bookstore.
export const addBook = api(
  { expose: true, method: "POST", path: "/books" },
  async (params: CreateBookParams): Promise<Book> => {
    const row = await db.queryRow<Book>(
      "INSERT INTO books (title, author) VALUES ($1, $2) RETURNING id, title, author",
      [params.title, params.author]
    );
    if (!row) {
      throw APIError.internal("failed to insert book");
    }
    return row;
  }
);

// List all books in the bookstore.
export const listBooks = api(
  { expose: true, method: "GET", path: "/books" },
  async (): Promise<{ books: Book[] }> => {
    const rows = await db.query<Book>("SELECT id, title, author FROM books ORDER BY id");
    const books: Book[] = [];
    for await (const row of rows) {
      books.push(row);
    }
    return { books };
  }
);

// Delete a book by ID.
export const deleteBook = api(
  { expose: true, method: "DELETE", path: "/books/:id" },
  async ({ id }: { id: number }): Promise<void> => {
    const result = await db.exec("DELETE FROM books WHERE id = $1", [id]);
    if (result.rowsAffected === 0) {
      throw APIError.notFound("book not found");
    }
  }
);