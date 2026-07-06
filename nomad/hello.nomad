job "hello-devops" {
  datacenters = ["dc1"]
  type = "service"

  group "app" {
    task "hello" {
      driver = "docker"

      config {
        image = "hello-devops:latest"
      }

      resources {
        cpu    = 100
        memory = 128
      }
    }
  }
}
