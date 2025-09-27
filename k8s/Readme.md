## 🚀 Deploying to Kubernetes (k8s)

This project is designed to be deployed to a Kubernetes cluster, following modern cloud-native principles. The manifests provided in the `/k8s` directory define all the necessary resources to run the application in a scalable, resilient, and configurable way.

### Architecture Overview

The deployment architecture consists of the following key components:
-   **Django/Gunicorn Deployment:** Runs the core backend application. Includes liveness and readiness probes for health checking.
-   **Nginx Deployment:** Acts as a reverse proxy, handling incoming traffic and serving static files.
-   **PostgreSQL Database:** (Assumed to be an external managed service like AWS RDS, or a separate stateful deployment).
-   **Kubernetes Job:** A dedicated job to handle database migrations safely before the main application is deployed or updated.
-   **Services:** `ClusterIP` services for internal communication between Nginx and Django.
-   **Ingress:** Manages external traffic, routing it to the Nginx service, and handles SSL termination.
-   **Configuration:** `Secrets` are used for sensitive data (e.g., database URL, secret keys) and `ConfigMaps` are used for non-sensitive configuration like the Nginx setup file.
-   **Storage:** A `PersistentVolumeClaim` is used to create a shared volume for static files between the Django and Nginx pods.

### Prerequisites

Before you begin, ensure you have the following:

1.  A running Kubernetes cluster (e.g., Minikube, Docker Desktop, GKE, EKS).
2.  `kubectl` configured to communicate with your cluster.
3.  An **Ingress Controller** installed in your cluster (e.g., Nginx Ingress Controller). This is required for the `Ingress` resource to work.
4.  Your Docker images (`job-board-api` and `job-board-nginx`) built and pushed to a container registry that your cluster can access (e.g., Docker Hub, GCR, ECR).

### File Structure

All Kubernetes manifests are located in the `/k8s` directory:

```
/k8s
├── 01-secret.yml
├── 02-nginx-configmap.yml
├── 03-pvc.yml
├── 04-migration-job.yml
├── 05-django-deployment.yml
├── 06-django-service.yml
├── 07-nginx-deployment.yml
├── 08-nginx-service.yml
└── 09-ingress.yml
```

### Configuration

Before applying the manifests, you must configure the following:

1.  **`/k8s/01-secret.yml`:** Update the `stringData` with your actual production secrets (database URL, Django secret key, etc.). **Note:** For true production, it's better to create secrets from files or use a secret management tool rather than committing base64-encoded values.
2.  **`/k8s/05-django-deployment.yml`:** Change the `image` value to point to your Django application image in your container registry.
3.  **`/k8s/07-nginx-deployment.yml`:** Change the `image` value to point to your Nginx image in your container registry.
4.  **`/k8s/09-ingress.yml`:**
    -   Change the `host` to your domain (e.g., `api.yourdomain.com`).
    -   Update the `secretName` to the name of the Kubernetes secret containing your TLS/SSL certificate. (This is often handled automatically by `cert-manager`).

### Deployment Steps

1.  **Apply the Manifests:**
    Navigate to the root of the project and apply all the configuration files from the `k8s` directory.

    ```bash
    kubectl apply -f k8s/
    ```
    This command will create all the necessary resources in the order specified. The migration job will run first, and upon completion, the deployments will proceed to create the application pods.

2.  **Check Deployment Status:**
    You can monitor the status of your resources using the following commands:

    ```bash
    # Check the status of your pods (they should eventually be 'Running')
    kubectl get pods

    # Check that your services have been created
    kubectl get services

    # Check if the Ingress has been assigned an IP address by the controller
    kubectl get ingress
    ```

3.  **Access Your Application:**
    Once the Ingress is assigned an IP address, you can configure your DNS to point your domain (`api.yourdomain.com`) to this IP. Your application should then be accessible via HTTPS.

### Manifests Breakdown

-   **`01-secret.yml`:** Creates a `Secret` to securely store all sensitive environment variables.
-   **`02-nginx-configmap.yml`:** Creates a `ConfigMap` to hold the `nginx.conf` file, allowing it to be mounted into the Nginx pods.
-   **`03-pvc.yml`:** Creates a `PersistentVolumeClaim`, requesting a persistent disk to be used for storing shared static files.
-   **`04-migration-job.yml`:** Defines a `Job` that runs the `python manage.py migrate` command. This ensures database migrations are applied safely and only once per deployment.
-   **`05-django-deployment.yml`:** Defines the `Deployment` for the main Django application. It manages the lifecycle of the Django pods, ensures the desired number of replicas are running, and includes **liveness and readiness probes** for robust health checking.
-   **`06-django-service.yml`:** Creates a `ClusterIP` `Service`, giving the Django pods a stable internal IP and DNS name (`django