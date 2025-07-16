
# Ambulance Dispatch System API

This is the backend API for the Ambulance Dispatch System, a Django-based application designed to manage and dispatch ambulances for emergency requests.

## Table of Contents

- [Project Overview](#project-overview)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [User Management](#user-management)
  - [Hospital Management](#hospital-management)
  - [Ambulance Management](#ambulance-management)
  - [Emergency Management](#emergency-management)
- [Models](#models)
  - [User App](#user-app)
  - [Ambulance App](#ambulance-app)
  - [Hospital App](#hospital-app)
  - [Emergency App](#emergency-app)
- [Setup and Installation](#setup-and-installation)
  - [Linux/Mac O](#linux-mac)
  - [Windows](#windows)
- [Postman link](#postman-link)
- [Dependencies](#dependencies)


## Project Overview

The Ambulance Dispatch System is a robust platform for managing emergency medical services. It allows users to request ambulances, and administrators to manage hospitals, ambulances, and emergency requests. The system is built with a modular architecture, with separate Django apps for each core functionality.

## Project Structure

The project is organized into the following main directories:

- `apps/`: Contains the core Django applications:
  - `user/`: Manages user authentication, profiles, and roles.
  - `hospital/`: Manages hospital information and locations.
  - `ambulance/`: Manages ambulance details, status, and locations.
  - `emergency/`: Handles emergency requests and ambulance dispatching.
- `core/`: Contains the main Django project configuration, including settings and URL routing.
- `utils/`: Contains utility modules and helper functions used across the project.
- `logs/`: Contains log files for debugging and error tracking.
- `static/`: Contains static files (CSS, JavaScript, images).
- `templates/`: Contains Django templates for rendering HTML pages.

## API Endpoints

The API is versioned and accessible under the `/v1/` prefix.

### User Management

- `POST /v1/users/signup/`: Register a new user.
- `POST /v1/users/email/verify/`: Verify a user's email address.
- `POST /v1/users/email/resend/`: Resend the email verification link.
- `POST /v1/users/login/`: Log in a user and obtain an authentication token.
- `POST /v1/users/refresh/`: Refresh the authentication token.
- `POST /v1/users/logout/`: Log out a user.
- `GET /v1/users/password-reset/<uidb64>/<token>/`: Check the validity of a password reset token.
- `POST /v1/users/password-reset/confirm/`: Set a new password after a password reset.
- `POST /v1/users/reset-password/validate`: Validate an OTP for password reset.
- `POST /v1/users/reset-password`: Request an OTP for password reset.
- `GET /v1/users/`: Get a list of users.

### Hospital Management

- `GET /v1/hospitals/`: Get a list of all hospitals.
- `POST /v1/hospitals/`: Create a new hospital.
- `GET /v1/hospitals/{id}/`: Get details of a specific hospital.
- `PUT /v1/hospitals/{id}/`: Update details of a specific hospital.
- `DELETE /v1/hospitals/{id}/`: Delete a hospital.

### Ambulance Management

- `GET /v1/ambulance/`: Get a list of all ambulances.
- `POST /v1/ambulance/`: Create a new ambulance.
- `GET /v1/ambulance/{id}/`: Get details of a specific ambulance.
- `PUT /v1/ambulance/{id}/`: Update details of a specific ambulance.
- `DELETE /v1/ambulance/{id}/`: Delete an ambulance.

### Emergency Management

- `GET /v1/emergency-requests/`: Get a list of all emergency requests.
- `POST /v1/emergency-requests/`: Create a new emergency request.
- `GET /v1/emergency-requests/{id}/`: Get details of a specific emergency request.
- `PUT /v1/emergency-requests/{id}/`: Update details of a specific emergency request.
- `DELETE /v1/emergency-requests/{id}/`: Delete an emergency request.

## Models

### User App

- **User**: Extends the default Django `AbstractUser` model with additional fields like `is_admin`, `role`, and `is_verified`.
- **Profile**: A one-to-one model with the `User` model to store additional user profile information like `gender` and `profile_picture`.

### Ambulance App

- **Ambulance**: Stores information about each ambulance, including its `status`, `ambulance_type`, `hospital`, and `busy_until` timestamp.
- **AmbulanceLocation**: Stores the real-time location of each ambulance with `latitude` and `longitude`.

### Hospital App

- **Hospital**: Stores information about each hospital, including its `name`, `contact_number`, and `address`.
- **HospitalLocation**: Stores the location of each hospital with `latitude` and `longitude`.

### Emergency App

- **EmergencyRequest**: Represents an emergency request made by a user, including the `user`, `ambulance` assigned, `severity` level, and `is_resolved` status.
- **EmergencyRequestLocation**: Stores the location of the emergency with `latitude` and `longitude`.

## Setup and Installation
### Linux/Mac OS

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SimpleNiQue/AmbulanceDispatchSystem.git
    ```

2.  **Navigate to the backend directory**
    ```bash
    cd AmbulanceDispatchSystem/backend
    ```

3.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
4. **Activate the virtual environment**
    ```bash
    source .venv/bin/activate
    ```
5.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Create a `.env` file** from the `.env.example` and fill in the required environment variables.(For testing purposes and simplicity, copy and paste this values below)
    ```bash
    SECRET_KEY="django-insecure-5_@2__!@=xd1-891#q7cq(6t$bfbo=i&2lm5(bf_7)lab2eh*("
    DEBUG="true"

    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST="smtp.gmail.com"
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER="simpleneek@gmail.com"
    EMAIL_HOST_PASSWORD="rpewmcchitpgraiz"
    DEFAULT_FROM_EMAIL="simpleneek@gmail.com"

    ```
7.  **Create database migrations:**
    ```bash
    python manage.py makemigrations
    ```

8.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
9.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

### Windows

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/SimpleNiQue/AmbulanceDispatchSystem.git
    ```

2.  **Navigate to the backend directory**
    ```bash
    cd AmbulanceDispatchSystem\backend
    ```

3.  **Create a virtual environment:**
    ```bash
    python -m venv .venv
    ```
4. **Activate the virtual environment**
    ```bash
    .venv\Scripts\activate
    ```
5.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
6.  **Create a `.env` file** from the `.env.example` and fill in the required environment variables.(For testing purposes and simplicity, copy and paste this values below)
    ```bash
    SECRET_KEY="django-insecure-5_@2__!@=xd1-891#q7cq(6t$bfbo=i&2lm5(bf_7)lab2eh*("
    DEBUG="true"

    EMAIL_BACKEND="django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST="smtp.gmail.com"
    EMAIL_PORT=587
    EMAIL_USE_TLS=True
    EMAIL_HOST_USER="simpleneek@gmail.com"
    EMAIL_HOST_PASSWORD="rpewmcchitpgraiz"
    DEFAULT_FROM_EMAIL="simpleneek@gmail.com"

    ```
7.  **Create database migrations:**
    ```bash
    python manage.py makemigrations
    ```

8.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
9.  **Start the development server:**
    ```bash
    python manage.py runserver
    ```

## Postman link
- https://simple-r.postman.co/workspace/Team-Workspace~90ab07f6-6cf7-448d-8511-1d9f81c02928/collection/20874435-a6605897-6bc8-4588-8620-536211391ef3?action=share&creator=20874435&active-environment=20874435-3189fceb-205f-4000-8ee0-ea9ab5b20072

## Dependencies
- `Django==5.2.4`
- `django-cors-headers==4.7.0`
- `django-environ==0.12.0`
- `djangorestframework==3.16.0`
- `djangorestframework_simplejwt==5.5.0`
- `pillow==11.3.0`
- `PyJWT==2.9.0`
