# 🛡️ Security Skills Collection

> **安全与渗透测试技能库** · 自包含 · 跨平台 · 可移植
>
> 一个面向安全 / 渗透测试场景的 Agent Skills 集合。每个技能都是**完整 `SKILL.md` 全文**，
> 任意支持 Agent Skills 规范的运行时（Claude Code / Cursor / 各类 Agent 框架）直接读取即可加载，
> 不依赖特定客户端、不依赖联网、不依赖固定安装路径。

![skills](https://img.shields.io/badge/skills-1404-blue)
![categories](https://img.shields.io/badge/categories-35-green)
![updated](https://img.shields.io/badge/updated-2026--09-orange)
![format](https://img.shields.io/badge/format-SKILL.md-purple)

---

## ✨ 特性

- 📦 **自包含**：1404 个技能的完整 `SKILL.md` 已 1:1 复制进 `skills/<分类>/<技能名>.md`，开箱即用。
- 🧭 **可移植**：包内统一使用相对路径，拷贝到任何机器 / 任何 Agent 都能定位。
- 🗂️ **已分类**：35 个语义分类（侦察 / Web / 域控 / 云 / 红队 / 代码审计 / CTF …）。
- 🤖 **机器可读**：`SKILL_FULL_REGISTRY.json` 提供结构化索引（名称 / 分类 / 路径 / 描述 / 体积）。
- 🔍 **覆盖全链**：从侦察 OSINT 到后渗透、从漏洞利用到防御检测响应。

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

## 🗂️ 仓库结构

```
.
├── README.md                  # 本文件
├── README_FULL.md             # 完整索引 + 分类表 + 来源
├── SKILL_REGISTRY.json        # 精简机器索引（核心技能）
├── SKILL_FULL_REGISTRY.json   # 完整机器索引（1404 技能）
├── search.py                  # 命令行搜索 / 筛选工具
├── PLACEHOLDERS.md            # 18 个权限受限占位技能清单
├── ctf/                       # CTF 方向手写摘要
├── pentest/                   # 渗透方向手写摘要
└── skills/                    # 1404 个完整 SKILL.md（按 35 个分类子目录）
```

## 📚 来源与致谢

| 来源仓库 | 说明 |
|----------|------|
| [wgpsec/AboutSecurity](https://github.com/wgpsec/AboutSecurity) | 200+ 渗透技能，完整攻击链（侦察→社工→利用→后渗透），中文 |
| [uphiago/recon-skills](https://github.com/uphiago/recon-skills) | 169 个侦察 / 红队技能 |
| [0x0pointer/skills](https://github.com/0x0pointer/skills) | agent-smith 渗透技能（web / API / 网络 / 后渗透 / 横向） |
| [crazyMarky/pentest-skills](https://github.com/crazyMarky/pentest-skills) | 模块化渗透技能（侦察 / SQLi / XSS / LFI / 报告） |
| [securityfortech/hacking-skills](https://github.com/securityfortech/hacking-skills) | Bug Bounty / 渗透 / CTF / 代码审计 |
| [SnailSploit/Claude-Red](https://github.com/SnailSploit/Claude-Red) | 进攻性安全技能（SQLi / shellcode / EDR 绕过 / 漏洞利用） |
| [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills) | CTF 技能（web / pwn / crypto / reverse / forensics / OSINT） |
| [hypnguyen1209/offensive-claude](https://github.com/hypnguyen1209/offensive-claude) | 31 个进攻工具技能 |
| [NovaCode37/claude-security-skills](https://github.com/NovaCode37/claude-security-skills) | 安全审计（秘钥扫描 / SAST / JWT / CORS / Dockerfile） |

另有部分技能来自 SkillHub 技能市场。
