import matplotlib.pyplot as plt

# ===== ① 在这里填你自己的数据 =====
# 密钥长度（示例）
key_lengths = [64, 128, 256, 512, 1024]

# 对应的攻击事件数量（或成功攻击次数、攻击概率等）
attack_events = [100, 60, 20, 5, 0]

# ===== ② 开始画图 =====
plt.figure()

# 画折线图（不手动指定颜色，使用默认样式）
plt.plot(key_lengths, attack_events, marker='o')

# 坐标轴标签和标题
plt.xlabel("密钥长度（比特）")
plt.ylabel("攻击事件数量")
plt.title("密钥长度与中间人攻击事件的关系")

# 可选：网格
plt.grid(True)

# 可选：让 x 轴只显示这些离散的密钥长度
plt.xticks(key_lengths)

# 显示图像
plt.show()
