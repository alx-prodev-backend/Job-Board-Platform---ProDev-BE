## ⚙️ Serializers (`api/serializers.py`)

Serializers in this project act as the "translators" between our database models and the JSON format used by the API. They are responsible for converting complex querysets into native Python datatypes that can then be easily rendered into JSON (serialization) and for validating and converting incoming JSON data back into complex types (deserialization).

### `RegisterSerializer`

This serializer is dedicated to handling new user registration.

-   **Purpose:** To validate and create a new `User` instance.
-   **Key Features:**
    -   Accepts `username`, `email`, `password`, and `role`.
    -   The `password` field is `write_only` for security, ensuring it is never exposed in an API response.
    -   It overrides the default `.create()` method to:
        1.  Securely hash the user's password using Django's `create_user()` manager method.
        2.  Conditionally create an associated `Company` or `Profile` instance based on the user's selected `role`.
    -   Requires an additional `company_name` field if the role is `'recruiter'`, enforcing our business logic at the validation stage.

### `UserSerializer`

This serializer is used for safely displaying a user's information, typically after they have authenticated.

-   **Purpose:** To serialize `User` model instances for API responses.
-   **Key Features:**
    -   Exposes non-sensitive fields like `id`, `username`, `email`, and `role`.
    -   Features a dynamic `details` field (using `SerializerMethodField`) which provides nested data relevant to the user's role:
        -   If the user is a `recruiter`, it embeds their company's data using `CompanySerializer`.
        -   If the user is a `job_seeker`, it embeds their profile data using `ProfileSerializer`.
    -   This design makes the `/api/users/me/` endpoint context-aware and highly efficient.

### `CompanySerializer` & `ProfileSerializer`

These are straightforward `ModelSerializer` classes for their respective models.

-   **Purpose:** To serialize `Company` and `Profile` model instances.
-   **Key Features:**
    -   They are used for nesting within the `UserSerializer` to provide rich, relational data in a single API call.
    -   They can also be used for any future API endpoints dedicated to managing company or profile details (e.g., `PUT /api/profile/me/`).
    -   The `ProfileSerializer` uses `depth = 1` to automatically include the string representation of nested objects, such as the names of the user's skills.