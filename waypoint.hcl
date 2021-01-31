project = "hashicheck"

app "hashicheck" {
  labels = {
    "service" = "hashicheck"
  }

  build {
    use "docker" {}
  }

  deploy {
    use "docker" {
      service_port = 80
    }
  }
}
