import subprocess
import time
from datetime import datetime
from typing import cast

import yaml
from cryptography.hazmat.primitives import serialization
from prometheus_client import Gauge, start_http_server


def get_ssh_cert_expiration(hostname: str) -> int | None:
    command = ["ssh-keyscan", "-c", hostname]
    try:
        result = subprocess.run(command, capture_output=True, check=True).stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")
        return None

    for line in result.splitlines():
        line = line.strip()
        if not line or line.startswith(b"#"):
            continue
        identity = serialization.load_ssh_public_identity(line)
        if isinstance(identity, serialization.SSHCertificate):
            return identity.valid_before
    return None


def load_hosts(path: str) -> list[str]:
    with open(path) as stream:
        config = cast(object, yaml.safe_load(stream))

    if not isinstance(config, dict):
        raise TypeError("expected a mapping with a 'hosts' list")
    entries = cast(dict[object, object], config).get("hosts")
    if not isinstance(entries, list):
        raise TypeError("expected 'hosts' to be a list")

    hosts: list[str] = []
    for entry in cast(list[object], entries):
        if not isinstance(entry, str):
            raise TypeError("each entry in 'hosts' must be a string")
        hosts.append(entry)
    return hosts


def convert_unix_time(ut: float) -> str:
    return datetime.fromtimestamp(ut).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    try:
        hosts = load_hosts("./hosts.yaml")
    except (OSError, TypeError, UnicodeError, yaml.YAMLError) as exc:
        raise SystemExit(f"Error loading hosts.yaml: {exc}") from exc

    g = Gauge(
        "ssh_cert_expiration",
        "Returns SSH Certificate Expiration in Unixtime",
        labelnames=["host"],
    )
    _ = start_http_server(8000)

    while True:
        for host in hosts:
            ssh_cert_expiration = get_ssh_cert_expiration(host)
            if ssh_cert_expiration is None:
                continue
            print(
                f"Certificate for {host} is valid until: {convert_unix_time(ssh_cert_expiration)}"
            )
            g.labels(host=host).set(ssh_cert_expiration)

        time.sleep(150)
