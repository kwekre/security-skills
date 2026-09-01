# ctf-reverse — CTF Reverse逆向工程

**路径**: `skills 目录/ctf-reverse/SKILL.md`

## 工具链

| 工具 | 用途 |
|------|------|
| `file` | 文件类型初步判断 |
| `strings` | 提取字符串 |
| `checksec` | 检查保护机制 |
| `upx -d` | UPX 脱壳尝试 |
| IDA Pro / IDA Free | 反编译（最强） |
| Ghidra | NSA 开源，免费友好 |
| x64dbg / OllyDbg | Windows 动态调试 |
| gdb / pwndbg / gef | Linux 动态调试 |
| radare2 / cutter | 命令行逆向框架 |

## 分析流程

```
1. file + strings 初步判断（语言、架构、是否加壳）
2. checksec 检查保护（NX / PIE / RELRO / Canary）
3. 运行程序观察行为
4. IDA/Ghidra 静态分析主逻辑
5. 动态调试定位关键函数
6. 写出逆向脚本或直接 Patch
```

## 常见算法逆向

### 解密模板
```python
data = [0x66, 0x6B, 0x63, 0x64, 0x7F, 0x6B]  # 从 IDA 提取
key = [1, 2, 3]

result = []
for i in range(len(data)):
    result.append((data[i] ^ key[i % len(key)]) - 0x10)

print(''.join(chr(c) for c in result))
```

### Base64 变种
```python
import base64, codecs
custom_table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
# 替换字母顺序后解码
```

## 动态调试

### GDB / pwndbg
```bash
gdb ./challenge
pwndbg ./challenge

# 常用命令
break main
break *0x08048484   # 地址断点
run
nexti / ni           # 单步（不进入）
stepi / si           # 步入
info registers
x/20x 0x08048000    # 内存（16进制）
x/s 0x08048000       # 内存（字符串）
continue / c
finish               # 运行到函数返回
```

### IDA 动态调试
```bash
# IDA Server 模式
idaserver64 -P12345
# 目标机器
idaq64 -rserver+ -P12345 ./challenge
```

## Patch

```python
from pwn import *

elf = ELF('./challenge')
# 修改函数
elf.asm(elf.symbols['check'], 'ret')
# patch 字节
elf.patch_byte(0x08048567, 0x90)  # NOP
elf.save()
```

## 脱壳

```bash
# UPX
upx -d challenge -o challenge_unpacked

# 手动脱壳流程：
# 1. 找 OEP（大量 pushad 后跳转到 OEP）
# 2. 在 OEP 处 dump 内存
# 3. 修复 IAT
```

## 常见套路

- **字符串比对** → 找关键函数 → 绕过或 Patch
- **迷宫问题** → 提取地图 → 找路径
- **虚拟机保护** → 分析 opcode → 模拟执行
- **自定义指令集** → 逆向字节码
- **加密算法** → 提取密钥 → 解密

## 触发词
CTF Reverse、逆向、IDA、Ghidra、反编译、算法逆向、调试、脱壳、Patch、PE/ELF
