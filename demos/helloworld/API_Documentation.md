**This documentation is automatically generated.**

**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**

# `/api/asynchelloworld`

    Content-Type: application/json

## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "string"
}
```

### Output Example
```json
"Hello (asynchronous) world!"
```


Shouts hello to the world (asynchronously)!





# `/api/greeting/(?P<name>[a-zA-Z0-9_]+)/?$`

    Content-Type: application/json

## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "string"
}
```

### Output Example
```json
"Greetings, Greg!"
```


Greets you.





# `/api/helloworld`

    Content-Type: application/json

## GET
### Input Schema
```json
null
```

### Output Schema
```json
{
    "type": "string"
}
```

### Output Example
```json
"Hello world!"
```


Shouts hello to the world!





# `/api/postit`

    Content-Type: application/json

## POST
### Input Schema
```json
{
    "type": "object", 
    "properties": {
        "body": {
            "type": "string"
        }, 
        "index": {
            "type": "number"
        }, 
        "title": {
            "type": "string"
        }
    }
}
```

### Input Example
```json
{
    "body": "Equally important message", 
    "index": 0, 
    "title": "Very Important Post-It Note"
}
```

### Output Schema
```json
{
    "type": "object", 
    "properties": {
        "message": {
            "type": "string"
        }
    }
}
```

### Output Example
```json
{
    "message": "Very Important Post-It Note was posted."
}
```



POST the required parameters to post a Post-It note

* `title`: Title of the note
* `body`: Body of the note
* `index`: An easy index with which to find the note


