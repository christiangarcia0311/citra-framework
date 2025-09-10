import subprocess
import re
import sys

def run_benchmark(url="http://127.0.0.1:8000/", requests=10000, concurrency=100):
    try:
        # Run wrk benchmark
        cmd = ["wrk", "-t2", f"-c{concurrency}", f"-d30s", url]
        print(f"Running benchmark: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            print("Error running wrk. Make sure it's installed.")
            print(result.stderr)
            return

        output = result.stdout
        print("\n=== Raw wrk Output ===")
        print(output)

        # Parse wrk output for key metrics
        rps_match = re.search(r"Requests/sec:\s+([\d.]+)", output)
        latency_match = re.search(r"Latency\s+([\d.]+)\s*([a-zµ]+)", output)
        transfer_match = re.search(r"Transfer/sec:\s+([\d.]+)\s*([A-Za-z/]+)", output)

        print("\n=== Benchmark Summary ===")
        if rps_match:
            print(f"Requests per Second (RPS): {rps_match.group(1)}")
        if latency_match:
            print(f"Average Latency: {latency_match.group(1)} {latency_match.group(2)}")
        if transfer_match:
            print(f"Transfer Rate: {transfer_match.group(1)} {transfer_match.group(2)}")

    except FileNotFoundError:
        print("wrk is not installed. Install it via your package manager:")
        print("  Ubuntu: sudo apt install wrk")
        print("  Fedora: sudo dnf install wrk")
        print("  macOS: brew install wrk")

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000/"
    run_benchmark(url)
