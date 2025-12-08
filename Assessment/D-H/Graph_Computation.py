import time
import matplotlib.pyplot as plt
from Crypto.Util.number import getPrime
import random

def test_dh_computation_time():
    # 1. 定义我们要测试的位长列表 (横轴)
    # 注意：2048位可能会比较慢，耐心等待
    bit_lengths = [128, 256, 512, 1024, 2048]
    times = []

    print("开始测试不同位长的计算时间...")

    for bits in bit_lengths:
        print(f"正在测试 {bits} bit...")
        
        # 动态生成该长度的质数 p
        p = getPrime(bits)
        g = 5
        a = random.randint(1, p - 2)
        
        # 2. 测量计算时间 (纵轴)
        start_time = time.time()
        
        # 模拟 D-H 的核心计算： A = g^a mod p
        # 在 MITM 攻击中，攻击者需要做两次这种计算
        _ = pow(g, a, p)
        
        end_time = time.time()
        
        # 记录耗时 (毫秒)
        duration = (end_time - start_time) * 1000
        times.append(duration)

    # 3. 画图
    plt.figure(figsize=(10, 6))
    plt.plot(bit_lengths, times, marker='o', linestyle='-', color='b')
    
    plt.title('D-H Computation Cost vs. Prime Bit Length')
    plt.xlabel('Prime Bit Length (bits)')
    plt.ylabel('Time (ms)')
    plt.grid(True)
    
    # 保存图片
    plt.savefig('dh_time_vs_length.png')
    print("图表已保存为 dh_time_vs_length.png")

if __name__ == "__main__":
    test_dh_computation_time()