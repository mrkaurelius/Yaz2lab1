DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS booksinuse;

CREATE TABLE books(
    id SERIAL,
    isbn VARCHAR(13) NOT NULL,
    title VARCHAR(200) NOT NULL,
    img_filname VARCHAR(255) NOT NULL,
    PRIMARY KEY(isbn) --one book for one isbn
);
--reconsider img_filname

CREATE TABLE users(
    id SERIAL PRIMARY KEY,
    passwdsha256 VARCHAR(100) NOT NULL, 
    user_role INT NOT NULL,
    username VARCHAR (100) NOT NULL
);
--smarter approach?
--role 0 admin 1 user
--varchar64 -> sha256

CREATE TABLE booksinuse(
    id SERIAL,
    book_id SERIAL NOT NULL,
    user_id SERIAL NOT NULL,
    return_date timestamp NOT NULL,
    PRIMARY KEY(book_id) --one book for one isbn
);