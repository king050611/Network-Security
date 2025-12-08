import time
import matplotlib.pyplot as plt
from Crypto.Util.number import getPrime
import random

def brute_force_discrete_log(g, A, p):
    # 简单的暴力破解：尝试每一个可能的 a，看 g^a 是否等于 A
    # 实际攻击中会有更优算法(如BSGS)，但这里演示趋势即可
    for candidate in range(1, p):
        if pow(g, candidate, p) == A:
            return candidate
    return None

def test_forge_attack():
    # 我们只能测很小的位长，否则电脑会卡死
    bit_lengths = [8, 10, 12, 14, 16, 18, 20]
    times = []

    print("开始测试暴力破解时间 (Forge Attack)...")

    for bits in bit_lengths:
        print(f"正在破解 {bits} bit...")
        
        p = getPrime(bits)
        g = 5
        # 真实的私钥
        a = random.randint(1, p // 2) 
        # 公钥
        A = pow(g, a, p)
        
        start_time = time.time()
        
        # 攻击！
        found_key = brute_force_discrete_log(g, A, p)
        
        end_time = time.time()
        times.append(end_time - start_time)

    # 画图
    plt.figure(figsize=(10, 6))
    plt.plot(bit_lengths, times, marker='x', linestyle='--', color='r')
    
    plt.title('Brute Force Attack Time vs. Prime Bit Length')
    plt.xlabel('Prime Bit Length (bits)')
    plt.ylabel('Time to Crack (seconds)')
    plt.yscale('log') # 破解时间通常是指数级增长，用对数坐标更好看
    plt.grid(True)
    
    plt.savefig('forge_attack_graph.png')
    print("图表已保存为 forge_attack_graph.png")

if __name__ == "__main__":
    test_forge_attack()