INSERT INTO arttime (timeis ) VALUES ('2020-03-10');

INSERT INTO books (title, isbn, img_filname ) VALUES (
    'code complete', '9783860635933','dummypath.jpg'
);

INSERT INTO books (title, isbn, img_filname ) VALUES (
    'milletlerin zenginligi', '9789754589276','dummypath.jpg'
);

INSERT INTO users (user_role, username, passwdsha256) VALUES (0,'admin',
'pbkdf2:sha256:150000$6AEOAf3p$6b529daad6f61ba05b5a431979b1370047eca33c654d0262adc25a0b18316d0e');
-- "1234"

INSERT INTO users (user_role, username, passwdsha256) VALUES (1,'mrk',
'pbkdf2:sha256:150000$2B98hDvI$3f6dfc081b29885b719f97d4387fb3964bf8023c59c009f749d953fd03b5a1b8');
-- "2929"

INSERT INTO users (user_role, username, passwdsha256) VALUES (1,'mehmet',
'pbkdf2:sha256:150000$2B98hDvI$3f6dfc081b29885b719f97d4387fb3964bf8023c59c009f749d953fd03b5a1b8');
-- "2929"

INSERT INTO users (user_role, username, passwdsha256) VALUES (1,'ali',
'pbkdf2:sha256:150000$2B98hDvI$3f6dfc081b29885b719f97d4387fb3964bf8023c59c009f749d953fd03b5a1b8');
-- "2929"

--mrk id: 2
INSERT INTO booksinuse (book_id, user_id, borrow_date ) VALUES (1,2,'2020-03-11');