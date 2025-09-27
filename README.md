# Job Board Platform - Backend Project

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.2+-green.svg)](https://www.djangoproject.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This project is a comprehensive backend application for a job board platform, developed as part of the **Project Nexus** initiative. It is designed as a modern, cloud-native application, containerized with Docker and ready for orchestration with Kubernetes. The API is robust, secure, and scalable, providing all the essential functionalities of a modern job board.

---

## 📜 Table of Contents

- [✨ Key Features](#-key-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📂 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [Method 1: Local Python Environment](#method-1-local-python-environment)
  - [Method 2: Using Docker Compose (Recommended)](#method-2-using-docker-compose-recommended)
- [📡 API Endpoints](#-api-endpoints)
- [🚀 Deploying to Kubernetes (k8s)](#-deploying-to-kubernetes-k8s)
- [⚙️ Environment Variables](#️-environment-variables)
- [📄 License](#-license)

---

## ✨ Key Features

-   **Authentication System:** Secure user registration and login using JWT (JSON Web Tokens).
-   **Role-Based Access Control (RBAC):** Clear separation of permissions between "Job Seekers" and "Recruiters".
-   **Full CRUD Functionality:** Complete create, read, update, and delete operations for Company Profiles and Job Postings.
-   **Advanced Application System:** Allows job seekers to easily apply for jobs and recruiters to track applications.
-   **Production-Ready Practices:**
    -   **API Throttling:** Rate limiting to prevent abuse and ensure fair usage.
    -   **Containerized:** Fully containerized with Docker for consistency across all environments.
    -   **Orchestration-Ready:** Includes a full suite of Kubernetes manifests for scalable deployment.

---

## 🛠️ Tech Stack

This project leverages a modern, robust tech stack suitable for scalable web applications.

| Category                      | Technology                                                                |
| ----------------------------- | ------------------------------------------------------------------------- |
| **Backend** | Python 3.11+, Django, Django REST Framework |
| **Application Server** | Gunicorn |
| **Database** | PostgreSQL |
| **Authentication** | djangorestframework-simplejwt |
| **Containerization** | Docker, Docker Compose |
| **Web Server / Reverse Proxy**| Nginx |
| **Deployment / Orchestration**| Kubernetes (k8s) |

---

## 📂 Project Structure

The project is organized into logical components for clarity and maintainability.

```
/
├── api/                # Core Django app (Models, Views, Serializers, etc.)
├── job_board_project/  # Django project settings and main URL configuration
├── k8s/                # Kubernetes manifest files for deployment
├── nginx/              # Nginx Dockerfile and configuration
├── .env                # Local environment variables (not committed)
├── docker-compose.yml  # Defines services for local Docker development
├── Dockerfile          # Dockerfile for the Django application
└── requirements.txt    # Python dependencies
```

---

## 🚀 Getting Started

You can run this project in two ways. Using Docker is recommended for an experience that closely mirrors production.

### Method 1: Local Python Environment

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd <repository-folder>
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    # venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    -   Create a `.env` file and populate it based on the `Environment Variables` section below.

5.  **Apply database migrations:**
    ```bash
    python manage.py migrate
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be available at `http://127.0.0.1:8000/`.

### Method 2: Using Docker Compose (Recommended)

This is the easiest and most reliable way to get the project running with all its services.

**Prerequisites:**
-   Docker
-   Docker Compose

**Steps:**

1.  **Clone the repository.**
2.  **Set up environment variables:**
    -   Create a `.env` file in the project root and populate it with the necessary variables (see section below). `docker-compose` will automatically load this file.
3.  **Build and run the containers:**
    ```bash
    docker-compose up --build
    ```
    This command will build the Docker images for both the Django app and Nginx, start the containers, run database migrations, and launch the Gunicorn server. The application will be accessible at `http://localhost/`.

---

## 📡 API Endpoints

The API is built following RESTful principles. See the project's documentation (e.g., Postman collection or Swagger UI if integrated) for detailed request/response examples.

| HTTP Method(s)              | URL Endpoint                | Description                                                                     | Permissions                               |
| --------------------------- | --------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------- |
| **POST** | `/api/auth/register/`       | Registers a new user (either a 'job_seeker' or a 'recruiter').                  | `AllowAny` (Public)                       |
| **POST** | `/api/auth/token/`          | Authenticates a user and returns a JWT token pair.                              | `AllowAny` (Public)                       |
| **GET**, **PUT**, **PATCH** | `/api/users/me/`            | Allows an authenticated user to view or update their own profile details.       | `IsAuthenticated` (Requires Login)        |
| **GET**, **POST** | `/api/jobs/`                | `GET`: Lists all available jobs. <br> `POST`: Creates a new job posting.      | `GET`: `AllowAny` <br> `POST`: `IsRecruiter` |
| **GET**, **PUT**, **DELETE** | `/api/jobs/{id}/`             | `GET`: Retrieves a specific job. <br> `PUT`/`DELETE`: Updates/deletes a job. | `GET`: `AllowAny` <br> `PUT`/`DELETE`: `IsRecruiter` |
| ...                         | ...                         | *Additional endpoints for applications, profiles, etc.* | ...                                       |

---

## 🚀 Deploying to Kubernetes (k8s)

This project is ready for deployment to a Kubernetes cluster. The manifests provided in the `/k8s` directory define all the necessary resources to run the application in a scalable and resilient way.

For full deployment instructions and an explanation of the architecture, please see the dedicated [Kubernetes Deployment Guide](./k8s/README.md). *(It's good practice to move the very long k8s section to its own README inside the k8s folder)*.

---

## ⚙️ Environment Variables

Create a `.env` file in the project root and add the following variables:

```env
# Django Settings
SECRET_KEY='your-strong-secret-key-goes-here'
DEBUG=True # Set to False in production

# Database Settings (PostgreSQL Example)
DATABASE_URL='postgres://user:password@host:port/dbname'

# JWT Settings (if needed by your configuration)
# JWT_SECRET_KEY='your-jwt-secret-key-for-signing'
```

---

## 📄 License

This project is licensed under the ALX ProDev. See the `ALX ProDev` file for more details.