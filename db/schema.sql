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
   note_location_x VARCHAR(32) NOT NULL,
   note_location_y VARCHAR(32) NOT NULL,
   note_image_url VARCHAR(1024) NOT NULL,
   note_status BOOLEAN NOT NULL DEFAULT FALSE
   );

--insert initial data
INSERT INTO USERS(user_name,user_username,user_password) VALUES
('Chris Davies','cjd47','pass'), 
('James Armitstead','ja336','pass'),
('Jamie Thompson','jt554','pass');

INSERT INTO PALACE(user_id,palace_title,palace_description) VALUES
('1','Fruit','Fruit Palace'),
('2','Fruit','Fruit Palace'),
('3','Fruit','Fruit Palace');

INSERT INTO NOTE(palace_id,note_title,note_description,note_location_x,note_location_y,note_image_url,note_status) VALUES
('1', 'Apple', 'Apple Description', '5.33','2.11', 'http://1.bp.blogspot.com/-sm2PC8KW-l4/UDP7Z4Mz80I/AAAAAAAAB6g/j91oeuESMcs/s1600/apple.jpg', FALSE),
('1', 'Orange', 'Orange Description', '1.7','8.4', 'http://producemadesimple.ca/wp-content/uploads/2015/01/orange-web-1024x768.jpg', TRUE),
('2', 'Banana', 'Banana Description', '6.1','9.0', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9b/Cavendish_Banana_DS.jpg/1920px-Cavendish_Banana_DS.jpg', FALSE),
('2', 'Grapes', 'Grapes Description', '4.5','6.3', 'http://www.viralnovelty.net/wp-content/uploads/2014/02/Red-Grapes.jpg', TRUE),
('3', 'Melon', 'Melon Description', '4.4','3.3', 'https://sanjeevkapoor.files.wordpress.com/2015/08/melon.jpg', FALSE),
('3', 'Pineapple', 'Pineapple Description', '0.9','8.9', 'https://www.toledoblade.com/image/2013/12/05/800x_b1_cCM_z/pineapple-jpg.jpg', TRUE);