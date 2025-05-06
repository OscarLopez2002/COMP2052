# Basic Flask Authentication with Flask-Login

This is a minimal example of a Flask application demonstrating basic user authentication using Flask-Login.

## Features

- User login and logout.
- A protected route accessible only to authenticated users.
- An in-memory user store (for demonstration purposes only).

## Setup and Running

1.  **Clone the repository or download the files.**
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Run the application:**
    ```bash
    python app.py
    ```
5.  Open your browser and go to `http://127.0.0.1:5000/`.

## Code Explanation

-   **`app.py`**: Contains the main Flask application logic.
    -   It initializes Flask and Flask-Login.
    -   A `User` class (inheriting from `UserMixin`) is defined to represent users.
    -   An in-memory dictionary `users_db` acts as a simple database. **For a real application, use a proper database.**
    -   `@login_manager.user_loader` provides a function to reload the user object from the user ID stored in the session.
    -   **Routes:**
        -   `/`: Home page. Shows login/logout links and a link to the protected page if authenticated.
        -   `/login`: Handles GET requests to display the login form and POST requests to process login attempts.
        -   `/protected`: A route decorated with `@login_required`. Access is granted only if the user is logged in. Otherwise, they are redirected to the login page.
        -   `/logout`: Logs the current user out.
-   **`requirements.txt`**: Lists the Python packages required for this project (Flask, Flask-Login).

## Security Note

-   The `SECRET_KEY` in `app.py` is hardcoded. **In a production environment, this key must be kept secret and should be set via environment variables or a configuration file.**
-   The user storage is in-memory and passwords are plaintext. **This is not secure for a real application.** Use a database with hashed passwords (e.g., using Werkzeug's security helpers or libraries like Passlib).
