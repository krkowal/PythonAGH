# Standard Users

- Librarian: email - admin, password - 123
- Reader: email - kowal, password - 123

# Assumptions

- User logs in using email and password
- 2 readers cannot have the same email and 2 librarians cannot have the same email
- Librarian can have the same email as a reader
- Librarian cannot borrow books
- Librarians can only be added manually to the database
- Reader borrows book for 28 days
- After 28 days of default borrowing, reader can prolong book rental up to 14 days if there are no reservations
- Reader cannot make a reservation on a book that they have already borrowed
- When librarian takes in book return, librarian needs only book_id (could be implemented as book_id and user_id (
  email), which
  creates new edge case)
- User can search through catalog using Search option
- Search finds books that have user input phrase in part of their name, part of their author name or one of their tags
- Search example: phrase: tom -> books found: Tom Sawyer, Tomcio Paluch; phrase: harry -> books found: Harry Potter I,
  Harry Potter II; etc.
- Email is just a mock (no verifying if email contains @ etc. when creating new user)
