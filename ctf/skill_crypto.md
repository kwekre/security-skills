# ctf-crypto — CTF Crypto密码学解题

**路径**: `skills 目录/ctf-crypto/SKILL.md`

## 编码解码

```python
import base64, urllib.parse

base64.b64decode("SGVsbG8gV29ybGQ=")
urllib.parse.unquote("name%3D%E5%93%88%E5%93%88")
"哈".encode('unicode_escape')   # b'\\u54c8'
"哈".encode('utf-8')            # b'\xe5\x93\x88'
```

## 对称加密

### XOR 异或

```python
# 单字节密钥暴力破解
for k in range(256):
    d = bytes([b ^ k for b in cipher])
    if b"flag" in d or b"CTF" in d:
        print(d)

# 已知明文攻击
key = bytes([m ^ c for m, c in zip(known_plaintext, cipher_text)])
```

### AES / DES

```python
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import pad, unpad

# AES CBC
cipher = AES.new(key, AES.MODE_CBC, iv)
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
```

## RSA

### 基础计算
```python
from Crypto.Util.number import inverse
phi = (p-1)*(q-1)
d = inverse(e, phi)
m = pow(c, d, n)
```

### 常见攻击

| 攻击 | 场景 |
|------|------|
| 低指数广播（CRT） | e=3，同一明文不同 n |
| 共模攻击 | 同一明文，不同 e |
| Wiener 攻击 | d 很小（d/n < 1/3） |
| Boneh-Durfee | d 和 phi 接近 |
| 私钥文件泄露 | .pem / .key 文件 |

```python
# 低指数广播（中国剩余定理）
from sympy import crt
m = crt([n1,n2,n3],[c1,c2,c3])[0]
result = round(pow(m, 1/3))

# Wiener
import gmpy2
```

## 哈希

### MD5 / SHA 碰撞
```python
import hashlib
hashlib.md5(data).hexdigest()
```

### Hash Length Extension
```python
import hashpump
new_digest, new_data = hashpump(
    original_digest, original_data, add_data, key_length
)
```

## 常用工具

```bash
# RSATool / RSaCtfTool
python3 rsactftool.py --uncipher c --key key.txt

# hashcat
hashcat -m 0 hash.txt wordlist.txt    # MD5
hashcat -m 100 hash.txt rockyou.txt   # SHA1
hashcat -m 1400 hash.txt rockyou.txt  # SHA256

# factordb（在线分解大整数）
# https://factordb.com/

# fastcoll（MD5 前缀碰撞）
fastcoll_v1.0.0.5.exe -p prefix.txt -o out1.bin out2.bin
```

## 类型识别

| 类型 | 特征 |
|------|------|
| Base64 | A-Za-z0-9+/= |
| Hex | 0-9a-f，偶数位 |
| URL Enc | %XX |
| MD5 | 32位十六进制 |
| SHA1 | 40位十六进制 |
| SHA256 | 64位十六进制 |
| RSA | 大十进制/十六进制数 |

## 触发词
CTF Crypto、密码学、RSA、AES、XOR、哈希、MD5碰撞、长度扩展攻击、编码解码、RSATool
