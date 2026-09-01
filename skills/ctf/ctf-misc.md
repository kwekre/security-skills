---
name: ctf-misc
description: CTF Misc综合。触发：隐写术(LSB/Zsteg)、流量分析(pcap/strings)、内存取证(volatility)、压缩包攻击、日志分析等场景。
---

# ctf-misc — CTF Misc综合方向

## 1. 图片隐写

### 基础工具

```bash
file image.jpg
binwalk image.jpg          # 分离嵌入文件
binwalk -e image.jpg       # 自动提取
exiftool image.jpg         # 元数据
strings image.jpg | grep -i flag

# 图片查看
identify image.jpg
display image.jpg
```

### LSB 隐写（最低有效位）

**zsteg（PNG/BMP）**
```bash
zsteg image.png            # 检测 LSB
zsteg image.png -b 1       # 第1列
zsteg image.png --lsb      # 所有层
zsteg image.png --all      # 全部尝试
```

**Steghide**
```bash
steghide extract -sf image.jpg -p ""   # 无密码
steghide extract -sf image.jpg -p password
steghide info image.jpg
```

**StegSolve（Java GUI）**
```bash
java -jar StegSolve.jar
```

### PNG 特殊

```bash
# CRC 错误修复（修改宽高后 CRC 损坏）
pngcheck -v image.png
python3 fixpng.py image.png   # 修复 CRC

# IHDR 块修改宽高（16进制编辑器）
```

## 2. 音频隐写

```bash
# 频谱分析
audacity audio.wav
ffmpeg -i audio.mp3 -show_freqs audio.png

# 频谱图转图片
sox audio.wav -n spectrogram -o spectrogram.png

# 提取数据
strings audio.mp3 | grep -i flag
```

**莫尔斯电码**：波形中找点和划线，或用 `morse2ascii` 工具

## 3. 流量分析（PCAP）

```bash
# tshark 命令行
tshark -r capture.pcap -Y "http" -T fields -e http.host -e http.request.uri | grep flag
tshark -r capture.pcap -Y "http.request.method == POST" -T fields -e http.file_data

# 导出 HTTP 对象
tshark -r capture.pcap -Y "http" --export-objects http,output_dir

# DNS 隧道检测
tshark -r capture.pcap -Y "dns" -T fields -e dns.qry.name | grep -v "^[0-9]"

# Base64 提取
tshark -r capture.pcap -Y "http" -T fields -e http.file_data | grep -E "^[A-Za-z0-9+/]{20,}={0,2}$"
```

## 4. PDF 隐写

```bash
pdftotext image.pdf -           # 提取文本
pdfinfo image.pdf               # 元信息

# 白色隐藏文字：改背景色或直接全选复制
# 工具：pdf-c11.py
python3 pdf-c11.py image.pdf
```

## 5. 压缩包攻击

```bash
# 基本信息
zipinfo archive.zip
7z l archive.zip

# 明文攻击（已知部分内容）
bkcrack -C archive.zip -c known.txt -k XXXXXXXX -r 0/

# 暴力破解
fcrackzip -v -u -l 1-6 -p passwords.txt archive.zip
fcrackzip -v -u -D -p rockyou.txt archive.zip

# CRC32 攻击（小文件，4字节明文）
python3 crc_attack.py
```

## 6. 内存取证

```bash
volatility -f memory.dmp imageinfo
volatility -f memory.dmp --profile=Win7SP1x64 pslist
volatility -f memory.dmp --profile=Win7SP1x64 netscan
volatility -f memory.dmp --profile=Win7SP1x64 hashdump
volatility -f memory.dmp --profile=Win7SP1x64 mimikatz
volatility -f memory.dmp --profile=Win7SP1x64 filescan
volatility -f memory.dmp --profile=Win7SP1x64 dumpfiles -Q 0xXXXX -D output/
```

## 7. 日志分析

```bash
grep -i "flag\|password\|admin\|error\|fail" access.log

# SQL 注入检测
grep -iE "union.*select|concat.*\(|char\(|0x[0-9a-f]" access.log

# XSS 检测
grep -iE "<script|javascript:|onerror=" access.log

# 时间分析
awk '{print $4}' access.log | sort | uniq -c | sort -rn | head -20
```

## 8. CyberChef

**在线**：https://gchq.github.io/CyberChef/

**常用 Recipe**：
```
Magic                  # 自动识别编码
From Base64            # Base64 解码
XOR ...                # 异或解密
ROT13                  # 凯撒移位
From Hex               # 16进制转字符
Gunzip / Inflate       # 解压
Reverse                # 反转字符串
Find / Replace         # 替换
```
