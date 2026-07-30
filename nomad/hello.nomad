job "hello-devops" {
  datacenters = ["dc1"]
  type = "service"

  group "app" {
    network {
      port "http" { static = 8000 }
    }

    task "hello" {
      driver = "docker"

      config {
        # Replace this with your registry image when you are ready to deploy from a registry.
        image = "hello-devops:latest"
        ports = ["http"]
      }

      resources {
        cpu    = 500
        memory = 256
      }

      service {
        name = "hello-devops"
        port = "http"

        check {
          name     = "http-check"
          type     = "http"
          path     = "/health"
          interval = "10s"
          timeout  = "2s"
        }
      }
    }
  }
}
