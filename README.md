# Django Chat Application

This is a real-time chat application built with Django, Django Channels, and WebSockets.

## Features

*   User signup and login
*   Display of all registered users in a collapsible left menu
*   One-on-one chat functionality
*   Message persistence in the database
*   Retrieval and display of chat history
*   Real-time communication using WebSockets

## Prerequisites

*   Python 3.7+
*   pip
*   A virtual environment (recommended)
*   PostgreSQL (or another database supported by Django)
*   Redis (for Channels)

## Setup

1.  **Clone the repository:**

    ```bash
    git clone [invalid URL removed] # Replace with your repo URL
    cd YOUR_REPO_NAME
    ```

2.  **Create a virtual environment (recommended):**

    ```bash
    python3 -m venv venv  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    source venv/bin/activate # On Linux/macOS
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Create a PostgreSQL database:**

    Create a new PostgreSQL database and user. Note down the database name, user, and password.

5.  **Configure Django settings:**

    *   Copy `mysite/settings.example.py` to `mysite/settings.py`:

        ```bash
        cp mysite/settings.example.py mysite/settings.py
        ```

    *   Edit `mysite/settings.py` and configure the following:
        *   `SECRET_KEY`: Generate a new secret key. You can use `python -c 'import os; print(os.urandom(24).hex())'`
        *   `DEBUG`: Set to `True` for development, `False` for production.
        *   `DATABASES`: Configure your PostgreSQL database settings:

            ```python
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': 'your_database_name',
                    'USER': 'your_database_user',
                    'PASSWORD': 'your_database_password',
                    'HOST': 'localhost',  # Or your database host
                    'PORT': '5432',  # Default PostgreSQL port
                }
            }
            ```

        *   `CHANNEL_LAYERS`: Configure Redis for Channels:

            ```python
            CHANNEL_LAYERS = {
                "default": {
                    "BACKEND": "channels_redis.core.RedisChannelLayer",
                    "CONFIG": {
                        "hosts": [("127.0.0.1", 6379)], # Replace with your Redis server details if needed
                    },
                },
            }
            ```

6.  **Run migrations:**

    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

7.  **Create a superuser:**

    ```bash
    python manage.py createsuperuser
    ```

8.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

9.  **Run the Channels development server (in a separate terminal):**

    ```bash
    daphne mysite.asgi:application
    ```

## Usage

1.  Open your web browser and go to `http://127.0.0.1:8000/`.
2.  Create an account or log in with the superuser credentials you created.
3.  You should see a list of users in the left menu. Click on a user to start a chat.

## Deployment (Production)

For production deployment, you'll need to use a production-ready WSGI/ASGI server (like Gunicorn or Uvicorn), a process manager (like Supervisor or Systemd), and a proper web server (like Nginx or Apache). You will also need to configure a production database and Redis server.

## Technologies Used

*   Django
*   Django Channels
*   WebSockets
*   PostgreSQL
*   Redis

## License

[Choose a license, e.g., MIT License]
