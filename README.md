# IT Service Desk Ticket Tracker - DevOps Project

A containerized IT Service Desk Ticket Management REST API built with Python and Flask, deployed on Kubernetes, backed by PostgreSQL, and supported by automated CI, Infrastructure as Code, and monitoring.

**GitHub Repository:** https://github.com/ashrafofficial-hash/ticket-tracker-devops

## Project Overview

This project simulates a real-world IT Service Desk ticket management system. Employees can create and manage support tickets for incidents such as VPN connectivity failures, system issues, and application access problems.

The project demonstrates practical DevOps workflows, including:

- Application development and automated testing.
- Docker containerization and PostgreSQL integration.
- Kubernetes deployment and persistent storage.
- CI automation and container image publishing.
- Terraform-based Kubernetes resource management.
- Prometheus metrics collection and Grafana dashboards.

## Architecture

```text
Developer
   |
   v
GitHub Repository
   |
   v
GitHub Actions
   |
   +---- Automated Tests
   |
   +---- Docker Image Build
              |
              v
      GitHub Container Registry
              |
              v
       Kubernetes (kind)
              |
       +------+------+
       |             |
       v             v
   Flask API     PostgreSQL
       |             |
       |          Persistent
       |           Storage
       |
       v
   Health Check

Terraform
   |
   v
Kubernetes ResourceQuota

Prometheus
   |
   v
Kubernetes Monitoring Targets
   |
   v
Grafana Dashboard
```

## Technology Stack

| Category | Technology |
|---|---|
| Backend | Python, Flask |
| Database | PostgreSQL 16 |
| ORM | Flask-SQLAlchemy |
| Testing | Pytest |
| Containerization | Docker |
| Container Orchestration | Kubernetes |
| Local Kubernetes | kind |
| CI/CD | GitHub Actions |
| Container Registry | GitHub Container Registry |
| Infrastructure as Code | Terraform |
| Kubernetes Package Management | Helm |
| Monitoring | Prometheus |
| Visualization | Grafana |
| Version Control | Git, GitHub |
| Operating System | Windows 11 |

## Application Features

- Create IT support tickets.
- Retrieve all tickets.
- Retrieve individual tickets.
- Update ticket status.
- Delete tickets.
- Validate ticket priority and required fields.
- Health-check endpoint.
- PostgreSQL database persistence.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Application health |
| POST | `/tickets` | Create ticket |
| GET | `/tickets` | List tickets |
| GET | `/tickets/<id>` | Get ticket details |
| PUT | `/tickets/<id>` | Update ticket status |
| DELETE | `/tickets/<id>` | Delete ticket |

### Example Ticket Request

```json
{
  "title": "VPN connection failure",
  "description": "Employee unable to connect to corporate VPN",
  "priority": "P1"
}
```

## Docker and PostgreSQL

Start the application and PostgreSQL database using Docker Compose:

```powershell
docker compose up -d --build
```

Check running containers:

```powershell
docker compose ps
```

Test the API:

```powershell
Invoke-RestMethod http://localhost:5001/health
```

## Kubernetes Deployment

The application was deployed locally using kind.

Create the cluster:

```powershell
kind create cluster --name ticket-tracker-cluster
```

Create the namespace:

```powershell
kubectl create namespace ticket-tracker
```

Create the database credentials as a Kubernetes Secret using your own generated credentials. Do not commit live credentials to Git.

Deploy PostgreSQL:

```powershell
kubectl apply -f .\k8s\postgres.yaml
```

Deploy the API:

```powershell
kubectl apply -f .\k8s\ticket-tracker.yaml
```

Verify Kubernetes resources:

```powershell
kubectl get pods -n ticket-tracker
kubectl get services -n ticket-tracker
kubectl get pvc -n ticket-tracker
```

Access the API:

```powershell
kubectl port-forward service/ticket-tracker-service 5002:80 -n ticket-tracker
```

In another PowerShell window:

```powershell
Invoke-RestMethod http://localhost:5002/health
```

Verify PostgreSQL records:

```powershell
kubectl exec deployment/postgres -n ticket-tracker -- psql -U ticketuser -d ticketdb -c "SELECT id, title, priority, status FROM ticket;"
```

### Kubernetes Features

- Deployments for Flask API and PostgreSQL.
- ClusterIP Services for internal communication.
- Kubernetes Secret for database credentials.
- PersistentVolumeClaim for PostgreSQL data.
- Readiness and liveness probes.
- CPU and memory requests and limits.
- Dedicated application namespace.

## Terraform Infrastructure Management

Terraform manages Kubernetes infrastructure through Infrastructure as Code.

The HashiCorp Kubernetes provider connects to the existing local kind cluster and manages a ResourceQuota in the `ticket-tracker` namespace.

**Configuration:** `terraform/main.tf`

| Configuration | Value |
|---|---|
| Provider | HashiCorp Kubernetes |
| Provider version | 2.38.0 |
| Kubernetes context | kind-ticket-tracker-cluster |
| Managed resource | ticket-tracker-quota |

### ResourceQuota

| Resource | Configured Limit |
|---|---:|
| Pods | 10 |
| Persistent Volume Claims | 2 |
| Requested Storage | 2Gi |

Run Terraform commands from the `terraform` directory:

```powershell
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
```

Terraform manages the Kubernetes ResourceQuota, while Kubernetes YAML manifests manage the API and PostgreSQL deployments.

Terraform state and provider directories are excluded from Git. The provider lock file is committed for consistent provider versions.

## CI/CD Pipeline

GitHub Actions is configured to:

- Run automated application tests.
- Validate application changes.
- Build Docker images.
- Publish the container image to GitHub Container Registry when changes are pushed to the `main` branch.

**Published container image:**

`ghcr.io/ashrafofficial-hash/ticket-tracker-api:latest`

The local kind deployment is managed separately from the hosted GitHub Actions workflow.

## Monitoring with Prometheus and Grafana

Prometheus and Grafana are deployed to the local Kubernetes cluster using Helm.

### Prometheus

- Kubernetes monitoring target discovery.
- Scraping of available Kubernetes metrics endpoints.
- Seven-day data retention.
- Persistent storage using a 2Gi PVC.
- Resource requests and limits.

### Grafana

A monitoring dashboard named **IT Ticket Tracker - DevOps Monitoring Dashboard** was created with four panels:

1. Prometheus Target Health.
2. Kubernetes Running Pods.
3. Kubernetes Pod CPU Usage.
4. Kubernetes Pod Memory Usage.

Prometheus is configured as the Grafana data source.

### Access Monitoring

Start Prometheus port forwarding:

```powershell
kubectl port-forward service/prometheus-server 9090:80 -n monitoring
```

Open:

`http://localhost:9090`

Start Grafana port forwarding in another PowerShell window:

```powershell
kubectl port-forward service/grafana 3000:80 -n monitoring
```

Open:

`http://localhost:3000`

Grafana credentials are stored in a Kubernetes Secret. The local dashboard is configured through the Grafana UI and is not automatically provisioned from the repository.

**Monitoring configuration and instructions:** [monitoring/README.md](monitoring/README.md)

**Note:** The current monitoring setup collects Kubernetes and infrastructure metrics. The Flask API does not yet expose its own Prometheus `/metrics` endpoint.

## Testing

Automated tests are implemented using Pytest.

Run:

```powershell
python -m pytest -v
```

The project currently has six automated tests covering health checks, ticket creation, retrieval, validation, updates, and deletion.

## Repository Structure

```text
ticket-tracker-devops/
|
|-- .github/
|   |-- workflows/
|
|-- app/
|   |-- __init__.py
|   |-- extensions.py
|   |-- main.py
|   |-- models.py
|   |-- routes.py
|
|-- tests/
|   |-- test_health.py
|
|-- k8s/
|   |-- postgres.yaml
|   |-- ticket-tracker.yaml
|
|-- terraform/
|   |-- main.tf
|   |-- .terraform.lock.hcl
|
|-- monitoring/
|   |-- prometheus-values.yaml
|   |-- grafana-values.yaml
|   |-- README.md
|
|-- docker/
|
|-- compose.yaml
|-- Dockerfile
|-- requirements.txt
|-- .env.example
|-- .gitignore
|-- README.md
```

## Future Enhancements

- Add application-level Prometheus instrumentation.
- Configure Grafana alerting and notification rules.
- Improve production application serving and security.
- Explore deployment to a cloud Kubernetes environment such as AWS.

## Author

**Ashraf G**

GitHub: https://github.com/ashrafofficial-hash

Project: https://github.com/ashrafofficial-hash/ticket-tracker-devops
