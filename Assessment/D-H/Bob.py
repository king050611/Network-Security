# bob.py
import socket
import pickle
from para import p, g, PASSWORD

def main():
    server = socket.socket()
    server.bind(('127.0.0.1', 8888))
    server.listen(1)
    print("[Bob] Server started, listening on 8888...")

    conn, addr = server.accept()
    print(f"[Bob] Connection accepted: {addr}")

    try:
        # Calculate Bob's public key and private key
        import random
        b = random.randint(1, p-2)
        B = pow(g, b, p)
        print(f"[Bob] Generated Public Key: {B}")

        # Get Alice's public key
        data = pickle.loads(conn.recv(4096))
        A = data['public_key']
        received_pwd = data.get('password', None) 
        mode = data.get('mode', 1)
        print(f"[Bob] Received Alice's public key: {A}")

        # --- mode 3: with authentication ---
        if mode == 3:
            print(f"[Bob] Received password: '{received_pwd}'")
            print(f"[Bob] Expected password: '{PASSWORD}'")

            if received_pwd == PASSWORD:
                print("[Bob] Password match successful! Identity verification passed")
            else:
                print("[Bob] Password mismatch! Refusing communication")
                conn.close()
                return
        elif mode == 2:
            print("[Bob] (Mode 2: Simulate D-H being attacked without any defense mechanism)")
        else:
            print("[Bob] (Mode 1: Simulate the standard D-H process)")

        # Send Bob's public key to Alice
        conn.send(pickle.dumps({'public_key': B}))

        # Calculate shared key
        shared_key = pow(A, b, p)
        print(f"[Bob] Shared Key: {shared_key}")

    except Exception as e:
        print(f"[Bob] Error: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    main()