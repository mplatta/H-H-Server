# H-H-Server
flask serwer web aplikacji mobilnej Hare & Hounds

## Featured endpoints:


- /api/login
```
"POST": {
                "description": "Check passed credentials.",
                "parameters": {
                    "email": {
                        "type": "string",
                        "description": "Users e-mail address."
                    },
                    "password": {
                        "type": "string",
                        "description": "Users password."
                    }
                },
                "example": {
                    "email": "admin@localhost.org",
                    "password": "5tr0ngp4ssw0rd"
                },
                "response": {
                    "success": {
                        "type": "boolean",
                        "description": "True if found user matching email and password. False otherwise."
                    },
                    "userId": {
                        "type": "integer",
                        "description": "Users ID from database. Null/None if failed to match."
                    },
                    "nickName": {
                        "type": "string",
                        "description": "Users nick name form database. Null/None if failed to match."
                    }
                }
            }
```

- /api/register
```
"POST": {
                "description": "Register new user.",
                "parameters": {
                    "email": {
                        "type": "string",
                        "description": "Users e-mail address."
                    },
                    "password": {
                        "type": "string",
                        "description": "Users password."
                    }
                },
                "example": {
                    "email": "admin@localhost.org",
                    "password": "5tr0ngp4ssw0rd"
                },
                "response": {
                    "success": {
                        "type": "boolean",
                        "description": "True if found user matching email and password. False otherwise."
                    },
                    "userId": {
                        "type": "integer",
                        "description": "Users ID from database. Null/None if failed to match."
                    },
                    "nickName": {
                        "type": "string",
                        "description": "Users nick name form database. Null/None if failed to match."
                    }
                }
            }
```

- /api/resetpswd

resetPassword
Methods: POST, OPTIONS

- /api/games

games
Methods: GET, HEAD, POST, OPTIONS

- /api/friends

friends
Methods: GET, HEAD, POST, OPTIONS
