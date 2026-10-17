/**
 * arena-template-db.mjs — 开放集模板库
 *
 * 每个模型一条模板：355 维数字分布 profile + 元数据。
 * ModelTrace bank 没有的模型（如 super_nova_ext）在这里建档，
 * 用过的会话越多，模板越准。
 *
 * 存储：JSON 文件（默认与脚本同目录 arena-templates.json）
 *
 * 用法:
 *   import { TemplateDB } from './arena-template-db.mjs';
 *
 *   const db = new TemplateDB();                    // 自动加载
 *   db.upsert('', profile, { family:'claude', bankProb:0.91, sessionId:'01a0...' });
 *   const m = db.match(profile);                    // → { matched, modelId, distance, ... }
 *   db.save();                                      // 落盘
 */

import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DEFAULT_DB_PATH = join(__dirname, 'arena-templates.json');

// 匹配阈值：JS 散度相似度高于此值认为是同一个模型
const MATCH_THRESHOLD = 0.90;
// 强匹配阈值：高于此值直接 RESOLVED
const STRONG_THRESHOLD = 0.95;

export class TemplateDB {
  constructor(path) {
    this.path = path || DEFAULT_DB_PATH;
    this.templates = {};
    this.load();
  }

  load() {
    if (existsSync(this.path)) {
      try {
        const raw = JSON.parse(readFileSync(this.path, 'utf8'));
        this.templates = raw.templates || {};
      } catch { this.templates = {}; }
    }
  }

  save() {
    const payload = {
      version: 1,
      updatedAt: new Date().toISOString(),
      templates: this.templates,
    };
    writeFileSync(this.path, JSON.stringify(payload, null, 2), 'utf8');
  }

  /**
   * 仅登记模型元数据（无 profile，供 batch 空闲后补指纹时占位）
   * @param {string} modelId - 模型标识（trace 标签）
   * @param {object} [meta] - { family, bankMatch, source, sessionId }
   */
  register(modelId, meta = {}) {
    if (!modelId) return false;
    const key = String(modelId);
    const t = this.templates[key] || {
      firstSeen: new Date().toISOString(),
      sessions: [],
    };

    if (t.profile) {
      // 已有 profile，只补元数据，不动指纹
      if (meta.family !== undefined) t.family = meta.family;
      if (meta.bankMatch !== undefined) t.bankMatch = meta.bankMatch;
      if (meta.bankProb !== undefined) t.bankProb = meta.bankProb;
      if (meta.source !== undefined) t.source = meta.source;
      if (meta.sessionId && !t.sessions.includes(meta.sessionId)) t.sessions.push(meta.sessionId);
      t.updatedAt = new Date().toISOString();
      this.templates[key] = t;
      return true;
    }

    if (meta.family !== undefined) t.family = meta.family;
    if (meta.bankMatch !== undefined) t.bankMatch = meta.bankMatch;
    if (meta.bankProb !== undefined) t.bankProb = meta.bankProb;
    if (meta.source !== undefined) t.source = meta.source;
    if (meta.sessionId) {
      if (!t.sessions.includes(meta.sessionId)) t.sessions.push(meta.sessionId);
      if (t.sessions.length > 50) t.sessions = t.sessions.slice(-50);
    }
    t.updatedAt = new Date().toISOString();
    this.templates[key] = t;
    return true;
  }

  /**
   * 插入或更新模板
   * @param {string} modelId - 模型标识（trace 标签或匿名 ID）
   * @param {number[]} profile - 355 维分布
   * @param {object} [meta] - { family, bankMatch, bankProb, sessionId, source }
   */
  upsert(modelId, profile, meta = {}) {
    if (!modelId || !Array.isArray(profile) || !profile.length) return false;
    const key = String(modelId);
    const t = this.templates[key] || {
      firstSeen: new Date().toISOString(),
      sessions: [],
    };

    // profile 用指数滑动平均合并（同一模型多次采样趋于稳定）
    if (t.profile && t.profile.length === profile.length) {
      const w = t.samples ? 0.7 : 0.5;   // 已有样本多信旧的，首采五五开
      t.profile = t.profile.map((v, i) => +(w * v + (1 - w) * profile[i]).toFixed(6));
      t.samples = (t.samples || 1) + 1;
    } else {
      t.profile = profile.map(v => +v.toFixed(6));
      t.samples = 1;
    }

    if (meta.family !== undefined) t.family = meta.family;
    if (meta.bankMatch !== undefined) t.bankMatch = meta.bankMatch;
    if (meta.bankProb !== undefined) t.bankProb = meta.bankProb;
    if (meta.source !== undefined) t.source = meta.source;
    if (meta.sessionId) {
      if (!t.sessions.includes(meta.sessionId)) t.sessions.push(meta.sessionId);
      if (t.sessions.length > 50) t.sessions = t.sessions.slice(-50);
    }
    t.updatedAt = new Date().toISOString();
    this.templates[key] = t;
    return true;
  }

  /**
   * 与所有模板比 JS 散度相似度，返回最接近的
   * @param {number[]} profile - 新样本 355 维分布
   * @returns {{ matched, modelId, similarity, strong, family, candidates }}
   */
  match(profile) {
    if (!Array.isArray(profile) || !profile.length) {
      return { matched: false, modelId: null, similarity: 0, strong: false, family: null, candidates: [] };
    }

    const candidates = [];
    for (const [modelId, t] of Object.entries(this.templates)) {
      if (!Array.isArray(t.profile) || t.profile.length !== profile.length) continue;
      const sim = this._jsSimilarity(profile, t.profile);
      candidates.push({
        modelId,
        similarity: +sim.toFixed(4),
        family: t.family || null,
        samples: t.samples || 1,
        bankMatch: t.bankMatch || null,
      });
    }
    candidates.sort((a, b) => b.similarity - a.similarity);

    if (!candidates.length) {
      return { matched: false, modelId: null, similarity: 0, strong: false, family: null, candidates: [] };
    }

    const best = candidates[0];
    const matched = best.similarity >= MATCH_THRESHOLD;
    const strong = best.similarity >= STRONG_THRESHOLD;

    return {
      matched,
      strong,
      modelId: matched ? best.modelId : null,
      similarity: best.similarity,
      family: matched ? best.family : best.family,   // 未达阈值也给出家族线索
      candidates: candidates.slice(0, 5),
    };
  }

  /** 统计两个分布的 JS 散度相似度（0-1，1=完全相同） */
  _jsSimilarity(p, q) {
    const ALPHA = 0.5;
    const pt = p.reduce((s, v) => s + v, 0);
    const qt = q.reduce((s, v) => s + v + ALPHA, 0);
    const pn = p.map(v => v / (pt + ALPHA));
    const qn = q.map(v => (v + ALPHA) / qt);
    let dp = 0, dq = 0;
    for (let i = 0; i < pn.length; i++) {
      const mid = (pn[i] + qn[i]) / 2;
      if (pn[i] > 0) dp += pn[i] * Math.log(pn[i] / mid);
      if (qn[i] > 0) dq += qn[i] * Math.log(qn[i] / mid);
    }
    const js = (dp + dq) / 2;
    return 1 - Math.sqrt(js / Math.log(2));
  }

  /** 获取模板 */
  get(modelId) { return this.templates[String(modelId)] || null; }

  /** 列出所有模板摘要 */
  list() {
    return Object.entries(this.templates).map(([modelId, t]) => ({
      modelId,
      family: t.family || null,
      samples: t.samples || 0,
      hasProfile: Array.isArray(t.profile) && t.profile.length > 0,
      bankMatch: t.bankMatch || null,
      bankProb: t.bankProb || null,
      sessions: (t.sessions || []).length,
      updatedAt: t.updatedAt,
    }));
  }

  /** 删除模板 */
  remove(modelId) {
    if (this.templates[String(modelId)]) {
      delete this.templates[String(modelId)];
      return true;
    }
    return false;
  }
}

/**
 * 完整 Layer 3 pipeline：探针 → 分析 → bank 匹配 → 模板匹配 → 归档
 *
 * @param {object} opts
 * @param {function} opts.sendFn      - async (prompt) => replyText
 * @param {string}   [opts.traceLabel] - trace 标签（有就归档到它名下）
 * @param {string}   [opts.sessionId]  - 会话 ID
 * @param {object}   [opts.bank]       - ModelTrace bank
 * @param {TemplateDB} [opts.db]       - 模板库
 * @returns {object} 判定结果
 */
export async function fullProbe({ sendFn, traceLabel, sessionId, bank, db }) {
  const mt = await import('./arena-modeltrace.mjs');
  if (!bank) bank = mt.loadBankSync();
  if (!db) db = new TemplateDB();

  // 1. 跑探针
  const probes = mt.generateProbes(bank.recommended_queries || 3);
  const responses = [];
  for (const p of probes) responses.push(await sendFn(p.prompt));

  // 2. ModelTrace 分析
  const result = mt.analyzeResponses(responses, bank, probes.map(p => p.expected_count));
  if (!result.ok) {
    return { layer3: result, template: null, final: { mode: 'UNKNOWN', reason: 'probe_failed' } };
  }

  // 3. 模板匹配
  const templateMatch = db.match(result._profile);

  // 4. 归档：优先归到 trace 标签名下，否则归到匹配到的模板名下，否则建匿名模板
  const archiveId = traceLabel
    || (templateMatch.matched ? templateMatch.modelId : null)
    || `anon_${new Date().toISOString().slice(0, 10)}_${Math.random().toString(36).slice(2, 6)}`;

  db.upsert(archiveId, result._profile, {
    family: result.family || (templateMatch.matched ? templateMatch.family : null),
    bankMatch: result.prediction,
    bankProb: +result.probability.toFixed(4),
    source: traceLabel ? 'trace_label' : (templateMatch.matched ? 'template_match' : 'no_label'),
    sessionId,
  });
  db.save();

  // 5. 融合判定
  let final;
  if (result.probability >= 0.75) {
    final = { mode: 'RESOLVED', modelId: result.prediction, source: 'modeltrace_bank', confidence: result.probability };
  } else if (templateMatch.strong) {
    final = { mode: 'RESOLVED', modelId: templateMatch.modelId, source: 'template_db', confidence: templateMatch.similarity };
  } else if (templateMatch.matched) {
    final = { mode: 'INFERRED', modelId: templateMatch.modelId, source: 'template_db', confidence: templateMatch.similarity };
  } else if (result.family) {
    final = { mode: 'INFERRED', modelId: null, family: result.family, source: 'modeltrace_family', confidence: result.family_probability };
  } else {
    final = { mode: 'UNKNOWN', modelId: null, family: null, confidence: 0 };
  }

  return { layer3: result, template: templateMatch, final, archiveId };
}

// ============================================================
//  七、会话对比：两个对话结束后，判定是否被路由
// ============================================================

/**
 * 对比两个已完成会话，判定它们是否由不同模型处理（是否被路由）。
 *
 * 三重证据，任一冲突即判 CHANGED：
 *   1. trace 标签（L1）：标签不同 → CHANGED
 *   2. 行为指纹（L3）：profile 相似度 < THRESHOLD → CHANGED
 *   3. 家族（L2）：family 不同 → CHANGED
 * 全部一致 → SAME。证据不足 → UNCERTAIN。
 *
 * @param {object} opts
 * @param {object} opts.session1 - { traceLabel?, profile?, family?, modelId? }
 * @param {object} opts.session2 - { traceLabel?, profile?, family?, modelId? }
 * @param {object} [opts.db]     - TemplateDB 实例（用于按 modelId 取历史 profile）
 * @returns {object} 判定结果
 */
export function compareSessions({ session1, session2, db } = {}) {
  if (!session1 || !session2) {
    return { routed: false, verdict: 'UNCERTAIN', reason: 'missing_session' };
  }
  const s1 = session1 || {};
  const s2 = session2 || {};

  // 若只给了 modelId，尝试从模板库取历史 profile
  let p1 = s1.profile;
  let p2 = s2.profile;
  if (!p1 && db && s1.modelId) { const t = db.get(s1.modelId); if (t) p1 = t.profile; }
  if (!p2 && db && s2.modelId) { const t = db.get(s2.modelId); if (t) p2 = t.profile; }

  // ---- 证据 1：trace 标签 ----
  const label1 = s1.traceLabel ? String(s1.traceLabel).trim() : '';
  const label2 = s2.traceLabel ? String(s2.traceLabel).trim() : '';
  const labelEvidence = label1 && label2 && label1 !== label2
    ? { conflict: true, detail: `${label1} vs ${label2}` }
    : { conflict: false, detail: label1 || label2 ? `${label1 || '?'} vs ${label2 || '?'}` : 'no labels' };

  // ---- 证据 2：家族 ----
  const famEvidence = s1.family && s2.family && s1.family !== s2.family
    ? { conflict: true, detail: `${s1.family} vs ${s2.family}` }
    : { conflict: false, detail: `${s1.family || '?'} vs ${s2.family || '?'}` };

  // ---- 证据 3：行为指纹 ----
  let similarity = null;
  let profileEvidence = { conflict: false, detail: 'no profiles' };
  if (Array.isArray(p1) && Array.isArray(p2) && p1.length === p2.length) {
    similarity = computeJS(p1, p2);
    profileEvidence = {
      conflict: similarity < MATCH_THRESHOLD,
      similarity: +similarity.toFixed(4),
      detail: `sim=${similarity.toFixed(4)} (threshold ${MATCH_THRESHOLD})`,
    };
  }

  // ---- 综合判定 ----
  const conflicts = [];
  if (labelEvidence.conflict) conflicts.push(`标签不同: ${labelEvidence.detail}`);
  if (famEvidence.conflict) conflicts.push(`家族不同: ${famEvidence.detail}`);
  if (profileEvidence.conflict) conflicts.push(`行为指纹不同: ${profileEvidence.detail}`);

  // 双方证据覆盖情况：某一边完全没有可对比信息
  const s1Has = !!(label1 || s1.family || p1);
  const s2Has = !!(label2 || s2.family || p2);
  const bothCovered = s1Has && s2Has;

  // 至少一个证据说换 → CHANGED；双方都有证据且都一致 → SAME；否则 UNCERTAIN
  let verdict, routed;
  if (conflicts.length) {
    verdict = 'CHANGED';
    routed = true;
  } else if (!bothCovered) {
    verdict = 'UNCERTAIN';
    routed = null;   // 有一边没证据，不擅自下结论
  } else if (label1 && label2 && label1 === label2) {
    verdict = 'SAME';
    routed = false;
  } else if (similarity !== null && similarity >= MATCH_THRESHOLD) {
    verdict = 'SAME';
    routed = false;
  } else if (similarity !== null) {
    // 有 profile 但低于阈值且无标签可比 → 保守判 UNCERTAIN
    verdict = 'UNCERTAIN';
    routed = null;
  } else {
    verdict = 'UNCERTAIN';
    routed = null;
  }

  return {
    routed,            // true=被路由(换了模型) / false=同一模型 / null=无法判定
    verdict,           // CHANGED / SAME / UNCERTAIN
    reason: conflicts.length ? conflicts.join('；')
      : !s1Has && !s2Has ? '双方均无证据，无法对比'
      : !bothCovered ? '仅一方有证据，无法对比'
      : (verdict === 'SAME' ? '证据一致' : '证据不足'),
    model1: label1 || s1.modelId || null,
    model2: label2 || s2.modelId || null,
    similarity,
    family1: s1.family || null,
    family2: s2.family || null,
    evidence: { label: labelEvidence, family: famEvidence, profile: profileEvidence },
  };
}

/** JS 散度相似度（模块内部复用，避免重复实现） */
function computeJS(p, q) {
  const ALPHA = 0.5;
  const pt = p.reduce((s, v) => s + v, 0);
  const qt = q.reduce((s, v) => s + v + ALPHA, 0);
  const pn = p.map(v => v / (pt + ALPHA));
  const qn = q.map(v => (v + ALPHA) / qt);
  let dp = 0, dq = 0;
  for (let i = 0; i < pn.length; i++) {
    const mid = (pn[i] + qn[i]) / 2;
    if (pn[i] > 0) dp += pn[i] * Math.log(pn[i] / mid);
    if (qn[i] > 0) dq += qn[i] * Math.log(qn[i] / mid);
  }
  return 1 - Math.sqrt(((dp + dq) / 2) / Math.log(2));
}

export default { TemplateDB, fullProbe, compareSessions, MATCH_THRESHOLD, STRONG_THRESHOLD };
