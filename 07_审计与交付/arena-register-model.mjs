/**
 * arena-register-model.mjs — 给模型建模板（补 bank 缺失的模型）
 *
 * 用法:
 *   node arena-register-model.mjs <sessionId> <modelName> [--send-fn script.mjs]
 *
 * 逻辑:
 *   1. 生成 3 条 ModelTrace 探针提示词
 *   2. 通过 sendFn 发给目标会话，收集 3 条回复
 *   3. analyzeResponses() 生成 355 维 profile
 *   4. 存入模板库 arena-templates.json，标记为 <modelName>
 *   5. 之后 compareSessions / fullProbe 就能用它做三选一
 *
 * --send-fn 指定一个导出 async send(prompt) => replyText 的模块；
 * 不传时使用内置的占位实现（需你自行替换）。
 */

import { TemplateDB, fullProbe } from './arena-template-db.mjs';
import { loadBankSync } from './arena-modeltrace.mjs';
import { writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));

// ---- 参数解析 ----
const argv = process.argv.slice(2);
const sessionId = argv[0];
const modelName = argv[1];
const sendFnIdx = argv.indexOf('--send-fn');
const sendFnPath = sendFnIdx >= 0 ? argv[sendFnIdx + 1] : null;

if (!sessionId || !modelName) {
  console.error(`用法: node arena-register-model.mjs <sessionId> <modelName> [--send-fn script.mjs]
示例: node arena-register-model.mjs 01a0de64-... claude-fable-5-1`);
  process.exit(1);
}

// ---- 发送通道 ----
let sendFn = null;
if (sendFnPath) {
  const abs = sendFnPath.startsWith('file:') ? sendFnPath
    : `file://${join(__dirname, sendFnPath).replace(/\\/g, '/')}`;
  const mod = await import(abs);
  if (typeof mod.send !== 'function' && typeof mod.default?.send !== 'function') {
    console.error(`--send-fn 模块需导出 async send(prompt) => replyText`);
    process.exit(1);
  }
  sendFn = mod.send || mod.default.send;
} else {
  // 占位实现：请替换为你的真实发送通道
  console.warn('⚠️  未指定 --send-fn，使用占位发送函数（不会真正发出消息）。');
  sendFn = async prompt => {
    console.error(`[占位] 应发送给会话 ${sessionId}:\n  ${prompt.slice(0, 80)}...`);
    throw new Error('占位 sendFn 未实现，请提供 --send-fn');
  };
}

// ---- 执行 ----
const bank = loadBankSync();
const db = new TemplateDB();

console.log(`\n=== 给模型建模板: ${modelName} ===`);
console.log(`会话: ${sessionId}`);
console.log(`bank 现有 ${bank.models.length} 个模型签名，模板库现有 ${Object.keys(db.templates).length} 条模板\n`);

// 先用探针收集回复
import('./arena-modeltrace.mjs').then(async mt => {
  const probes = mt.generateProbes(bank.recommended_queries || 3);
  const responses = [];
  for (let i = 0; i < probes.length; i++) {
    console.log(`[${i + 1}/${probes.length}] 发送探针（要求 ${probes[i].expected_count} 个整数）...`);
    const reply = await sendFn(probes[i].prompt);
    const nums = (reply.match(/\d+/g) || []).length;
    console.log(`  回复 ${nums} 个数字${nums < 80 ? '（⚠️ 数量不足，可能被判无效）' : ''}`);
    responses.push(reply);
  }

  const result = mt.analyzeResponses(responses, bank, probes.map(p => p.expected_count));
  if (!result.ok) {
    console.error('\n❌ 探针失败:', result.error);
    console.error('建议: 检查发送通道是否真的发到 Arena、会话是否在线、回复是否包含足够数字。');
    process.exit(2);
  }

  console.log(`\nModelTrace 判定: ${result.prediction}（${(result.probability * 100).toFixed(1)}%）`);
  console.log(`top5: ${result.top5.map(t => `${t.model}(${t.probability})`).join(', ')}`);

  // 写入模板库，标记为 modelName
  db.upsert(modelName, result._profile, {
    family: result.family,
    bankMatch: result.prediction,
    bankProb: +result.probability.toFixed(4),
    source: 'manual_register',
    sessionId,
  });
  db.save();

  console.log(`\n✅ 模板已建: ${modelName}`);
  console.log(`   355 维 profile 已存入 ${db.path}`);
  console.log(`   采样次数: ${db.get(modelName).samples}`);
  console.log(`   ModelTrace 最接近的 bank 签名: ${result.prediction}（${(result.probability * 100).toFixed(1)}%）`);
  console.log('\n下次探测时，该模型会在 compareSessions / fullProbe 的模板匹配里出现。');
}).catch(e => { console.error('\n❌ 执行失败:', e.message || e); process.exit(1); });
