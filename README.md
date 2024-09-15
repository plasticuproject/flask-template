# WIP FlasK Project Template

## Project Structure
```
├── app.py
├── blueprints
│   ├── admin
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── static
│   │   └── templates
│   │       ├── base.html
│   │       ├── login.html
│   │       └── register.html
│   ├── auth
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   ├── static
│   │   └── templates
│   │       ├── base.html
│   │       ├── login.html
│   │       └── register.html
│   ├── errors
│   │   ├── handlers.py
│   │   ├── __init__.py
│   │   └── templates
│   │       ├── 404.html
│   │       ├── 500.html
│   │       └── base.html
│   ├── __init__.py
│   └── main
│       ├── __init__.py
│       ├── routes.py
│       ├── static
│       └── templates
│           ├── base.html
│           ├── dashboard.html
│           └── home.html
├── config.py
├── create_admin.py
├── env
├── extensions.py
├── models.py
├── mypy.ini
├── pytest.ini
├── README.md
├── requirements.txt
├── stubs
│   ├── flask_argon2
│   │   └── __init__.pyi
│   ├── flask_login
│   │   └── __init__.pyi
│   ├── flask_sqlalchemy
│   │   └── __init__.pyi
│   ├── flask_testing
│   │   └── __init__.pyi
│   ├── flask_wtf
│   │   ├── csrf.pyi
│   │   └── __init__.pyi
│   └── wtforms
│       ├── fields
│       │   └── core.pyi
│       ├── __init__.pyi
│       └── validators.pyi
├── tests
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_create_admin.py
│   ├── test_errors.py
│   └── test_main.py
└── wsgi.py
```

## Explanation

- **app.py**: The application factory that creates and configures the Flask app. 
  It initializes the extensions and registers blueprints for routing.
  
- **config.py**: Holds configuration settings such as environment-specific 
  settings, secret keys, database URIs, and other constants.
  
- **extensions.py**: Initializes and manages Flask extensions (e.g., SQLAlchemy, 
  Flask-Login) used throughout the application. This file centralizes extension 
  management.

- **models.py**: Defines the database models (e.g., `User`) used in the app. 
  These models are mapped to the database using SQLAlchemy.

- **blueprints/admin**: Contains routes and templates specific to admin 
  functionality, such as user management. It includes:
  - `routes.py`: Defines the admin-specific routes.
  - `templates/`: Contains HTML templates like `login.html` and `register.html` 
    for admin pages.

- **blueprints/auth**: Handles authentication, including user login and 
  registration. It includes:
  - `forms.py`: Defines WTForms used for login and registration.
  - `routes.py`: Handles user authentication routes.
  - `templates/`: Contains HTML templates related to user authentication 
    (e.g., `login.html`, `register.html`).

- **blueprints/errors**: Manages custom error handling for the app.
  - `handlers.py`: Defines custom error pages (e.g., for 404 and 500 errors).
  - `templates/`: Contains error templates such as `404.html` and `500.html`.

- **blueprints/main**: A blueprint for the main parts of the application, such 
  as the home page and user dashboard.
  - `routes.py`: Defines routes for the main pages (e.g., home, dashboard).
  - `templates/`: Contains the main templates, including `home.html` and 
    `dashboard.html`.

- **stubs/**: Contains type stubs for libraries like `flask_argon2`, 
  `flask_login`, `flask_sqlalchemy`, and `wtforms`, which help with static type 
  checking using `mypy`.

- **wsgi.py**: The entry point for running the application using a WSGI server 
  (e.g., Gunicorn). It imports and runs the Flask app from `app.py`.

- **create_admin.py**: A script to create an admin user if required during the 
  initial setup.

- **tests/**: Contains unit tests and integration tests for the application. 
  This directory includes tests for various parts of the application, such as 
  authentication, error handling, and route functionality. Tests are typically 
  written using pytest and may utilize fixtures (defined in conftest.py) to set 
  up a testing environment with a temporary database and mock objects.

## Running the Application

1. Install Dependencies
```
pip install -r requirements.txt
```

2. Set Environment Variables (Optional)

For development purposes:

- On Linux/macOS:
```
export FLASK_APP=app.py
export FLASK_ENV=development
```

- On Windows
```
set FLASK_APP=app.py
set FLASK_ENV=development
```

3. Configure Variables and Initialize the Database

Copy the contents of `env` to `.env`
```
cp env .env
```

Edit the `.env` file as necessary.

Run the following commands to create and set up the database:
```
touch site.db
flask db init
flask db migrate -m "Initialization"
flask db upgrade
```

4. Create Admin User
If you need to create an admin user, run the create_admin.py script:
```
python create_admin.py
```

5. Run the Application

```
gunicorn --bind 0.0.0.0:8000 wsgi:app
```

Access the application at http://localhost:8000.
