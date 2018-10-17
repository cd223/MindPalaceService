--drop schemas
DROP TABLE notes;

--create schemas
CREATE TABLE notes(
   note_id SERIAL PRIMARY KEY,
   note_title VARCHAR(255) NOT NULL,
   note_description VARCHAR(255) NOT NULL,
   note_location VARCHAR(255),
   note_status VARCHAR(255) NOT NULL
   );

--insert dummy data
INSERT INTO notes(note_title,note_description,note_location,note_status) VALUES 
('Note 1','First note', '3.4,5.6','yes'),
('Note 2','Second note', '2.3,6.1','yes'),
('Note 3','Third note', '1.4,9.2','yes');