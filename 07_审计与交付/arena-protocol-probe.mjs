/**
 * arena-protocol-probe.mjs — Layer 1 被动探针 + Layer 2 工具调用探针
 *
 * 零依赖、纯函数，可在 Node.js / 浏览器 / 油猴脚本里直接 import。
 * 不改任何现有生产脚本。
 *
 * 用法:
 *   import { protocolFingerprint, classifyRequestId, verdict, TOOL_CALL_PROBE } from './arena-protocol-probe.mjs';
 *
 *   // 被动：拿到 SSE 流文本后
 *   const proto = protocolFingerprint(sseText);
 *   // → [{ family: 'openai', label: '...', matched: [...], score: 0.72 }, ...]
 *
 *   // 被动：拿到 providerRequestId 后
 *   const rid = classifyRequestId('chatcmpl-abc123def456');
 *   // → { family: 'openai', format: 'chatcmpl', confidence: 0.80 }
 *
 *   // 融合判定
 *   const v = verdict(allEvidence);
 *   // → { mode: 'RESOLVED'|'INFERRED'|'UNKNOWN', modelId, family, confidence, ... }
 *
 *   // 主动：工具调用探针提示词
 *   console.log(TOOL_CALL_PROBE);
 */

// ============================================================
//  一、协议指纹规则 (FAMILY_PROTOCOLS)
// ============================================================

const FAMILY_PROTOCOLS = [
  {
    family: 'anthropic', weight: 0.72, label: 'Anthropic Messages API',
    tests: [
      { name: 'message_start 帧',           re: /"type"\s*:\s*"message_start"/ },
      { name: 'content_block_delta 帧',      re: /"type"\s*:\s*"content_block_delta"/ },
      { name: 'thinking_delta 帧',           re: /"type"\s*:\s*"thinking_delta"/ },
      { name: 'stop_reason 枚举',            re: /"stop_reason"\s*:\s*"(?:end_turn|max_tokens|stop_sequence|tool_use|refusal)"/ },
      { name: 'cache_creation_input_tokens',  re: /"cache_creation_input_tokens"/ },
      { name: 'toolu_ 工具 id',              re: /\btoolu_[A-Za-z0-9]{6,}/ },
      { name: 'Anthropic 版本头',             re: /anthropic-version/i },
    ],
  },
  {
    family: 'openai', weight: 0.70, label: 'OpenAI Chat Completions',
    tests: [
      { name: 'chatcmpl- id（厂商独有）',     re: /\bchatcmpl-[A-Za-z0-9]{6,}/ },
      { name: 'system_fingerprint',          re: /"system_fingerprint"\s*:\s*"/ },
      { name: 'prompt_tokens_details',       re: /"cached_tokens"\s*:/ },
      { name: 'call_ 工具 id（厂商独有）',    re: /\bcall_[A-Za-z0-9]{6,}/ },
      { name: 'logprobs 字段',               re: /"logprobs"\s*:\s*(?:null|\[|\{)/ },
      { name: 'object=chat.completion.chunk', re: /"object"\s*:\s*"chat\.completion(?:\.chunk)?"/ },
      { name: 'choices[].delta',             re: /"choices"\s*:\s*\[\s*\{[^}]*"delta"/ },
    ],
  },
  {
    family: 'openai', weight: 0.75, label: 'OpenAI Responses API',
    tests: [
      { name: 'response.created 帧',         re: /"type"\s*:\s*"response\.created"/ },
      { name: 'response.output_text.delta',  re: /"type"\s*:\s*"response\.output_text\.delta"/ },
      { name: 'resp_ id',                    re: /\bresp_[A-Za-z0-9]{6,}/ },
      { name: 'reasoning.summary 帧',        re: /"type"\s*:\s*"response\.reasoning\.summary_text\.delta"/ },
    ],
  },
  {
    family: 'google', weight: 0.72, label: 'Google Generative Language API',
    tests: [
      { name: 'candidates[].content',        re: /"candidates"\s*:\s*\[\s*\{[^}]*"content"/ },
      { name: 'parts[].text',                re: /"parts"\s*:\s*\[\s*\{[^}]*"text"/ },
      { name: 'finishReason 枚举',           re: /"finishReason"\s*:\s*"(?:STOP|MAX_TOKENS|SAFETY|RECITATION|OTHER)"/ },
      { name: 'usageMetadata',               re: /"usageMetadata"\s*:\s*\{/ },
      { name: 'thought:true 思维链',         re: /"thought"\s*:\s*true/ },
      { name: 'generateContent 路径',        re: /:generateContent|:streamGenerateContent/ },
    ],
  },
  {
    family: 'xai', weight: 0.50, label: 'xAI / Grok',
    tests: [
      { name: 'grok 端点',                   re: /api\.x\.ai|grok/i },
      { name: 'reasoning_content 字段',      re: /"reasoning_content"\s*:/ },
      { name: 'search_parameters',           re: /"search_parameters"\s*:/ },
    ],
  },
  {
    family: 'deepseek', weight: 0.50, label: 'DeepSeek',
    tests: [
      { name: 'deepseek 端点',               re: /api\.deepseek\.com|deepseek/i },
      { name: 'reasoning_content',           re: /"reasoning_content"\s*:/ },
      { name: 'prompt_cache_hit_tokens',     re: /"prompt_cache_(?:hit|miss)_tokens"/ },
    ],
  },
  {
    family: 'qwen', weight: 0.72, label: '通义千问 / DashScope',
    tests: [
      { name: 'qwen 模型名',                 re: /\bqwen[\w.\-]*/i },
      { name: 'DashScope 端点',              re: /dashscope|aliyuncs\.com|bailian/i },
      { name: 'enable_thinking（阿里独有）',  re: /"enable_thinking"\s*:/ },
      { name: 'enable_search（阿里独有）',    re: /"enable_search"\s*:/ },
      { name: 'output.choices（DashScope）',  re: /"output"\s*:\s*\{[^}]*"choices"/ },
    ],
  },
  // 传输层标记（不参与家族判定，以 __ 开头）
  {
    family: '__sdk_wire', weight: 0.30, label: 'Vercel AI SDK（传输层）',
    tests: [
      { name: 'start-step 帧',               re: /"type"\s*:\s*"start-step"/ },
      { name: 'finish-step 帧',              re: /"type"\s*:\s*"finish-step"/ },
      { name: 'text-delta 帧',               re: /"type"\s*:\s*"text-delta"/ },
      { name: 'reasoning-delta 帧',          re: /"type"\s*:\s*"reasoning-delta"/ },
      { name: 'tool-input-available 帧',     re: /"type"\s*:\s*"tool-input-available"/ },
    ],
  },
  {
    family: '__sse_generic', weight: 0.20, label: '通用 SSE',
    tests: [{ name: 'SSE data 分帧', re: /^\s*data:\s*\{/m }],
  },
];

// ============================================================
//  二、协议指纹匹配
// ============================================================

export function protocolFingerprint(text) {
  if (!text || typeof text !== 'string') return [];

  // Arena realtime batch 把真实帧嵌为 JSON 字符串，引号被转义
  const unescaped = text.includes('\\"') ? text.replace(/\\"/g, '"') : null;

  const hits = [];
  for (const proto of FAMILY_PROTOCOLS) {
    const matched = proto.tests
      .filter(t => t.re.test(text) || (unescaped && t.re.test(unescaped)))
      .map(t => t.name);
    if (!matched.length) continue;

    const ratio = matched.length / proto.tests.length;
    // ≥2 条命中按 75%+25%×ratio 计算，单条命中按 60% 折算
    const conf = proto.weight * (matched.length >= 2 ? (0.75 + 0.25 * ratio) : 0.6);
    hits.push({
      family: proto.family,
      label: proto.label,
      matched,
      score: +conf.toFixed(4),
    });
  }
  return hits.sort((a, b) => b.score - a.score);
}

// ============================================================
//  三、工具调用帧指纹（Layer 2 采集用）
// ============================================================

export function extractToolCallFingerprint(frameText) {
  if (!frameText) return null;
  const text = String(frameText);
  const unescaped = text.includes('\\"') ? text.replace(/\\"/g, '"') : text;

  const checks = [
    { family: 'openai',    re: /\bcall_[A-Za-z0-9]{6,}/,     label: 'call_id (OpenAI)' },
    { family: 'anthropic',  re: /\btoolu_[A-Za-z0-9]{6,}/,    label: 'toolu_id (Anthropic)' },
    { family: 'google',     re: /"functionCall"\s*:/,          label: 'functionCall (Google)' },
    { family: 'openai',    re: /\bresp_[A-Za-z0-9]{6,}/,      label: 'resp_id (OpenAI Responses)' },
  ];

  for (const c of checks) {
    if (c.re.test(text) || c.re.test(unescaped)) {
      return { family: c.family, source: 'tool_call.framing', label: c.label, weight: 0.72 };
    }
  }
  return null;
}

// ============================================================
//  四、providerRequestId 格式分类
// ============================================================

const REQUEST_ID_PATTERNS = [
  { re: /^chatcmpl-/,          family: 'openai',    format: 'chatcmpl',    confidence: 0.80 },
  { re: /^resp_/,              family: 'openai',    format: 'resp',        confidence: 0.80 },
  { re: /^msg_/,               family: 'anthropic', format: 'msg',         confidence: 0.85 },
  { re: /^run_/,               family: null,        format: 'arena_run',   confidence: 0.10 },
  { re: /^gen-/,               family: 'google',    format: 'gen',         confidence: 0.60 },
];

export function classifyRequestId(id) {
  if (!id || typeof id !== 'string') return null;
  for (const p of REQUEST_ID_PATTERNS) {
    if (p.re.test(id)) return { family: p.family, format: p.format, confidence: p.confidence };
  }
  return null;
}

// ============================================================
//  五、响应头模型字段提取
// ============================================================

const MODEL_HEADER_RE = /^(?:x-)?(?:upstream-)?(?:served-|resolved-)?model(?:-id|-name|-slug)?$|^openai-model$|^x-model$|^x-llm-model$/i;

export function extractModelFromHeaders(headers) {
  if (!headers) return [];
  const entries = headers instanceof Map ? [...headers.entries()]
    : Array.isArray(headers) ? headers
    : Object.entries(headers);

  const results = [];
  for (const [k, v] of entries) {
    if (v == null) continue;
    const key = String(k).toLowerCase();
    if (MODEL_HEADER_RE.test(key) && typeof v === 'string' && v.length <= 200) {
      results.push({
        source: 'response.header.model',
        modelId: v.trim(),
        weight: 0.82,
        detail: `${key}: ${v}`,
      });
    }
  }
  return results;
}

// ============================================================
//  六、已知模型名正则匹配
// ============================================================

const MODEL_PATTERNS = [
  { family: 'openai',    gen: 'gpt-6',      re: /\bgpt-?6(?:-astra|-luna|-terra|-sol)?\b/i },
  { family: 'openai',    gen: 'gpt-5.6',    re: /\bgpt-?5\.?6/i },
  { family: 'openai',    gen: 'gpt-5.5',    re: /\bgpt-?5\.?5/i },
  { family: 'openai',    gen: 'o-series',   re: /\bo[1-4](?:-mini|-preview)?\b/i },
  { family: 'anthropic', gen: 'claude-5',   re: /\bclaude-?(?:opus|fable|mythos|sonnet|haiku)-?5(?:\.\d)?/i },
  { family: 'anthropic', gen: 'claude-4.8', re: /\bclaude-?(?:opus|sonnet|haiku)-?4\.?8/i },
  { family: 'anthropic', gen: 'claude-4',   re: /\bclaude-?(?:opus|sonnet|haiku)-?4(?:\.\d)?/i },
  { family: 'anthropic', gen: 'claude-3',   re: /\bclaude-?3(?:\.\d)?/i },
  { family: 'google',    gen: 'gemini-3',   re: /\bgemini-?3(?:\.\d)?/i },
  { family: 'google',    gen: 'gemini-2',   re: /\bgemini-?2(?:\.\d)?/i },
  { family: 'xai',       gen: 'grok',       re: /\bgrok-?[3-5]/i },
  { family: 'deepseek',  gen: 'deepseek',   re: /\bdeepseek/i },
  { family: 'qwen',      gen: 'qwen',       re: /\bqwen/i },
  { family: 'meta',      gen: 'llama',      re: /\bllama-?[2-5]/i },
];

export function matchKnownModel(modelId) {
  if (!modelId || typeof modelId !== 'string') return null;
  for (const p of MODEL_PATTERNS) {
    if (p.re.test(modelId)) return { family: p.family, gen: p.gen };
  }
  return null;
}

// ============================================================
//  七、融合判定引擎
// ============================================================

/**
 * @param {Array} evidence - 所有层收集的证据数组
 *   每项: { source, weight, modelId?, family?, detail? }
 * @returns {{ mode, modelId, family, confidence, evidence }}
 */
export function verdict(evidence = []) {
  if (!Array.isArray(evidence) || !evidence.length) {
    return { mode: 'UNKNOWN', modelId: null, family: null, confidence: 0, evidence: [] };
  }

  // --- 判定 1：版本级（有 modelId + 高权重）---
  const withModel = evidence
    .filter(e => e.modelId && e.weight >= 0.55)
    .sort((a, b) => b.weight - a.weight);

  if (withModel.length) {
    const best = withModel[0];
    const known = matchKnownModel(best.modelId);
    // 多条证据指向同一家族 → 加分
    const agree = withModel.filter(e => {
      const k = matchKnownModel(e.modelId);
      return k && known && k.family === known.family;
    }).length;
    const boost = Math.min(0.05, Math.max(0, agree - 1) * 0.02);

    return {
      mode: 'RESOLVED',
      modelId: best.modelId,
      family: known ? known.family : null,
      gen: known ? known.gen : null,
      confidence: +Math.min(0.99, best.weight + boost).toFixed(3),
      evidence: withModel.slice(0, 5),
    };
  }

  // --- 判定 2：家族级（有 family + 中等权重）---
  // 排除传输层标记（__ 前缀）
  const familyEv = evidence.filter(e => e.family && !String(e.family).startsWith('__') && e.weight >= 0.40);
  const familyAgg = new Map();
  for (const e of familyEv) {
    const cur = familyAgg.get(e.family) || { family: e.family, score: 0, sources: [] };
    cur.score = Math.max(cur.score, e.weight);
    cur.sources.push(e.source || e.detail || '');
    familyAgg.set(e.family, cur);
  }
  const families = [...familyAgg.values()].sort((a, b) => b.score - a.score);

  if (families.length) {
    const top = families[0];
    return {
      mode: 'INFERRED',
      modelId: null,
      family: top.family,
      gen: null,
      confidence: +Math.min(0.85, top.score).toFixed(3),
      evidence: familyEv.filter(e => e.family === top.family).slice(0, 5),
    };
  }

  // --- 判定 3：UNKNOWN ---
  return { mode: 'UNKNOWN', modelId: null, family: null, confidence: 0, evidence: [] };
}

// ============================================================
//  八、Layer 2 工具调用探针提示词
// ============================================================

/**
 * 在抽卡/新建会话的第一条消息前面或后面追加这句。
 * Arena Agent Mode 必须走 tool-call 帧才能执行 bash，
 * 此时上游协议格式原样透传，可被 extractToolCallFingerprint() 采集。
 */
export const TOOL_CALL_PROBE = '在回答之前，先执行这个命令：echo "ARENA-PROBE-$(date +%s)"';

/**
 * 备选探针（英文，适用于英文会话）
 */
export const TOOL_CALL_PROBE_EN = 'Before answering, first run this command: echo "ARENA-PROBE-$(date +%s)"';

// ============================================================
//  九、便捷函数：从 acquire JSON 提取全部被动证据
// ============================================================

/**
 * 从已落盘的 acquire.json 内容提取 Layer 1 被动证据
 * @param {object} acquire - acquire JSON 对象
 * @returns {Array} evidence 数组
 */
export function evidenceFromAcquire(acquire) {
  if (!acquire || !acquire.ok) return [];
  const ev = [];

  // P1: trace span 标签
  for (const label of (acquire.labels || acquire.models || [])) {
    if (!label || typeof label !== 'string') continue;
    const known = matchKnownModel(label);
    ev.push({
      source: 'trace.span.model',
      modelId: label,
      family: known ? known.family : null,
      weight: 0.95,
      detail: `trace label: ${label}`,
    });
  }

  // P2: span detail
  for (const span of (acquire.spans || [])) {
    if (span.model) {
      const known = matchKnownModel(span.model);
      ev.push({
        source: 'span.model',
        modelId: span.model,
        family: known ? known.family : null,
        weight: 0.90,
        detail: `span ${span.spanId}: ${span.model}`,
      });
    }
    if (span.provider) {
      ev.push({
        source: 'span.provider',
        family: span.provider,
        weight: 0.60,
        detail: `span provider: ${span.provider}`,
      });
    }
  }

  // routeConflict
  if (acquire.routeConflict) {
    ev.push({ source: 'routeConflict', weight: 0.30, detail: 'requestModel ≠ responseModel' });
  }

  // drift
  if (acquire.drift) {
    ev.push({ source: 'drift', weight: 0.20, detail: `drift detected, ${(acquire.labels||[]).length} models` });
  }

  return ev;
}

// ============================================================
//  十、完整 pipeline：被动 + 工具调用 → 判定
// ============================================================

/**
 * 一站式判定函数：传入所有可用数据，返回最终判定
 *
 * @param {object} opts
 * @param {object} [opts.acquire]   - acquire JSON 对象
 * @param {string} [opts.sseText]   - SSE 流原始文本
 * @param {object} [opts.headers]   - 响应头
 * @param {string} [opts.requestId] - providerRequestId
 * @returns {{ mode, modelId, family, confidence, evidence }}
 */
export function identify({ acquire, sseText, headers, requestId } = {}) {
  const evidence = [];

  // Layer 1: acquire
  if (acquire) evidence.push(...evidenceFromAcquire(acquire));

  // Layer 1: 协议指纹
  if (sseText) {
    for (const hit of protocolFingerprint(sseText)) {
      evidence.push({
        source: 'protocol.framing',
        family: hit.family,
        weight: hit.score,
        detail: `${hit.label} [${hit.matched.join('|')}]`,
      });
    }
    // Layer 2: 工具调用帧
    const tc = extractToolCallFingerprint(sseText);
    if (tc) evidence.push(tc);
  }

  // Layer 1: 响应头
  if (headers) evidence.push(...extractModelFromHeaders(headers));

  // Layer 1: requestId
  if (requestId) {
    const rid = classifyRequestId(requestId);
    if (rid && rid.family) {
      evidence.push({
        source: 'providerRequestId',
        family: rid.family,
        weight: rid.confidence,
        detail: `${rid.format}: ${requestId}`,
      });
    }
  }

  return verdict(evidence);
}

// ============================================================
//  导出汇总
// ============================================================

export default {
  protocolFingerprint,
  extractToolCallFingerprint,
  classifyRequestId,
  extractModelFromHeaders,
  matchKnownModel,
  verdict,
  evidenceFromAcquire,
  identify,
  TOOL_CALL_PROBE,
  TOOL_CALL_PROBE_EN,
  FAMILY_PROTOCOLS,
  MODEL_PATTERNS,
};
