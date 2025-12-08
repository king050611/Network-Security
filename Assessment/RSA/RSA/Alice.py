import json
import os
import socket
import subprocess
import sys
import time
from typing import Tuple

from utils import rsa_encrypt, str_to_int, int_to_str, encrypt_message_to_blocks, join_int_blocks_to_message


HOST = "127.0.0.1"
BOB_PORT = 65432
EVE_PORT = 65433


# Configuration: Can be overridden by environment variables to control key size and time limits for Scenario 2
# Example: Run in PowerShell:
#   $env:SCENARIO2_BITS="96"; $env:SCENARIO2_TIME_LIMIT="8"; python Alice.py
SCENARIO2_BITS = int(os.getenv("SCENARIO2_BITS", "32"))
SCENARIO2_TIME_LIMIT = float(os.getenv("SCENARIO2_TIME_LIMIT", "5.0"))


def send_json(conn: socket.socket, data: dict) -> None:
    payload = (json.dumps(data) + "\n").encode("utf-8")
    conn.sendall(payload)


def recv_json(conn: socket.socket, timeout: float | None = None) -> dict:
    try:
        if timeout is not None:
            conn.settimeout(timeout)
        with conn.makefile("rb") as f:
            line = f.readline()
        if not line:
            return {}
        return json.loads(line.decode("utf-8"))
    except Exception:
        return {}


def wait_for_port(host: str, port: int, timeout: float = 10.0) -> bool:
    end = time.time() + timeout
    while time.time() < end:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                return True
        except OSError:
            time.sleep(0.1)
    return False


def start_bob(bits: int) -> subprocess.Popen:
    # Start Bob server process
    bob_path = os.path.join(os.path.dirname(__file__), "Bob.py")
    print(f"[Alice] Starting Bob, key size {bits} bits...")
    proc = subprocess.Popen([sys.executable, bob_path, str(bits)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Wait for port to be ready
    if not wait_for_port(HOST, BOB_PORT, timeout=10.0):
        print("[Alice] Timed out waiting for Bob to start!")
    return proc


def start_eve(max_time_seconds: float = 20.0) -> subprocess.Popen:
    eve_path = os.path.join(os.path.dirname(__file__), "Eve.py")
    print(f"[Alice] Starting Eve, max attack duration {max_time_seconds}s...")
    proc = subprocess.Popen([sys.executable, eve_path, str(max_time_seconds)], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    # Avoid probe connection interfering with Eve, wait briefly instead
    time.sleep(0.3)
    return proc


def collect_proc_output(name: str, proc: subprocess.Popen):
    try:
        if proc and proc.stdout:
            out = proc.stdout.read()
            if out:
                print(f"[{name} OUTPUT]\n{out}")
    except Exception:
        pass


def scenario_1_baseline():
    print("\n=== Scenario 1: No attack, normal communication (128 bits) ===")
    bob = start_bob(128)
    try:
        with socket.create_connection((HOST, BOB_PORT), timeout=5.0) as conn:
            send_json(conn, {"action": "get_pubkey"})
            pub = recv_json(conn, timeout=5.0)
            if not pub:
                time.sleep(0.2)
                pub = recv_json(conn, timeout=5.0)
            n = int(pub["n"]) if "n" in pub else 0
            e = int(pub["e"]) if "e" in pub else 65537
            print(f"[Alice] Received Bob's public key n={n}, e={e}")
            message = "Hello RSA baseline"
            c_blocks = encrypt_message_to_blocks(message, (n, e))
            print(f"[Alice] Plaintext: {message}")
            print(f"[Alice] Number of ciphertext blocks: {len(c_blocks)}")
            send_json(conn, {"ciphertexts": [str(c) for c in c_blocks]})
            resp = recv_json(conn)
            print(f"[Alice] Received Bob's receipt: {resp}")
    finally:
        if bob:
            bob.terminate()
            collect_proc_output("Bob", bob)


def scenario_2_attack_success():
    print(f"\n=== Scenario 2: Attack active ({SCENARIO2_BITS} bits), expect success, TIME_LIMIT={SCENARIO2_TIME_LIMIT}s ===")
    TIME_LIMIT = SCENARIO2_TIME_LIMIT
    bob = start_bob(SCENARIO2_BITS)
    # Give Eve a looser overall factoring duration (can be adjusted or made into an env var)
    eve = start_eve(max_time_seconds=max(20.0, TIME_LIMIT + 10.0))
    try:
        # Get public key
        with socket.create_connection((HOST, BOB_PORT), timeout=5.0) as conn_bob:
            send_json(conn_bob, {"action": "get_pubkey"})
            pub = recv_json(conn_bob, timeout=5.0)
            n = int(pub["n"]) if "n" in pub else 0
            e = int(pub["e"]) if "e" in pub else 65537
            print(f"[Alice] Received Bob's public key n={n}, e={e}")

            # Forward public key to Eve
            with socket.create_connection((HOST, EVE_PORT), timeout=30) as conn_eve:
                send_json(conn_eve, {"n": str(n), "e": str(e)})
                res = recv_json(conn_eve, timeout=35.0)
                print(f"[Alice] Received Eve's attack result: {res}")
                success = bool(res.get("success", False))
                time_spent = float(res.get("time_spent", 0.0))
                if success and time_spent < TIME_LIMIT:
                    print(f"[Alice] Attack successful ({time_spent:.4f}s < {TIME_LIMIT}s)")
                    d_found = int(res.get("d_found"))
                    # Prepare to send ciphertext blocks and let Eve decrypt
                    message = "Attack success demo"
                    c_blocks = encrypt_message_to_blocks(message, (n, e))
                    print(f"[Alice] Test ciphertext block count: {len(c_blocks)}")
                    # Verify Eve can decrypt (Alice local verification)
                    m_blocks = [pow(c, d_found, n) for c in c_blocks]
                    recovered = join_int_blocks_to_message(m_blocks)
                    print(f"[Alice] Recovered text using Eve's d: '{recovered}'")
                else:
                    print(f"[Alice] Attack failed within time limit (time_spent={time_spent:.4f}s)")

            # Perform actual communication with Bob to confirm decryption still works
            message2 = "Hello Bob despite Eve"
            c2_blocks = encrypt_message_to_blocks(message2, (n, e))
            send_json(conn_bob, {"ciphertexts": [str(c) for c in c2_blocks]})
            resp = recv_json(conn_bob, timeout=10.0)
            print(f"[Alice] Received Bob's receipt: {resp}")
    finally:
        if eve:
            eve.terminate()
            collect_proc_output("Eve", eve)
        if bob:
            bob.terminate()
            collect_proc_output("Bob", bob)


def scenario_3_defense_fail_attack():
    print("\n=== Scenario 3: Defense active (256 bits), expect attack failure, TIME_LIMIT=10s ===")
    TIME_LIMIT = 10.0
    bob = start_bob(256)
    eve = start_eve(max_time_seconds=20.0)
    try:
        with socket.create_connection((HOST, BOB_PORT), timeout=5.0) as conn_bob:
            send_json(conn_bob, {"action": "get_pubkey"})
            pub = recv_json(conn_bob, timeout=5.0)
            n = int(pub["n"]) if "n" in pub else 0
            e = int(pub["e"]) if "e" in pub else 65537
            print(f"[Alice] Received Bob's public key n={n}, e={e}")

            with socket.create_connection((HOST, EVE_PORT), timeout=5.0) as conn_eve:
                send_json(conn_eve, {"n": str(n), "e": str(e)})
                res = recv_json(conn_eve, timeout=40.0)
                print(f"[Alice] Received Eve's attack result: {res}")
                success = bool(res.get("success", False))
                time_spent = float(res.get("time_spent", 0.0))
                if (not success) or (time_spent > TIME_LIMIT):
                    print(f"[Alice] Defense successful (time_spent={time_spent:.4f}s > {TIME_LIMIT}s or Eve failed)")
                else:
                    print(f"[Alice] Warning: Eve succeeded within time limit ({time_spent:.4f}s <= {TIME_LIMIT}s)")

            # Confirm with normal communication to Bob
            message = "Secure message under defense"
            c_blocks = encrypt_message_to_blocks(message, (n, e))
            send_json(conn_bob, {"ciphertexts": [str(c) for c in c_blocks]})
            resp = recv_json(conn_bob, timeout=10.0)
            print(f"[Alice] Received Bob's receipt: {resp}")
    finally:
        if eve:
            eve.terminate()
            collect_proc_output("Eve", eve)
        if bob:
            bob.terminate()
            collect_proc_output("Bob", bob)


def main():
    scenario_1_baseline()
    scenario_2_attack_success()
    scenario_3_defense_fail_attack()


if __name__ == "__main__":
    main()