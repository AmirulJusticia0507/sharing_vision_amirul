Flask Backend for Sharing Vision

This is a backend system developed using Flask, Flask-Migrate, and MySQL for the Sharing Vision project. The backend handles database migrations, user management, and other essential functionalities.
Features

    Flask-based backend
    MySQL database integration
    Flask-Migrate for database migrations
    User management
    RESTful API endpoints

Prerequisites

Before you begin, ensure you have met the following requirements:

    Python 3.7+
    MySQL Server
    Pip (Python package manager)
    Virtual environment (optional, but recommended)

    Installation
1. Clone the Repository
git clone https://github.com/username/sharing_vision_amirul.git
cd sharing_vision_amirul/backend

2.  Set Up the Virtual Environment (Optional)
python -m venv venv
source venv/bin/activate  # For Linux/MacOS
venv\Scripts\activate  # For Windows

3.   Install Dependencies
pip install -r requirements.txt

4.  Set Up MySQL Database

    Create a MySQL database named sharing_vision_db.
    Update the database configuration in config.py or .env with your MySQL credentials.
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/sharing_vision_db'

5. Initialize and Migrate the Database

If this is your first time setting up the database:
flask db init  # Skip this if the migrations directory already exists
flask db migrate
flask db upgrade

Usage
Running the Development Server

Start the Flask development server:
flask run

The server will be running at http://127.0.0.1:5000/.
API Endpoints

You can access the API endpoints at http://127.0.0.1:5000/api. Detailed API documentation will be provided separately.
Testing

To run tests, use the following command:
pytest

Folder Structure:
sharing_vision_amirul
  backend
  frontend

  Troubleshooting
Error: Directory migrations already exists and is not empty

This error occurs when trying to initialize Alembic migrations on an existing project. If you see this message, skip the flask db init step.
Error: No changes in schema detected

This message indicates that no changes were found in your models compared to the last migration. Ensure that you've made changes to your models if this isn't expected.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Contact

If you have any questions or feedback, feel free to reach out to me at [amirulputra0507@gmail.com].
