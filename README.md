# Track_reading_project

A system that tracks the time a user spends reading a book. 
The user can start a reading session, end it, and the system stores the duration of 
each session and the total reading time for each book.

API FUNCTIONALITY:
Using DRF, I created an API that allows you to:
- Get a list of books with information (title, author, year of publication, short description)
- Get book details (title, author, year of publication, short description, full description, date of last reading)
- Start and end a reading session by specifying the book ID. Each user has their own session. The user cannot start more than one session with the same book,
if the user starts a session with another book, the session with the previous book should end automatically.
- Get the total reading time for each book and general user statistics.
- A task has been created that collects daily statistics on the user's total reading time for the last 7 and 30 days and saves it to the user's profile.

HOW TO RUN:
- set up pipenv environment
- write in terminal "docker compose up --build"
