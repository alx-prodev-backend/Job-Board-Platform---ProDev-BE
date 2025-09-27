## 🌐 API URL Structure & Endpoints

The API's URL structure is designed to be logical, predictable, and RESTful. It follows Django's best practice of using a two-tiered routing system: a main project-level router and a dedicated app-level router for modularity.

-   **Project-Level Routing (`job_board_project/urls.py`):** This file acts as the primary entry point for all traffic. It directs any request with the `/api/` prefix to the `api` app's dedicated URL configuration for handling.

-   **App-Level Routing (`api/urls.py`):** This is where all specific API endpoints are defined. It uses a combination of DRF's `DefaultRouter` to automatically generate URLs for the `JobViewSet` and Django's `path()` function for standalone views like registration and user profile management.

### Endpoint Summary

| HTTP Method(s)              | URL Endpoint                | Description                                                                     | Permissions                               |
| --------------------------- | --------------------------- | ------------------------------------------------------------------------------- | ----------------------------------------- |
| **POST** | `/api/auth/register/`       | Registers a new user (either a 'job_seeker' or a 'recruiter').                  | `AllowAny` (Public)                       |
| **POST** | `/api/auth/login/`          | *Standard JWT endpoint to authenticate a user and receive access/refresh tokens.* | `AllowAny` (Public)                       |
| **GET**, **PUT**, **PATCH** | `/api/users/me/`            | Allows an authenticated user to view or update their own profile details.       | `IsAuthenticated` (Requires Login)        |
| **GET**, **POST** | `/api/jobs/`                | `GET`: Lists all available jobs. <br> `POST`: Creates a new job posting.      | `GET`: `AllowAny` <br> `POST`: `IsRecruiter` |
| **GET**, **PUT**, **DELETE** | `/api/jobs/{id}/`             | `GET`: Retrieves a specific job. <br> `PUT`/`DELETE`: Updates/deletes a job. | `GET`: `AllowAny` <br> `PUT`/`DELETE`: `IsRecruiter` |
| | | | |