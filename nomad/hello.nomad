job "hello-devops" {
  datacenters = ["dc1"]
  type = "service"

  group "app" {
    network {
      port "http" {
        static = 8001
        to = 8000
      }
    }

    task "hello" {
      driver = "docker"

      config {
        image = "ghcr.io/tulasikumar4449/hello-devops:latest"
        ports = ["http"]
      }

      resources {
        cpu    = 500
        memory = 256
      }

      service {
        provider = "nomad"

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