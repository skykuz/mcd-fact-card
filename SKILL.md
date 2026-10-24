---
name: mcd-fact-card
description: 麦当劳双标签页工具 —— 🍔营养对比（原生 datalist 搜索 67 条餐品，差值换算为楼层/鸡蛋，Top5 榜单，Canvas 导出分享图）+ ⏱️资产体检（券/积分按过期倒计时排序、即将过期高亮、Canvas 体检报告）。零依赖、断网可跑、file:// 双击可用。当需要把抽象营养数字翻译成人话、管理优惠券过期、或需要可断网运行的纯原生对比卡片时使用。
---

# mcd-fact-card

把"这个比那个高多少"翻译成人话。

## 何时使用

- 需要把两份食物的营养差值换算成日常可感知单位（层楼、鸡蛋）。
- 需要一个**零依赖、断网可跑**的对比卡片，可双击直接打开。
- 需要一份可平滑替换为真实数据源（MCP / API）的前端壳。

## 输入 / 输出

| | 说明 |
|---|---|
| 输入 | `menu.json`（餐品数组，字段 `id/name/calories/protein/sodium`） |
| 输出 | 浏览器中的对比卡片：三项指标的双条形对比 + 差值 + 换算结果 |

## 目录结构

```
mcd-fact-card/
├── index.html                 # 单文件对比壳（HTML+CSS+JS 全内联）
├── menu.json                  # 餐品数据
├── README.md                  # 运行与数据说明
├── MCP_INTEGRATION.md         # 接入 list-nutrition-foods 的计划
├── CONTEST_DECLARATION.md     # 参赛声明模板
├── mcp-config.example.json    # MCP 配置示例（{{TOKEN}} 占位）
└── S1验证报告.md              # 验收报告
```

## 数据结构

```json
{
  "version": 2,
  "categories": {"burger": "汉堡", "side": "小食", "drink": "饮料", "dessert": "甜品", "breakfast": "早餐"},
  "items": [
    { "id": "big-mac", "name": "巨无霸", "category": "burger", "calories": 550, "protein": 25.8, "sodium": 1010 }
  ]
}
```

- **规模**：67 条（汉堡 14 / 小食 15 / 饮料 17 / 甜品 12 / 早餐 9）。
- **单位强制**：`calories` 大卡、`protein` 克、`sodium` **毫克**（展示时才换算为克）。
- **数据唯一源**：`_gen_data.py` 同时生成 `menu.json` 与 `index.html` 内嵌兜底数据，改数据只改脚本。
- 数据加载时经过 `normalize()` 校验：缺字段或类型非数字的条目会被直接剔除，不会渲染出 `NaN`。

## 换算口径（唯一真源）

| 指标 | 计算 | 输出单位 |
|---|---|---|
| 热量 | `|Δkcal| / 15` | 层楼（1 位小数） |
| 蛋白质 | `|Δg| / 6` | 个鸡蛋（1 位小数） |
| 钠 | `|Δmg| / 1000` | 克（2 位小数） |

## 交互规范

1. 两个**搜索输入框**基于原生 `<input list>` + `<datalist>`（67 条 option，`label` 附分类与热量）。
2. **输入值必须校验**：datalist 只提供建议，手输任意值不产生选中态 —— 值必须精确匹配某个
   `item.name` 才算选中，保证输入框的名字与对比数据永远一致。
3. **未选 / 只选一个 / 两边同款 → 不显示卡片**，显示空态提示。
4. 选中两个不同餐品 → 实时渲染；输入框 `×` 清除；中间 `⇄` 交换 A / B。
5. **榜单**：底部「🔥 热量刺客 Top 5」（卡路里降序前 5）与「🌱 减脂红榜 Top 5」（升序前 5），
   直接读数据排序，随数据自动更新。
6. **分享**：对比卡右上「生成图片」→ 原生 `<canvas>` 手绘（2× DPR）→ `toDataURL` → `<a download>` 下载。

## 视觉与文案规范

- **字体层级**：差值 = 特大数字（34px/800，375px 下降至 27px）+ 小单位（13px）。
- **对比条**：差值下方 A/B 占比切分圆角条（A 朱橙 `#FF4A1C`、B 墨黑 `#141110`），附百分比图例。
- **情绪化文案**：`emotionText()` 按差值分档输出网感表达（≥300 大卡「帕梅拉白跳了」、
  ≥800mg「钠含量直接爆表」等）；**页面与导出图必须共用此函数**，不得两处各写一套。
- **微交互**：卡片 `fadeUp` 淡入、差值数字 `pop` 弹入（hidden 切换后需移除/重加 class 强制重放）、
  按钮 hover 上浮 + 加深阴影、榜单行 hover 轻移。
- **响应式**：560px 断点（选择器/榜单单列、大数字 30px）+ 375px 断点（27px、64px 名称列）；
  验收标准：`document.documentElement.scrollWidth <= clientWidth`。
- **canvas 差值块背景**必须与页面一致（`rgba(255,74,28,.08)`），两处颜色不同源是实测踩过的坑。

## 资产体检模块（T5）

- **数据**：`assets.json`（8 条模拟资产：满减券/兑换券/次数/积分），字段
  `id/name/face/unit/count/estimate/expireAt`；`expireAt` 为毫秒时间戳，允许 `null`。
- **时间戳解析**：`parseExpire()` 兼容数字/数字字符串/ISO 字符串/秒级时间戳；
  **任何解析失败一律返回 null 并渲染为「未知时间」，绝不抛错白屏**。
- **排序**：未过期（剩余时间升序）→ 已过期 → 未知时间。
- **高亮**：剩余 <24h 朱橙高亮 +「即将过期」标签；已过期置灰。
- **总览**：总资产估值（Σ estimate×count）与 24h 内即将流失金额/条数。
- **报告导出**：与营养分享图共用 roundRect/drawBar 等绘制基建；文件名含生成时间戳。
- **数据同源**：`assets.json` 与内嵌兜底由 `_gen_data.py` 同一时刻生成（时间戳 = 生成时刻 + 相对偏移，
  重跑脚本即刷新为当前时间基准）。

## 红线（不得违反）

- **严禁**任何 UI 框架（Vue / React / jQuery）、CSS 框架、图标字体、CDN、外部 API、统计脚本。
- **严禁**在代码中写入任何真实 Token / 密钥，配置示例只允许 `{{TOKEN}}` 占位符。
- **必须**断网可跑：任何资源不得来自网络。
- **配色固定**：纸色 `#F3EADA`、墨色 `#141110`、朱橙 `#FF4A1C`。

## 关键实现要点（踩坑固化）

### 1. `file://` 下读不了本地 json

Chromium（Chrome / Edge）在 `file://` 下会以 CORS 策略拦截 `fetch()` 与 `XMLHttpRequest` 读取本地 json，
双击打开必然失败。因此采用**三级降级**：

```
fetch('menu.json') → XMLHttpRequest → 内置同源兜底数据
```

命中兜底时页面顶部显示提示条，并给出 `python -m http.server` 方案。
兜底数据与 `menu.json` **由同一脚本 `_gen_data.py` 生成，绝对一致**（脚本内有断言校验），
双击场景展示效果无差别（67 条全量内嵌，单文件 28.6 KB，远低于 100 KB 抽离阈值）。

### 2. 验证手法

页面 JS 包在 IIFE 里，内部函数外部调不到。自动化验证只能靠事件驱动模拟真实操作：

```js
// datalist 选餐品（输入值 → input 事件 → 内部校验）
input.value = '巨无霸';
input.dispatchEvent(new Event('input'));
// Canvas 导出：stub 掉 <a>.click() 避免 headless 触发真实下载挂起，
// 同时捕获 href（data:image/png 前缀）与 download 文件名
HTMLAnchorElement.prototype.click = function () { window.__href = this.href; };
shareBtn.click();
```

注意：headless 下真实触发 `<a download>` 下载会让进程挂起 —— **必须 stub `click()`**，
再从捕获的 `href` 解码 base64 落盘，用肉眼核验绘制内容（DOM 正确 ≠ 画布正确）。

配合 Headless 浏览器导出 DOM：

```bash
msedge.exe --headless=new --disable-gpu --no-sandbox \
  --virtual-time-budget=8000 --dump-dom "file:///.../index.html"
```

- 不带 `--allow-file-access-from-files` → 验证兜底分支（提示条应出现）。
- 带该 flag 且给 `menu.json` 打标记值 → 验证 `menu.json` 确为真实数据源。

## 验收清单

- [ ] 双击 `index.html` 能看到完整页面（纸色背景、卡片居中圆角阴影）。
- [ ] 未选 / 只选一个 / 同款 → 不显示卡片。
- [ ] 选两个不同餐品 → 卡片渲染，三项指标与换算值正确。
- [ ] 断网状态下功能不受影响。
- [ ] 全文检索无 `cdn`、`unpkg`、`vue`、`react` 等外部依赖痕迹。
