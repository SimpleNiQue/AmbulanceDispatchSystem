
# Ambulance Dispatch System Documentation

This document provides a comprehensive overview of the Ambulance Dispatch System, a Django-based application designed to manage and dispatch ambulances for emergency requests.

## 1. Project Overview

The Ambulance Dispatch System is a web-based platform that connects users in need of emergency medical assistance with available ambulances. The system is designed to be used by patients, ambulance drivers, and hospital administrators.

### 1.1. Key Features

*   **User Management:** The system supports different user roles, including patients, ambulance drivers, and hospital administrators.
*   **Ambulance Management:** Hospital administrators can add, update, and manage ambulances in the system.
*   **Emergency Request Management:** Patients can create emergency requests, which are then assigned to the nearest available ambulance.
*   **Real-time Location Tracking:** The system tracks the real-time location of ambulances, allowing for efficient dispatching.
*   **Hospital Management:** The system allows for the management of hospitals and their associated ambulances.

### 1.2. Technology Stack

*   **Backend:** Django, Django REST Framework
*   **Database:** SQLite (for development), PostgreSQL (recommended for production)
*   **Authentication:** Simple JWT (JSON Web Token)
*   **Real-time Communication:** (Not yet implemented, but planned for future development)

## 2. Data Models

The system is composed of the following data models:

### 2.1. User App

*   **User:** Represents a user of the system. It includes fields for email, password, first name, last name, and role.
*   **Profile:** Represents a user's profile, which includes additional information such as gender and a profile picture.

### 2.2. Ambulance App

*   **Ambulance:** Represents an ambulance in the system. It includes fields for status (available, busy, etc.), ambulance type (BLS, ALS, etc.), and the hospital it belongs to.
*   **AmbulanceLocation:** Represents the real-time location of an ambulance.

### 2.3. Hospital App

*   **Hospital:** Represents a hospital in the system. It includes fields for name, contact number, and address.
*   **HospitalLocation:** Represents the location of a hospital.

### 2.4. Emergency App

*   **EmergencyRequest:** Represents an emergency request made by a user. It includes fields for the user who made the request, the assigned ambulance, the severity of the emergency, and whether the request has been resolved.
*   **EmergencyRequestLocation:** Represents the location of an emergency.

## 3. API Endpoints

The system exposes the following API endpoints:

### 3.1. User API

*   `/v1/users/register/`: Registers a new user.
*   `/v1/users/login/`: Logs in a user and returns a JWT token.
*   `/v1/users/profile/`: Gets and updates the user's profile.

### 3.2. Ambulance API

*   `/v1/ambulances/`: Lists all ambulances.
*   `/v1/ambulances/<id>/`: Gets, updates, and deletes a specific ambulance.
*   `/v1/ambulances/<id>/location/`: Gets and updates the location of a specific ambulance.

### 3.3. Hospital API

*   `/v1/hospitals/`: Lists all hospitals.
*   `/v1/hospitals/<id>/`: Gets, updates, and deletes a specific hospital.
*   `/v1/hospitals/<id>/location/`: Gets and updates the location of a specific hospital.

### 3.4. Emergency API

*   `/v1/emergencies/`: Creates a new emergency request.
*   `/v1/emergencies/<id>/`: Gets, updates, and deletes a specific emergency request.
*   `/v1/emergencies/<id>/location/`: Gets and updates the location of a specific emergency.

## 4. In progress

The following features are still in progress:

*   **Real-time Ambulance Tracking:** Implement real-time Ambulance location Tracking.

*   **Response Analysis** 