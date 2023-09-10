# Internship Task

## Run Using [Docker]

Make sure that you are inside the project directory, where the `Dockerfile` file is present. Now, building and running the application server using `docker` :
```
Building or fetching the necessary images and later, creating and starting containers for the application
    $ sudo docker build -t 'flask-app' .

Run using
    $ sudo docker run flask-app
```

## URL Routes

| Method     | URI                               | Description                                                  |
|------------|-----------------------------------|---------------------------------------------------------|
| `GET`     | `/users`                        |Get list of all users in JSON format |
| `POST` | `/users`                        |Send form data to register new user |
| `GET`     | `/users/<id>`                        |Get details about user in JSON format |
| `PUT`     | `/users/<id>`                        |Send relevant form-data to update user details |
| `DELETE`     | `/users/<id>`                        |Delete user with id = <id> from database |


### Send requests using Postman to routes with relevant data for `POST` and `PUT` methods to get results. API has been tested and works as requested.

