**This documentation is automatically generated.**

**Output schemas only represent `data` and not the full output; see output examples and the JSend specification.**

# /api/asynchelloworld/\(?P\<name\>\[a\-zA\-Z0\-9\_\\\-\]\+\)/?$

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "type": "string"
}
```


**Output Example**
```json
"Hello (asynchronous) world! My name is Fred."
```


**Notes**

Shouts hello to the world (asynchronously)!



<br>
<br>

# /api/freewilled/?

    Content-Type: application/json



<br>
<br>

# /api/greeting/\(?P\<fname\>\[a\-zA\-Z0\-9\_\\\-\]\+\)/\(?P\<lname\>\[a\-zA\-Z0\-9\_\\\-\]\+\)/?$

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "type": "string"
}
```


**Output Example**
```json
"Greetings, Named Person!"
```


**Notes**

Greets you.



<br>
<br>

# /api/helloworld/?

    Content-Type: application/json

## GET


**Input Schema**
```json
null
```



**Output Schema**
```json
{
    "type": "string"
}
```


**Output Example**
```json
"Hello world!"
```


**Notes**

Shouts hello to the world!



<br>
<br>

# /api/postit/?

    Content-Type: application/json

## POST


**Input Schema**
```json
{
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
    },
    "type": "object"
}
```


**Input Example**
```json
{
    "body": "Equally important message",
    "index": 0,
    "title": "Very Important Post-It Note"
}
```


**Output Schema**
```json
{
    "properties": {
        "message": {
            "type": "string"
        }
    },
    "type": "object"
}
```


**Output Example**
```json
{
    "message": "Very Important Post-It Note was posted."
}
```


**Notes**

POST the required parameters to post a Post-It note

* `title`: Title of the note
* `body`: Body of the note
* `index`: An easy index with which to find the note


