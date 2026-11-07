# IT Service Desk Ticket Tracker - DevOps Project



A containerized IT Service Desk Ticket Management REST API deployed using Docker and Kubernetes, with PostgreSQL persistence and automated CI/CD using GitHub Actions.



## Project Overview



This project simulates a real-world IT Service Desk ticket management system. Employees can create support tickets for incidents such as VPN connectivity failures, system issues, and application access problems.



The project demonstrates practical DevOps skills, including containerization, database orchestration, Kubernetes deployment, CI automation, and container image publishing.



## Architecture



```text

&#x20;                Developer

&#x20;                    |

&#x20;                    v

&#x20;               GitHub Repo

&#x20;                    |

&#x20;                    v

&#x20;             GitHub Actions

&#x20;              CI Pipeline

&#x20;                    |

&#x20;             Tests and Build

&#x20;                    |

&#x20;                    v

&#x20;            GitHub Container

&#x20;                Registry

&#x20;                    |

&#x20;                    v

&#x20;             Kubernetes

&#x20;              (kind)

&#x20;                    |

&#x20;            API Service

&#x20;                    |

&#x20;             Flask API Pod

&#x20;                    |

&#x20;             PostgreSQL

&#x20;                    |

&#x20;             Persistent

&#x20;                Storage

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

| Version Control | Git, GitHub |

| Operating System | Windows 11 |



## Application Features



\- Create IT support tickets.

\- Retrieve all tickets.

\- Retrieve individual tickets.

\- Update ticket status.

\- Delete tickets.

\- Validate ticket priority and required fields.

\- Health-check endpoint.

\- PostgreSQL database persistence.



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

&#x20; "title": "VPN connection failure",

&#x20; "description": "Employee unable to connect to corporate VPN",

&#x20; "priority": "P1"

}

```



## Docker and PostgreSQL



The application and PostgreSQL database can be started using Docker Compose.



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



### 1. Create Kubernetes cluster



```powershell

kind create cluster --name ticket-tracker-cluster

```



### 2. Create namespace



```powershell

kubectl create namespace ticket-tracker

```



### 3. Create database credentials



Create the Kubernetes Secret using your own generated credentials. Do not commit live credentials to Git.



### 4. Deploy PostgreSQL



```powershell

kubectl apply -f .\\k8s\\postgres.yaml

```



### 5. Deploy Flask API



```powershell

kubectl apply -f .\\k8s\\ticket-tracker.yaml

```



### 6. Verify deployments



```powershell

kubectl get pods -n ticket-tracker

kubectl get services -n ticket-tracker

kubectl get pvc -n ticket-tracker

```



### 7. Access the application



```powershell

kubectl port-forward service/ticket-tracker-service 5002:80 -n ticket-tracker

```



Open another PowerShell window:



```powershell

Invoke-RestMethod http://localhost:5002/health

```



### 8. Verify PostgreSQL records



```powershell

kubectl exec deployment/postgres -n ticket-tracker -- psql -U ticketuser -d ticketdb -c "SELECT id, title, priority, status FROM ticket;"

```



## Kubernetes Features Implemented



\- Deployment resources for Flask API and PostgreSQL.

\- ClusterIP Services for internal communication.

\- Kubernetes Secret for database credentials.

\- PersistentVolumeClaim for PostgreSQL data.

\- Readiness and liveness probes.

\- CPU and memory requests and limits.

\- Dedicated Kubernetes namespace.



## CI/CD Pipeline



GitHub Actions is configured to:



\- Run automated application tests.

\- Validate application changes.

\- Build and publish the Docker image to GitHub Container Registry.

\- Publish the image when changes are pushed to the main branch.



Container image:



`ghcr.io/ashrafofficial-hash/ticket-tracker-api:latest`



## Testing



Automated tests are implemented using Pytest.



```powershell

python -m pytest -v

```



The application has six automated tests covering health checks, ticket creation, retrieval, validation, updates, and deletion.



## Repository Structure



```text

ticket-tracker-devops/

â”‚

â”œâ”€â”€ app/

â”‚   â”œâ”€â”€ \_\_init\_\_.py

â”‚   â”œâ”€â”€ extensions.py

â”‚   â”œâ”€â”€ main.py

â”‚   â”œâ”€â”€ models.py

â”‚   â””â”€â”€ routes.py

â”‚

â”œâ”€â”€ tests/

â”‚   â””â”€â”€ test\_health.py

â”‚

â”œâ”€â”€ k8s/

â”‚   â”œâ”€â”€ postgres.yaml

â”‚   â””â”€â”€ ticket-tracker.yaml

â”‚

â”œâ”€â”€ .github/

â”‚   â””â”€â”€ workflows/

â”‚

â”œâ”€â”€ Dockerfile

â”œâ”€â”€ docker-compose.yml

â”œâ”€â”€ requirements.txt

â”œâ”€â”€ .env.example

â””â”€â”€ README.md

```



## Future Enhancements



\- Terraform infrastructure provisioning.

\- Prometheus metrics collection.

\- Grafana monitoring dashboards.

\- Kubernetes resource monitoring.

\- Cloud deployment on AWS.

\- Enhanced production deployment and security.



## Author



\*\*Ashraf G\*\*



GitHub: https://github.com/ashrafofficial-hash



Project: https://github.com/ashrafofficial-hash/ticket-tracker-devops
