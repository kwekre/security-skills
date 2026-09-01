# 安全与渗透测试技能库 — 完整索引

- 版本：v3（2026-09-01）整合 GitHub 渗透技能仓库
- 技能总数：**1404** ｜ 分类数：**35**
- 自包含：每个技能的完整 `SKILL.md` 已 1:1 复制进 `skills/<分类>/<技能名>.md`。

## v3 更新说明
在既有技能库基础上，从 GitHub 新增 **591** 个渗透 / 安全技能（去重后库总量达 1404）。

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

## 分类统计（35 类，合计 1404）

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

## 核心渗透技能链（按阶段）
1. 侦察 / OSINT：`recon-osint`、`hunt-osint`、`pentest`
2. Web 利用：`web-attack`、`exploiting`、`offensive`、`ctf`
3. 内网 / 域控：`active-directory`、`redteam`、`privilege-escalation`
4. 隧道 / 穿透：`pentest`、`redteam`
5. 云 / 容器：`cloud`、`devsecops`
6. 代码审计：`php-audit`、`java-audit`、`code-audit`、`devsecops`
7. CTF：`ctf`
8. 报告：`pentest`

## 防御 / 检测 / 响应体系
- 检测：`detecting`、`hunting`、`hunt-osint`、`scanning`
- 分析 / 情报：`analyzing`、`threat-intel`、`malware-analysis`
- 响应 / 取证：`ops-response`、`reverse-engineering`
- 加固 / 建设：`securing`、`implementing`、`building`、`configuring`、`conducting`、`performing`、`auditing`

## 机器可读索引
- `SKILL_FULL_REGISTRY.json`：每项含 `name` / `category` / `path`（包内相对路径）/ `description` / `size_bytes`。
- 程序加载示例：
```python
import json
reg = json.load(open('SKILL_FULL_REGISTRY.json', encoding='utf-8'))
for s in reg['skills']:
    if 'sqli' in s['name']:
        print(s['path'], s['description'])
```

## 使用方式
- 直接读取：`read skills/<分类>/<技能名>.md`（全文自带 frontmatter + 正文）。
- 装入 Agent：把 `skills/` 复制到 Agent 的 skills 目录即可自动加载。

## 安全边界
仅对**已获书面授权**的目标执行主动测试；不绕过防护、不 DoS、不爆破、不无授权横向、不拖取 PII。CTF / 靶场仅用于授权训练。

## 已知限制
- 约 18 个技能源文件因本机权限受限无法读取，包内以占位说明标注，路径不悬空。
- `misc-pentest` 为未匹配上述语义规则的其余技能汇总，按需可进一步细分。
