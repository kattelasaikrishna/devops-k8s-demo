# DevOps Kubernetes CI/CD Challenge

Minimal production-style stack:
- Flask REST API
- PostgreSQL dependency
- Docker containerization
- Kubernetes on Minikube
- GitHub Actions CI/CD using a self-hosted Linux runner
- Readiness/liveness probes
- PersistentVolumeClaim for PostgreSQL
- Intentional database connectivity failure for live debugging

## Main endpoints
- `/` application information
- `/visits` increments a PostgreSQL-backed visit counter
- `/health/live` process liveness
- `/health/ready` database-aware readiness
