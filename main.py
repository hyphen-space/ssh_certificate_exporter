import subprocess
from cryptography.hazmat.primitives import serialization
from datetime import datetime
import time
import yaml
from prometheus_client import start_http_server, Gauge
import json


def get_ssh_cert_expiration(host):
    try:
        command = ["ssh-keyscan", "-c", host]
        result = subprocess.run(command, capture_output=True, check=True).stdout.strip()
        ssh_cert = serialization.load_ssh_public_identity(result)
        return ssh_cert.valid_before

    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


def convert_unix_time(ut):
    return datetime.fromtimestamp(ut).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == "__main__":
    g = Gauge(
        "ssh_cert_expiration",
        "Returns SSH Certificate Expiration in Unixtime",
        labelnames=["host"],
    )
    start_http_server(8000)

    with open("./hosts.yaml") as stream:
        try:
            hosts = yaml.safe_load(stream)["hosts"]
        except yaml.YAMLError as exc:
            print(exc)

    while True:
        for host in hosts:
            ssh_cert_expiration = get_ssh_cert_expiration(host)
            print(
                f"Certificate for {host} is valid until: {convert_unix_time(ssh_cert_expiration)}"
            )
            g.labels(host=host).set(ssh_cert_expiration)

        time.sleep(150)
