from hello import app


def test_app_instance():
    from fastapi import FastAPI

    assert isinstance(app, FastAPI)


def test_routes_exist():
    paths = {r.path for r in app.routes}
    assert "/" in paths
    assert "/health" in paths
