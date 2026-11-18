# SSH Certificate Exporter

Copy the example configuration and replace `ssh.example.com` with the SSH hostnames you want to monitor.

```sh
cp hosts.yaml.example hosts.yaml
```

Run `docker compose up --build` to start the exporter. Prometheus metrics are available at `http://localhost:8000/metrics`.
