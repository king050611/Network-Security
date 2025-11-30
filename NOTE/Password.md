# 网络安全课程学习笔记：密码管理

## 1. 密码认证 (Password Authentication)

- **基本步骤 (Basic Steps)**: 
  1. **标识 (Identification)**: 通过提供用户名 (Username)
  2. **验证 (Verification)**: 使用预先约定的密钥 (Secret agreed in advance) - 密码 (Password)
  - *示例 (Example)*: 用户名 (Username): abdnuser123 密码 (Password): ************

## 2. 密码的互补数据 (Complementary Data for Passwords)

- **存储位置 (Storage)**: 通常存储在密码文件 (Password file) 中
- **要求 (Requirements)**: 互补数据必须能快速验证密码，不一定是密码本身
- **保密性 (Confidentiality)**: 密码必须足够保密，初始通信也需安全
- **双方责任 (Dual Responsibility)**:
  1. 系统需保护互补数据和使用位置 (System must have security around complementary data and places where used)
  2. 用户需保护密码，避免泄露 (User must have security around password and avoid leakage)
- *常见假设错误 (Common Assumption Errors)*: 这些假设经常不正确 (These assumptions are often incorrect)

## 3. 密码攻击向量 (General Attack Vectors on Passwords)

- **系统端 (System-side)**:
  1. 默认密码 (Default passwords)
  2. 暴力破解 (Brute force: try all possible passwords)
  3. 字典攻击 (Dictionary attack: guess passwords using common words)
  4. 直接窃取互补数据 (Steal complementary data directly, e.g., password file)
- **用户端 (User side)**:
  1. 抄写密码 (Copy knowledge, e.g., if found written-down)
  2. 窃听 (Snooping: shoulder-surfing, key-logging etc.)
  3. 社会工程学 (Social engineering)
  4. 共享 (Sharing)
  5. 伪造 (Spoofing)
- **通信渠道 (Communications channel)**: 窃听密码 (Eavesdrop password)
- **其他 (Other)**: 从密码重用推断 (Inference from password re-use elsewhere)
- *常见点 (Common Point)*: 许多攻击是混合的 (Many attacks are a mix)

## 4. 密码保护策略 (Protecting Passwords)

- **用户视角 (User perspective)**: 用户只关心保护自己的密码 (User may only care about protecting their own password)
- **系统管理员视角 (System manager perspective)**: 系统管理员关心保护所有用户密码 (System managers care about protecting all user passwords)
- *两个不同问题 (Two Different Problems)*: 
  1. 用户关心保护特定密码 (Attacker may only care about getting that particular password)
  2. 系统管理员关心保护所有密码 (Attacker may only care about finding some, or any one, of the passwords)

## 5. 密码文件保护选项 (Options for Protecting Password Files)

- **选项1: 明文存储 (Store passwords in the clear)**:
  - *缺点 (Disadvantages)*: 
    1. 文件是攻击者的主要目标 (These files are major targets for attackers)
    2. 历史证明它们可能被攻击者泄露 (History shows that they may well be compromised)
    3. 如果泄露，攻击者可以冒充合法用户 (If compromised, attacker can impersonate legitimate users)
  - *不推荐 (Not Recommended)*

- **选项2: 加密整个密码文件 (Encrypt the entire password file)**:
  - *缺点 (Disadvantages)*: 
    1. 每次验证都需要解密整个文件 (Have to decrypt entire file every time verification needed)
    2. 所有密码都会暴露 (All passwords are then exposed)
    3. 更改密码或新增用户时需加密整个文件 (Have to encrypt whole file every time password changed or new user enrolled)
    4. 如果加密被破解，所有明文密码都会被泄露 (If encryption cracked, all plaintext passwords compromised)

- **选项3: 加密单个密码 (Encrypt individual passwords next to user identities)**:
  - *缺点 (Disadvantages)*: 
    1. 用户密码在系统内部使用时仍暴露 (User password is still exposed during use when inside system)
    2. 攻击者可能在使用时发现密码 (Attacker may be able to discover it when in use)
    3. 如果攻击者能解密，可以发现所有密码 (If attacker can figure out how to decrypt, can discover all passwords)

- **选项4: 使用哈希函数 (Usual solution: cryptographic hash function)**:
  - *优点 (Advantages)*: 
    1. 使从互补信息反向推导原始密码变得困难 (Makes it hard to reverse complementary info into authentication info)
    2. 即使攻击者获得哈希密码，也无法获得原始密码 (Even if attacker gets hashed password, can't get original password)
    3. 如果需要提取任何密码（而非特定密码），可能稍微容易些 (Might be slightly easier if attacker gets whole password file and just needs to extract any password)

## 6. 加密 vs. 哈希密码 (Encrypting vs. Hashing Passwords)

- **哈希优点 (Arguments for hashing)**:
  1. 无需解密密码 (No real need to be able to decrypt passwords)
  2. 消除丢失加密密钥的风险 (Remove risk of lost encryption keys)
  3. 哈希产生足以保证 (Ability to produce a hash is sufficient assurance)

- **哈希缺点 (Arguments against hashing)**:
  1. 引入伪密码 (Pseudo-passwords: plaintexts that are not passwords for any user but hash to same value as genuine password)
  2. 哈希算法攻击被定期发现 (Attacks to break hashing algorithms are being regularly discovered)

- *主流观点 (Balance of opinion)*: 哈希是最佳选择 (Hashing is the best option)

## 7. UNIX-like系统中的密码保护 (Password Protection in UNIX-like Systems)

- **早期 (Originally)**:
  1. 密码文件包含明文密码 (Password file contained passwords in the clear)
  2. 对写入和读取进行保护 (Protected against being written or read)

- **后来 (Next)**:
  1. 加盐、加密密码 (Salted, encrypted passwords)
  2. 后来是加盐、哈希密码 (Later salted, hashed passwords)

- **现代 (Modern)**:
  1. 哈希密码存储在影子密码文件中 (Hashed passwords stored in shadow password files)
  2. 仅特权账户（如root）可读 (Only accounts with special privileges, e.g., root, can read)
  3. 文件示例 (Example): /etc/shadow, /etc/master.passwd (OS X: /var/db/shadow)

## 8. Windows中的密码保护 (Password Protection in Windows)

- **警告 (Warning)**: 一切可能已随Windows 10改变
- **Windows安全账户管理器 (Windows Security Account Manager, SAM)**
- **至少自XP以来 (At least since XP)**
- **存储哈希密码在数据库中 (Stores hashed passwords in database)**
- **直到最近 (Until quite recently)**: 存储在 \windows\system32\config
- **现在 (Now)**: 可能已在最新Windows版本中更改

## 9. 密码破解 (Cracking Passwords)

- **密码空间估计 (Password space estimate)**:
  - 保守估计 (Conservative estimate):
    1. 扩展ASCII字符: 2^8 (=256)
    2. 通常键盘上有少于2^7 (64)个字符
    3. 保守估计: 2^6 (=64)个字符

- **破解速度 (Cracking speed)**:
  - 单CPU: John the Ripper每秒约90,000,000次尝试 (2^27)
  - GPU: 约10^10或2^34次尝试/秒
  - 一年尝试次数: 约2^25
  - *计算 (Calculation)*: 2^17秒/天, 2^25秒/年

- **有资源的攻击者 (Well-resourced attacker)**:
  - 10^6 GPU: 一年可尝试2^79次
  - *平均情况 (On average)*: 只需搜索空间的一半 (On average, only half to search half the space)

## 10. 默认密码 (Default Passwords)

- **常见默认凭证 (Common default credentials)**:
  1. admin: admin, guest: guest
  2. 移动电话PIN码 (PIN for mobile/cell-phone)
  3. 手机数据网络密码 (Password for mobile-phone data networks)
  4. 路由器密码 (Router)
  5. 服务器密码 (Server)
  6. "帮助"网站 (e.g. http://www.phenoelit.org/)
- *问题 (Problem)*: 如果管理员和用户未更改 (Big problem if not changed by admins and users)
- *解决方案 (Solution)*: 需要培训和激励管理员和用户 (Need to train and incentivize admins and users)

## 11. 字典攻击 (Dictionary Attacks)

- **类型 (Types)**:
  1. **在线 (Online Type 1)**: 直接尝试认证 (Try to authenticate directly)
  2. **离线 (Offline Type 2)**: 获取密码文件后尝试 (Password file obtained by attacker)

- **离线攻击 (Offline Type 2)**:
  - *情况 (Situation)*: 密码文件被攻击者获取 (Password file obtained by attacker)
  - *方法 (Method)*: 
    1. 推断哈希函数 (Hash function inferred)
    2. 使用字典加速 (Use wordlist to speed up)
    3. 使用查找表、哈希链和彩虹表 (Use lookup tables, hash chaining and rainbow tables)
  - *工具 (Tools)*: John the Ripper

- **在线攻击 (Online Type 1)**:
  - *情况 (Situation)*: 密码文件不可用或无法使用
  - *方法 (Method)*: 直接尝试认证 (Try to authenticate directly)
  - *风险 (Risk)*: 可能导致锁定或发现 (May result in lock-out, or discovery)
  - *工具 (Tools)*: Hydra

## 12. 加盐 (Salting)

- **定义 (Definition)**: 一种进一步保护密码的技术
- **操作 (Process)**:
  1. 为每个用户的密码p附加额外信息s（盐）(Append additional information s, the salt, to each user's password p)
  2. 连接密码和盐: p :: s (Concatenate password and salt p :: s)
  3. 应用哈希函数: h = H(p :: s) (Apply hash function H to p :: s)
  4. 存储对(h, s) (Store the pair (h, s) on the system)
- *规则 (Rule)*: 没有两个用户获得相同的盐 (No two users get the same salt)
- *盐生成 (Salt generation)*: 通常生成为(伪)随机 (Salt is usually generated to be pseudo-random)

## 13. 加盐的优势 (Advantage of Salting)

- **主要优势 (Main advantage)**: 使同时攻击多个密码变得不可能
  1. 无法为多个密码同时搜索 (Makes it impossible to search for passwords of several users simultaneously)
  2. 为整个密码集合提供保护 (Gives herd-level protection)
- *示例 (Example)*: 如果两个用户有相同密码p，使用不同盐s1和s2，存储的互补数据为H(p::s1)和H(p::s2)，不同

## 14. 无盐系统攻击 (Attacks on Systems Without Salts)

- **攻击 (Attack)**:
  1. 尝试猜测p1；计算h1=H(p1)；检查整个密码文件
  2. 尝试p2；计算h2=H(p2)
  3. 对所有m个猜测重复此操作 (Do this for all m passwords: p1, p2, ..., pm)
- *计算量 (Computation)*: m次计算 (There are m computations involved)

## 15. 有盐系统攻击 (Attacks on Systems With n Known Salts)

- **攻击 (Attack)**:
  1. 对于对(h1, s1)，尝试用盐s1猜测p1；计算H(p1::s1)=h1,1；检查是否h1,1=h1
  2. 如果失败，尝试p2与盐s1，检查H(p2::s1)=h2,1=h1
  3. 对所有m个密码重复此操作
  4. 对于(h2, s2)，重新尝试所有m个密码与盐s2
  5. 对所有n个盐重复此操作
- *计算量 (Computation)*: n × m次计算 (There are n × m computations)
- *关键点 (Key Point)*: 无法在多个密码之间重用相同的测试哈希值 (Can't re-use same test hash value across multiple passwords)

## 16. 查看表和彩虹表 (Lookup and Rainbow Tables)

- **查看表 (Lookup table)**: 攻击者有预先计算的常见密码哈希表
- **彩虹表 (Rainbow tables)**: 查看表的巧妙概率修改版本
- **加盐优势 (Salting advantage)**: 使表变得太大 (Makes table too big)

## 17. 系统中不安全的存储和缓存 (Insecure Storage on System and Caching)

- **密码缓存 (Password caching)**: 密码存储在中间位置如缓冲区、缓存、网页中
- *问题 (Problem)*: 管理不在用户控制范围内 (Management not under user control)
- *示例 (Example)*: 早期网上银行，cookie存储用户信息允许用户在网页间回溯
  1. 关闭银行应用但不关闭浏览器，允许第二个用户访问第一个用户的账户
  2. 这是一个低级实现缺陷 (This is an example of a low-level implementation flaw)

## 18. 用户参与的密码/PIN系统攻击 (Attacks on Password/PIN Systems Where Users Play a Role)

- **猜测攻击 (Guessing attacks)**:
  1. 包括"配偶"攻击 (Including 'spouse' attacks)
  2. 使用关于用户的可猜测信息 (Use of guessable information about the user)
- **肩部窥视攻击 (Shoulder-surfing attacks)**
- **刷卡攻击 (Skimming attacks, e.g., at ATMs)**
- **窃听攻击 (Sniffing attacks: key loggers, click-and-clack attacks)**
- **伪造 (Spoofing)**
- **密码重用 (Password re-use)**

## 19. 伪造 (Spoofing)

- **定义 (Definition)**: 认证是不对称的 (Authentication is asymmetric)
- **方法 (Method)**:
  1. 诱使用户尝试向受损端点认证 (Trick user into trying to authenticate to a compromised end-point)
  2. 密码发送到错误地方 (Password is sent to wrong place)
  3. 用户可能被告知认证失败，然后被重定向回真实登录 (Authentication may appear to abort or fail, then user directed back to true log-in)
  4. 变体: 自动传递用户，使其实际登录 (Variant: pass user automatically, so they do actually log-in)
- *相关 (Related)*: 钓鱼和社交工程利用了类似特性 (Phishing and social engineering exploits have similar characteristics)

## 20. 伪造预防 (Spoofing Prevention)

- **显示失败登录次数 (Display failed log-ins)**:
  1. 如果第一次登录失败，第二次尝试被告知这是第一次尝试，则应怀疑 (If first login fails, and told at second attempt this is first attempt, should be suspicious)
- **相互认证 (Mutual authentication)**:
  1. 例如在分布式系统中，系统必须向用户认证 (e.g. in distributed system, system required to authenticate to user)
- **可信路径 (Trusted path)**:
  1. 保证用户与真实另一方通信 (Guarantee user communicates with true other party)
  2. 已认证连接，提供保密性(secrecy)和完整性 (Authenticated connection, providing confidentiality and integrity)
  3. 在本地OS上，守护程序常称为安全内核或参考监控器 (On local OS, guard often called security kernel or reference monitor)
  4. 在某些Windows版本中，最好使用CTRL-ALT-DEL获取安全注意序列 (In some Windows versions, better to do CTRL-ALT-DEL to get secure attention sequence)

## 21. 密码重用 (Password Re-use)

- **问题 (Problem)**: 密码数量增加 (Proliferation of passwords)
- **行为 (Behavior)**:
  1. 人们倾向于重用密码 (People tend to re-use them)
  2. 人们倾向于在多个服务之间共享密码 (People tend to share them across multiple services)
- *风险 (Risk)*: 大量人使用相同密码用于关键服务（如银行账户）和非关键网络服务 (Large numbers of people use same passwords for critical services e.g. bank accounts and non-critical stuff on web)

## 22. 选择密码 (Choosing Passwords)

- **密码构造策略 (Password construction policy)**:
  1. 组织设置密码策略 (Organizations set password policies)
  2. 策略规定密码必须如何构造 (These state how passwords must be constructed)
  3. 通常包括: 密码长度、内容、更改频率、登录尝试次数 (Password length, content, frequency of change, number of login attempts)
- **密码空间 (Password space)**: 所有可能密码的集合 (The set A of all possible passwords)
  1. 即长度不超过特定长度S的所有字符序列 (All sequences of characters that constitute allowable passwords, no greater than certain length S)

## 23. 通用Anderson公式 (The Generalised Anderson Formula)

- **公式 (Formula)**:
  1. P ≥ TG/N
  2. P: 攻击者在指定时间内猜中密码的概率 (Probability attacker guesses password in specified time period)
  3. G: 一单位时间内可测试的猜测数 (Number of guesses that can be tested in one time unit)
  4. T: 猜测发生的时间单位数 (Number of time units during which guessing occurs)
  5. N: 所有可能密码的数量 (Number of all possible passwords)

- **示例计算 (Example Calculation)**:
  - 设定 (Setup):
    1. 密码字符集: 96个字符 (96 characters)
    2. 每秒可测试10^4次猜测 (10^4 guesses per second)
    3. 安全工程师希望365天内成功猜测概率不超过0.5 (Probability no greater than 0.5 in 365 days)
  - 需要 (Need): N ≥ TG/P = (365×24×60×60)×10^4/0.5 ≈ 6.31×10^11
  - 计算 (Calculation): 需要S ≥ 6 (Length S ≥ 6)

## 24. 熵 (Entropy)

- **定义 (Definition)**: 信息论中的概念 (Concept from information theory)
- **描述 (Description)**: 关于从数据中推断信息的能力 (About information that can be inferred from data using probabilistic structure)
- **密码熵 (Password entropy)**:
  1. 描述密码空间中密码的概率分布 (Describes probability distribution of passwords over password space)
  2. "n位熵/强度" (n bits of entropy/strength): 表示在2^n个密码的均匀分布中 (Mean uniform distribution over passwords that have length n)
  3. 有2^n个密码，随机猜测一个密码的概率为1/2^n (There are 2^n passwords, probability of guessing at random is 1/2^n)

## 25. 最大熵 (Maximum Entropy)

- **定理 (Theorem)**: 当P均匀时，T（猜测所需平均时间）最大
  1. P均匀: 所有密码等概率 (All passwords equiprobable)
  2. P(a)=1/N，对所有a (P(a)=1/N, for all a)
- *问题 (Problem)*: 人类不随机选择密码
  1. 人类难以随机选择长密码 (Humans find it difficult to do so for long passwords)
  2. 选择易读密码 (Choose pronounceable passwords)
  3. 使用名字、单词、用户名、键盘模式等 (Use names, words, user names, keyboard patterns, variants of old/other passwords)
  4. *参考 (Reference)*: 热力图演示 (Heat maps at: https://blog.qualys.com/securitylabs/2012/07/12/discovered-patterns-in-numeric-passwords-raise-new-questions)

## 26. 密码强度检查 (Password Strength Checks)

- **主动密码检查器 (Proactive password checkers)**:
  1. 阻止用户选择弱密码 (Block users from selecting poor passwords)
  2. 为用户创建新密码提供易于理解的反馈 (Provide users creating new passwords with easy-to-understand feedback)
  3. 有些系统只提供建议 (Some systems only provide advice to user)

## 27. 密码管理 (Managing Passwords)

- **核心问题 (Core Problem)**: 密码应保密，正确的密码应在正确的时间和地点
- **引导问题 (Bootstrap Problem)**:
  1. 如何将密码送到正确位置 (How to get passwords to right places)
  2. 例子 (Examples):
     - 用户需到办公室领取 (Users have to come to office to collect)
     - 通过邮件、电子邮件、电话发送 (Send by mail, email, phone)
     - 远程用户在网页上自行设置密码 (Remote user sets password themselves on web page)
       *问题 (Problem)*: 如何在设置前认证用户? (How do they authenticate before doing that?)
     - *参考 (Reference)*: Wired人士黑客事件 (See the Wired guy hack later)
  3. 谁可能收集? 谁可能拦截? (Who might collect? Who might intercept?)

- **引导解决方案 (Possible Bootstrap Solutions)**:
  1. 电话 (Phone): 让用户从可信电话号码致电，然后回拨 (Get user to call from trusted telephone number, then call them back there)
  2. 呼叫他人 (Call someone else): 让经理等能验证用户的人呼叫 (Call someone else who can authenticate user, e.g., their manager)
  3. 一次性设置密码 (Single-use set-up password): 第一次成功登录后立即更改 (Have to change immediately after first successful login)
  4. 邮件 (Mail): 使用个人(安全)投递 (Use personal(secure) delivery)
  5. 不同渠道确认 (Different channel confirmation): 网页密码后，通过短信确认 (Password on web-page, followed by confirmation by SMS)

## 28. 凭证恢复 (Credential Recovery)

- **定义 (Definition)**: 忘记密码，需要新密码 (You forget password, need new one)
- **方法 (Methods)**:
  1. 部分自动化 (Partly-automated): 使用备份认证和互补信息 (Using back-up authentication and complementary information)
     - *问题 (Problem)*: 备份信息可能丢失或忘记 (Backup info may be lost or forgotten)
  2. 完整流程 (Full process for credential recovery)
- **组织支持 (Organizational Support)**:
  1. 组织通常有处理密码支持的单位 (Many organizations have a unit to do password support)
  2. 人员需要审核 (Personnel require vetting)
  3. 人员需要培训 (Personnel require training)
  4. 耗时 (Time consuming for organization)
  5. 昂贵 (Can be very expensive)
- *重要点 (Important Point)*: 合法用户可能无法访问 (Legitimate users may be unable to gain access)
- *安全要求 (Security Requirement)*: 安全解决方案必须能有效处理此问题 (Security solution must be able to handle this effectively)

## 29. 单点登录 (Single Sign-on, SSO)

- **问题 (Problem)**: 使用多个IT系统时需要多次认证 (Use many IT systems with same owner)
  1. 工作站密码 (Password 1 for workstation)
  2. 网络访问密码 (Password 2 for network access)
  3. 服务器访问密码 (Password 3 for server access)
  4. 数据库管理系统密码 (Password 4 for database management system)
  5. 数据库表密码 (Password 5 to open a table in database)

- **解决方案 (Solution)**: 一次认证，然后传递认证事实 (Get user to authenticate once, and then pass-on this fact appropriately)

- **SSO权衡 (SSO Trade-off)**:
  1. **引入漏洞 (Introduces vulnerabilities)**:
     - 可能导致比单独系统更少的细粒度控制 (Possibly leads to less fine-grained control)
     - 未正确实施时，系统B可能允许应仅允许进入A的用户访问 (Need to make sure access controls for separate systems not allowing access to system B to those whose sign-on should only allow into A)
     - *关键点 (Key Point)*: 避免混淆认证和访问控制 (Okay provided not committed sin of confusing authentication and access control)
  2. **保护问题 (Protection problems)**:
     - 系统一部分存储、缓存、使用密码必须不弱于系统另一部分的要求 (Storage, caching, use, etc. by one part must not be weaker than requirements of another part)
  3. **密码成为更诱人的目标 (Password becomes juicier target)**:
     - 有更多权力 (More power)
  4. **权衡 (Trade-off)**: Gollmann称之为"便利的诅咒" (Gollmann calls this an instance of the curse of convenience)

## 30. 生物识别技术 (Biometrics)

- **定义 (Definition)**: 属于"你是什么"因素 ("Something you are" factor)
- **例子 (Examples)**: 指纹、语音识别、虹膜扫描等 (Fingerprints, voice recognition, iris scans, etc.)
- **优势 (Advantage)**: 解决密码的可用性问题 (Helps to solve many usability problems with passwords)

## 31. 生物识别问题 (Biometric Problems)

- **假阳性/假阴性问题 (False positives and false negatives)**
- **无法识别的用户 (Failures to enroll)**: 用户具有系统无法识别的属性
- **互补数据存储问题 (Complementary data storage)**:
  1. 不能简单哈希 (Cannot just be hashed)
  2. 需要检查输入数据是否接近存储数据 (Need to see if authentication data supplied is close to stored data, not exact match)
  3. *可能的解决方案 (Possible solution)*: 使用新型同态加密方法 (Advanced way around using very new homomorphic encryption methods)
- **敏感数据存储 (Sensitive private data storage)**: 必须存储敏感私人数据
- **凭证撤销困难 (Difficult to revoke credentials)**:
  1. 难以撤销和颁发新凭证 (Difficult to revoke credentials and issue new ones)
  2. *可能的解决方案 (Possible solution)*: 仅使用部分生物特征数据 (Relies on using only partial biometric data, e.g. specified parts of fingerprint that can later be changed)