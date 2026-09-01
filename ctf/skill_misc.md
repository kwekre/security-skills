# ctf-misc — CTF Misc综合

**路径**: `skills 目录/ctf-misc/SKILL.md`

## 图片隐写

### 基础分析
```bash
file image.jpg
binwalk image.jpg          # 分离嵌入文件
binwalk -e image.jpg       # 自动提取
exiftool image.jpg         # 元数据
strings image.jpg | grep -i flag
```

### LSB 隐写

```bash
# zsteg（PNG/BMP 最强）
zsteg image.png             # 检测
zsteg image.png --lsb      # 所有层
zsteg image.png --all      # 全部尝试

# Steghide
steghide extract -sf image.jpg -p ""
steghide extract -sf image.jpg -p password

# StegSolve（Java GUI）
java -jar StegSolve.jar
```

### PNG 特殊

```bash
# CRC 错误（宽高修改后 CRC 损坏）
pngcheck -v image.png
python3 fixpng.py image.png   # 修复 CRC
```

## 音频隐写

```bash
# 频谱分析
audacity audio.wav
ffmpeg -i audio.mp3 -show_freqs audio.png

# 频谱图
sox audio.wav -n spectrogram -o spectrogram.png

# 提取数据
strings audio.mp3 | grep -i flag
```

莫尔斯电码：用 `morse2ascii` 工具或手动辨认波形中点和划线。

## 流量分析（PCAP）

```bash
# 基础提取
tshark -r capture.pcap -Y "http" -T fields -e http.host -e http.request.uri

# 导出 HTTP 对象
tshark -r capture.pcap -Y "http" --export-objects http,output_dir

# DNS 隧道
tshark -r capture.pcap -Y "dns" -T fields -e dns.qry.name | grep -v "^[0-9]"

# Base64 提取
tshark -r capture.pcap -Y "http" -T fields -e http.file_data | \
  grep -E "^[A-Za-z0-9+/]{20,}={0,2}$"
```

## PDF 隐写

```bash
pdftotext image.pdf -          # 提取文本
pdfinfo image.pdf              # 元信息

# 白色隐藏文字
# 方法：全选复制 / 改背景色 / pdf-c11.py
python3 pdf-c11.py image.pdf
```

## 压缩包攻击

```bash
# 基本信息
zipinfo archive.zip
7z l archive.zip

# 明文攻击（已知部分文件内容）
bkcrack -C archive.zip -c known.txt -k XXXXXXXX -r 0/

# 暴力破解
fcrackzip -v -u -l 1-6 -p passwords.txt archive.zip

# CRC32 攻击（小文件，4字节）
python3 crc_attack.py
```

## 内存取证

```bash
volatility -f memory.dmp imageinfo                              # 确定系统
volatility -f memory.dmp --profile=Win7SP1x64 pslist          # 进程
volatility -f memory.dmp --profile=Win7SP1x64 netscan          # 网络
volatility -f memory.dmp --profile=Win7SP1x64 hashdump         # 密码哈希
volatility -f memory.dmp --profile=Win7SP1x64 mimikatz        # 明文密码
volatility -f memory.dmp --profile=Win7SP1x64 filescan         # 文件
volatility -f memory.dmp --profile=Win7SP1x64 dumpfiles -Q 0xXXXX -D out/
```

## 日志分析

```bash
grep -i "flag\|password\|admin\|error\|fail" access.log

# SQL 注入特征
grep -iE "union.*select|concat.*\(|char\(|0x[0-9a-f]" access.log

# XSS 特征
grep -iE "<script|javascript:|onerror=" access.log

# 时间分析
awk '{print $4}' access.log | sort | uniq -c | sort -rn | head -20
```

## CyberChef

在线：https://gchq.github.io/CyberChef/

常用 Recipe：`Magic` → `From Base64` → `XOR` → `From Hex` → `Gunzip`

## 触发词
CTF Misc、隐写、LSB、zsteg、流量分析、pcap、内存取证、volatility、压缩包、日志分析
