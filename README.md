# 🛡️ Security Skills Collection

> **安全与渗透测试 Agent Skills 库** · 自包含 · 跨平台 · 可移植
>
> 面向安全 / 渗透测试场景构建的 Agent Skills 库。每个技能均为**完整 `SKILL.md` 全文**，
> 任意支持 Agent Skills 规范的运行时（Claude Code / Cursor / 各类 Agent 框架）直接读取即可加载，
> 不依赖特定客户端、不依赖联网、不依赖固定安装路径。

![skills](https://img.shields.io/badge/skills-1404-blue)
![categories](https://img.shields.io/badge/categories-35-green)
![updated](https://img.shields.io/badge/updated-2026--09-orange)
![format](https://img.shields.io/badge/format-SKILL.md-purple)

---

## ✨ 特性

- 🗂️ **自研语义分类**：设计 35 类分类体系（侦察 / Web / 域控 / 云 / 红队 / 代码审计 / CTF …），覆盖完整攻击链与防御响应。
- 🤖 **机器可读索引**：生成 `SKILL_FULL_REGISTRY.json` 结构化索引（名称 / 分类 / 路径 / 描述 / 体积），支持程序化检索。
- 🔎 **检索工具**：附带 `search.py` 命令行检索，按分类 / 关键词快速定位技能。
- 📦 **自包含**：1404 个技能的完整 `SKILL.md` 已 1:1 固化进 `skills/<分类>/<技能名>.md`，开箱即用。
- 🧭 **可移植**：包内统一相对路径，拷贝到任意机器 / Agent 即可定位，无需特定环境。

## 📊 技能分类（35 类 · 合计 1404）

| 分类 | 数量 |
|------|------|
| `misc-pentest` | 175 |
| `implementing` | 156 |
| `performing` | 156 |
| `web-attack` | 86 |
| `offensive` | 79 |
| `detecting` | 75 |
| `hunt-osint` | 72 |
| `analyzing` | 70 |
| `pentest` | 69 |
| `recon-osint` | 50 |
| `exploiting` | 36 |
| `hunting` | 35 |
| `php-audit` | 35 |
| `building` | 32 |
| `cloud` | 28 |
| `redteam` | 23 |
| `conducting` | 22 |
| `network-infra` | 20 |
| `testing` | 20 |
| `configuring` | 18 |
| `active-directory` | 17 |
| `ctf` | 17 |
| `ops-response` | 16 |
| `devsecops` | 13 |
| `java-audit` | 12 |
| `securing` | 12 |
| `mobile` | 10 |
| `malware-analysis` | 10 |
| `threat-intel` | 8 |
| `reverse-engineering` | 8 |
| `auditing` | 7 |
| `scanning` | 6 |
| `phishing-social` | 5 |
| `code-audit` | 4 |
| `privilege-escalation` | 2 |

## 🚀 快速开始

**方式一 · 任意 Agent 直接读取（推荐）**
```python
# 直接读某个技能全文
read skills/web-attack/sqli-blind.md
# 或按程序批量定位
import json
reg = json.load(open('SKILL_FULL_REGISTRY.json', encoding='utf-8'))
for s in reg['skills']:
    if s['category'] == 'active-directory':
        print(s['name'], '->', s['path'])
```

**方式二 · 装入你的 Agent skills 目录**
```powershell
# 把整包技能按原名复制到 Agent 的 skills 目录即可自动加载
Copy-Item -Recurse skills\* <你的 skills 目录>\
```

**方式三 · 命令行检索**
```powershell
python search.py --list-cats          # 列出全部分类及数量
python search.py -c web-attack        # 按分类筛选
python search.py -k sqli              # 按关键词筛选
```

## 🗂️ 仓库结构

```
.
├── README.md                  # 本文件
├── README_FULL.md             # 完整索引 + 分类表 + 参考来源
├── SKILL_REGISTRY.json        # 精简机器索引（核心技能）
├── SKILL_FULL_REGISTRY.json   # 完整机器索引（1404 技能）
├── search.py                  # 命令行搜索 / 筛选工具
├── PLACEHOLDERS.md            # 18 个权限受限占位技能清单
├── ctf/                       # CTF 方向手写摘要
├── pentest/                   # 渗透方向手写摘要
└── skills/                    # 1404 个完整 SKILL.md（按 35 个分类子目录）
```

## 📚 参考来源

技能内容参考了社区公开的安全项目，整理时按统一规范重构、分类并生成索引：

| 来源仓库 | 方向 |
|----------|------|
| [wgpsec/AboutSecurity](https://github.com/wgpsec/AboutSecurity) | 渗透攻击链 |
| [uphiago/recon-skills](https://github.com/uphiago/recon-skills) | 侦察 / 红队 |
| [0x0pointer/skills](https://github.com/0x0pointer/skills) | Web / API / 后渗透 |
| [crazyMarky/pentest-skills](https://github.com/crazyMarky/pentest-skills) | 模块化渗透 |
| [securityfortech/hacking-skills](https://github.com/securityfortech/hacking-skills) | Bug Bounty / CTF |
| [SnailSploit/Claude-Red](https://github.com/SnailSploit/Claude-Red) | 进攻性安全 |
| [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills) | CTF |
| [hypnguyen1209/offensive-claude](https://github.com/hypnguyen1209/offensive-claude) | 进攻工具 |
| [NovaCode37/claude-security-skills](https://github.com/NovaCode37/claude-security-skills) | 安全审计 |
