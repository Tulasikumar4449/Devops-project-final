from scripts.generate_nomad_job import generate_nomad_job


CASES = [
    {
        "job_name": "hello-api",
        "image": "example/hello:1.0",
        "cpu": 500,
        "memory": 256,
        "port": 8000,
        "exposed_port": 8001,
    },
    {
        "job_name": "payments-service",
        "image": "example/payments:2.4",
        "cpu": 1000,
        "memory": 512,
        "port": 8080,
        "exposed_port": 18080,
    },
    {
        "job_name": "worker-service",
        "image": "example/worker:3.1",
        "cpu": 250,
        "memory": 128,
        "port": 9000,
        "exposed_port": 19000,
    },
]


def test_generates_three_dynamic_nomad_jobs():
    for case in CASES:
        job = generate_nomad_job(**case)

        assert f'job "{case["job_name"]}"' in job
        assert f'image = "{case["image"]}"' in job
        assert f"cpu    = {case['cpu']}" in job
        assert f"memory = {case['memory']}" in job
        assert f"static = {case['exposed_port']}" in job
        assert f"to = {case['port']}" in job
        assert 'path     = "/health"' in job


def test_rejects_invalid_port():
    case = {**CASES[0], "port": 70000}

    try:
        generate_nomad_job(**case)
    except ValueError as error:
        assert "port" in str(error)
    else:
        raise AssertionError("Expected invalid port to be rejected")
