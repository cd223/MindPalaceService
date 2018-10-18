# Mind Palace Service
A RESTful service for CRUD operations on Mind Palace project data.

Service URL: <https://mindpalaceservice.herokuapp.com/>

## REST API

### USERS
#### List all users

**Definition**

`GET /users`

**Response**

- `200 OK` on success
- `505 INTERNAL SERVER ERROR` on failure (e.g. SQL error)

```json
[
  {
    "user_id": 1, 
    "user_name": "Chris Davies", 
    "user_password": "pass", 
    "user_username": "cjd47"
  }, 
  {
    "user_id": 2, 
    "user_name": "James Armitstead", 
    "user_password": "pass", 
    "user_username": "ja336"
  }, 
  {
    "user_id": 3, 
    "user_name": "Jamie Thompson", 
    "user_password": "pass", 
    "user_username": "jt554"
  }
]
```

**CURL Command**
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" <https://mindpalaceservice.herokuapp.com/users>
```

#### Add new user

**Definition**

`POST /newuser`

**Arguments**

- `"user_name":string` the name of the new user
- `"user_username":string` a friendly username for the user
- `"user_password":string` a password for the user to login to the application

```json
{
  "user_name" : "Joe Bloggs",
  "user_username" : "jbloggs999",
  "user_password" : "pass"
}
```

**Response**

- `200 OK` on success
- `505 INTERNAL SERVER ERROR` on failure (e.g. SQL error)

**CURL Command**
```
curl -H "Content-Type: application/json" -X POST -d @ExampleNewUser.json <https://mindpalaceservice.herokuapp.com/newuser>
```


### PALACES
#### List all palaces

**Definition**

`GET /palaces`

**Response**

- `200 OK` on success
- `505 INTERNAL SERVER ERROR` on failure (e.g. SQL error)

```json
[
  {
    "palace_description": "dummy description 1", 
    "palace_id": 1, 
    "palace_title": "palace 1", 
    "user_id": 1
  }, 
  {
    "palace_description": "dummy description 2", 
    "palace_id": 2, 
    "palace_title": "palace 2", 
    "user_id": 2
  }, 
  {
    "palace_description": "dummy description 3", 
    "palace_id": 3, 
    "palace_title": "palace 3", 
    "user_id": 3
  }
]
```

**CURL Command**
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" <https://mindpalaceservice.herokuapp.com/palaces>
```

#### Add new palace

**Definition**

`POST /newpalace`

**Arguments**

- `"user_id":string` id of the user the palace is to be registered with
- `"palace_title":string` a friendly title for the palace
- `"palace_description":string` a description of what the palace is for

```json
{
  "user_id" : "2",
  "palace_title" : "Test Palace",
  "palace_description" : "Palace added by example JSON"
}
```

**Response**

- `200 OK` on success
- `505 INTERNAL SERVER ERROR` on failure (e.g. SQL error)

**CURL Command**
```
curl -H "Content-Type: application/json" -X POST -d @ExampleNewPalace.json <https://mindpalaceservice.herokuapp.com/newpalace>
```





### NOTES
#### List all notes

**Definition**

`GET /notes`

**Response**

- `200 OK` on success
- `505 INTERNAL SERVER ERROR` on failure (e.g. SQL error)

```json
[
  {
    "note_description": "Palace 1 Note 1", 
    "note_id": 1, 
    "note_location": "5.3,2.1", 
    "note_status": false, 
    "note_title": "P1N1", 
    "palace_id": 1
  }, 
  {
    "note_description": "Palace 1 Note 2", 
    "note_id": 2, 
    "note_location": "1.7,8.4", 
    "note_status": true, 
    "note_title": "P1N2", 
    "palace_id": 1
  }, 
  {
    "note_description": "Palace 2 Note 2", 
    "note_id": 4, 
    "note_location": "4.5,6.3", 
    "note_status": true, 
    "note_title": "P2N2", 
    "palace_id": 2
  }, 
  {
    "note_description": "Palace 3 Note 1", 
    "note_id": 5, 
    "note_location": "4.4,3.3", 
    "note_status": false, 
    "note_title": "P3N1", 
    "palace_id": 3
  }
]
```

**CURL Command**
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" <https://mindpalaceservice.herokuapp.com/notes>
```

#### Add new note

**Definition**

`POST /newnote`

**Arguments**

- `palace_id:string` id of the palace the note is to be registered with
- `note_title:string` a friendly title for the note
- `note_description:string` a description of what the note is
- `note_location:string` a string representing the location of the note in the room
- `note_status:boolean` a status over whether the note has been remembered

```json
{
  "palace_id" : "1",
  "note_title" : "Test Note",
  "note_description" : "Note added by example JSON",
  "note_location" : "10.0,7.3",
  "note_status" : false
}
```

**Response**

- `200 OK` on success
- `505 INTERNAL SERVER ERROR` on failure (e.g. SQL error)

**CURL Command**
```
curl -H "Content-Type: application/json" -X POST -d @ExampleNewNote.json <https://mindpalaceservice.herokuapp.com/newnote>
```

## DELETE Commands
```
curl -X "DELETE" <https://mindpalaceservice.herokuapp.com/user/1>
```
```
curl -X "DELETE" <https://mindpalaceservice.herokuapp.com/note/1
```
```
curl -X "DELETE" <https://mindpalaceservice.herokuapp.com/palace/1>
```