# Arena 模型指纹识别工具包

在 Arena Agent Mode 匿名路由下，识别实际路由到的模型。**不需要 Arena 主动给标签。**

## 包含文件

| 文件 | 作用 |
|---|---|
| `arena-modeltrace.mjs` | ModelTrace 数字探针核心（内嵌 17 个模型签名库） |
| `arena-protocol-probe.mjs` | 协议指纹 + 工具调用探针 + 融合判定引擎 |
| `arena-template-db.mjs` | 开放集模板库 + 会话路由对比 |
| `modeltrace-bank.b64` | ModelTrace reference bank（17 模型，gzip+base64） |
| `arena-register-model.mjs` | 一键给模型建模板（补 bank 缺失的模型） |

## 快速开始

```bash
# 1. 建模板（bank 里没有的模型，如 claude-fable-5-1）
node arena-register-model.mjs <sessionId> claude-fable-5-1

# 2. 探测一次会话（用你现有的发送通道）
node -e "
import('./arena-template-db.mjs').then(async m => {
  const r = await m.fullProbe({
    sendFn: async prompt => await sendToArena(sid, prompt),  // 替换为你的发送函数
    traceLabel: labels[0],   // trace 标签（可选）
    sessionId: sid,
  });
  console.log(r.final);
});
"

# 3. 对比两个会话是否被路由
node -e "
import('./arena-template-db.mjs').then(m => {
  const r = m.compareSessions({
    session1: { traceLabel: 'claude-opus-5-5', profile: profileA },
    session2: { traceLabel: 'gpt-6-luna',      profile: profileB },
  });
  console.log(r.verdict, r.routed, r.reason);
});
"
```

## 三层探测架构

```
Layer 1 被动（零成本，每次请求自动）
  trace 标签 · 协议指纹 · 响应头 · providerRequestId
Layer 2 廉价主动（1 条消息）
  强制工具调用 → 泄漏上游协议帧格式（call_ / toolu_）
Layer 3 完整主动（3 条消息）
  ModelTrace 数字分布指纹 + 开放集模板匹配
```

## 判定等级

| 级别 | 含义 | 来源 |
|---|---|---|
| RESOLVED | 定到具体版本 | trace 标签 / bank 签名 / 响应头 |
| INFERRED | 定到家族 | 协议指纹 / 工具调用帧 |
| UNKNOWN | 无法判定 | — |

## 会话路由对比

`compareSessions()` 用三重证据（trace 标签 / 家族 / 行为指纹）对比两个会话：
- 任一冲突 → `CHANGED`（被路由）
- 双方证据一致 → `SAME`
- 任何一方没证据 → `UNCERTAIN`（不臆断）

## 依赖

- Node.js 18+（内置 zlib，无第三方依赖）
- `arena-register-model.mjs` 需要一个能向 Arena 发消息的通道（sendFn）

## 已知限制

- bank 只有 17 个模型签名，新模型需用 `arena-register-model.mjs` 建模板
- 探针需要真实发消息，Layer 3 一次 3 条
- 模板库文件（arena-templates.json）在首次建模板时自动生成

## 版权

ModelTrace 算法来自 https://github.com/xqy2006/ModelTrace (MIT License)，bank 数据构建于 2026-09-30。
