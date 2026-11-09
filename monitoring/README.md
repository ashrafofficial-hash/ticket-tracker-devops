\# Kubernetes Monitoring – Prometheus \& Grafana



\## Overview



Prometheus and Grafana monitor the Kubernetes infrastructure running the IT Service Desk Ticket Tracker application.



\## Technology Stack



\- Kubernetes (kind)

\- Helm

\- Prometheus

\- Grafana

\- kube-state-metrics



\## Architecture



\- Prometheus collects metrics from Kubernetes nodes, API server, cAdvisor, CoreDNS and kube-state-metrics.

\- Grafana uses Prometheus as its data source.

\- Both services run in the monitoring namespace.

\- Persistent volumes retain monitoring data.



\## Prometheus Configuration



\- Helm chart: 29.45.0

\- Data retention: 7 days

\- Persistent storage: 2 GiB

\- CPU request: 100m

\- Memory request: 256 MiB

\- CPU limit: 500m

\- Memory limit: 512 MiB



\## Grafana Configuration



\- Helm chart: 14.4.0

\- Persistent storage: 1 GiB

\- CPU request: 100m

\- Memory request: 128 MiB

\- CPU limit: 500m

\- Memory limit: 512 MiB

\- Prometheus configured as the default data source.

\- Admin credentials stored in a Kubernetes Secret.



\## Access



Prometheus: http://localhost:9090



Grafana: http://localhost:3000



Grafana username: admin



\## Grafana Dashboard



Dashboard: IT Ticket Tracker – DevOps Monitoring Dashboard



Panels:

1\. Prometheus Target Health

2\. Kubernetes Running Pods

3\. Kubernetes Pod CPU Usage

4\. Kubernetes Pod Memory Usage



\## Validation Commands



\- kubectl get pods -n monitoring

\- kubectl get services -n monitoring

\- kubectl get pvc -n monitoring

\- helm list -n monitoring



\## Notes



\- Monitoring runs locally on a kind Kubernetes cluster.

\- Port forwarding must remain active to access the dashboards.

\- The Grafana dashboard was configured through the Grafana UI.

\- The application does not yet expose its own Prometheus /metrics endpoint.

\- Kubernetes Secret values and Terraform state files must not be committed to Git.

\- Production deployments require appropriate secret management and access controls.

