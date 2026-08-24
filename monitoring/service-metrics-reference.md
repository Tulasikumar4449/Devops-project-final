# Nomad, Consul, and Vault Prometheus metrics

This reference records the metrics used by the Grafana dashboards in this directory. Each service must expose telemetry in Prometheus format and Prometheus must scrape the endpoint before the queries return data.

## Nomad

Enable Prometheus telemetry in Nomad with `telemetry { prometheus_metrics = true }`, then scrape the agent metrics endpoint (normally `/v1/metrics?format=prometheus`).

| Area | Metrics | Use |
| --- | --- | --- |
| Allocations | `nomad_client_allocs_running`, `nomad_client_allocs_pending`, `nomad_client_allocs_failed`, `nomad_client_allocs_unhealthy`, `nomad_client_allocs_complete` | Allocation state and health |
| Capacity | `nomad_client_host_cpu_total`, `nomad_client_host_cpu_idle`, `nomad_client_host_memory_total`, `nomad_client_host_memory_available` | Client CPU and memory utilization |
| Jobs | `nomad_nomad_job_summary_running`, `nomad_nomad_job_summary_queued`, `nomad_nomad_job_summary_failed` | Per-job health |
| Runtime | `nomad_runtime_num_goroutines`, `nomad_runtime_alloc_bytes` | Agent runtime pressure |

## Consul

Enable telemetry with `telemetry { prometheus_retention_time = "24h" }`, then scrape `/v1/agent/metrics?format=prometheus` from each Consul agent.

| Area | Metrics | Use |
| --- | --- | --- |
| Cluster | `consul_raft_peers`, `consul_raft_leader`, `consul_serf_lan_members` | Quorum and membership |
| Services | `consul_catalog_service_count`, `consul_health_service_status` | Registered and passing services |
| Runtime | `consul_runtime_num_goroutines`, `consul_runtime_heap_objects` | Agent runtime pressure |
| Requests | `consul_http_request_count` | API request volume |

`consul_health_service_status` includes service and status labels. Filter with `status="passing"`, `status="warning"`, or `status="critical"` when those labels are available in the deployed Consul version.

## Vault

Enable telemetry with `telemetry { prometheus_retention_time = "24h" }`, then scrape `/v1/sys/metrics?format=prometheus` using an authenticated Prometheus scrape configuration.

| Area | Metrics | Use |
| --- | --- | --- |
| Availability | `vault_core_unsealed`, `vault_core_active` | Sealed and active node state |
| Requests | `vault_core_handle_request`, `vault_core_handle_request_count` | API request activity, depending on Vault version |
| Storage | `vault_expire_num_leases`, `vault_identity_num_entities` | Lease and identity growth |
| Runtime | `vault_runtime_heap_alloc_bytes`, `vault_runtime_num_goroutines` | Agent runtime pressure |

Metric names can vary slightly between service versions and enabled collectors. Confirm the names in Prometheus Explore before adding alert thresholds.
