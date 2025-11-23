# Late Show API

A simple RESTful API to manage episodes, guests, and appearances for a late show. Built with **Flask** and **Flask-SQLAlchemy**, the API allows listing episodes, viewing episode details with nested guest appearances, adding appearances, and deleting episodes. 
## Folder Structure
```bash
.
├── README.md
├── __init__.py
├── instance
├── migrations
│   ├── README
│   ├── alembic.ini
│   ├── env.py
│   ├── script.py.mako
│   └── versions
├── requirements.txt
└── server
    ├── __init__.py
    ├── app.py
    ├── instance
    ├── models.py
    ├── seed.py
    └── testing
```

## Features

- List all episodes (`GET /episodes`)  
- View episode details with appearances and guest info (`GET /episodes/<id>`)  
- Delete an episode with cascading deletion of appearances (`DELETE /episodes/<id>`)  
- List all guests (`GET /guests`)  
- Create a new appearance with rating validation (`POST /appearances`)  

## Technologies

- Python 3.8+  
- Flask  
- Flask-SQLAlchemy  
- Flask-Migrate  
- SQLite (for local development)  
- SQLAlchemy-Serializer  

## Installation

1. **Clone the repository**

```bash
git clone <repository-url>
cd late_show_api/server
```
2. **Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate   # On Linux/macOS
venv\Scripts\activate      # On Windows
```
3. **Install the Dependencies**
```bash
pip install -r requirements.txt
# Ensure requirements.txt pins SQLAlchemy<2.0 to avoid deprecation issues.
```
4. **Database Seeding**
```bash
python seed.py
# This should be done before running the app so that you create tables with sample data
```
5. **Run the App**
```bash
python app.py
```
- The API will be available at: http://127.0.0.1:5555/
- Sample: GET http://127.0.0.1:5555/episodes

## Author
Name: Ian Ngoru Njuguna
Email: njugunaian65@gmail.com 

