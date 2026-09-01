# ctf-writeup — CTF Writeup 撰写规范

**路径**: `skills 目录/ctf-writeup/SKILL.md`

## Writeup 结构

```
1. 题目信息（名称、平台、分值、方向）
2. 题目附件（文件路径 / 下载链接）
3. 分析过程
   3.1 初步分析（file / strings / checksec）
   3.2 详细分析（IDA / 调试 / 算法还原）
   3.3 解题步骤
4. 最终 Payload / Flag
5. 参考资料
```

## 各方向 Writeup 要点

### Web
- 漏洞类型 + 发现过程
- Payload 构造思路
- 关键代码片段

### Crypto
- 算法识别过程
- 攻击原理（数学推导或代码）
- 解密脚本

### Pwn
- 漏洞类型 + 保护机制分析
- 漏洞点定位（gdb / IDA）
- Exploit 代码 + 注释

### Reverse
- 关键算法还原
- 解密脚本

### Misc
- 解题工具 + 步骤
- 关键数据提取过程

## Flag 格式
- 提交时去掉 `flag{...}` 包裹
- 或按平台要求提交

## 参考资料
- 引用使用的工具和脚本
- 引用参考的 Writeup / 文章
