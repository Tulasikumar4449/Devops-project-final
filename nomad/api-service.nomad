job "api-service" {
  datacenters = ["dc1"]
  type = "service"

  group "app" {
    network {
      port "http" {
        static = 8001
        to = 8000
      }
    }

    task "api-service" {
      driver = "docker"

      config {
        image = "hello-devops:local"
        ports = ["http"]
      }

      resources {
        cpu    = 500
        memory = 256
      }

      service {
        name = "api-service"
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
