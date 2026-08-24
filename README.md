# Devops-project-final

This project demonstrates a minimal end-to-end DevOps pipeline: a long-lived web service, CI that tests/builds/pushes a container image, deployment with Nomad, and log collection into Loki via Promtail.

Name: Your Name
Date: 2026-07-06

Tech Used:
- Git & GitHub
- Python (FastAPI)
- Docker
- GitHub Actions (CI)
- Nomad
- Grafana Loki + Promtail

Architecture Overview
- `hello.py` — FastAPI application exposing `/` and `/health`.
- `Dockerfile` — builds the app image and runs `uvicorn` on port `8000`.
- `.github/workflows/ci.yml` — runs tests, builds, and pushes the image to a registry (registry URL and credentials provided via GitHub secrets).
- `nomad/hello.nomad` — Nomad job that pulls the pushed image, maps port `8000`, and performs an HTTP health check against `/health`.
- `monitoring/promtail.yaml` & `monitoring/docker-compose-promtail.yml` — Promtail configuration and compose file to ship Docker container logs into Loki.
- `scripts/sysinfo.sh` — improved shell script with basic error handling.

Run locally

1. Build and run the app container:

```bash
docker build -t hello-devops:local .
docker run --rm -p 8000:8000 hello-devops:local
```

Visit http://localhost:8000/ and http://localhost:8000/health

2. Run tests locally:

```bash
python -m pip install -r requirements.txt
pytest -q
```

CI/CD

The GitHub Actions workflow `ci.yml` does the following:
- `test` job: installs dependencies and runs `pytest`.
- `build-and-push` job: logs into the configured container registry and pushes the built image to `${{ secrets.REGISTRY_URL }}/hello-devops:latest`.

Make sure to set the following repository secrets:
- `REGISTRY_URL` (e.g., `ghcr.io/yourorg` or `registry.example.com`)
- `REGISTRY_USERNAME`
- `REGISTRY_PASSWORD`

Nomad Deployment

Update `nomad/hello.nomad` to set `NOMAD_META_REGISTRY_URL` (or replace the `image` field) to the pushed image, then run:

```bash
nomad job run nomad/hello.nomad
```

Monitoring and Logs

1. Start Loki (example):

```bash
docker run -d --name loki -p 3100:3100 grafana/loki:3.0.0
```

2. From the `monitoring/` folder, start Promtail to ship Docker logs:

```bash
docker compose -f docker-compose-promtail.yml up -d
```

Promtail is configured to read Docker container logs from `/var/lib/docker/containers/*/*-json.log` and push them to Loki at `http://loki:3100`.

### Nomad Grafana dashboard

`monitoring/nomad-cluster-health.json` is an importable Grafana dashboard for Nomad cluster health. It includes client CPU and memory utilization, allocation state, per-job health, unhealthy or pending allocations, client count, and Nomad runtime activity.

The dashboard expects Nomad telemetry to be exposed in Prometheus format and scraped by Prometheus. To use it:

1. Add Prometheus as a Grafana data source.
2. Import `monitoring/nomad-cluster-health.json` in Grafana.
3. Select the Prometheus data source when Grafana prompts for `DS_PROMETHEUS`.

The existing Promtail/Loki configuration provides logs only; it does not collect the Prometheus metrics required by this dashboard.

The related dashboards are also available for [Consul](monitoring/consul-cluster-health.json) and [Vault](monitoring/vault-cluster-health.json). Metric names and service telemetry setup are documented in [monitoring/service-metrics-reference.md](monitoring/service-metrics-reference.md).

Notes

- The CI assumes valid registry credentials are stored in GitHub Secrets.
- The sample Promtail compose file may require elevated permissions to read Docker container logs on Linux hosts.
- Adjust Nomad networking and resource values to match your environment.

If you want, I can also run the tests and build locally, or prepare a sample `docker-compose` to run the whole stack for local testing.
