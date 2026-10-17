/**
 * arena-modeltrace.mjs — Layer 3 ModelTrace 数字探针
 *
 * 从油猴脚本 ArenaModelTraceCore 提取，封装为独立 Node.js 模块。
 * 零外部依赖（只用 Node.js 内置 zlib）。
 *
 * 用法:
 *   import { loadBank, generateProbes, analyzeResponses } from './arena-modeltrace.mjs';
 *
 *   const bank = await loadBank();               // 加载 reference bank
 *   const probes = generateProbes(3);             // 生成 3 条探针提示词
 *   // ... 把 probes 发给模型，收集 3 条回复 ...
 *   const result = analyzeResponses(responses, bank);
 *   // → { prediction, probability, family, results[], diagnostics[] }
 */

import { readFileSync } from 'node:fs';
import { gunzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ============================================================
//  一、Bank 加载
// ============================================================

let _bankCache = null;

export async function loadBank(bankPath) {
  if (_bankCache) return _bankCache;
  const p = bankPath || join(__dirname, 'modeltrace-bank.b64');
  const b64 = readFileSync(p, 'utf8').trim();
  const buf = Buffer.from(b64, 'base64');
  const json = gunzipSync(buf).toString('utf8');
  _bankCache = JSON.parse(json);
  return _bankCache;
}

export function loadBankSync(bankPath) {
  if (_bankCache) return _bankCache;
  const p = bankPath || join(__dirname, 'modeltrace-bank.b64');
  const b64 = readFileSync(p, 'utf8').trim();
  const buf = Buffer.from(b64, 'base64');
  const json = gunzipSync(buf).toString('utf8');
  _bankCache = JSON.parse(json);
  return _bankCache;
}

// ============================================================
//  二、探针提示词生成
// ============================================================

const OPENINGS = [
  '这是一次独立的数值选择记录',
  '请完成下面的无语义整数选择任务',
  '执行一次第一反应取值记录',
  '生成一组不承载语义的整数选择',
  '进行一轮快速逐项取值',
];
const ACTIONS = [
  '为各个位置分别凭第一反应选择',
  '逐项选择',
  '每次只决定当前一项，共给出',
  '分别凭第一反应给出',
  '逐个直接选择',
];
const ENDINGS = [
  '相邻数字用空格分隔，一次写完，不要换行或解释。',
  '用空格隔开，一次全部输出，不加标点或说明。',
  '一行输出，空格分隔，不要任何多余文字。',
];

export function generateProbes(count = 3) {
  const pick = arr => arr[Math.floor(Math.random() * arr.length)];
  const probes = [];
  const usedLengths = new Set();

  for (let i = 0; i < count; i++) {
    let len;
    do { len = 292 + Math.floor(Math.random() * 41); } while (usedLengths.has(len));
    usedLengths.add(len);

    const prompt = `${pick(OPENINGS)}。${pick(ACTIONS)} ${len} 个 1 到 355 之间的整数。${pick(ENDINGS)}`;
    probes.push({ prompt, expected_count: len });
  }
  return probes;
}

// ============================================================
//  三、核心算法（从 ArenaModelTraceCore 提取）
// ============================================================

const VALUE_MIN = 1;
const VALUE_MAX = 355;
const DIMENSION = VALUE_MAX - VALUE_MIN + 1;
const ALPHA = 0.5;

function parseNumbers(text) {
  const runs = [];
  let current = [];
  let prevEnd = 0;
  const re = /\d+/g;
  let m;
  while ((m = re.exec(String(text))) !== null) {
    const sep = String(text).slice(prevEnd, m.index);
    if (current.length && /\p{L}/u.test(sep)) { runs.push(current); current = []; }
    const v = Number(m[0]);
    if (Number.isInteger(v) && v >= VALUE_MIN && v <= VALUE_MAX) current.push(v);
    prevEnd = m.index + m[0].length;
  }
  if (current.length) runs.push(current);
  if (!runs.length) return [];
  return runs.reduce((best, run) => run.length > best.length ? run : best, []);
}

function countNumbers(numbers) {
  const counts = Array(DIMENSION).fill(0);
  for (const n of numbers) {
    if (Number.isInteger(n) && n >= VALUE_MIN && n <= VALUE_MAX) counts[n - VALUE_MIN]++;
  }
  return counts;
}

function standardize(values) {
  const mean = values.reduce((s, v) => s + v, 0) / values.length;
  const variance = values.reduce((s, v) => s + (v - mean) ** 2, 0) / values.length;
  const scale = Math.max(Math.sqrt(variance), 1e-12);
  return values.map(v => (v - mean) / scale);
}

function norm(values) {
  return Math.sqrt(values.reduce((s, v) => s + v * v, 0));
}

function dot(a, b) {
  let s = 0;
  for (let i = 0; i < a.length; i++) s += a[i] * b[i];
  return s;
}

function hellingerFeature(counts) {
  const vals = counts.map(v => v + ALPHA);
  const total = vals.reduce((s, v) => s + v, 0);
  return vals.map(v => Math.sqrt(v / total));
}

function projectFeature(feature, mean, scale, basis) {
  const proj = feature.map((v, i) => (v - mean[i]) / scale[i]);
  if (basis && basis.length) {
    for (const vec of basis) {
      const coeff = dot(proj, vec);
      for (let i = 0; i < proj.length; i++) proj[i] -= coeff * vec[i];
    }
  }
  return proj;
}

function robustScoreCounts(counts, bank) {
  const art = bank.robust.hellinger;
  const feature = hellingerFeature(counts);
  const proj = projectFeature(feature, art.feature_mean, art.feature_scale, art.nuisance_basis);
  const len = Math.max(norm(proj), 1e-12);
  const normalized = proj.map(v => v / len);
  const nuisanceRaw = art.centroids.map(c => dot(normalized, c));
  const nuisance = standardize(nuisanceRaw);
  const fused = standardize(nuisance);
  return { fused, nuisance };
}

function orderedBlockFeature(numbers) {
  const q = Math.floor(numbers.length / 4);
  const r = numbers.length % 4;
  const pieces = [];
  let off = 0;
  for (let b = 0; b < 4; b++) {
    const len = q + (b < r ? 1 : 0);
    const bins = Array(16).fill(0);
    for (let i = off; i < off + len; i++) {
      let bin = Math.floor(((numbers[i] - 1) / 355) * 16);
      bins[Math.max(0, Math.min(15, bin))]++;
    }
    off += len;
    const total = bins.reduce((s, v) => s + v + 0.5, 0);
    pieces.push(...bins.map(v => Math.sqrt((v + 0.5) / total)));
  }
  const digits = Array(10).fill(0);
  for (const v of numbers) digits[v % 10]++;
  const dTotal = digits.reduce((s, v) => s + v + 0.5, 0);
  pieces.push(...digits.map(v => Math.sqrt((v + 0.5) / dTotal)));
  return pieces;
}

function orderedBlockScores(numbers, bank) {
  const art = bank.robust.ordered_blocks;
  const feature = orderedBlockFeature(numbers);
  const sf = feature.map((v, i) => (v - art.feature_mean[i]) / art.feature_scale[i]);
  const fn = Math.max(norm(sf), 1e-12);
  const normalized = sf.map(v => v / fn);

  const envScores = art.environment_centroids.map(cs => cs.map(c => dot(normalized, c)));
  const mc = bank.robust.model_order.length;
  const template = Array(mc).fill(-Infinity);
  for (const scores of envScores) {
    for (let i = 0; i < mc; i++) if (scores[i] > template[i]) template[i] = scores[i];
  }
  const st = standardize(template);

  const proj = projectFeature(sf, Array(sf.length).fill(0), Array(sf.length).fill(1), art.nuisance_basis);
  const pn = Math.max(norm(proj), 1e-12);
  const np2 = proj.map(v => v / pn);
  const nuisance = standardize(art.centroids.map(c => dot(np2, c)));
  const combined = st.map((v, i) => 0.5 * v + 0.5 * nuisance[i]);
  return standardize(combined);
}

function robustScoreNumbers(numbers, bank) {
  const marginal = robustScoreCounts(countNumbers(numbers), bank);
  const art = bank.robust.ordered_blocks;
  const weight = art ? Number(art.weight || 0) : 0;
  if (!art || weight === 0) return { ...marginal, marginal_fused: marginal.fused, ordered: marginal.fused };
  const ordered = orderedBlockScores(numbers, bank);
  const fused = marginal.fused.map((v, i) => (1 - weight) * v + weight * ordered[i]);
  return { ...marginal, fused, marginal_fused: marginal.fused, ordered };
}

function softmax(values) {
  const max = Math.max(...values);
  const w = values.map(v => Math.exp(v - max));
  const total = w.reduce((s, v) => s + v, 0);
  return w.map(v => v / total);
}

function jsSimilarity(left, right) {
  const lt = left.reduce((s, v) => s + v, 0);
  const rt = right.reduce((s, v) => s + v + ALPHA, 0);
  const p = left.map(v => v / lt);
  const q = right.map(v => (v + ALPHA) / rt);
  let dp = 0, dq = 0;
  for (let i = 0; i < p.length; i++) {
    const mid = (p[i] + q[i]) / 2;
    if (p[i]) dp += p[i] * Math.log(p[i] / mid);
    if (q[i]) dq += q[i] * Math.log(q[i] / mid);
  }
  return 1 - Math.sqrt((dp + dq) / 2 / Math.log(2));
}

// ============================================================
//  四、主分析函数
// ============================================================

/**
 * 分析模型回复，返回判定结果
 * @param {string[]} responses - 模型回复文本数组（对应 generateProbes 的输出）
 * @param {object} bank - loadBank() 返回的 bank 对象
 * @param {number[]} [expectedCounts] - 每条回复预期的数字个数
 * @returns {object} 判定结果
 */
export function analyzeResponses(responses, bank, expectedCounts) {
  const modelIds = bank.models.map(m => m.id);
  const valid = [];
  const diagnostics = [];

  for (let i = 0; i < responses.length; i++) {
    // 剥 HTML 标签再解析（Arena 回复的数字被 <span data-agent-word> 包裹，
    // 标签里的字母会把数字序列切碎，必须先剥）
    const text = String(responses[i] || '').replace(/<[^>]+>/g, ' ');
    const expected = expectedCounts ? expectedCounts[i] : 0;
    const numbers = parseNumbers(text);
    const minimum = expected ? Math.max(80, Math.ceil(expected * 0.55)) : 80;
    const accepted = numbers.length >= minimum;
    diagnostics.push({ index: i, parsed_numbers: numbers.length, minimum_numbers: minimum, accepted });
    if (accepted) {
      const counts = countNumbers(numbers);
      const components = robustScoreNumbers(numbers, bank);
      valid.push({ counts, scores: components.fused, ...components });
    }
  }

  if (!valid.length) {
    return {
      ok: false,
      error: '没有可用回答：未找到达到最小数量的完整数字序列',
      diagnostics,
      prediction: null,
      probability: 0,
    };
  }

  const combinedScores = modelIds.map((_, i) =>
    valid.reduce((s, item) => s + item.scores[i], 0) / valid.length);
  const combinedNuisance = modelIds.map((_, i) =>
    valid.reduce((s, item) => s + item.nuisance[i], 0) / valid.length);

  const calKey = String(Math.min(valid.length, 3));
  const cal = bank.calibration[calKey] || { beta: 1, cv_accuracy: null };
  const beta = Number(cal.beta || 1);
  const probabilities = softmax(combinedScores.map(v => beta * v));

  // 池化 counts 用于 profile similarity
  const pooled = Array(DIMENSION).fill(0);
  for (const item of valid) {
    for (let i = 0; i < DIMENSION; i++) pooled[i] += item.counts[i];
  }

  const modelMap = new Map(bank.models.map(m => [m.id, m]));
  const results = modelIds.map((id, i) => {
    const model = modelMap.get(id);
    return {
      model: id,
      display_name: model.display_name,
      probability: probabilities[i],
      profile_similarity: jsSimilarity(pooled, model.counts),
      score: combinedScores[i],
      family: model.family || 'unknown',
      family_name: model.family_name || model.family || 'unknown',
    };
  }).sort((a, b) => b.probability - a.probability);

  // 家族聚合
  const familyOrder = [...new Set(bank.models.map(m => m.family || 'unknown'))];
  const familyProbs = {};
  for (const f of familyOrder) {
    familyProbs[f] = results.filter(r => r.family === f).reduce((s, r) => s + r.probability, 0);
  }
  const winFamily = familyOrder.reduce((best, f) => familyProbs[f] > familyProbs[best] ? f : best, familyOrder[0]);

  return {
    ok: true,
    prediction: results[0].model,
    prediction_name: results[0].display_name,
    probability: results[0].probability,
    family: results[0].family,
    family_prediction: winFamily,
    family_probability: familyProbs[winFamily],
    used_outputs: valid.length,
    total_outputs: responses.length,
    top5: results.slice(0, 5).map(r => ({
      model: r.model, probability: +r.probability.toFixed(4), family: r.family,
    })),
    diagnostics,
    calibration: { queries: calKey, beta, cv_accuracy: cal.cv_accuracy ?? null },
    // 导出 pooled counts 用于模板库
    _profile: pooled,
  };
}

// ============================================================
//  五、便捷 pipeline
// ============================================================

/**
 * 一站式：生成探针 → 分析回复 → 返回结果
 * @param {function} sendFn - async (prompt) => responseText
 * @param {object} [bank] - 可选，不传则自动加载
 * @returns {object} 判定结果
 */
export async function probe(sendFn, bank) {
  if (!bank) bank = await loadBank();
  const probes = generateProbes(bank.recommended_queries || 3);
  const responses = [];
  for (const p of probes) {
    const reply = await sendFn(p.prompt);
    responses.push(reply);
  }
  return analyzeResponses(responses, bank, probes.map(p => p.expected_count));
}

export default { loadBank, loadBankSync, generateProbes, analyzeResponses, probe };
