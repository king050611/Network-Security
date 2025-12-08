import json
import socket
import sys
import threading
from typing import Tuple

from utils import generate_rsa_keys, rsa_decrypt, int_to_str, decrypt_blocks_to_message


HOST = "127.0.0.1"
PORT = 65432


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


def start_server(key_size: int) -> None:
    public_key, private_key = generate_rsa_keys(key_size)
    n, e = public_key
    n_priv, d, p, q = private_key
    print(f"[Bob] Keys generated bits={key_size}\n    n={n}\n    e={e}\n    d={d}\n    p={p}\n    q={q}")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen(5)
        print(f"[Bob] Listening on {HOST}:{PORT}, waiting for Alice...")
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    print(f"[Bob] Accepted connection: {addr}")
                    # Receive client request first to avoid protocol sync issues
                    req = recv_json(conn, timeout=2.0)
                    if not req:
                        print("[Bob] Empty request or timeout, closing connection")
                        continue
                    action = req.get("action")
                    if action != "get_pubkey":
                        print(f"[Bob] Unknown action: {action}, closing connection")
                        continue
                    # Send public key
                    send_json(conn, {"n": n, "e": e})
                    print("[Bob] Public key sent")
                    # Receive ciphertext
                    data = recv_json(conn, timeout=60.0)
                    if not data:
                        print("[Bob] No ciphertext received or timeout, closing connection")
                        continue
                    if "ciphertexts" in data:
                        c_list = [int(x) for x in data.get("ciphertexts", [])]
                        print(f"[Bob] Received {len(c_list)} ciphertext blocks")
                        plain_text = decrypt_blocks_to_message(c_list, private_key)
                        print(f"[Bob] Recovered plaintext: '{plain_text}'")
                        send_json(conn, {"status": "ok", "message": plain_text})
                        print("[Bob] Block decryption complete, replied to Alice")
                    else:
                        ciphertext = int(data.get("ciphertext", 0))
                        print(f"[Bob] Received ciphertext C={ciphertext}")
                        m_int = rsa_decrypt(ciphertext, private_key)
                        print(f"[Bob] Decrypted plaintext integer M={m_int}")
                        send_json(conn, {"status": "ok", "decrypted_M": str(m_int), "message": int_to_str(m_int)})
                        print("[Bob] Decryption complete, replied to Alice")
            except KeyboardInterrupt:
                print("[Bob] Received interrupt, exiting.")
                break
            except Exception as ex:
                print(f"[Bob] Error handling connection: {ex}")


if __name__ == "__main__":
    # Allow specifying bits via command line args, default 128
    bits = 128
    if len(sys.argv) >= 2:
        try:
            bits = int(sys.argv[1])
        except ValueError:
            pass
    start_server(bits)