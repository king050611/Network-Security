import json
import socket
import sys
import time

from utils import mod_inverse, pollard_rho_factor


HOST = "127.0.0.1"
PORT = 65433


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


def start_server(max_time_seconds: float = 20.0) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print("Eve ready")
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    data = recv_json(conn, timeout=2.0)
                    if not data:
                        continue
                    n = int(data.get("n", 0))
                    e = int(data.get("e", 65537))
                    if n == 0:
                        continue
                    t0 = time.time()
                    p, q = pollard_rho_factor(n, max_time_seconds=max_time_seconds)
                    elapsed = time.time() - t0
                    success = (p != 1 and p * q == n)
                    result = {"success": success, "time_spent": elapsed}
                    if success:
                        phi = (p - 1) * (q - 1)
                        try:
                            d = mod_inverse(e, phi)
                            result.update({"d_found": str(d)})
                        except Exception as ex:
                            result.update({"success": False})
                    send_json(conn, result)
            except KeyboardInterrupt:
                print("Eve exit")
                break
            except Exception as ex:
                # Minimize output: ignore single errors
                pass


if __name__ == "__main__":
    # Allow specifying max attempt time (seconds) via command line args, default 20s
    max_time = 20.0
    if len(sys.argv) >= 2:
        try:
            max_time = float(sys.argv[1])
        except ValueError:
            pass
    start_server(max_time_seconds=max_time)