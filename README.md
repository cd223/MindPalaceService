# Mind Palace Service
A RESTful service for CRUD operations on Mind Palace project data.

## CURL Commands
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" https://mindpalaceservice.herokuapp.com/users
```
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" https://mindpalaceservice.herokuapp.com/palaces
```
```
curl -i -H "Accept: application/json" -H "Content-Type: application/json" https://mindpalaceservice.herokuapp.com/notes
```

```
curl -H "Content-Type: application/json" -X POST -d @ExampleNewUser.json https://mindpalaceservice.herokuapp.com/newuser
```
```
curl -H "Content-Type: application/json" -X POST -d @ExampleNewNote.json https://mindpalaceservice.herokuapp.com/newnote
```
```
curl -H "Content-Type: application/json" -X POST -d @ExampleNewPalace.json https://mindpalaceservice.herokuapp.com/newpalace
```

```
curl -X "DELETE" https://mindpalaceservice.herokuapp.com/user/1
```
```
curl -X "DELETE" https://mindpalaceservice.herokuapp.com/note/3
```
```
curl -X "DELETE" https://mindpalaceservice.herokuapp.com/palace/3
```

## Usage
REST API to be added...

### List all notes

**Definition**

`GET /notes`

**Response**

- `200 OK` on success