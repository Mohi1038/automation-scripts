import requests
import os
import time

PROM_URL = "http://localhost:9090/api/v1/query"
QUERY = '100 - (avg(rate(node_cpu_seconds_total{mode="idle"}[1m])) * 100)'
THRESHOLD = 70
COOLDOWN = 60  # seconds

def get_cpu_usage():
    try:
        response = requests.get(PROM_URL, params={"query": QUERY})
        data = response.json()

        if not data['data']['result']:
            print("[WARN] No data received from Prometheus")
            return 0

        return float(data['data']['result'][0]['value'][1])

    except Exception as e:
        print(f"[ERROR] Failed to fetch metrics: {e}")
        return 0


def create_vm():
    print("[ACTION] Creating VM on GCP...")
    result = os.system("bash scripts/gcp_create_vm.sh")

    if result == 0:
        print("[SUCCESS] VM created successfully")
    else:
        print("[ERROR] VM creation failed")


def main():
    print("🚀 Auto-Scaler Started...")

    while True:
        cpu = get_cpu_usage()
        print(f"[INFO] CPU Usage: {cpu:.2f}%")

        if cpu > THRESHOLD:
            print("[TRIGGER] Threshold exceeded!")
            create_vm()
            print(f"[COOLDOWN] Sleeping for {COOLDOWN} seconds...")
            time.sleep(COOLDOWN)

        time.sleep(10)


if __name__ == "__main__":
    main()