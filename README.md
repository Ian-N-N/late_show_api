# Late Show API

A simple RESTful API to manage episodes, guests, and appearances for a late show. Built with **Flask** and **Flask-SQLAlchemy**, the API allows listing episodes, viewing episode details with nested guest appearances, adding appearances, and deleting episodes. 

## Features

- List all episodes (`GET /episodes`)  
- View episode details with appearances and guest info (`GET /episodes/<id>`)  
- Delete an episode with cascading deletion of appearances (`DELETE /episodes/<id>`)  
- List all guests (`GET /guests`)  
- Create a new appearance with rating validation (`POST /appearances`)  