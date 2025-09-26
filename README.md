# Job Board Platform - Backend Project

This project is a comprehensive backend application for a job board platform, developed as part of the **Project Nexus** initiative within the **ProDev Backend Program**. It aims to provide all the essential functionalities of a modern job board, focusing on building a robust, secure, and scalable API.

---

## 📜 Table of Contents

- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📊 Database Schema](#-database-schema)
- [📡 API Endpoints](#-api-endpoints)
- [🚀 Getting Started](#-getting-started)
- [⚙️ Environment Variables](#️-environment-variables)
- [📄 License](#-license)

---

## ✨ Key Features

-   **Authentication System:** Secure user registration and login using JWT (JSON Web Tokens).
-   **Role-Based Access Control (RBAC):** Clear separation of permissions between "Job Seekers" and "Recruiters".
-   **Company Profile Management:** Recruiters can create and manage their company profiles.
-   **Job Posting Management (CRUD):** Recruiters can create, read, update, and delete job postings.
-   **Advanced Job Search & Filtering:** Job seekers can search for jobs and filter them based on various criteria (title, location, job type, etc.).
-   **Easy Application System:** Job seekers can easily apply for jobs.
-   **Application Tracking:** Recruiters can review and update the status of job applications (e.g., viewed, accepted, rejected).
-   **User Profile Management:** Job seekers can create and update their professional profiles, including skills and resume links.

---

## 🛠️ Tech Stack

-   **Programming Language:** Python 3.10+
-   **Framework:** Django & Django REST Framework (DRF)
-   **Database:** PostgreSQL
-   **Authentication:** `djangorestframework-simplejwt`
-   **Environment Management:** `python-decouple` or `python-dotenv`

---

## 📊 Database Schema

The database is designed to be relational and scalable. It includes tables for users, companies, jobs, applications, profiles, and skills. Relationships (One-to-One, One-to-Many, and Many-to-Many) are used to ensure data integrity and efficiency.

For a detailed view of the schema, please refer to the ERD documentation.

---

## 📡 API Endpoints

The API is built following RESTful principles.

### Auth & Users

-   `POST /api/auth/register/`: Register a new user (job_seeker or recruiter).
-   `POST /api/auth/login/`: Log in to receive an access and refresh token pair.
-   `POST /api/auth/token/refresh/`: Refresh an expired access token.
-   `GET /api/users/me/`: Get the profile of the currently authenticated user.

### Companies

-   `POST /api/companies/`: Create a new company profile (Recruiters only).
-   `GET /api/companies/my-company/`: Retrieve the company profile linked to the current recruiter.
-   `PUT /api/companies/my-company/`: Update the company profile (Owner only).

### Jobs

-   `GET /api/jobs/`: List all available jobs with search and filtering capabilities.
-   `GET /api/jobs/{id}/`: Retrieve details for a specific job.
-   `POST /api/jobs/`: Create a new job posting (Recruiters only).
-   `PUT /api/jobs/{id}/`: Update a job posting (Creator only).
-   `DELETE /api/jobs/{id}/`: Delete a job posting (Creator only).

### Applications

-   `POST /api/jobs/{id}/apply/`: Apply for a specific job (Job Seekers only).
-   `GET /api/applications/`: List applications. (Job Seekers see their own; Recruiters see applications for their company's jobs).
-   `GET /api/applications/{id}/`: Retrieve details for a specific application.
-   `PATCH /api/applications/{id}/`: Update the status of an application (Recruiters only).

### Profiles

-   `GET /api/profile/me/`: Retrieve the personal profile of the current user (Job Seekers only).
-   `PUT /api/profile/me/`: Create or fully update the user's personal profile (Job Seekers only).

---

## 🚀 Getting Started

Follow these steps to set up and run the project on your local machine.

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Create a new file named `.env` in the project's root directory.
    -   Copy the contents from `.env.example` into your new `.env` file.
    -   Fill in the required values (see the section below).

5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

---

## ⚙️ Environment Variables

Your `.env` file should contain the following variables:

```env
# Django Settings
SECRET_KEY='your-strong-secret-key'
DEBUG=True

# Database Settings (PostgreSQL Example)
DATABASE_URL='postgres://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>'

# JWT Settings
JWT_SECRET_KEY='your-jwt-secret-key-for-signing'
```

---

## 📄 License

This project is licensed under the ALX ProDev . See the `ALX ProDev` file for more details.