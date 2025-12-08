import socket
import pickle
import random
from para import p, g, PASSWORD

def main():
    print("Select mode:")
    print("1 -> Unencrypted D-H (No Defense)")
    print("2 -> Attacked D-H (Man-in-the-Middle Attack)")
    print("3 -> Defended D-H (With Password Verification)")
    choice = input("Enter 1/2/3: ").strip()

    if choice not in ['1', '2', '3']:
        print("Invalid choice, defaulting to mode 1")
        choice = '1'

    # Determine connection target
    if choice == '2':
        port = 9999  # Attacker port
        print("[Alice] Mode Two: Simulating attacked D-H, connecting to attacker (9999)")
    else:
        port = 8888  # Bob port
        print(f"[Alice] Mode {choice}: Connecting to Bob (8888)")

    client = socket.socket()
    try:
        client.connect(('127.0.0.1', port))
    except ConnectionRefusedError:
        print(f"[Alice] Connection failed: Target port {port} not started")
        return

    try:
        # Generate private key and public key
        a = random.randint(1, p-2)
        A = pow(g, a, p)
        print(f"[Alice] Generated Public Key: {A}")

        # Construct data to send
        data = {'public_key': A, 'mode': int(choice)}

        # Only send password in mode 3
        if choice == '3':
            data['password'] = PASSWORD
            print("[Alice] Sending password for authentication")

        client.send(pickle.dumps(data))

        # Receive peer's public key
        resp = pickle.loads(client.recv(4096))
        B = resp['public_key']
        print(f"[Alice] Received peer's public key: {B}")

        # Calculate shared key
        shared_key = pow(B, a, p)
        print(f"[Alice] Calculated Shared Key: {shared_key}")

    except Exception as e:
        print(f"[Alice] Communication error: {e}")
    finally:
        client.close()

if __name__ == "__main__":
    main()