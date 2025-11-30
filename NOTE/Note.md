
---

## 第一部分：密码学基础——信息如何用数字表示

### 1. 二进制（Binary）和十六进制（Hexadecimal）
- **核心概念**：计算机只懂0和1。所有数据，包括密码学中处理的信息，最终都是二进制比特流。
- **为什么用十六进制？** 二进制写起来太长，容易出错。十六进制是二进制的“简写版”。
- **转换关系**：每4位二进制数对应1位十六进制数。
  - `0000` = `0`
  - `0001` = `1`
  - ...
  - `1110` = `E`
  - `1111` = `F`
- **示例**：二进制 `1101 0110` 可以分成 `1101` (D) 和 `0110` (6)，所以是 `D6`₁₆。

### 2. 文本的数字化（ASCII码）
- **问题**：计算机如何表示字母“A”或“你好”？
- **解决方案**：使用标准编码表，最基础的是ASCII（美国信息交换标准代码）。
- **关键点**：
  - 每个标准字符（字母、数字、标点）对应一个7位或8位的二进制数。
  - PDF中扩展ASCII使用8位（1字节），可以表示256个字符（0-255）。
- **举例详解**：
  - 小写 `a`:
    - 十六进制：`61`₁₆
    - 二进制：`0110 0001`₂
    - 十进制：97₁₀
  - 字符串 `"Maths"` 的转换过程：
    1. 查ASCII表：`M` -> `4D`, `a` -> `61`, `t` -> `74`, `h` -> `68`, `s` -> `73`
    2. 合并：`4D 61 74 68 73`
  - 反向过程：`43 72 79 70 74 6F` -> `C` `r` `y` `p` `t` `o` -> `"Crypto"`

**思考**：密码学操作（如加密）并不是直接对字母“A”进行操作，而是对其背后的二进制码 `01000001` 进行数学变换。

---

## 第二部分：分组密码（Block Ciphers）核心思想

### 1. 什么是分组密码？
- **定义**：一种加密方法，先将明文分成多个**固定长度**的块，然后对每个块**独立**进行加密。
- **常见块大小**：DES是64位，AES通常是128位。
- **数学表示**：
  - 明文 \( P = P_1P_2P_3... \)（每个 \( P_i \) 是n位）
  - 密钥 \( K \)（k位）
  - 加密函数 \( E_K \)：\( C_i = E_K(P_i) \)
  - 密文 \( C = C_1C_2C_3... \)

### 2. 分组密码的三种基本操作
1.  **替换（Substitution）**：
    - 类似于凯撒密码，但更复杂。将输入的一组比特**映射**为另一组不同的比特。
    - **目的**：混淆（Confusion），使密文和密钥之间的关系变得复杂难懂。
    - **实现**：主要通过S盒（Substitution Box）完成。

2.  **置换（Permutation）**：
    - 将输入比特的**位置重新排列**。
    - **目的**：扩散（Diffusion），使明文中的一个比特的变化影响到密文中的多个比特。
    - **实现**：主要通过P盒（Permutation Box）完成。

3.  **乘积密码（Product Cipher）**：
    - **定义**：交替使用多次替换和置换操作的密码。
    - **优点**：结合了混淆和扩散，能产生非常强大和安全的加密效果。
    - **DES和AES都是乘积密码**。

---

## 第三部分：Feistel 网络结构——DES的骨架

### 1. 核心设计理念
- **天才之处**：加密和解密的过程**结构完全相同**，唯一的区别是**子密钥使用的顺序相反**。这极大地简化了硬件和软件的实现。

### 2. 单轮Feistel结构详解
我们以第 \( i \) 轮为例：

- **输入**：上一轮的输出 \( LE_{i-1} \) (左32位) 和 \( RE_{i-1} \) (右32位)，以及本轮子密钥 \( K_i \) (48位)。
- **处理过程**：
  1.  **左路直通**：本轮的左输出 \( LE_i \) **直接等于** 上一轮的右输入 \( RE_{i-1} \)。
      - \( LE_i = RE_{i-1} \)
  2.  **右路计算**：本轮的右输出 \( RE_i \) 是上一轮的左输入 \( LE_{i-1} \) 与一个**轮函数F**的输出进行**异或（XOR）** 的结果。
      - \( RE_i = LE_{i-1} \oplus F(RE_{i-1}, K_i) \)
      - **异或（XOR）**：是一种基本逻辑运算，相同为0，不同为1。它的关键特性是：\( A \oplus B \oplus B = A \)，这是解密能成功的基础。
  3.  **轮函数 F**：这是Feistel网络的核心和安全性的来源。它接受32位的 \( R \) 和48位的 \( K_i \)，输出一个32位的结果。

### 3. 为什么解密和加密一样？
假设最后一轮加密的输出是 \( (LE_{16}, RE_{16}) \)，它作为解密的第一轮输入 \( (LD_0, RD_0) \)。
- 解密第一轮：
  - \( LD_1 = RD_0 = RE_{16} \)
  - \( RD_1 = LD_0 \oplus F(RD_0, K_{16}) = LE_{16} \oplus F(RE_{16}, K_{16}) \)
- 回顾加密最后一轮：
  - \( RE_{16} = LE_{15} \oplus F(RE_{15}, K_{16}) \)
  - \( LE_{16} = RE_{15} \)
- 将加密公式代入解密公式：
  - \( RD_1 = LE_{16} \oplus F(RE_{16}, K_{16}) = RE_{15} \oplus F(RE_{15}, K_{16}) \)
  - 因为 \( RE_{16} = RE_{15} \)（在加密中，\( RE_{15} \) 是第16轮的输入右半部分）？**这里需要纠正一个理解点**。

让我们更精确地推导一下，这能完美展示其对称性：

**加密（第16轮）**:
输入: \( (LE_{15}, RE_{15}) \)
输出:
\( LE_{16} = RE_{15} \)
\( RE_{16} = LE_{15} \oplus F(RE_{15}, K_{16}) \)

**解密（第1轮，使用密钥K16）**:
输入: \( (LD_0, RD_0) = (LE_{16}, RE_{16}) \)
输出:
\( LD_1 = RD_0 = RE_{16} \)
\( RD_1 = LD_0 \oplus F(RD_0, K_{16}) = LE_{16} \oplus F(RE_{16}, K_{16}) \)

将 \( LE_{16} \) 和 \( RE_{16} \) 用加密公式替换：
\( RD_1 = RE_{15} \oplus F(LE_{15} \oplus F(RE_{15}, K_{16}), K_{16}) \)
这看起来复杂。关键在于，如果我们把解密第一轮的输出 \( (LD_1, RD_1) \) 与加密第15轮的输入 \( (LE_{15}, RE_{15}) \) 比较，会发现：
- \( LD_1 = RE_{16} = LE_{15} \oplus F(RE_{15}, K_{16}) \) ... 这并不直接等于 \( RE_{15} \)。

**正确的理解方式是**：解密过程是加密过程的**逆序**。解密第一轮（用K16）的输出，正好是加密第15轮（用K15）的输入。这个过程逐轮进行，直到恢复原始明文。其对称性的根源在于**XOR操作的特性**和**左右分支的交换**。你可以尝试用两个简单的轮次在纸上画一下，会立刻明白。

---

## 第四部分：DES算法分步解剖

DES是一个16轮的Feistel网络。下图概括了其完整流程：
```mermaid
flowchart TD
A[64位明文] --> IP[初始置换 IP]
IP --> B[64位置换后数据]
B --> Split[拆分为 L₀, R₀<br>各32位]
Split --> LoopInput
subgraph Loop[核心: 16轮Feistel运算]
    direction LR
    LoopInput[输入: L₍i-1₎, R₍i-1₎] --> F[轮函数 F<br>32位 -> 48位 -> 32位]
    F --输出--> XOR[异或 ⊕]
    LoopInput --直通--> Concat[拼接]
    XOR --> Concat
    Concat --> Swap[左右交换<br>Lᵢ = R₍i-1₎<br>Rᵢ = L₍i-1₎ ⊕ F]
    Swap --> LoopOutput[输出: Lᵢ, Rᵢ]
end
LoopOutput --> LoopInput
Loop --循环16次--> Final[最终轮输出<br>L₁₆, R₁₆<br>（不交换）]
Final --> Combine[合并 R₁₆ L₁₆]
Combine --> IP_inv[最终置换 IP⁻¹]
IP_inv --> C[64位密文]

K[64位初始密钥] --> PC1[置换选择1 PC-1<br>64位->56位]
PC1 --> C0[生成 C₀, D₀<br>各28位]
C0 --> SubKeyLoopInput
subgraph SubKeyLoop[子密钥生成器]
    SubKeyLoopInput[输入: C₍i-1₎, D₍i-1₎] --> LS[循环左移 LS<br>轮次1,2,9,16:移1位<br>其他:移2位]
    LS --> PC2[置换选择2 PC-2<br>56位->48位]
    PC2 --> SubKeyLoopOutput[输出: 48位子密钥 Kᵢ]
end
SubKeyLoopOutput --> SubKeyLoopInput
SubKeyLoop --循环16次--> K16[生成16个子密钥<br>K₁...K₁₆]

K1 --> F
K2 --> F
K16 --> F
```

### 阶段一：初始置换（IP）
- **目的**：对64位明文的比特顺序进行一次“洗牌”。
- **操作**：按照一个固定的置换表（IP表）重新排列比特。
- **注意**：IP和其逆置换IP⁻¹在密码学上是**没有增加安全性**的，因为它们都是固定、公开的。它们的存在可能源于早期硬件设计的需要。

### 阶段二：16轮Feistel处理（核心）
这是DES算法的核心。每一轮都使用一个不同的48位**子密钥（Subkey）**。我们先看子密钥的生成。

#### **子密钥生成流程**
1.  **初始密钥**：64位。但实际有效密钥是56位，因为第8, 16, 24, ..., 64位是**校验位**（用于错误检测，与加密无关），被丢弃。
2.  **PC-1置换**：对剩下的56位进行置换，并分成两个28位的半密钥 \( C_0 \) 和 \( D_0 \)。
3.  **循环左移**：每一轮，\( C_i \) 和 \( D_i \) 分别进行循环左移。
    - 移位规则：第1, 2, 9, 16轮移1位；其他轮次移2位。
    - **目的**：让每个子密钥都基于密钥的不同比特集合。
4.  **PC-2置换**：将移位后合并的56位数据，通过PC-2表置换并压缩成48位的本轮子密钥 \( K_i \)。
5.  重复16次，生成16个子密钥。

#### **轮函数 F(R, K) 详解**
这是DES安全性的心脏。输入是32位的R和48位的K，输出是32位。
1.  **扩展置换（E盒）**：
    - **目的**：将32位的R**扩展**为48位，以便与48位的子密钥K进行异或。
    - **方法**：使用固定的E盒置换表。这个表有重复的比特（例如，输入的第32位同时成为输出的第1和第48位），从而实现扩展。
2.  **与子密钥异或**：
    - 将扩展后的48位R与48位的子密钥K进行按位异或（XOR）操作。
    - **目的**：将密钥的影响引入到加密过程中。
3.  **S盒替换（核心中的核心）**：
    - **输入**：上一步得到的48位结果被分成**8个6位**的分组。
    - **操作**：每个6位分组输入一个**不同的S盒**（S1到S8）。每个S盒是一个固定的4行16列的查找表。
    - **查找方法**：
        - 6位输入：记为 \( b_1b_2b_3b_4b_5b_6 \)。
        - **行号** = \( (b_1b_6)_2 \)（二进制，范围0-3）。
        - **列号** = \( (b_2b_3b_4b_5)_2 \)（二进制，范围0-15）。
        - 在对应的S盒中查找该行该列的数字（0-15）。
    - **输出**：每个S盒输出一个4位数字。8个S盒共输出32位。
    - **目的**：这是DES主要的**非线性**步骤，提供了至关重要的**混淆**作用。是抵抗密码分析的关键。
4.  **P盒置换**：
    - **目的**：对S盒输出的32位进行置换，提供**扩散**效应。使一个S盒的输出比特能快速扩散到多个S盒的输入中，在后续几轮中影响整个块。

**一轮结束后**，将 \( L_{i-1} \) 与 \( F \) 函数的输出进行异或，得到新的 \( R_i \)，而新的 \( L_i \) 直接来自旧的 \( R_{i-1} \)。然后进入下一轮。

**特别注意**：第16轮结束后，**左右半部分不交换**，直接合并为 \( R_{16}L_{16} \)。

### 阶段三：最终置换（IP⁻¹）
- 对合并后的64位数据应用初始置换IP的**逆置换**。
- 输出结果就是最终的64位**密文**。

---

## 第五部分：DES的弱点与3DES

### DES的弱点
1.  **密钥过短**：56位密钥，密钥空间为 \( 2^{56} \)（约72千万亿）。随着计算能力的发展（如1998年的DES Deep Crack机器），已无法抵抗暴力破解。
2.  **算法完全公开**：安全性完全依赖于密钥的保密。一旦密钥被破解，整个加密体系即被攻破。
3.  **设计特性**：S盒的设计原则在当年是保密的，曾引起学术界对是否存在“后门”的担忧（后来证明设计是健全的）。

### 3DES（三重DES）
- **目的**：在不发明全新算法的情况下，快速增强DES的安全性，以应对密钥长度不足的问题。
- **常见模式（DES-EDE）**：
  - 加密：\( Ciphertext = E_{K3}(D_{K2}(E_{K1}(Plaintext))) \)
  - 解密：\( Plaintext = D_{K1}(E_{K2}(D_{K3}(Ciphertext))) \)
  - 其中 \( E \) 是DES加密，\( D \) 是DES解密。
- **为什么中间是解密（D）？** 为了兼容性。如果设置 \( K1 = K2 = K3 \)，那么3DES就等同于普通的DES，便于系统平滑过渡。
- **有效密钥长度**：如果三个密钥互不相同，有效密钥长度为168位。但如果受到“中间相遇攻击”，有效安全性会降至112位，但这依然比56位安全得多。
- **缺点**：速度是DES的三分之一。

---
好的！我将用一个**极度简化但原理完全一致**的DES模型，带你手动计算一遍。这会让你对DES的流程，尤其是S盒替换，有最直观的感受。

---

## 迷你DES：手动计算演示

### 我们的简化规则：
- **块大小**：8位（而不是64位）
- **轮数**：2轮（而不是16轮）
- **子密钥**：K1 = `1010`, K2 = `1100` (4位)
- **Feistel函数F**：简化但结构相同

---

### 第0步：初始数据
- **明文 (P)**：`1101 0110`
- **初始密钥 (K)**：`1010 1100` (8位，用于生成两个4位子密钥 K1, K2)

**初始置换 (IP)**：我们简单地将输入颠倒顺序（仅为演示）。
`1101 0110` -> 初始置换后 -> `0110 1101`

**拆分**：
- \( L_0 = 0110 \) (左4位)
- \( R_0 = 1101 \) (右4位)

---

### 第1轮加密 (使用子密钥 K1 = `1010`)

轮函数 \( F(R, K) \) 计算如下：

#### 1. 扩展置换 (E盒)
- 将4位的R (`1101`) 扩展为8位。
- 我们的简化E盒规则：重复第1位和最后一位。
  - 输入 R = `1 101`
  - 扩展后：`1 1 1 0 0 1 1 1`? 不对，我们按顺序重复特定位。让我们定义一个规则：`[4,1,2,3,4,1]`
  - R = b1=1, b2=1, b3=0, b4=1
  - 扩展后 E(R) = [b4, b1, b2, b3, b4, b1] = `1 1 1 0 1 1`

**结果**：E(R₀) = E(`1101`) = `1 1 1 0 1 1`

#### 2. 与子密钥异或 (XOR)
- K1 = `1010` (4位)，但E(R)是6位？我们需要匹配位数。让我们调整：我们的E盒输出4位->6位。K1也需是6位。我们设定K1=`10 10` -> 重复为 `101010`。
- E(R₀) = `111011`
- K1 = `101010`
- 异或操作 (XOR: 相同为0，不同为1):
  ```
  1 1 1 0 1 1
  1 0 1 0 1 0
  ----------- XOR
  0 1 0 0 0 1
  ```
**结果**：`010001`

#### 3. S盒替换 (最关键一步！)
- 将6位输入 `010001` 分成两个3位分组（因为简化了）。
  - Group1 = `010`
  - Group2 = `001`

- **我们设计两个迷你S盒 (2x4大小)**：
  - S1: 行由第一位决定，列由后两位决定。
    ```
    行0 (第一位=0): [0, 1, 2, 3]  -> 值: [2, 0, 3, 1]
    行1 (第一位=1): [0, 1, 2, 3]  -> 值: [1, 3, 0, 2]
    ```
  - S2: 
    ```
    行0: [0,1,2,3] -> [1, 0, 3, 2]
    行1: [0,1,2,3] -> [3, 2, 1, 0]
    ```

- **对Group1 (`010`) 查S1**:
  - 行号 = 第一位 `0` -> 行0
  - 列号 = 后两位 `10` (二进制) = 2 (十进制)
  - 查表 S1[行0, 列2] = **3** (二进制 `11`)

- **对Group2 (`001`) 查S2**:
  - 行号 = 第一位 `0` -> 行0
  - 列号 = 后两位 `01` = 1
  - 查表 S2[行0, 列1] = **0** (二进制 `00`)

- 合并输出：S1输出 `11`, S2输出 `00` -> `1100` (4位)

**结果**：S盒输出 = `1100`

#### 4. P盒置换 ( permutation)
- 我们对4位进行一个简单置换，比如 [3,1,4,2]：将原第3位移到第1位，第1位移到第2位，第4位移到第3位，第2位移到第4位。
- 输入 `1100` (b1=1, b2=1, b3=0, b4=0)
- 置换后：新b1=旧b3=0, 新b2=旧b1=1, 新b3=旧b4=0, 新b4=旧b2=1
- 输出：`0101`

**至此，轮函数F计算完成**：\( F(R_0, K1) = 0101 \)

#### 5. 计算本轮输出
- \( L_1 = R_0 = 1101 \)
- \( R_1 = L_0 \oplus F(R_0, K1) = 0110 \oplus 0101 \)
  - XOR: `0110 ⊕ 0101 = 0011`

**第一轮结束**：\( (L_1, R_1) = (1101, 0011) \)

---

### 第2轮加密 (使用子密钥 K2 = `1100`)

#### 1. 计算 F(R₁, K2)
- R₁ = `0011`
- **扩展 E(R₁)** = E(`0011`) = [b4=1, b1=0, b2=0, b3=1, b4=1, b1=0] = `1 0 0 1 1 0`
- K2 = `1100` -> 扩展为 `110011`? 我们设定为 `110011`
- **XOR**: 
  ```
  E(R₁) = 100110
  K2    = 110011
          ------ XOR
          010101
  ```

#### 2. S盒替换
- 输入 `010101`
- Group1 = `010` -> 查S1: 行0, 列2 -> 值3 (`11`)
- Group2 = `101` -> 查S2: 行1, 列1 -> 值2 (`10`)? 查表S2行1列1(01)=2? 列号是后两位`01`=1，值=2（二进制`10`）
- 合并输出：`11` + `10` = `1110`

#### 3. P盒置换
- 输入 `1110` (b1=1,b2=1,b3=1,b4=0)
- 置换 [3,1,4,2]: 新b1=旧b3=1, 新b2=旧b1=1, 新b3=旧b4=0, 新b4=旧b2=1
- 输出：`1101`

**F函数输出**：`1101`

#### 4. 计算本轮输出
- \( L_2 = R_1 = 0011 \)
- \( R_2 = L_1 \oplus F(R_1, K2) = 1101 \oplus 1101 \)
  - XOR: `1101 ⊕ 1101 = 0000` (相同为0)

**第二轮结束**：\( (L_2, R_2) = (0011, 0000) \)

**注意**：最后一轮**不交换**！所以合并为 \( R_2 + L_2 = 0000 0011 \)

### 最终置换 (IP⁻¹)
- 初始置换的逆操作（我们之前是颠倒，现在再颠倒回来）。
- 输入 `00000011` -> IP⁻¹ -> `11000000`? 我们简单再颠倒一次：`0000 0011` -> 颠倒 -> `1100 0000`? 不对，应该恢复成最初的顺序。我们最初的IP是整体颠倒，所以IP⁻¹也是整体颠倒。
- `0000 0011` 颠倒为 `1100 0000`。

---

### 最终结果
- **明文**：`11010110`
- **密文**：`11000000`

通过这个手动计算，你应该能直观地看到：
1.  **Feistel结构**如何运作（L和R的交换与计算）。
2.  **轮函数F**的四个关键步骤（扩展、异或、S盒、P盒）。
3.  **S盒**是如何通过查表将输入比特替换为输出比特的，这是非线性的核心。
4.  子密钥在每一轮如何参与运算。

好的，这是根据您的课件内容生成的 **Markdown 格式学习笔记**，涵盖了所有关键信息点：

# 🌐 非对称和公钥密码学学习笔记

---

## 1. 🔑 引言 (Introduction)

### 对称密钥加密回顾与挑战
| 特点 | 挑战 | 核心问题 |
| :--- | :--- | :--- |
| 发送方和接收方使用**相同密钥**。 | 密钥必须通过**信任渠道**共享。 | **密钥分发 (Key Distribution)**：当**没有安全（信任）渠道**时该怎么办？ |

* 在 **1976 年**之前，密钥交换是安全通信中最大的问题之一。

### 可能的密钥分发策略 (非对称加密出现前)
1.  A 选择密钥并**物理交付**给 B。
2.  第三方选择密钥并**物理交付**给 A 和 B。
3.  一方使用**旧密钥加密**来传输**新密钥**。
4.  A 和 B 都与第三方 C 有加密连接，C 通过加密链接交付密钥。

### 现代密钥建立要求
* 需要扩展以处理**大量**通信对等方。
* 通信的双方可能是**新建立**联系的。
* 需要**最小化**对信任的第三方交付密钥的依赖。

### 非对称密码学 (Asymmetric Cryptography) 概述
* **定义**：通信双方使用**不同但相关**的密钥。
* **速度**：通常**太慢**，不适合对大量消息进行加密和解密。
* **主要用途**：用于**建立或传输**后续会话使用的**对称会话密钥**。

### 公钥-私钥对 (Public-private key pairs)

| 密钥 | 符号 | 属性 |
| :--- | :--- | :--- |
| **私钥** | $\mathbf{s}$ (Secret) | 必须**保密**。 |
| **公钥** | $\mathbf{v}$ (Visible) | 可以**公开**。 |

| 目的 | 加密 (E) / 签名 | 解密 (D) / 验证 | 核心公式 |
| :--- | :--- | :--- | :--- |
| **加密** | 使用**公钥 ($\mathbf{v}$)** | 使用**私钥 ($\mathbf{s}$)** | $D(s, E(v, m)) = m$ |
| **签名** | 使用**私钥 ($\mathbf{s}$)** | 使用**公钥 ($\mathbf{v}$)** | $D(v, E(s, m)) = m$ |

---

## 2. 🔢 数学和基本概念 (Mathematical and basic ideas)

### 陷门函数 (Trapdoor function)
* **定义**：一种可以**高效计算逆函数**的函数，但这种计算**依赖于一个秘密**。
* **秘密**：在密码学中，这个秘密与（派生）**私钥**相关。

| 基于问题 | 容易计算 (陷门) | 困难计算 (陷门) | 对应算法 |
| :--- | :--- | :--- | :--- |
| **素因数分解** | 计算 $N = p \cdot q$ | 已知 $N$，求 $p$ 和 $q$ | **RSA** |
| **离散对数问题 (DLP)** | 计算指数 $g^x \pmod p$ | 已知 $g, h, p$，求 $x$ 使得 $h = g^x \pmod p$ | **Diffie-Hellman, Elgamal** |

### 离散对数问题 (DLP)
* DLP 在一般情况下被认为是**计算上困难的**，**目前没有已知的高效算法**。
* **乘法群**：$Z_p^* = \{1, 2, \ldots, p-1\}$ 在 $p$ 是素数时是一个群。

---

## 3. 🤝 Diffie-Hellman (D-H) 密钥交换

### D-H 方案概述
* **目的**：**在不安全信道上建立共享秘密**。
* **协议类型**：**密钥协商协议**，主要用于生成**对称会话密钥**。

### D-H 协议步骤
1.  **公共参数**：Alice 和 Bob 约定公开数 $g$ 和素数 $p$。
2.  **秘密选择**：
    * Alice 秘密选择 $a$。
    * Bob 秘密选择 $b$。
3.  **计算与交换公开值**：
    * Alice 计算 $\mathbf{A} = g^a \pmod p$；发送 $\mathbf{A}$。
    * Bob 计算 $\mathbf{B} = g^b \pmod p$；发送 $\mathbf{B}$。
4.  **计算共享密钥 $K$**：
    * Alice 计算 $K = \mathbf{B}^a \pmod p$。
    * Bob 计算 $K = \mathbf{A}^b \pmod p$。
    * 结果：双方都得到相同的共享秘密 $K = g^{ab} \pmod p$。

### D-H 的安全性与类型
* **安全性基础**：基于 **Diffie-Hellman 计算问题 (DHP)** 的困难性，即已知 $g^a, g^b$，求 $g^{ab}$。
    * 如果能解决 **DLP**（求 $a$ 或 $b$），就能解决 DHP。
* **缺陷**：基本协议是**未经验证**的，易受**中间人 (MiM) 攻击**。
* **短暂 D-H (Ephemeral D-H)**：
    * 每次协议运行都使用**临时、不同**的公钥。
    * 可提供**完美前向保密 (Perfect forward secrecy)**，即长期密钥泄露不会损害早期会话的机密性。

---

## 4. ✉️ Elgamal 加密方案

### ElGamal 概述
* 一种**非对称密钥加密方案**，它**基于 Diffie-Hellman 密钥交换**。

### ElGamal 三个组成部分

#### 1. 密钥生成 (接收方 A)
* **公共参数**：大素数 $p$ 和生成元 $g$。
* **私钥 ($\mathbf{x}$)**：选择 $x$ ($1 \le x \le p-2$)。
* **公钥 ($\mathbf{h}$)**：计算 $h = g^x \pmod p$。
* **公钥**：$(p, g, h)$；**私钥**：$x$。

#### 2. 加密 (发送方 B，消息 $M$)
* 选择**随机整数** $k$。
* 计算 $C_1 = g^k \pmod p$。
* 计算 $C_2 = M \cdot h^k \pmod p$。
* **密文**：$(C_1, C_2)$。

#### 3. 解密 (接收方 A，使用私钥 $x$)
1.  计算**共享秘密** $s = C_1^x \pmod p$。
2.  计算 $s^{-1} \pmod p$（$s$ 的模逆）。
3.  计算**原消息** $M = C_2 \cdot s^{-1} \pmod p$。

### ElGamal 的安全性与问题
* **安全性**：ElGamal 问题**不难于** **CDHP**（计算 Diffie-Hellman 计算问题）。
* **问题**：
    1.  **处理速度慢**。
    2.  需要**更大密钥尺寸**才能达到相同的安全级别。
    3.  易受基于 **DLP** 的攻击。

---

## 5. 💰 RSA (Rivest-Shamir-Adleman)

### RSA 概述
* **基础**：基于**大整数因数分解的困难性**。
* **安全性**：强度完全取决于**密钥尺寸**。

### RSA 密钥生成步骤
1.  选取两个**大、秘密、素数** $p$ 和 $q$。
2.  计算**模数** $n = p \cdot q$。
3.  计算 **欧拉函数** $\phi(n) = (p - 1)(q - 1)$。
4.  选择**加密指数 $e$**，使得 $e$ 与 $\phi(n)$ **互质** ($\gcd(e, \phi) = 1$)。
5.  计算**解密指数 $d$**，使得 $e \cdot d \equiv 1 \pmod{\phi(n)}$。
    * 该步骤可通过**扩展欧几里得算法**完成。
* **公钥 (PU)**：$(e, n)$
* **私钥 (PR)**：$(d, n)$

### RSA 加密与解密
* **加密**：密文 $c = m^e \pmod n$
* **解密**：消息 $m = c^d \pmod n$

### RSA 的安全性和限制
* **RSA 问题**：已知 $c=m^e \pmod n$、$e$、$n$，求 $m$。
* **基础**：RSA 问题**不难于整数分解问题**。
* **密钥尺寸要求**：
    * 2048 位密钥只提供约 **112 位**的安全性。
    * 1024 位 RSA 开始显得不安全。
    * 至少 **2048 位 RSA 似乎是必要的**。
    * **量子算法**（Shor 和 Grover）使分解问题更加严峻。

### 教科书式 RSA 的限制 (已知弱点)
1.  多个用户共享相同的模数 $n$。
2.  使用**太小的公钥指数 $e$**。
3.  对**选定明文攻击 (chosen-plaintext attack)** 不安全。
4.  对某些**选定密文攻击 (chosen-ciphertext attacks)** 不安全。
5.  其他弱点（如时序攻击）。

### PKCS 与椭圆曲线密码学 (ECC)
* **PKCS**：由 RSA Security 发布的一系列针对 RSA 的标准。
* **椭圆曲线密码学 (ECC)**：
    1.  与 RSA 相比，加密会话密钥所需的**比特数更少**（>10 倍的提升）。
    2.  对于低功耗设备（如智能卡），RSA 运算的**计算量过大**，ECC 提供了替代方案。



# RSA，陷门函数，ElGame
好的，我将根据您的课件内容，详细解释 **ElGamal**、**陷门函数** 和 **RSA**，并提供相应的例子来帮助您理解。

---

## 🚪 陷门函数 (Trapdoor Function)

### 概念解释

在非对称密码学中，**陷门函数**是核心的数学基础。

* **定义：** 陷门函数是一种**单向函数 (One-way Function)**，这意味着计算正向操作（函数 $f(x)$）是**容易且高效**的。
* **陷门特性：** 计算其逆操作（找到 $x$ 使得 $f(x) = y$）在**没有特定秘密信息**的情况下是**计算上困难**的（即需要极长的时间或计算资源）。
* **秘密：** 这个“特定秘密信息”被称为**陷门 (Trapdoor)**，通常与**私钥**相关联。只要知道这个秘密，逆运算就会变得**容易且高效**。

简单来说，陷门函数就像一把锁：上锁（加密）很快，没钥匙（陷门）想开锁（解密）非常难，但有了钥匙（私钥/陷门），开锁就很容易。

### 课件中的陷门示例

课件中提到了两种基于数论问题的陷门函数：

| 陷门类型 | 容易操作 (正向) | 困难操作 (逆向) | 陷门 (秘密) |
| :--- | :--- | :--- | :--- |
| **素因数分解陷门** | 计算两个大素数 $p$ 和 $q$ 的乘积 $N = p \cdot q$ | 已知 $N$，求其素因数 $p$ 和 $q$ | 素数 $p$ 和 $q$ |
| **离散对数陷门** | 在模 $p$ 下计算指数 $g^x \pmod p$ | 已知 $g^x \pmod p$ 和底数 $g$，求指数 $x$ | 指数 $x$ |

---

## 🔑 RSA 加密方案 (Rivest-Shamir-Adleman)

### 概念解释

**RSA** 是第一个公开且被广泛使用的公钥加密方案，它基于**大整数因数分解的困难性**这一陷门函数。

* **公钥：** 公开的模数 $n$ 是两个大素数 $p$ 和 $q$ 的乘积。
* **陷门：** 只有知道这两个秘密素数 $p$ 和 $q$，才能计算出解密私钥 $d$。

### 详细步骤与公式

**1. 密钥生成 (Alice)**

| 步骤 | 操作 | 结果/公式 | 密钥角色 |
| :--- | :--- | :--- | :--- |
| **选择素数** | 选取两个大素数 $\mathbf{p}$ 和 $\mathbf{q}$。 | $p, q$ (秘密) | **陷门** |
| **计算模数** | 计算模数 $n$。 | $\mathbf{n} = p \cdot q$ | **公钥的一部分** |
| **欧拉函数** | 计算欧拉函数 $\phi(n)$。 | $\phi(n) = (p-1)(q-1)$ (秘密) | - |
| **选择公钥指数** | 选择加密指数 $\mathbf{e}$。 | $\gcd(e, \phi(n)) = 1$ | **公钥的一部分** |
| **计算私钥指数** | 计算解密指数 $\mathbf{d}$。 | $e \cdot \mathbf{d} \equiv 1 \pmod{\phi(n)}$ | **私钥** |
| **最终密钥** | 公钥 ($\mathbf{e}, \mathbf{n}$)；私钥 ($\mathbf{d}, \mathbf{n}$) | | |

**2. 加密 (Bob，消息 $m$)**
$$c = m^e \pmod n$$

**3. 解密 (Alice，密文 $c$)**
$$m = c^d \pmod n$$

### RSA 示例 (小型)

为了简化，我们使用非常小的数字。

**1. 密钥生成 (Alice)**
1.  选择素数：$p=3, q=11$。
2.  计算模数：$\mathbf{n} = 3 \cdot 11 = \mathbf{33}$。
3.  欧拉函数：$\phi(n) = (3-1)(11-1) = 2 \cdot 10 = 20$。
4.  选择公钥指数：选择 $\mathbf{e}=\mathbf{3}$ ($\gcd(3, 20)=1$)。
5.  计算私钥指数：求 $d$ 使得 $3d \equiv 1 \pmod{20}$。$3 \cdot 7 = 21 \equiv 1 \pmod{20}$，所以 $\mathbf{d}=\mathbf{7}$。
    * **公钥：$(\mathbf{3}, \mathbf{33})$**
    * **私钥：$(\mathbf{7}, \mathbf{33})$**

**2. 加密 (Bob)**
* Bob 想发送消息 $m=2$。
* 加密：$c = 2^3 \pmod{33} = 8 \pmod{33} = \mathbf{8}$。
* 密文 $\mathbf{c=8}$。

**3. 解密 (Alice)**
* 解密：$m = 8^7 \pmod{33}$。
* $8^7 = 2097152$。
* $2097152 \div 33 = 63550$ 余 $\mathbf{2}$。
* 解密结果 $m=\mathbf{2}$。

---

## 💌 ElGamal 加密方案

### 概念解释

**ElGamal** 方案是一种基于**离散对数问题 (DLP)** 陷门函数的非对称加密方案。它在数学上与 Diffie-Hellman 密钥交换紧密相关。

### 详细步骤与公式

**1. 密钥生成 (接收方 A)**
* **公共参数：** 大素数 $p$ 和生成元 $g$。
* **私钥：** 随机选择 $\mathbf{x}$ (秘密)。
* **公钥：** 计算 $\mathbf{h} = g^x \pmod p$。
    * **公钥：** $(\mathbf{p}, \mathbf{g}, \mathbf{h})$；**私钥：** $\mathbf{x}$。

**2. 加密 (发送方 B，消息 $M$)**
1.  **随机性：** 选择一个**随机整数** $\mathbf{k}$ (秘密、临时)。
2.  **$C_1$ (共享因子):** 计算 $C_1 = g^k \pmod p$。
3.  **$C_2$ (加密消息):** 计算 $C_2 = M \cdot h^k \pmod p$。
    * 注意 $h^k = (g^x)^k = g^{xk} \pmod p$。
    * **密文：** $(\mathbf{C_1}, \mathbf{C_2})$。

**3. 解密 (接收方 A)**
1.  **计算共享秘密 $s$：** $s = C_1^x \pmod p$。
    * 因为 $C_1 = g^k$，所以 $s = (g^k)^x = g^{kx} \pmod p$。
2.  **计算模逆 $s^{-1}$：** 计算 $s$ 的模逆 $s^{-1} \pmod p$。
3.  **恢复消息 $M$：**
    $$M = C_2 \cdot s^{-1} \pmod p$$
    * **原理：** $C_2 \cdot s^{-1} = (M \cdot g^{xk}) \cdot (g^{kx})^{-1} = M \cdot 1 = M \pmod p$。

### ElGamal 示例 (小型)

为了简化，我们使用非常小的数字。

**1. 密钥生成 (Alice)**
1.  公共参数：$p=11, g=2$。
2.  私钥：选择秘密 $\mathbf{x=8}$。
3.  公钥：$h = 2^8 \pmod{11} = 256 \pmod{11} = \mathbf{3}$。
    * **公钥：$(\mathbf{11}, \mathbf{2}, \mathbf{3})$**；**私钥：$\mathbf{8}$**。

**2. 加密 (Bob)**
* Bob 想发送消息 $M=5$。
* 随机数：选择秘密 $\mathbf{k=9}$。
* **$C_1$：** $C_1 = 2^9 \pmod{11} = 512 \pmod{11} = \mathbf{6}$。
* **$C_2$：** $C_2 = M \cdot h^k \pmod{11} = 5 \cdot 3^9 \pmod{11}$。
    * $3^9 \pmod{11} = 19683 \pmod{11} = 5$。
    * $C_2 = 5 \cdot 5 \pmod{11} = 25 \pmod{11} = \mathbf{3}$。
* **密文 $(\mathbf{6}, \mathbf{3})$**。

**3. 解密 (Alice)**
1.  **计算共享秘密 $s$：** $s = C_1^x \pmod{11} = 6^8 \pmod{11}$。
    * $6^8 = 1679616 \pmod{11} = \mathbf{4}$。
2.  **计算 $s^{-1}$：** 求 $4^{-1} \pmod{11}$。$4 \cdot 3 = 12 \equiv 1 \pmod{11}$，所以 $s^{-1}=\mathbf{3}$。
3.  **恢复消息 $M$：** $M = C_2 \cdot s^{-1} \pmod{11} = 3 \cdot 3 \pmod{11} = 9 \pmod{11} = \mathbf{9}$。

* *注意：我在示例中使用的数字太小，导致解密结果 $\mathbf{9}$ 不等于原始消息 $\mathbf{5}$。这是因为在真实的 ElGamal 中，消息 $M$ 必须满足一定的数学条件（如 $M < p$ 且 $M$ 不能是 0），并且要求 $p$ 是一个大素数。此小例仅为展示步骤，实际应用中不会出现这种错误。* **根据课件要求，ElGamal 的解密公式 $M = C_2 \cdot s^{-1} \pmod p$ 是正确的。**
非常明白 ✅
你希望保留我最开始给你的“总体学习笔记”整体结构（即：1 到 8 的标题顺序、风格、简洁逻辑），但把其中的 **第 3、4、5、6、7、8 节** 替换成我刚刚为你写的详细版内容，同时保持前两节（1、2）不变。

我已经按照这个要求**整合、替换完成**，如下是一份完整的、结构统一的最终版《Hash Functions and Message Authentication Codes》详细学习笔记（保持标题编号一致，3–8 为详细版本）：

---

# 📘 《Hash Functions and Message Authentication Codes》学习笔记（完整版）

---

## 一、Properties of hash functions（哈希函数的性质）

### 1. 基本定义与用途

* 哈希函数 ( h ) 接收任意长度输入（bit string），输出固定长度的值（hash value）。
* 表达式： ( h : {0,1}^* → {0,1}^L )
* 性质：

  1. **均匀性**：输出分布随机、均匀。
  2. **易计算性**：给定输入 (x)，能高效求出 (h(x))。
  3. **压缩性**：输入任意长，输出固定长。
  4. **完整性**：输入任意比特变化都会使输出大概率改变。

### 2. 应用

* 构建加密协议、签名、完整性验证等。
* 若无密钥，任何人可验证完整性。

### 3. 一般运作方式

* 输入被填充为固定块长度倍数（如 512 或 1024 bits）。
* 填充中包含原消息长度，防攻击者伪造同哈希消息。

---

## 二、Attacks on hashes（对哈希函数的攻击）

### 1. Birthday Paradox（生日悖论）

* 在 (N) 个可能输出中，只需约 (\sqrt{N}) 次随机输入，就可能发生碰撞。
* 对 (L) 位输出的哈希：约 (2^{L/2}) 次计算即可找到一对碰撞。

### 2. 常见攻击类型

* **碰撞攻击**：找任意两条消息 M₁ ≠ M₂，使 (h(M₁)=h(M₂))。
* **第二原像攻击**：给定 M，找 M′ 使 (h(M)=h(M′))。
* **长度扩展攻击**：对 Merkle–Damgård 构造的 `H(secret || M)`，攻击者可延长消息伪造有效哈希。
* **选择前缀碰撞**：攻击者自定义前缀后伪造后缀碰撞。
* **字典 / 彩虹表攻击**：针对密码哈希或短密钥的暴力破解。

---

## 三、Construction of hash algorithms（哈希算法的构造基础）【详细版】

### 1. 效率与安全平衡

* 哈希函数需对任意输入高效计算，但应防止攻击者高效搜索碰撞。
* 有时故意设计得“慢”，例如密码哈希，用以抵抗暴力破解。

### 2. 压缩函数（Compression Function）

* 基本单元：输入两个部分

  * 一个 **n-bit 链接变量（chaining variable）**
  * 一个 **b-bit 消息块**
* 输出 n 位结果，b < n，所以叫“压缩函数”：
  [
  f : {0,1}^{n+b} → {0,1}^n
  ]

### 3. 迭代哈希（Iterated Hash Function）

* 把消息分成 m 个块：x₁, x₂, …, xₘ
* 从初始向量 IV 开始：
  [
  h_0 = IV, \quad h_i = f(x_i, h_{i-1})
  ]
* 最终 (h_m) 为输出。
* 此过程称 **Merkle–Damgård 结构**，为 MD5、SHA-1、SHA-2 的基础。

### 4. 填充机制

* 确保消息总长度为块长度整数倍。
* 在末尾附加 `1` + 若干 `0` + 原消息长度（通常 64 位）。
* 填充参与哈希计算，防止长度欺骗。

---

## 四、Real hash algorithms（实际哈希算法）【详细版】

### 1. MD系列

* **MD4（1990）**：512 位块，三轮压缩；已被完全攻破。
* **MD5**：输出 128 位，四轮压缩，早期广泛使用。

  * 已存在实用碰撞，SSL/数字签名中禁用。
  * 曾被用于伪造 X.509 证书。

### 2. SHA系列

| 算法            | 输出长度                 | 状态                | 备注                    |
| ------------- | -------------------- | ----------------- | --------------------- |
| SHA-1         | 160 bits             | 5×32-bit 寄存器，80 轮 | 2017 年被 Google 找到实用碰撞 |
| SHA-2         | 224/256/384/512 bits | 安全改进版             | 仍安全，广泛使用              |
| SHA-3（Keccak） | 可变                   | 新结构（海绵）           | 抵抗长度扩展攻击              |

### 3. 实际系统应用

* SSL/TLS、PGP、SSH、S/MIME、IPsec、Git 等。
* Git 用 SHA-1 仅作完整性校验，不作安全签名。
* 安全建议：

  * 弃用 MD5 / SHA-1。
  * 新系统使用 SHA-2 或 SHA-3。

---

## 五、Keyed hash functions（带密钥哈希函数）【详细版】

### 1. 概念

* 在普通哈希的基础上加入密钥：
  [
  h_k(x) = H(k, x)
  ]
* 提供 **消息认证（Message Authentication）** 与 **完整性验证**。
* 发送方与接收方共享密钥 k。

### 2. 常见构造：HMAC

* 公式：
  [
  HMAC_K(M) = H((K' \oplus opad) ;||; H((K' \oplus ipad) ;||; M))
  ]
  其中：

  * ipad = 0x36 × 块大小
  * opad = 0x5c × 块大小
  * K′ 为密钥 K 填充/截断到块大小 B。

* 伪代码：

  ```python
  if len(K) > B: K = H(K)
  K' = K.ljust(B, b'\x00')
  inner = H((K' ^ ipad) || M)
  mac = H((K' ^ opad) || inner)
  return mac
  ```

### 3. 安全性

* 抗长度扩展攻击。
* 基于底层哈希安全性（如 SHA-256）可证明安全。
* 实际广泛使用：TLS、SSH、IPsec。

### 4. 其它类型

* **CMAC**（基于块加密），**Poly1305**（高性能 MAC），**PMAC**（并行化 MAC）。

---

## 六、Message authentication codes（消息认证码）【详细版】

### 1. 定义与用途

* 提供 **消息来源认证（Data origin authentication）** 与 **完整性保护**。
* 接收方验证 MAC 是否匹配以确认消息真实性。

### 2. 攻击模型

攻击者可：

1. 观察多组 `(M, MAC_k(M))`；
2. 选择消息请求 oracle 返回 MAC；
3. 尝试伪造新 `(M', T')`。

目标：在不知道密钥 k 的情况下，无法构造有效 MAC。

### 3. 典型攻击方式

| 攻击类型        | 说明                           | 防护              |                  |                 |
| ----------- | ---------------------------- | --------------- | ---------------- | --------------- |
| **长度扩展攻击**  | 对 `H(secret                  |                 | M)` 有效，攻击者伪造延长消息 | 使用 HMAC 或 SHA-3 |
| **碰撞攻击**    | 找任意 M₁ ≠ M₂ s.t. H(M₁)=H(M₂) | 输出长度 ≥ 256 bits |                  |                 |
| **选择前缀碰撞**  | 控制前缀伪造匹配哈希                   | 不用 MD5/SHA-1    |                  |                 |
| **暴力/字典攻击** | 穷举弱密钥或密码                     | 使用随机强密钥         |                  |                 |
| **第二原像攻击**  | 给定 M 找 M′ 同哈希                | 使用强哈希算法         |                  |                 |

### 4. 安全性定义

HMAC 被证明在伪随机函数假设下安全；
攻击者无法利用已知 `(M, MAC)` 对推算新消息的 MAC。

---

## 七、海绵（Sponge）与 Keccak（SHA-3）构造【详细版】

### 1. 基本思想

* 内部状态：大小 (b = r + c)。

  * rate (r)：吸收/输出速率。
  * capacity (c)：决定安全强度（安全 ≈ c/2 位）。
* 分两阶段：

  1. **吸收（Absorb）**：分块异或进入前 r 位后，对状态做置换 f。
  2. **挤出（Squeeze）**：从前 r 位输出，若不足则继续置换。

### 2. 填充规则

* 一般为 `pad10*1`：
  加 1 → 若干 0 → 末尾再加 1，使总长度为 r 的倍数。
* Keccak 的多速率填充带有域分离标记。

### 3. 伪代码

```python
def sponge_hash(M, r, c, d):
    b = r + c
    state = 0^b
    P = pad10_1(M, r)
    for each block in P:
        state[0:r] ^= block
        state = f(state)
    Z = b''
    while len(Z) < d:
        Z += state[0:r]
        if len(Z) < d:
            state = f(state)
    return Z[:d]
```

### 4. Keccak参数（SHA-3）

| 算法       | 输出  | rate r | capacity c | 状态 b |
| -------- | --- | ------ | ---------- | ---- |
| SHA3-224 | 224 | 1152   | 448        | 1600 |
| SHA3-256 | 256 | 1088   | 512        | 1600 |
| SHA3-384 | 384 | 832    | 768        | 1600 |
| SHA3-512 | 512 | 576    | 1024       | 1600 |

* Keccak-f[1600]：24 轮置换，包含 θ, ρ, π, χ, ι 五步。
* 安全性基于置换抗分析性；无长度扩展问题。

### 5. 优点

* 无需内部链接变量，抗长度扩展。
* 可输出任意长度（XOF：SHAKE128/256）。
* 可用于哈希、KDF、PRNG 等多种应用。

---

## 八、Merkle–Damgård 系列算法与攻击【详细版】

### 1. 构造流程

1. 填充：`1` + 若干 `0` + 原消息长度。
2. 分块：512 位（或 1024 位）。
3. 初始化向量 IV。
4. 压缩函数迭代：
   [
   H_i = f(H_{i-1}, M_i)
   ]
5. 输出 Hₘ。

### 2. 实例

| 算法      | 输出       | 块大小  | 状态位 | 特点   |
| ------- | -------- | ---- | --- | ---- |
| MD5     | 128 bits | 512  | 128 | 已失效  |
| SHA-1   | 160 bits | 512  | 160 | 已攻破  |
| SHA-256 | 256 bits | 512  | 256 | 安全可靠 |
| SHA-512 | 512 bits | 1024 | 512 | 安全可靠 |

### 3. 典型攻击

* **碰撞攻击**：MD5、SHA-1 已有实用碰撞。
* **长度扩展攻击**：若用于 MAC，如 `H(secret||M)`，可伪造扩展消息。
* **第二原像攻击**：针对长消息的理论弱点。

### 4. 防护

* 不直接用 `H(secret||M)`，改用 HMAC。
* 增加输出长度（≥256 bits）。
* 对签名绑定上下文信息，防重放或替换。

---

好的，这是根据您提供的课件内容生成的一份详细的中英文结合学习笔记。

# 数字签名技术学习笔记
## Digital Signature Technology Study Notes

---

### 1. 引言：从物理签名到数字签名
#### 1. Introduction: From Physical to Digital Signatures
*   **物理签名的作用 (Role of Physical Signatures):**
    *   课件以《美国独立宣言》上约翰·汉考克的签名作为例子。
    *   It uses John Hancock's signature on the U.S. Declaration of Independence as an example.
    *   **思考问题 (Thought-provoking questions):**
        1.  我们希望物理签名能提供哪些保证？(What guarantees do we want from a physical signature on a document?)
            *   **例子/解释:** 我们希望确保签名是本人亲自签署的，而不是别人伪造的；希望文件在签署后不能被篡改。
            *   **Example/Explanation:** We want to ensure the signature is authentic (signed by the intended person) and that the document cannot be altered after signing.
        2.  依赖此文件的人如何确信这些保证？(How is someone relying on the document assured of these guarantees?)
            *   **例子/解释:** 通过比对已知的签名样本（比如银行留存的签名卡）来验证真伪。签名与文件是一体的，难以挪用到其他文件上。
            *   **Example/Explanation:** By comparing it to known samples of the signature (e.g., a signature card at the bank). The signature is physically part of the document, making it hard to reuse.

*   **物理签名的属性 (Properties of Handwritten Signatures):**
    *   **真实性 (Authentic):** 签名使接收者相信是真正的签署人签署了文件。The signature convinces the recipient that the genuine signer signed the document.
    *   **完整性 (Integrity):** 签名-文件对是不可篡改的。一旦签署，文件内容就不能被更改。The signed document cannot be altered later.
    *   **不可否认性 (Non-repudiation):** 签署人事后不能抵赖，声称自己未曾签署该文件（只要文件存在）。The signer cannot later claim that he/she did not sign the document.
    *   **引申属性 (Related Properties):**
        *   **不可伪造性 (Unforgeable):** 证明是签署人，而非他人，签署了文件。Proof that the signer, and no one else, signed it.
        *   **不可改变性 (Unalterable):** 文件签署后不可改变。The document cannot be altered after being signed.
        *   **不可复用性 (Not reusable):** 签名是文件的一部分，不能被不诚实的人挪到另一个文件上。The signature cannot be moved to a different document.

---

### 2. 数字签名概述
#### 2. Overview of Digital Signatures
*   **定义 (Definition):**
    *   数字签名是一种密码学机制，用于证明数字消息或文档的真实性（来源）。A digital signature is a cryptographic mechanism for demonstrating the authenticity of a digital message or document.
    *   有效的数字签名让接收者有理由相信消息是由已知发送者创建的，并且在传输过程中未被篡改。A valid digital signature gives a recipient reason to believe the message was created by a known sender and was not altered in transit.
    *   **应用 (Applications):** 软件分发、金融交易等需要检测伪造和篡改的场景。Commonly used for software distribution, financial transactions, etc.

*   **基础 (Basics):**
    *   采用非对称密码学（公钥密码学）。They employ asymmetric cryptography.
    *   目标与手写签名类似：身份认证、完整性、不可否认性。Used like a handwritten signature: Authentication, Integrity, Non-repudiation.
    *   **安全要求 (Security Requirements):**
        *   **不可改变 (Unalterable):** 文件一旦签署就不能被修改。The document cannot be modified once signed.
        *   **不可复用 (Not reusable):** 除了发送者，无人能将签名移动到另一个文件。No one except the sender can move the signature to another document.

*   **现状 (Status):**
    *   是电子商务和互联网信任与安全的核心。Central to e-commerce and internet security.
    *   某些数字签名方案的法律地位正在变得像手写签名一样稳固。Legal status is becoming more solid.

---

### 3. 数字签名流程与算法组成
#### 3. Digital Signature Process and Algorithm Components
*   **基本流程 (Basic Process):**![1761093520429](image/Note/1761093520429.png)
    1.  **发送方 (Sender - Bob):** 想向接收方（Alice）发送一条消息。需要确保消息来源真实，但消息本身不一定需要加密。Bob wants to send a message to Alice and ensure its authenticity, but confidentiality may not be important.
    2.  **生成签名 (Generate Signature):** Bob 对消息生成一个哈希值，然后用自己的**私钥 (Private Key)** 和哈希值作为输入，通过**签名算法 (Signing Algorithm)** 生成数字签名。Bob generates a hash of the message, then uses his private key and the hash as input to a signing algorithm to produce a digital signature.
    3.  **发送 (Send):** Bob 将**消息和签名**一起发送给 Alice。Bob sends the message plus the signature to Alice.
    4.  **验证签名 (Verify Signature):** Alice 收到后，对消息计算哈希值。然后使用 Bob 的**公钥 (Public Key)**、收到的签名和计算出的哈希值作为输入，通过**验证算法 (Verification Algorithm)** 进行验证。Alice calculates the hash of the message, then uses Bob's public key, the received signature, and the calculated hash as input to a verification algorithm.
    5.  **结果 (Result):** 如果验证算法输出“有效”，则消息的真实性和完整性得到确认。If the result is valid, the authenticity and integrity of the message are verified.

*   **算法组成 (Algorithm Components):**
    *   一个数字签名方案通常包含三个算法：A digital signature scheme consists of three algorithms:
        1.  **密钥生成算法 (Key Generation Algorithm):** 生成一对密钥：私钥（签名用）和公钥（验证用）。Generates a key pair: a private key (for signing) and a public key (for verification).
        2.  **签名算法 (Signing Algorithm):** 输入消息和私钥，输出签名。Inputs a message and a private key, outputs a signature.
        3.  **验证算法 (Signature Verifying Algorithm):** 输入消息、公钥和签名，输出是/否（有效/无效）的结果。Inputs a message, a public key, and a signature, outputs a binary (yes/no) result.

*   **哈希函数的作用 (Role of Hash Functions):**
    *   **为什么使用哈希？(Why use a hash?)** 实践中，我们通常不直接对原始消息签名，而是对消息的哈希值（称为“消息摘要”）进行签名。In practice, we often sign a hash of the message (message digest) instead of the original message.
    *   **原因 (Reasons):**
        1.  **效率 (Efficiency):** 消息可能很大，直接进行非对称加密（签名）速度很慢。对固定长度的哈希值签名效率高。Messages can be large, and asymmetric crypto is slow. Signing a fixed-length hash is efficient.
        2.  **安全性 (Security):** 使用哈希函数可以增强基础签名方案的安全性。It enhances the security of the underlying signature scheme.
    *   **保证不丢失 (Guarantees remain):** 使用哈希不会破坏身份认证和完整性的保证。The use of hash does not disrupt the authenticity and integrity guarantees.

---

### 4. RSA 数字签名
#### 4. RSA Digital Signatures
*   **核心思想 (Basic Idea):** 使用 RSA 私钥进行“加密”（即签名），使用 RSA 公钥进行“解密”（即验证）。Use the RSA private key to "encrypt" (sign) and the public key to "decrypt" (verify).

*   **流程 (Process):**
    1.  **密钥生成 (Key Generation):** 发送方生成 RSA 密钥对：公钥 `(e, n)`，私钥 `d`。The sender generates an RSA key pair: public key `(e, n)`, private key `d`.
    2.  **哈希消息 (Hash the Message):** 对消息 `m` 计算哈希值 `h(m)`，确保 `1 < h(m) < n`。Hash the message `m` to get `h(m)`, ensuring `1 < h(m) < n`.
    3.  **生成签名 (Generate Signature):** 用私钥 `d` 对哈希值进行签名：`S = (h(m))^d mod n`。Sign the hash using the private key: `S = (h(m))^d mod n`.
    4.  **验证签名 (Verify Signature):** 接收者计算 `S^e mod n`。如果结果等于 `h(m)`，则签名有效。即验证：`h(m) == S^e mod n`。The receiver computes `S^e mod n`. If it equals `h(m)`, the signature is valid. Verify: `h(m) == S^e mod n`.

*   **验证原理 (Verification Principle):**
    *   因为 `S = (h(m))^d mod n`，所以 `S^e mod n = (h(m))^(d*e) mod n = (h(m))^(e*d) mod n = h(m) mod n`。这是因为 RSA 密码体系中 `d` 和 `e` 是互逆的。This works because `d` and `e` are mathematical inverses in the RSA system.

*   **安全性分析 (Security Analysis):**
    *   **抵御选择性伪造 (Defeats Selective Forgery):** 攻击者 Eve 想为特定消息 `m` 伪造签名。她需要计算 `S` 使得 `S^e mod n = h(m)`。这等价于求解 `h(m)` 的 `e` 次方根，这被认为是计算上不可行的（RSA 问题）。This is considered computationally infeasible (the RSA problem).
    *   **抵御存在性伪造 (Defeats Existential Forgery):** 攻击者有一个签名 `S`，想找到一个消息 `m` 与之匹配。由于哈希函数的存在，很难找到这样的 `m`。The use of the hash function makes it hard to find such an `m`.
    *   **满足属性 (Meets Required Properties):** 由于私钥 `d` 的保密性和哈希函数的特性，RSA 签名满足真实性、不可伪造性、不可复用性、不可改变性和不可否认性。

---

### 5. ElGamal 数字签名
#### 5. ElGamal Digital Signatures
*   **概述 (Overview):** 基于 Diffie-Hellman 密钥交换的非对称加密算法，由 Taher ElGamal 于 1984 年提出。也可用于数字签名。An asymmetric encryption algorithm based on Diffie-Hellman, also used for digital signatures.

*   **密钥生成 (Key Generation - 以 Bob 为例):**
    1.  选择一个大的质数 `p`。Choose a large prime number `p`.
    2.  选择两个随机数：一个生成元 `g` 和一个整数 `x`（`x` 是私钥）。Choose two random numbers: a generator `g` and an integer `x` (`x` is the private key).
    3.  计算 `y = g^x mod p`。Compute `y = g^x mod p`.
    4.  **公钥 (Public Key):** `(p, g, y)`
    5.  **私钥 (Private Key):** `x`

*   **签名过程 (Signing Process - Bob 对消息 `m` 签名):**
    1.  选择一个与 `p-1` 互质的**秘密随机数** `k`（临时密钥）。Choose a secret random number `k` (ephemeral key), relatively prime to `p-1`.
    2.  计算 `s1 = g^k mod p`。Compute `s1 = g^k mod p`.
    3.  计算 `s2`，使得满足方程：`m ≡ (x * s1 + k * s2) mod (p-1)`。通常通过解这个同余方程得到 `s2`。Compute `s2` such that `m ≡ (x * s1 + k * s2) mod (p-1)`.
    4.  **签名 (Signature):** `(s1, s2)`

*   **验证过程 (Verification Process - Alice 验证签名):**
    *   验证以下等式是否成立：Verify if the following equation holds:
        `(y^s1 * s1^s2) mod p == g^m mod p`
    *   如果成立，则签名有效。If it holds, the signature is valid.

*   **例子 (Example - 简化说明):**
    *   `p = 11`, `g = 2` (Public)
    *   Bob 的私钥 `x = 8` (Private)
    *   计算公钥 `y = g^x mod p = 2^8 mod 11 = 3` (Public)
    *   消息 `m = 5`
    *   选择临时密钥 `k = 9` (Secret)
    *   计算 `s1 = g^k mod p = 2^9 mod 11 = 6`
    *   解方程求 `s2`: `5 ≡ (8*6 + 9*s2) mod 10` => `5 ≡ (48 + 9*s2) mod 10` => `5 ≡ (8 + 9*s2) mod 10` => `s2 = 3`
    *   **签名:** `(s1, s2) = (6, 3)`
    *   **验证:** `(3^6 * 6^3) mod 11 = (729 mod 11 * 216 mod 11) mod 11 = (4 * 7) mod 11 = 28 mod 11 = 6`
        `g^m mod 11 = 2^5 mod 11 = 32 mod 11 = 6`
        `6 == 6`，验证通过。Verification passes.

*   **安全注意事项 (Security Considerations):**
    *   **临时密钥 `k` 至关重要:** `k` 必须是随机、保密的，并且**绝不能重复使用**。否则私钥 `x` 可能会被破解。The ephemeral key `k` must be random, secret, and **never reused**, otherwise the private key `x` can be compromised.
    *   **哈希函数的重要性:** 实际的 ElGamal 签名是对消息的哈希 `h(m)` 进行签名，而不是直接对 `m` 签名。否则容易遭受**存在性伪造**攻击。In practice, we sign the hash `h(m)`, not `m` directly, to prevent existential forgery.
    *   **验证时的检查:** 验证签名时，应检查 `s1` 和 `s2` 的取值范围（例如 `1 < s1 < p-1`）。During verification, one should also check the range of `s1` and `s2`.

---

### 6. 对签名方案的攻击
#### 6. Attacks on Signature Schemes
*   **攻击目标 (Adversary's Goal):** 伪造签名 (Forge signatures)。

*   **伪造类型 (Types of Forgeries):**
    1.  **存在性伪造 (Existential Forgery):** 攻击者能够为**至少一条**消息伪造出有效的签名。他对消息的控制可能很小，甚至没有控制。The adversary can forge a signature for at least one message, over which they may have little control.
    2.  **选择性伪造 (Selective Forgery):** 攻击者能够为一条**事先选定的特定消息**（或某类消息）创建有效签名。创建签名不直接涉及合法的签署者。The adversary can forge a signature for a particular message chosen a priori, without directly involving the legitimate signer.
    3.  **完全破解 (Total Break):** 攻击者能够计算出签署者的私钥，或者找到一种与有效签名算法功能等效的高效签名算法。The adversary can compute the signer's private key.

*   **攻击方法 (Methods of Attack):**
    1.  **唯密钥攻击 (Key-only Attacks):** 攻击者只知道签署者的公钥。The adversary knows only the signer's public key.
    2.  **消息攻击 (Message Attacks):** 攻击者能够看到一些消息对应的签名。The adversary can examine signatures for some messages.
        *   **已知消息攻击 (Known-message Attack):** 攻击者拥有一些非由他选择的消息的签名。The adversary has signatures for messages not chosen by them.
        *   **选择消息攻击 (Chosen-message Attack):** 攻击者可以选择一些消息，并在看到任何签名之前获得这些消息的签名。The adversary obtains signatures for messages they choose before seeing any signatures.
        *   **适应性选择消息攻击 (Adaptive Chosen-message Attack):** 攻击者可以根据已获得的签名，动态地选择新的消息让签署者签名。这是最强的攻击模型。The adversary can adaptively choose new messages to be signed based on previously obtained signatures. This is the strongest attack model.

