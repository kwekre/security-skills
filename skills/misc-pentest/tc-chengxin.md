---
name: tc-chengxin
description: 同程程心 Skill - 基于同程旅行大模型（程心）的在线旅游搜索能力。提供更专业的机票、火车票、酒店、度假产品（自由行/跟团游）、旅游攻略、行程规划、特价机票、汽车票、长途汽车、景区、门票等的查询能力，基于同程官方数据，更加实时准确可靠，一键进入预订页面，让旅行更简单，更快乐。
metadata:
  author: 同程网络科技股份有限公司
  homepage: https://www.ly.com
  openclaw:
    requires:
      bins: ["node"]
    primaryEnv: CHENGXIN_API_KEY
    env:
      - name: CHENGXIN_API_KEY
        description: 同程程心 API Key（未配置时可使用试用额度，超出后需申领激活码）
        required: false
---

# tc-chengxin - 同程程心 Skill

_同程旅行官方旅游助手_

---

## 🔧 环境与认证

### ⚡ 强制初始化（每次加载 Skill 必须执行）

**进入本 Skill 后，在执行任何用户操作之前，必须先完成 Token 获取。不得跳过此步骤。**

#### 执行步骤

1. **调用 Token 获取脚本**（根据当前操作系统，`SKILL_DIR` 为本 skill 根目录）：
   - macOS/Linux：
     ```bash
     CHENGXIN_API_KEY=$(bash "${SKILL_DIR}/get-token.sh")
     ```
   - Windows：
     ```powershell
     $token = & "${SKILL_DIR}\get-token.ps1"
     ```

2. **将获取到的 token 用于后续 API 调用**，作为 `Authorization: Bearer ${CHENGXIN_API_KEY}` header 传入。

3. **仅当脚本执行失败（exit code ≠ 0）时**，提示用户在集成面板中完成同程程心授权。

#### 🚫 禁止行为

- ❌ **禁止**跳过脚本直接询问用户手动输入 token（除非脚本失败）
- ❌ **禁止**使用之前会话中缓存的 token 值
- ❌ **禁止**将 token 明文输出到终端

### Token 使用方式

| 通道 | 使用方式 |
|------|----------|
| REST API | HTTP请求头 `Authorization: Bearer ${CHENGXIN_API_KEY}` |
| MCP 连接 | `headers.Authorization: Bearer ${CHENGXIN_API_KEY}` |

> ⚠️ Token 有效期 **30 天**，每次调用脚本都会获取最新有效 token。若 API 返回 401 错误，重新执行脚本获取新 token。

---

## ✅ 执行前自检清单

调用本技能前,大模型必须确认:

1. [ ] 已执行 Token 获取脚本（见上方「环境与认证」）
2. [ ] 已读取用户查询的完整文本(包含日期、时间、人数等)
3. [ ] 已确定正确的意图类型或查询方式
4. [ ] 已从 Inbound Context 获取 `channel` 和 `surface` 参数
5. [ ] 准备调用正确的专用脚本(见「何时使用」与各节示例)
6. [ ] 准备**输出脚本的查询结果**，以及预订链接

---

## 🎯 用户需求保留原则（重要）

调用本技能时，用户的任何**修饰性需求**都不应被丢弃，必须完整传入 `--extra`。

| 需求类型 | 示例关键词 | 处理方式 |
|---------|-----------|---------|
| **时间偏好** | 最早、最晚、上午、下午、晚上、夜间 | 传入 `--extra` |
| **价格偏好** | 最便宜、低价、经济型、预算有限 | 传入 `--extra`（机票特价需求可配合 `--low-price`） |
| **服务等级** | 高铁、动车、一等座、商务舱、五星级、含早餐 | 传入 `--extra` |
| **行程偏好** | 直飞、中转、经停、少换乘、快、自驾 | 传入 `--extra` |
| **人群偏好** | 亲子、情侣、老人、宠物友好 | 传入 `--extra` |
| **特色筛选** | 免费、夜景、夜游、赏花、海景 | 传入 `--extra` |

> ⚠️ **规则**：先提取结构化参数（出发地/目的地/日期等），剩余**所有修饰用户需求**全部拼接到 `--extra` 中，不得省略。补偿查询时，`extra` 会原样传递给下游接口，确保需求链不中断。

---

## 🎯 何时使用

| 意图类型 | 用户示例 | 调用方式 |
|---------|---------|---------|
| **机票查询** | "北京到上海的机票"、"明天飞广州的航班" | **`flight-query.js`** |
| **特价机票** | "上海到北京的特价机票"、"北京出发的特价机票"、"从上海飞哪里便宜" | **`flight-query.js --low-price`**（可与 `--destination` 同时使用） |
| **火车票查询** | "北京到上海的高铁"、"苏州到上海的火车票" | **`train-query.js`** |
| **酒店查询** | "上海外滩附近的酒店"、"下周一北京的五星级酒店" | **`hotel-query.js`** |
| **长途汽车 / 汽车票** | "北京到上海的长途汽车"、"苏州到上海的大巴"、"苏州到南京的汽车票"、"买张苏州到北京客运票" | **`bus-query.js`** |
| **度假产品 / 跟团游 / 自由行 / 行程规划** | "云南旅游团"、"三亚自由行"、"帮我规划北京三日游"、"从苏州出发到杭州玩三天" | **`travel-query.js`** |
| **交通查询** | "北京到上海怎么走"、"去苏州有什么交通方式"、"苏州到南京" | **`traffic-query.js`** |
| **景区查询** | "苏州有哪些景区"、"上海迪士尼门票"、"杭州有什么好玩的景点" | **`scenery-query.js`** |

> ⚠️ **路由规则**:上表每一类意图**只**通过对应的 `*-query.js` 调用 API;参数不足时**引导用户补齐**后再执行脚本,不使用其它入口替代。

## 🚗 交通资源智能查询 (traffic-query.js)

> 🚨 **智能推荐**:当用户**未明确指定交通方式**时使用此接口!

**智能交通查询能力**,同时返回机票、火车票、汽车票等多种交通方式,方便用户对比选择。

### 使用场景

| 场景 | 示例 | 推荐接口 |
|------|------|---------|
| 用户明确说"火车票" | "北京到上海的火车票" | `train-query.js` ✅ |
| 用户明确说"机票" | "明天飞北京的航班" | `flight-query.js` ✅ |
| 用户明确说"汽车票/大巴/客运"(公路) | "苏州到南京的汽车票"、"买大巴票" | `bus-query.js` ✅ |
| **用户未指定交通方式** | "北京到上海怎么走" | **`traffic-query.js`** ✅ |

### 合法参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |

### 参数说明

| 参数 | 说明 |
|------|------|
| `--departure <城市>` | 出发地城市(必填) |
| `--destination <城市>` | 目的地城市(必填) |
| `--extra <补充信息>` | 额外信息(日期、偏好等) |

### extra 参数示例

- `"明天"` - 明天的班次
- `"自驾"` - 偏好自驾路线
- `"明天 高铁优先"` - 多条件组合
- `"最早"` / `"最晚"` - 时间偏好
- `"最便宜"` - 价格优先

### 调用示例

```bash
# 北京到上海,智能推荐交通方式
node scripts/traffic-query.js --departure "北京" --destination "上海" --channel webchat --surface webchat

# 明天出发
node scripts/traffic-query.js --departure "北京" --destination "上海" --extra "明天" --channel webchat --surface webchat

# 包含自驾偏好
node scripts/traffic-query.js --departure "苏州" --destination "南京" --extra "自驾" --channel webchat --surface webchat
```

### 输出结果

**同时展示多种交通方式**:
- 🚄 火车票
- ✈️ 机票
- 🚌 汽车票

**每种交通方式都包含**:
- 完整班次/航班信息

### 调用优先级

> ⚠️ **重要**: `traffic-query.js` 的调用优先级**低于**专用查询接口!

**正确用法:**
1. 用户说"火车票" → 使用 `train-query.js`
2. 用户说"机票" → 使用 `flight-query.js`
3. 用户说"汽车票" → 使用 `bus-query.js`
4. 用户**未指定**交通方式 → 使用 `traffic-query.js`

---

## ✈️ 机票专用查询 (flight-query.js)

> 🚨 **优先级最高**:查询机票时,**必须优先使用此方法**!

**更精准的机票查询能力**,支持航班号精确查询、特价机票查询、多列表推荐。

### 合法参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |
| 航班号 | `--flight-number "CA1234"` | 精确查航班 |
| 出发地 + lowPrice | `--departure "北京" --low-price` | 特价/低价（未指定目的地时,可查多地低价推荐） |
| 出发地 + 目的地 + lowPrice | `--departure "上海" --destination "北京" --low-price` | 指定航线上的特价/低价查询 |

### 参数说明

| 参数 | 说明 |
|------|------|
| `--departure <城市>` | 出发地城市 |
| `--destination <城市>` | 目的地城市 |
| `--flight-number <航班号>` | 航班号 (如 CA1234) |
| `--extra <补充信息>` | 额外信息 (日期、偏好等) |
| `--low-price` | 特价/低价查询;**可与 `--destination` 同用**(指定航线),也可**仅出发地**(多地低价推荐) |

### lowPrice 参数说明

`--low-price` 表示用户要**特价、低价、便宜**等优惠向机票,有两种常见说法:

1. **已说明出发地与目的地**(如「上海到北京的特价机票」):同时传 `--departure`、`--destination` 与 `--low-price`,查该航线上的低价/特价结果。
2. **只说了出发地或未点明目的地**(如「从北京出发哪里便宜」):仅传 `--departure` 与 `--low-price`,由接口返回从该地出发的低价推荐(含目的地推荐)。

**触发关键词:**
- "特价机票"、"低价机票"、"便宜机票"
- "A 到 B 的特价票"、"XX 飞 YY 最便宜"
- "从 XX 出发哪里便宜"、"XX 出发的优惠机票"
- "清明节/五一/春节 特价机票"(节假日低价推荐)

**示例场景:**
| 用户查询 | 调用方式 | 说明 |
|---------|---------|------|
| "上海到北京的特价机票" | `--departure "上海" --destination "北京" --low-price` | 指定航线特价/低价 |
| "北京出发的特价机票" | `--departure "北京" --low-price` | 北京出发低价航线/推荐 |
| "清明节北京出发的特价机票" | `--departure "北京" --low-price --extra "清明节"` | 带节假日条件 |
| "从上海飞哪里便宜" | `--departure "上海" --low-price` | 查询低价目的地推荐 |
| "周末从广州出发哪里好玩" | `--departure "广州" --low-price --extra "周末"` | 带时间偏好 |

### `--low-price` 与 `--extra` 的协同

`--low-price` 用于触发特价/低价专属查询逻辑，可与 `--extra` 同时使用以叠加更多用户需求：

| 用户查询 | 调用方式 | 说明 |
|---------|---------|------|
| "上海到北京明天最便宜的机票" | `--departure "上海" --destination "北京" --low-price --extra "明天 最便宜"` | 指定航线 + 特价逻辑 + 时间/价格偏好 |
| "北京出发哪里便宜（要最早的）" | `--departure "北京" --low-price --extra "最早"` | 低价推荐 + 时间偏好 |
| "清明节北京出发的特价机票" | `--departure "北京" --low-price --extra "清明节"` | 低价推荐 + 节假日 |

> 原则：`--low-price` 负责触发 API 的特价/低价查询逻辑；`--extra` 负责承载用户的其他修饰需求（时间、偏好等）。两者不互斥。

**引导话术(仅出发地、未说目的地时):**
```
💡 您只提供了出发地,没有指定目的地。
您可以:
1. 补充目的地 (如:北京到上海),需要特价可加 --low-price
2. 或继续用 --low-price 查看从该地出发到全国各地的低价推荐
```

### 调用示例

```bash
# 北京到上海，明天的机票
node scripts/flight-query.js --departure "北京" --destination "上海" --extra "明天" --channel webchat --surface webchat

# 查询特定航班
node scripts/flight-query.js --flight-number "CA1234" --channel webchat --surface webchat

# 指定航线特价(上海 → 北京)
node scripts/flight-query.js --departure "上海" --destination "北京" --low-price --channel webchat --surface webchat

# 从北京出发的特价/低价推荐(未指定目的地)
node scripts/flight-query.js --departure "北京" --low-price --channel webchat --surface webchat

# 清明节北京出发的特价/低价
node scripts/flight-query.js --departure "北京" --low-price --extra "清明节" --channel webchat --surface webchat
```

### 参数不完整时的处理

若用户**只提供出发地**、未提供目的地:**提示用户**要么补充目的地(可加 `--low-price` 查该航线特价),要么使用 `--low-price` 查从该地出发的低价推荐。

### 无结果时的备选策略（临近出发机场 / 空铁联运）

当 `flight-query.js` **无航班**、脚本输出「无结果」或 API `code` 为 `1`（见 `references/error-handling.md`）时,可引导用户尝试「从临近枢纽机场所在城市出发」的空铁联运思路。**原则**:不编造航班、价格与预订链接;航班与链接**只**能来自脚本输出,地面段车次、班次与链接**只**能来自对应脚本输出。

1. **说明与备选出发地**:告知用户当前出发地直飞无合适结果,可尝试从**区域枢纽机场所在城市**等临近点出发;结合地理常识给出 **1～2 个**备选城市即可,在**脚本返回前**不要写出该城市出发的具体航班、价格或链接。
2. **重查机票(替代出发地)**:对**每个**备选出发城市再次执行 `flight-query.js`:将 `--departure` 改为该临近城市,**保持** `--destination`、`--extra` 与用户原查询一致,并沿用相同 `--channel` / `--surface`,**完整输出**脚本结果。  
   `node scripts/flight-query.js --departure "<临近城市>" --destination "<原目的地>" [--extra "<原日期/偏好>"]` 及相同的 `--channel` / `--surface`
3. **地面衔接**:若需展示用户常住地/原出发城市 → 临近出发城市的衔接,通过 **`train-query.js`**、**`traffic-query.js`** 或必要时 **`bus-query.js`** 查询,**仅**采用脚本返回的车次、班次与链接。
4. **换乘与时间**:结合脚本给出的出发/到达时刻提示预留换乘与进站时间;值机、安检与建议到达机场时间属**出行常识**,非 API 实时数据,仅作缓冲说明并提醒以航司、机场与出票信息为准。国内线可提示常见**不晚于起飞前约 1.5～2 小时**到机场办理乘机手续,国际线或大型枢纽宜更久。

---

## 🏨 酒店专用查询 (hotel-query.js)

> 🚨 **优先级最高**:查询酒店时,**必须优先使用此方法**!

**更精准的酒店查询能力**,支持位置偏好、日期指定等多列表推荐。

### 合法参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 目的地城市 | `--destination "上海"` | 按城市查询 |
| 目的地 + 位置偏好 | `--destination "上海" --extra "外滩附近"` | 指定区域 |
| 目的地 + 入住日期 | `--destination "上海" --extra "明天入住"` | 指定日期 |

### 参数说明

| 参数 | 说明 |
|------|------|
| `--destination <城市>` | 目的地城市(必填) |
| `--extra <补充信息>` | 额外信息(日期、位置偏好等) |

### extra 参数示例

- `"明天入住"` - 明天入住
- `"外滩附近"` - 外滩附近区域
- `"最便宜"` - 价格优先
- `"五星级"` - 星级筛选
- `"含早餐"` - 设施偏好
- `"明天入住 外滩附近 五星级"` - 多条件组合

### 调用示例

```bash
# 上海酒店,明天入住
node scripts/hotel-query.js --destination "上海" --extra "明天入住" --channel webchat --surface webchat

# 上海外滩附近的酒店
node scripts/hotel-query.js --destination "上海" --extra "外滩附近" --channel webchat --surface webchat

# 简单查询(仅目的地)
node scripts/hotel-query.js --destination "上海" --channel webchat --surface webchat
```

### 参数不完整时的处理

如果用户没有提供目的地:**提示用户补充目的地城市**。

---

## 🏞️ 景点专用查询 (scenery-query.js)

> 🚨 **优先级最高**:查询景点时,**必须优先使用此方法**!

**更精准的景点查询能力**,支持特色筛选、类型推荐等多列表推荐。

### 合法参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 目的地城市 | `--destination "杭州"` | 按城市查询 |
| 目的地 + 特色 | `--destination "杭州" --extra "适合亲子"` | 指定特色 |
| 目的地 + 类型 | `--destination "苏州" --extra "园林 5A 景区"` | 指定类型 |

### 参数说明

| 参数 | 说明 |
|------|------|
| `--destination <城市>` | 目的地城市(必填) |
| `--extra <补充信息>` | 额外信息(特色、类型等) |

### extra 参数示例

- `"适合亲子"` - 亲子游景点
- `"5A 景区"` - 5A 级景区
- `"免费"` - 免费景点
- `"夜景"` / `"夜游"` - 时段特色
- `"适合亲子 5A 景区 免费"` - 多条件组合

### 调用示例

```bash
# 杭州景点,适合亲子
node scripts/scenery-query.js --destination "杭州" --extra "适合亲子" --channel webchat --surface webchat

# 苏州园林景点
node scripts/scenery-query.js --destination "苏州" --extra "园林" --channel webchat --surface webchat

# 简单查询(仅目的地)
node scripts/scenery-query.js --destination "杭州" --channel webchat --surface webchat
```

### 参数不完整时的处理

如果用户没有提供目的地:**提示用户补充目的地城市**。

---

## 🧳 旅行资源专用查询 (travel-query.js)

> 🚨 **度假产品/跟团游/自由行专属接口**：当用户提到**旅游团、跟团游、自由行、度假、玩几天、几日游、规划行程**时，**必须**使用此接口！

> ⚠️ **与 scenery-query.js 的边界**：
> - 用户说"**云南旅游团**"、"**三亚自由行**"、"**玩三天**" → `travel-query.js` ✅（要的是**旅游产品/套餐**）
> - 用户说"**三亚有哪些景点**"、"**上海迪士尼门票**" → `scenery-query.js` ✅（要的是**景点列表/门票**）



**专业的度假产品查询能力**,支持自由行、跟团游等多种旅游产品推荐。

### 使用场景

| 场景 | 示例 | 推荐接口 |
|------|------|---------|
| 用户查询"三亚自由行" | "三亚自由行套餐" | **`travel-query.js`** ✅ |
| 用户查询"云南旅游团" | "云南6天5晚跟团游" | **`travel-query.js`** ✅ |
| 用户有明确意向 | "我想去三亚玩" | **`travel-query.js`** ✅ |
| 用户要行程规划 | "帮我规划北京三日游" | **`travel-query.js`** ✅ |
| 用户说"玩几天" | "苏州到杭州玩三天" | **`travel-query.js`** ✅ |

### 典型用户说法（看到这些关键词直接用 travel-query.js）

| 用户说法 | 关键词 | 调用 |
|---------|--------|------|
| "**云南旅游团**"、"**跟团游**" | 旅游团、跟团 | `travel-query.js` |
| "**三亚自由行**"、"**自由行套餐**" | 自由行 | `travel-query.js` |
| "**玩三天**"、"**几日游**"、"**规划行程**" | 天数、行程 | `travel-query.js` |
| "**从苏州出发到杭州玩**" | 出发地 + 玩 | `travel-query.js` |
| "**度假**"、"**度假产品**" | 度假 | `travel-query.js` |

### 合法参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 目的地 | `--destination "三亚"` | 按城市/地区查询 |
| 出发地 + 目的地 | `--departure "苏州" --destination "杭州"` | 含往返交通规划 |
| 出发地 + 目的地 + 天数 | `--departure "苏州" --destination "杭州" --extra "3天2晚"` | 含行程规划 ⭐ |
| 目的地 + 天数 + 类型 | `--destination "云南" --extra "6天5晚 自由行"` | 指定行程 |

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--departure <城市>` | 可选 | 出发地城市，提供后可触发 AI 推荐往返交通+完整行程规划 |
| `--destination <城市/地区>` | ✅ | 目的地城市或地区 |
| `--extra <补充信息>` | 可选 | 额外信息(假期、天数、类型、行程规划请求等) |

### extra 参数示例

- `"五一假期"` - 五一期间
- `"3天2晚"` / `"6天5晚"` - 行程天数
- `"自由行"` / `"跟团游"` - 自由行产品、跟团游产品
- `"帮我规划南京三日游行程"` - 触发 AI 行程规划（推荐配合 departure 使用）
- `"苏州到杭州 3天2晚 自由行"` - 出发地+天数+类型组合
- `"五一假期 6天5晚 自由行"` - 多条件组合
- `"最便宜"` - 价格优先
- `"海景"` / `"亲子"` - 主题偏好

### 调用示例

```bash
# 经典场景：从某地出发到某地玩几天（推荐）；返回：交通推荐 + 酒店 + 景区 + 行程规划 + 度假产品 + UGC攻略
node scripts/travel-query.js --departure "苏州" --destination "杭州" --extra "3天2晚" --channel webchat --surface webchat

# 仅目的地查询
node scripts/travel-query.js --destination "三亚" --channel webchat --surface webchat

# 带假期条件
node scripts/travel-query.js --destination "三亚" --extra "五一假期" --channel webchat --surface webchat

# 指定天数和类型
node scripts/travel-query.js --destination "云南" --extra "6天5晚 自由行" --channel webchat --surface webchat
```

---

## 🚌 长途汽车专用查询 (bus-query.js)

> 🚨 **优先级最高**:查询长途汽车时,**必须优先使用此方法**!

**更精准的长途汽车查询能力**,支持站到站精确查询、多列表推荐。

### 使用场景与同义词

| 用户常怎么说 | 说明 |
|-------------|------|
| **汽车票**、**大巴票**、**客运**、**长途汽车**、**班车** | 均指公路客运班次,**全部**路由到本节 `bus-query.js` |

### 合法参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |
| 出发站 + 到达站 | `--departure-station "北京六里桥客运站" --arrival-station "上海长途汽车客运站"` | 精确站点查询 |

### 参数说明

| 参数 | 说明 |
|------|------|
| `--departure <城市>` | 出发地城市 |
| `--destination <城市>` | 目的地城市 |
| `--departure-station <站>` | 出发站(精确) |
| `--arrival-station <站>` | 到达站(精确) |
| `--extra <补充信息>` | 额外信息(日期、偏好等) |

### extra 参数示例

- `"明天"` - 明天的班次
- `"上午"` - 上午出发的班次
- `"最早"` / `"最晚"` - 时间偏好
- `"最便宜"` - 价格优先
- `"明天 上午"` - 多条件组合

### 调用示例

```bash
# 北京到上海,明天的长途汽车
node scripts/bus-query.js --departure "北京" --destination "上海" --extra "明天" --channel webchat --surface webchat

# 站到站精确查询
node scripts/bus-query.js --departure-station "北京六里桥客运站" --arrival-station "上海长途汽车客运站" --channel webchat --surface webchat

# 简单查询(仅城市)
node scripts/bus-query.js --departure "北京" --destination "上海" --channel webchat --surface webchat
```

### 参数不完整时的处理

如果用户只提供了部分参数:**提示用户补充参数**。

---

## 🚂 火车票专用查询(train-query.js)

> 🚨 **优先级最高**:查询火车票时,**必须优先使用此方法**!

**更精准的火车票查询能力**,支持站到站、车次精确查询。

**为什么优先使用:**
- ✅ 调用专用 API 接口(`/gateway/trainResource`)
- ✅ 返回更丰富的车次选择
- ✅ 支持结构化参数(出发地、目的地、车次号、偏好等)
- ✅ 参数不完整时会明确提示用户补齐

### 合法参数组合

| 组合 | 参数示例 | 说明 |
|------|---------|------|
| 出发地 + 目的地 | `--departure "北京" --destination "上海"` | 按城市查询 |
| 车次号 | `--train-number "G1234"` | 精确查车次 |
| 出发站 + 到达站 | `--departure-station "北京南站" --arrival-station "上海虹桥站"` | 精确站点查询 |

### 参数说明

| 参数 | 说明 |
|------|------|
| `--departure <城市>` | 出发地城市 |
| `--destination <城市>` | 目的地城市 |
| `--departure-station <站>` | 出发站(精确) |
| `--arrival-station <站>` | 到达站(精确) |
| `--train-number <车次>` | 车次号(如 G1234) |
| `--extra <补充信息>` | 额外信息(日期、偏好等) |

### extra 参数示例

- `"明天"` - 明天的车次
- `"高铁"` - 只查高铁
- `"动车"` - 只查动车
- `"一等座"` - 优先一等座
- `"最早"` / `"最晚"` - 时间偏好
- `"最便宜"` - 价格优先
- `"明天 高铁 赏花专线"` - 多条件组合

### 参数不完整时的处理

如果用户只提供了部分参数,**必须提醒用户补齐**:

```
⚠️ 参数不完整,请提供以下组合之一:
  1. 出发地 + 目的地
  2. 车次号
  3. 出发站 + 到达站
```

---

## 🚀 标准执行流程

### 步骤 1:保留完整 query

包括日期、时间、人数等所有信息:
- ✅ `"3 月 29 日苏州到上海火车票"`
- ✅ `"明天北京到上海的机票"`
- ✅ `"下周一南京夫子庙附近酒店"`

### 步骤 2:调用专用脚本(唯一数据源)

按「何时使用」选择 `scripts/` 下对应的 `*-query.js`,传入结构化参数与 `channel`、`surface`。示例(火车票):

```bash
node scripts/train-query.js --departure "北京" --destination "上海" --extra "明天 高铁" --channel webchat --surface webchat
```

### 步骤 3:原样输出脚本结果

**必须完整输出脚本返回的所有内容:**
- 表格或卡片格式。逻辑由 `scripts/lib/output-mode.js` 的 `resolve_output_mode` 实现。
- 底部引导语

**禁止:**
- ❌ 修改表格格式
- ❌ 省略底部引导语
- ❌ 添加脚本未返回的信息

---

## 🎁 如何获取 API Key (CHENGXIN_API_KEY)

当鉴权失败或需要配置 API Key 时,请按以下方式申领:

1. 打开 **同程旅行 APP** 或 **同程旅行小程序**(微信 - 我 - 服务 → 火车票机票/酒店民宿)
2. 在顶部搜索栏中搜索「**程心激活码**」
3. 按页面提示完成申领即可获取 API Key
4. 将激活码配置到环境变量或 `config.json` 文件中。环境变量与本地 `config.json` 的配置方式、示例与注意事项详见 `references/config.md`。

> 💡 **快捷方式**:也可以直接回复「**帮我把 xxxxx(激活码)配置到 tc-chengxin 这个 skill 上**」,助手会自动帮你完成配置。

---

## ⚠️ 错误处理

### API Key 未配置或无效

展示申领引导(见 `references/error-handling.md`)

### 错误码处理

| Code | 处理方式 |
|------|---------|
| `0` | 正常解析并输出结果 |
| `1` | 告知用户未找到相关资源,建议调整搜索词 |
| `3` | 检查是否为鉴权问题,展示对应引导 |

**详细错误处理指南**:见 `references/error-handling.md`

---

## 📞 客服支持

使用过程中遇到问题?同程旅行提供 7×24 小时服务:

- **📞 旅行者热线**:**95711**
- **💬 在线客服**:[https://www.ly.com/public/newhelp/CustomerService.html](https://www.ly.com/public/newhelp/CustomerService.html)

---

## 📚 参考文档

- `references/output-format.md` - 输出格式示例(表格/卡片)
- `references/error-handling.md` - 错误处理指南
- `references/api-examples.md` - API 调用示例

---

## 🔒 隐私与数据处理说明

本技能会将用户查询发送到**同程官方 API** (`https://wx.17u.cn/skills/gateway/api/v1/gateway`)，以获取实时旅行结果。

- **发送内容**：结构化参数（出发地、目的地、日期等）和自由文本意图（`--extra` 字段）。
- **发送去向**：仅发送至同程官方 API，无第三方服务。
- **不会做的事**：不记录用户查询日志、不收集遥测数据、不窃取环境变量或本地文件。
- **预订链接**：由官方 API 生成，指向 `ly.com` / `17u.cn` 域名，无中间跟踪。

如对查询文本中的个人信息有顾虑，请避免输入敏感信息，或直接查看 `scripts/lib/api-client.js`（网络调用）和 `scripts/lib/query-response.js`（响应处理）以确认数据流向。

---

_同程旅行 · 让旅行更简单,更快乐_