INSERT INTO books (title, isbn, img_filname ) VALUES (
    'the ultimate guide for vocabulary', '9786058962620','dummypath.jpg'
);

INSERT INTO books (title, isbn, img_filname ) VALUES (
    'beyaz geceler', '9786053321392','dummypath.jpg'
);

INSERT INTO books (title, isbn, img_filname ) VALUES (
    'harry potter ve sirlar odasi', '9789750802959','dummypath.jpg'
);

/*
INSERT INTO books (title, isbn, img_filname ) VALUES (
    'milletlerin zenginligi', '9789754589276','dummypath.jpg'
);

INSERT INTO books (title, isbn, img_filname ) VALUES (
    'uluslarin dususu', '9786050918120','dummypath.jpg'
);
*/
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

INSERT INTO users (user_role, username, passwdsha256) VALUES (1,'ayşe',
'pbkdf2:sha256:150000$2B98hDvI$3f6dfc081b29885b719f97d4387fb3964bf8023c59c009f749d953fd03b5a1b8');
-- "2929"

INSERT INTO users (user_role, username, passwdsha256) VALUES (1,'fatma',
'pbkdf2:sha256:150000$2B98hDvI$3f6dfc081b29885b719f97d4387fb3964bf8023c59c009f749d953fd03b5a1b8');
-- "2929"

INSERT INTO users (user_role, username, passwdsha256) VALUES (1,'deniz',
'pbkdf2:sha256:150000$2B98hDvI$3f6dfc081b29885b719f97d4387fb3964bf8023c59c009f749d953fd03b5a1b8');
-- "2929"

--mrk id: 2
INSERT INTO booksinuse (book_id, user_id, return_date ) VALUES (1,2,'2020-05-5');
INSERT INTO booksinuse (book_id, user_id, return_date ) VALUES (2,2,'2020-05-5');