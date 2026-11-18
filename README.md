# SSH Certificate Exporter

Copy the example configuration and replace `ssh.example.com` with the SSH hostnames you want to monitor.

```sh
cp hosts.yaml.example hosts.yaml
```

Run `docker compose up -d` or `podman compose up -d` to start the exporter from the published GHCR image. Podman requires a Compose provider.

To update the image, run `docker compose pull` or `podman compose pull`, then run `up -d` again. Prometheus metrics are available at `http://localhost:8000/metrics`.
