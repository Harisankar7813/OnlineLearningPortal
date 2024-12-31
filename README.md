# Project Name: Booking Management System

## Overview

The Booking Management System is a web application that allows users to book courses and manage their bookings. The application provides features such as user registration, login, and booking management. The backend is powered by Flask (Python), and the frontend uses HTML, CSS, and JavaScript. The database is managed using PHPMyAdmin (via XAMPP) with MySQL.

---

## Technologies Used

### Backend

- **Flask (Python):** A lightweight web framework for backend development.
- **Flask Extensions:**
  - Flask-MySQLdb: For database connection.
  - Flask-Bcrypt: For password hashing and security.
  - Flask-WTF: For form handling and validation.
  - Flask-Session: To manage user sessions.

### Frontend

- **HTML & CSS:** For creating the UI.
- **JavaScript:** For handling client-side interactivity and API integration.

### Database

- **XAMPP Server:**
  - Apache for hosting.
  - PHPMyAdmin for managing the MySQL database.
- **Database Details:**
  - Database Name: `mydatabase`
  - Tables: `users`, `booking`

---

## Requirements

### Software

1. Python 3.x
2. XAMPP with Apache and PHPMyAdmin
3. Browser (e.g., Chrome, Firefox)

### Python Packages

Install the required packages using the following command:

```bash
pip install -r requirements.txt
```

#### Requirements File

- Flask
- Flask-MySQLdb
- Flask-Bcrypt
- Flask-WTF
- Flask-Session

---

## Features

### 1. User Authentication

- **Login:**
  - Secure login with hashed passwords.
  - Session management to ensure users stay logged in.
- **Signup:**
  - Registration form with validation.
  - Prevent duplicate emails during registration.

### 2. Booking Management

- **Dashboard:**
  - Displays all existing bookings for the logged-in user.
  - Booking details include course name, trainee name, date, and time slot.
- **Create Bookings:**
  - Allows users to select a course, trainee, date, and time slot.
  - Validates that all fields are filled before submission.
- **Edit Bookings:**
  - Placeholder functionality to allow future enhancements for editing bookings.

### 3. Backend APIs

- `/login`: Allows users to log in with their registered credentials.

- `/signup`: Handles user registration and stores user details securely.

- `/dashboard`: Displays user-specific details and existing bookings after login.

- `/book`: Handles booking submissions.

- `/get_bookings`: Fetches all bookings for the logged-in user.

---

## Database Structure

### 1. `users` Table

| Column Name | Data Type         | Description            |
| ----------- | ----------------- | ---------------------- |
| id          | INT (Primary Key) | Unique user ID.        |
| name        | VARCHAR(100)      | Full name of the user. |
| email       | VARCHAR(100)      | User email address.    |
| password    | VARCHAR(255)      | Hashed password.       |

### 2. `booking` Table

| Column Name   | Data Type         | Description                |
| ------------- | ----------------- | -------------------------- |
| id            | INT (Primary Key) | Unique booking ID.         |
| user\_id      | INT (Foreign Key) | Related to ID of the user. |
| course        | VARCHAR(100)      | Name of the course booked. |
| trainee       | VARCHAR(100)      | Name of the trainee.       |
| booking\_date | DATE              | Date of the booking.       |
| slot          | VARCHAR(50)       | Time slot of the booking.  |

---

## Installation and Setup

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd <repository_folder>
   ```

2. Set up the backend:

   - Install Python and required packages.
   - Configure the database connection in the Flask app.

3. Set up the database:

   - Start XAMPP and ensure MySQL is running.
   - Create a database named `mydatabase` in PHPMyAdmin.
   - Import the database schema (SQL file provided).

4. Run the Flask app:

   ```bash
   python sampleapp.py
   ```

5. Access the application:

   - Open a browser and navigate to `http://127.0.0.1:5000/`.

---

## Important Notes

- Ensure XAMPP is running with both Apache and MySQL services active.
- The application assumes a database structure as outlined above. Changes to the database schema must be reflected in the code.
- Passwords are securely hashed using `bcrypt`.

---

## Future Enhancements

- Implement booking edit functionality.
- Add admin-level features for better management.
- Enhance error handling and logging.
- Add support for sending email notifications for bookings.

