
## 🧠 Views & API Logic (`api/views.py`)

The `views.py` file is the brain of the API. It contains the logic that processes incoming HTTP requests, interacts with the database via the `Models`, formats the data using the `Serializers`, and returns the final JSON response.

### Custom Permissions (`api/permissions.py`)

To enforce the application's business rules, a custom permission class was created.

-   **`IsRecruiterOrReadOnly`**:
    -   **Purpose:** To ensure that only users with the `recruiter` role can create, update, or delete job postings.
    -   **Logic:**
        1.  It allows read-only access (using safe methods like `GET`) for all users, including unauthenticated ones. This allows anyone to browse jobs.
        2.  For write methods (`POST`, `PUT`, `DELETE`), it checks that the user is both authenticated and has the `'recruiter'` role.

---

### Authentication & User Management Views

These views handle user registration and profile management.

-   #### `RegisterView` (`POST /api/auth/register/`)
    -   **Purpose:** Handles new user registration.
    -   **Class:** Inherits from `generics.CreateAPIView`, a class-based view designed specifically for creating new objects.
    -   **Permissions:** Uses `permissions.AllowAny` to allow any unauthenticated user to access this endpoint and create an account.

-   #### `ManageUserView` (`GET`, `PUT`, `PATCH /api/users/me/`)
    -   **Purpose:** Allows an authenticated user to view and update their own profile information.
    -   **Class:** Inherits from `generics.RetrieveUpdateAPIView` for reading and updating a single instance.
    -   **Key Logic:** The `get_object` method is overridden to always return `request.user`. This means the view always operates on the currently authenticated user, making the endpoint secure and convenient.
    -   **Permissions:** Uses `permissions.IsAuthenticated` to ensure only logged-in users can access their own data.

---

### Job Board Views

This viewset provides the full CRUD functionality for job postings.

-   #### `JobViewSet` (Handles all actions for `/api/jobs/`)
    -   **Purpose:** To provide a complete set of endpoints for listing, creating, retrieving, updating, and deleting jobs.
    -   **Endpoints Provided:**
        -   `GET /api/jobs/`: Lists all jobs.
        -   `POST /api/jobs/`: Creates a new job.
        -   `GET /api/jobs/{id}/`: Retrieves a single job.
        -   `PUT /api/jobs/{id}/`: Updates a job.
        -   `DELETE /api/jobs/{id}/`: Deletes a job.
    -   **Class:** Inherits from `viewsets.ModelViewSet`, which provides all the above actions with minimal code.
    -   **Permissions:** Uses our custom `IsRecruiterOrReadOnly` permission to protect all write operations.
    -   **Key Logic:** The `perform_create` method is overridden to automatically associate a newly created job with the logged-in recruiter's user account and their registered `Company`. This ensures data integrity and simplifies the API for the frontend client.