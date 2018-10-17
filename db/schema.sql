--drop schemas
DROP TABLE NOTE;
DROP TABLE PALACE;
DROP TABLE USERS;

--recreate schemas
CREATE TABLE USERS(
   user_id SERIAL PRIMARY KEY,
   user_name VARCHAR(64) NOT NULL,
   user_username VARCHAR(64) NOT NULL,
   user_password VARCHAR(64) NOT NULL
   );

CREATE TABLE PALACE(
   palace_id SERIAL PRIMARY KEY,
   user_id INTEGER REFERENCES USERS (user_id) ON DELETE CASCADE,
   palace_title VARCHAR(64) NOT NULL,
   palace_description VARCHAR(255) NOT NULL
   );

CREATE TABLE NOTE(
   note_id SERIAL PRIMARY KEY,
   palace_id INTEGER REFERENCES PALACE (palace_id) ON DELETE CASCADE,
   note_title VARCHAR(64) NOT NULL,
   note_description VARCHAR(255) NOT NULL,
   note_location VARCHAR(64),
   note_status BOOLEAN NOT NULL DEFAULT FALSE
   );

--insert initial data
INSERT INTO USERS(user_name,user_username,user_password) VALUES
('Chris Davies','cjd47','pass'),
('James Armitstead','ja336','pass'),
('Jamie Thompson','jt554','pass');

INSERT INTO PALACE(user_id,palace_title,palace_description) VALUES
('1','palace 1','dummy description 1'),
('2','palace 2','dummy description 2'),
('3','palace 3','dummy description 3');

INSERT INTO NOTE(palace_id,note_title,note_description,note_location,note_status) VALUES
('1', 'P1N1', 'Palace 1 Note 1', '5.3,2.1',FALSE),
('1', 'P1N2', 'Palace 1 Note 2', '1.7,8.4',TRUE),
('2', 'P2N1', 'Palace 2 Note 1', '6.1,9.0',FALSE),
('2', 'P2N2', 'Palace 2 Note 2', '4.5,6.3',TRUE),
('3', 'P3N1', 'Palace 3 Note 1', '4.4,3.3',FALSE),
('3', 'P3N2', 'Palace 3 Note 2', '0.9,8.9',TRUE);