---
name: ctf-reverse
description: CTF Reverse逆向工程。触发：IDA/Ghidra反编译、PE/ELF分析、算法逆向、动态调试、脱壳、Patch修改等场景。
---

# ctf-reverse — CTF Reverse逆向工程

## 1. 基础工具链

```bash
# 文件分析
file challenge
strings challenge | grep -i flag
strings challenge | head -50

# 查壳
rabin2 -I challenge        # rabin2 (r2)
upx -d challenge           # 尝试脱 UPX 壳
```

**常用工具**：
- **IDA Pro / IDA Free** — 最强反编译器
- **Ghidra** — NSA 开源逆向工具，免费
- **x64dbg / OllyDbg** — Windows 动态调试
- **gdb / pwndbg / gef** — Linux 动态调试
- **radare2 / cutter** — 命令行逆向框架

## 2. 分析流程

```
1. file + strings 初步判断（语言、架构、是否加壳）
2. 运行程序观察行为
3. IDA/Ghidra 静态分析主逻辑
4. 动态调试定位关键函数
5. 写出逆向脚本或直接修改程序
```

## 3. 常见算法逆向

### 简单算法（数组 / 循环）

```python
# 观察 IDA 中的 for 循环
# 找关键数组和索引
data = [...]
for i in range(len(data)):
    data[i] = (data[i] ^ key[i % keylen]) - 0x20
print(''.join(chr(c) for c in data))
```

### Base64 变种

```python
import base64
custom_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
# 替换字母顺序
import codecs
codecs.encode(b"data", "base64")
```

### 自定义加密

```python
def decrypt(data, key):
    out = []
    for i, c in enumerate(data):
        out.append((c ^ key[i % len(key)]) - 0x10)
    return bytes(out)
```

### TEA/XTEA/XXTEA

```python
# 找特征：DELTA = 0x9E3779B9（TEA 常数）
# 32轮循环
```

## 4. 动态调试

### GDB / pwndbg

```bash
gdb ./challenge
# 或 pwndbg
pwndbg ./challenge

# 常用命令
break main          # 断点
break *0x08048484  # 地址断点
run                 # 运行
nexti / ni          # 单步
stepi / si          # 步入函数
info registers      # 查看寄存器
x/20x 0x08048000   # 内存查看（16进制）
x/s 0x08048000     # 内存查看（字符串）
continue / c        # 继续执行
finish              # 运行到函数返回
```

### Python 脚本动态修改

```python
from pwn import *

p = process('./challenge')
# 或远程
# p = remote('host', port)

# 发送输入
p.sendline(b'A' * 100)

# 调试信息
p.interactive()
```

## 5. 脱壳

### UPX 脱壳

```bash
upx -d challenge -o challenge_unpacked
# 如果加壳了自定义壳，用手动脱壳
```

### 手动脱壳流程

```
1. 找 OEP（原始入口点）
   - 在调试器中单步执行，直到来到程序真正入口
   - OEP 特征：大量 pushad / pushfd 之后跳转到 OEP

2. Dump 内存
   - 在 OEP 处断下
   - 用工具 dump 所有内存段

3. 修复 IAT（导入地址表）
   - 重建导入表
```

## 6. Patch 与修改

```python
from pwn import *

elf = ELF('./challenge')
# 修改函数
elf.asm(elf.symbols['check'], 'ret')

# patch 字节
elf.patch_byte(0x08048567, 0x90)  # NOP

elf.save()
```

## 7. 常见逆向套路

```
- 字符串比对 → 找关键函数 → 绕过
- 迷宫问题 → 提取地图 → 找路径
- 虚拟机保护 → 分析 opcode → 模拟执行
- 自定义指令集 → 逆向字节码
- 加密算法 → 提取密钥 → 解密
```

## 8. 解题模板

```python
data = [0x66, 0x6B, 0x63, 0x64, 0x7F, 0x6B]  # 提取的数据
key = [1, 2, 3]

result = []
for i in range(len(data)):
    result.append((data[i] ^ key[i % len(key)]) - 3)

print(''.join(chr(c) for c in result))
```
