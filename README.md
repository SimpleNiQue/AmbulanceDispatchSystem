# Ambulance Dispatch System

This is a Django-based application for managing and dispatching ambulances for emergency requests.

## Setup Instructions

### For Linux and Mac Users

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/AmbulanceDispatchSystem.git
    ```

2.  **Navigate to the backend directory:**

    ```bash
    cd AmbulanceDispatchSystem/backend
    ```

3.  **Create a virtual environment:**

    ```bash
    python3 -m venv .venv
    ```

4.  **Activate the virtual environment:**

    ```bash
    source .venv/bin/activate
    ```

5.  **Install the required dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

6.  **Create a `.env` file:**

    Create a `.env` file in the `backend` directory and copy the content from `.env.example` or modify it with your own credentials:

    ```
    SECRET_KEY="de-5_@2__!@=xd1-891#q7cq(6t$bfbo=i&2lm5(bf_7)lab2eh*("
    DEBUG="true"

    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST="smtp.gmail.com"
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER="example@gmail.com"
    EMAIL_HOST_PASSWORD="xxxxxxxx"
    DEFAULT_FROM_EMAIL="example@gmail.com"
    ```

7.  **Run the database migrations:**

    ```bash
    python manage.py migrate
    ```

8.  **Start the development server:**

    ```bash
    python manage.py runserver
    ```

### For Windows Users

1.  **Clone the repository:**

    ```cmd
    git clone https://github.com/your-username/AmbulanceDispatchSystem.git
    ```

2.  **Navigate to the backend directory:**

    ```cmd
    cd AmbulanceDispatchSystem\backend
    ```

3.  **Create a virtual environment:**

    ```cmd
    python -m venv .venv
    ```

4.  **Activate the virtual environment:**

    ```cmd
    .venv\Scripts\activate
    ```

5.  **Install the required dependencies:**

    ```cmd
    pip install -r requirements.txt
    ```

6.  **Create a `.env` file:**

    Create a `.env` file in the `backend` directory and copy the content from `.env.example` or modify it with your own credentials:

    ```
    SECRET_KEY="de-5_@2__!@=xd1-891#q7cq(6t$bfbo=i&2lm5(bf_7)lab2eh*("
    DEBUG="true"

    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST="smtp.gmail.com"
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER="example@gmail.com"
    EMAIL_HOST_PASSWORD="xxxxxxxx"
    DEFAULT_FROM_EMAIL="example@gmail.com"
    ```

7.  **Run the database migrations:**

    ```cmd
    python manage.py migrate
    ```

8.  **Start the development server:**

    ```cmd
    python manage.py runserver
    ```
