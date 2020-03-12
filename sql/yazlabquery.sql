/*
CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR(13) NOT NULL,
    title VARCHAR(200) NOT NULL,
    img_filname VARCHAR(255) NOT NULL
);
CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    passwdsha256 VARCHAR(100) NOT NULL, 
    user_role INT NOT NULL,
    username VARCHAR (100) NOT NULL
);
--role 0 admin 1 user
CREATE TABLE booksinuse(
    id SERIAL,
    book_id SERIAL NOT NULL,
    user_id SERIAL NOT NULL,
    return_date timestamp NOT NULL,
    PRIMARY KEY(id, book_id)
);
*/
-- somehow we get username no need tree table inner join

--debug query

/*
SELECT users.username, books.title, booksinuse.return_date
FROM booksinuse 
INNER JOIN users ON users.id = booksinuse.user_id
INNER JOIN books ON books.id = booksinuse.book_id
where users.username = 'asdf';
*/


-- list all users and borrowed books
/*
SELECT username 
FROM users 
WHERE username 
NOT IN (
    SELECT users.username
    FROM booksinuse 
    INNER JOIN users ON users.id = booksinuse.user_id
    INNER JOIN books ON books.id = booksinuse.book_id
    ) AND user_role != 0;
*/

/*
SELECT users.username, books.title, booksinuse.return_date
FROM booksinuse 
INNER JOIN users ON users.id = booksinuse.user_id
INNER JOIN books ON books.id = booksinuse.book_id
*/

-- available books
/*
SELECT title, isbn
FROM books
WHERE isbn
NOT IN (
    SELECT books.isbn
    FROM books 
    INNER JOIN booksinuse ON books.id = booksinuse.book_id
    );
*/

-- user borrowed book count
/*
SELECT COUNT(u.username)
FROM users u
INNER JOIN booksinuse biu ON u.id = biu.user_id
WHERE u.username = 'mrk'
*/

-- user return date
SELECT biu.return_date
FROM users u
INNER JOIN booksinuse biu ON u.id = biu.user_id
WHERE u.username = 'mrk'