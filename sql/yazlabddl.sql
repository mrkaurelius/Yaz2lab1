DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS booksinuse;
DROP TABLE IF EXISTS arttime;

CREATE TABLE books(
    id SERIAL PRIMARY KEY,
    isbn VARCHAR(13) NOT NULL,
    title VARCHAR(200) NOT NULL
);

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
    borrowing_time timestamp NOT NULL,
    PRIMARY KEY(id, user_id)
);

-- howto use timetstaps in postgres
CREATE TABLE arttime(
    timeis timestamp
);