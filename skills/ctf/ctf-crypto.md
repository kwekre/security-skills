---
name: ctf-crypto
description: CTF Crypto密码学解题。触发：RSA/AES/DES加密、哈希长度扩展攻击、数字签名、编码解码、MD5碰撞等场景。
---

# ctf-crypto — CTF Crypto方向解题

## 常用编码与解码

**Base64 / Base32 / Base16**
```python
import base64
base64.b64decode("SGVsbG8gV29ybGQ=")
base64.b32decode("JBSWY3DPEBLW64TMMQ======")
base64.b16decode("48656C6C6F576F726C64")
```

**URL / HTML 编码**
```python
import urllib.parse
urllib.parse.unquote("name%3D%E5%93%88%E5%93%88")
```

**Unicode 编码**
```python
"哈".encode('unicode_escape')  # b'\\u54c8'
"哈".encode('utf-8')          # b'\xe5\x93\x88'
```

## 对称加密

### XOR 异或

```python
# 已知明文攻击（已知部分明文恢复密钥）
key = bytes([m ^ c for m, c in zip(known_plaintext, cipher_text)])

# 单字节密钥（暴力破解）
for k in range(256):
    decrypted = bytes([b ^ k for b in cipher])
    if b"flag" in decrypted or b"CTF" in decrypted:
        print(decrypted)
```

### AES / DES

```python
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad

# AES CBC 解密
key = b'16byte_key_here!!!'
iv = b'16byte_iv_here!!!'
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

# DES
key = b'8byteke'
des = DES.new(key, DES.MODE_ECB)
plaintext = unpad(des.decrypt(ciphertext), DES.block_size)
```

## 非对称加密

### RSA

**基础计算**
```python
from Crypto.Util.number import inverse, GCD, getPrime
import math

# 已知 n, e, c，求 m
phi = (p-1)*(q-1)
d = inverse(e, phi)
m = pow(c, d, n)
```

**常见攻击**

1. **e 太小（e=3），低指数广播攻击（同一明文，不同 n）**
```python
from sympy import crt
m = crt([n1, n2, n3], [c1, c2, c3])[0]
result = round(pow(m, 1/3))
```

2. **共模攻击（同一明文，不同 e）**
```python
import gmpy2
s = gmpy2.invert(e1, e2)
m = pow(c1, s, n)  # 需调整
```

3. **Wiener 攻击（d 很小）**
```python
import gmpy2
# 适用 d/n < 1/3
```

**工具**
```bash
# RSATool / RSaCtfTool
python3 rsactftool.py --uncipher c --key key.txt
# factordb: https://factordb.com/
```

### ECC（椭圆曲线）

```python
# 已知 P, Q, G，求 k 使得 k*G = Q
from sympy import discrete_log
k = discrete_log(mod, Q, G)
```

## 哈希与签名

### MD5 / SHA1 碰撞

```python
import hashlib
hashlib.md5(data).hexdigest()
```

**前缀碰撞**
```bash
# 利用 fastcoll 生成相同前缀不同内容的 MD5 碰撞
fastcoll_v1.0.0.5.exe -p prefix.txt -o out1.bin out2.bin
```

### Hash Length Extension Attack

```python
# python3 -m pip install hashpump
import hashpump
digest = "5d41402abc4b2a76b9719d911017c592"
original_data = "original"
add_data = "追加内容"
key_length = 5

new_digest, new_data = hashpump(digest, original_data, add_data, key_length)
```

## CTF 专用工具

```bash
# RSATool / RSaCtfTool
python3 rsactftool.py --uncipher c --key key.txt

# hashcat
hashcat -m 0 hash.txt wordlist.txt          # MD5
hashcat -m 100 hash.txt wordlist.txt         # SHA1
hashcat -m 1400 hash.txt wordlist.txt        # SHA256

# John the Ripper
john --wordlist=rockyou.txt hashes.txt
```

## 常见密码类型识别

| 类型 | 特征 | 工具 |
|------|------|------|
| Base64 | A-Za-z0-9+/= | Python base64 |
| Hex | 0-9a-f | Python b16decode |
| URL Enc | %XX | urllib.parse |
| MD5 | 32位16进制 | hashlib |
| SHA1 | 40位16进制 | hashlib |
| SHA256 | 64位16进制 | hashlib |
| RSA | 大整数 | RSATool |
| AES | 16/24/32字节倍数 | Crypto库 |
