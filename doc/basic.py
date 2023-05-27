tags = [
    {
        "name": "Login",
        "description": "This is the login endpoint, it will take a username and password and return a JWT token",
    },
    {
        "name": "Register",
        "description": "Any one can register with Unique username, email. Also user needs to provide fast and last name with password",
        "externalDocs": {
            "description": "Look For Internal Doc",
            "url": "https://dev.prerevise.com/",
        },
    },
    {
        "name": "Start Following",
        "description": "This is the start following endpoint, it will take a username and return a JWT token, this is a protected endpoint",
    },
    {
        "name": "Stop Following",
        "description": "This is the stop following endpoint, it will take a username and return a JWT token, this is a protected endpoint",
    }
    ,
    {
        "name": "Current User",
        "description": "This is a protected endpoint that will return logged in user details",
    }
    ,
    {
        "name": "Create Post",
        "description": "This is a protected endpoint that let user create new post",
    },
    {
        "name": "Login History",
        "description": "This is a protected endpoint that will return last 10 login attempt",
    }
]