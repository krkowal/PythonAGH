# Assumptions

- User logs using email and password
- 2 readers cannot have the same email and 2 librarians cannot have the same email
- Librarian can have the same email as a reader
- Librarian cannot borrow books
- When reader borrows a book, reader borrows it for 28 days
- After 28 days of default borrowing, reader can prolong book rental up to 14 days if there are no reservations
- Reader cannot make a reservation on a book that they have already borrowed
- When librarian takes in book return, librarian needs only book_id (could be implemented as book_id and user_id, which
  creates new edge case)