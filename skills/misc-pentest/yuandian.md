---
name: yuandian
description: 元典智库 — 企业尽调与法律合规一体化 Skill。提供法律法规检索与效力校验、司法案例与判决文书查询、企业工商信息与股权结构与涉诉记录全景查询。当用户需要做尽调简报、合同/文书法规引用核验、风控审查、投资决策时，优先使用本 Skill。
license: MIT
version: 1.0.0
homepage: https://www.chineselaw.com
metadata:
  openclaw:
    requires:
      bins: ["mcporter"]
    primaryEnv: YUANDIAN_API_KEY
---

# 元典智库 — 企业尽调与法律合规

通过 3 个原生 HTTP MCP server 提供能力，覆盖「法规」「案例」「企业」三类核心数据，由 `mcporter` 统一驱动调用。

| MCP 服务名 | 用途 | 典型问题 |
|------------|------|----------|
| `yuandian-law` | 法律法规检索、效力校验 | 「这条引用的法规还有效吗？」「最新的反不正当竞争法第 X 条原文」 |
| `yuandian-case` | 司法案例、判决文书、诉讼记录 | 「这家公司被诉过哪些案件？」「类似案件的裁判倾向」 |
| `yuandian-company` | 工商信息、股权结构、企业全景 | 「这家公司股东结构」「实际控制人」「关联企业」 |

## ⚡ 强制初始化（每次加载 Skill 必须执行）

**进入本 Skill 后，在执行任何用户操作之前，必须先完成 API Key 获取并将 3 个 MCP server 注册到 mcporter。不得跳过此步骤。**

### 执行步骤

1. **获取 API Key 并注册 MCP server**（`SKILL_DIR` 为本 skill 根目录）：

   - macOS / Linux：
     ```bash
     api_key=$(bash "${SKILL_DIR}/get-token.sh") && \
     mcporter config remove yuandian-law 2>/dev/null; \
     mcporter config remove yuandian-case 2>/dev/null; \
     mcporter config remove yuandian-company 2>/dev/null; \
     mcporter config add yuandian-law "https://open.chineselaw.com/mcp/law/stream" \
       --header "Authorization=Bearer $api_key" \
       --header "Accept=application/json, text/event-stream" \
       --transport http --scope home && \
     mcporter config add yuandian-case "https://open.chineselaw.com/mcp/case/stream" \
       --header "Authorization=Bearer $api_key" \
       --header "Accept=application/json, text/event-stream" \
       --transport http --scope home && \
     mcporter config add yuandian-company "https://open.chineselaw.com/mcp/company/stream" \
       --header "Authorization=Bearer $api_key" \
       --header "Accept=application/json, text/event-stream" \
       --transport http --scope home
     ```

   - Windows (PowerShell)：
     ```powershell
     $apiKey = & "${SKILL_DIR}\get-token.ps1"
     mcporter config remove yuandian-law 2>$null
     mcporter config remove yuandian-case 2>$null
     mcporter config remove yuandian-company 2>$null
     mcporter config add yuandian-law "https://open.chineselaw.com/mcp/law/stream" `
       --header "Authorization=Bearer $apiKey" `
       --header "Accept=application/json, text/event-stream" `
       --transport http --scope home
     mcporter config add yuandian-case "https://open.chineselaw.com/mcp/case/stream" `
       --header "Authorization=Bearer $apiKey" `
       --header "Accept=application/json, text/event-stream" `
       --transport http --scope home
     mcporter config add yuandian-company "https://open.chineselaw.com/mcp/company/stream" `
       --header "Authorization=Bearer $apiKey" `
       --header "Accept=application/json, text/event-stream" `
       --transport http --scope home
     ```

2. **完成注入后**，使用 mcporter 调用：
   ```bash
   mcporter list yuandian-law --schema           # 查看法规服务的工具列表
   mcporter list yuandian-case --schema          # 查看案例服务的工具列表
   mcporter list yuandian-company --schema       # 查看企业服务的工具列表
   mcporter call yuandian-company.<tool> --args '{...}'
   ```

3. **仅当脚本执行失败（exit code ≠ 0）或 mcporter 调用返回 401**，提示用户在集成面板中完成元典智库授权。

### 🚫 禁止行为

- ❌ **禁止**跳过 `get-token.sh` 直接询问用户手动输入 API Key（除非脚本失败）
- ❌ **禁止**使用之前会话中缓存的 API Key 值
- ❌ **禁止**将 API Key 明文输出到终端
- ❌ **禁止**直接 curl 调用 https://open.chineselaw.com/mcp/* — 必须通过 mcporter

## 使用准则

### 准则 1：调用方式

所有工具调用统一通过 `mcporter call <server>.<tool>` 完成；先用 `mcporter list <server> --schema` 获取工具列表与参数规范，再按规范填参数。

### 准则 2：工具选择

- 用户问"法规/法条/规定/条款是否有效/被废止/最新文本" → `yuandian-law`
- 用户问"案件/判决/诉讼/裁判/案例" → `yuandian-case`
- 用户问"公司/工商/股东/控股/关联企业/实际控制人/企业基本信息" → `yuandian-company`
- 涉及多类数据（如「公司涉诉记录」既包含 case 也包含 company） → 分别调用，最后由 Agent 合并归纳

### 准则 3：参数获取顺序

1. 用户**已提供精确实体名/法规名**：直接传入
2. 用户**只给关键词或模糊描述**：先用对应 server 的检索类工具拿候选列表，向用户确认目标后再调用详情类工具
3. 不得编造企业全名、法规序号、案号

### 准则 4：结果呈现

- 输出使用 Markdown，关键字段（公司名、案号、法规名、生效日期、当事人、裁判结果）加粗或表格化
- 引用法规/案例/企业全景时，必须保留原始来源链接或 ID 字段（mcporter 返回中通常带 `url` / `id` / `caseNo` / `creditCode`）
- 涉及风险点（涉诉、行政处罚、股权异常）单独高亮，不要混在普通信息里

## 典型场景示例

### 场景 1：企业风险简报

> 用户：「查一下北京华宇元典信息服务有限公司的基本信息、股东结构和涉诉记录，整理成一份风险简报」

执行顺序：
1. `mcporter call yuandian-company.<search_or_detail>` —— 拿基本信息 + 股东结构
2. `mcporter call yuandian-case.<list_by_company>` —— 拿涉诉记录
3. Agent 整合输出风险简报：
   - 基本信息（统一社会信用代码、注册资本、经营范围、成立日期）
   - 股权结构（股东名称、持股比例、出资额）
   - 涉诉摘要（案件总数、典型案件、裁判结果分布）
   - 风险提示（如有重大诉讼、股权变更频繁、行政处罚）

### 场景 2：法规效力核验

> 用户：「校验这段法律意见书引用的法规是否还有效，并标出失效或已修订的条款」

执行顺序：
1. 解析用户提供的文本，逐条提取「法规名 + 条款序号」
2. 对每条 `mcporter call yuandian-law.<verify_or_detail>` 拿当前效力状态与最新文本
3. Agent 输出对照表：
   - ✅ 有效条款：保留原文
   - ⚠️ 已修订：原文 + 现行文本对比
   - ❌ 已失效/废止：标注失效日期与替代法规

## 错误处理

| 现象 | 处理动作 |
|------|---------|
| `get-token.sh` 退出码 ≠ 0 | 提示用户在集成面板中完成元典智库授权，**禁止**引导用户去 open.chineselaw.com 手动取 Key 填入命令 |
| `mcporter call` 返回 401/403 | 重新执行强制初始化步骤获取最新 token |
| `mcporter list` 找不到 server | 检查初始化是否成功执行；可手动运行 `mcporter config list` 确认 3 个 server 已注册 |
| 工具参数错误 | 重新阅读 `mcporter list <server> --schema` 输出，按返回的 schema 修正参数；**禁止**主动修改用户提供的实体名 |

## 不触发场景

- 通用法律咨询、法律意见生成（仅做规则引用核验时才走本 Skill）
- 个人征信查询（与企业征信不同）
- 实时舆情、新闻、社交媒体内容
