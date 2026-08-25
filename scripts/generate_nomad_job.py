"""Generate a deployable Nomad service job specification."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

_IDENTIFIER = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")


def validate_parameters(
    job_name: str,
    cpu: int,
    memory: int,
    port: int,
    exposed_port: int,
) -> None:
    if not _IDENTIFIER.fullmatch(job_name):
        raise ValueError("job_name must start with a letter and contain only letters, numbers, '_' or '-'")
    if cpu <= 0:
        raise ValueError("cpu must be greater than zero")
    if memory <= 0:
        raise ValueError("memory must be greater than zero")
    for name, value in (("port", port), ("exposed_port", exposed_port)):
        if not 1 <= value <= 65535:
            raise ValueError(f"{name} must be between 1 and 65535")


def generate_nomad_job(
    job_name: str,
    image: str,
    cpu: int,
    memory: int,
    port: int,
    exposed_port: int,
    datacenter: str = "dc1",
) -> str:
    """Return a Nomad HCL service job with the supplied deployment values."""
    validate_parameters(job_name, cpu, memory, port, exposed_port)
    if not image.strip():
        raise ValueError("image must not be empty")
    if not datacenter.strip():
        raise ValueError("datacenter must not be empty")

    return f'''job "{job_name}" {{
  datacenters = ["{datacenter}"]
  type = "service"

  group "app" {{
    network {{
      port "http" {{
        static = {exposed_port}
        to = {port}
      }}
    }}

    task "{job_name}" {{
      driver = "docker"

      config {{
        image = "{image}"
        ports = ["http"]
      }}

      resources {{
        cpu    = {cpu}
        memory = {memory}
      }}

      service {{
        provider = "nomad"
        name = "{job_name}"
        port = "http"

        check {{
          name     = "http-check"
          type     = "http"
          path     = "/health"
          interval = "10s"
          timeout  = "2s"
        }}
      }}
    }}
  }}
}}
'''


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--job-name", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--cpu", type=int, required=True, help="CPU units in MHz")
    parser.add_argument("--memory", type=int, required=True, help="Memory in MB")
    parser.add_argument("--port", type=int, required=True, help="Container port")
    parser.add_argument("--exposed-port", type=int, required=True, help="Host port")
    parser.add_argument("--datacenter", default="dc1")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    job = generate_nomad_job(
        job_name=args.job_name,
        image=args.image,
        cpu=args.cpu,
        memory=args.memory,
        port=args.port,
        exposed_port=args.exposed_port,
        datacenter=args.datacenter,
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(job, encoding="utf-8")
    print(f"Generated {args.output}")


if __name__ == "__main__":
    main()
