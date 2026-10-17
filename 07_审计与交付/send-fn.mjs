/**
 * send-fn.mjs — 向 Arena 指定会话发送探针的发送模块
 *
 * 供 arena-register-model.mjs 用 --send-fn 引用。
 * 复用 hub.mjs 连到浏览器，通过 browser_run_code_unsafe 执行 Playwright
 * 代码：导航到指定会话 → 写探针 → 点发送 → 等回复稳定 → 返回文本。
 *
 * 用法（由 arena-register-model.mjs 调用）:
 *   node arena-register-model.mjs <sid> claude-fable-5-1 --send-fn ./send-fn.mjs
 *
 * 模块导出:
 *   export async function send(prompt) => replyText
 *   export const sessionId = <从命令行或默认读>
 */

import { connect, unquote, sleep } from 'file:///C:/Users/赵豪/.agents/skills/arena-flagship/scripts/hub.mjs';

// 目标会话：优先取命令行第一个 --session 之后的参数，否则用 FABLE_SID 环境变量
const argv = process.argv.slice(2);
const si = argv.indexOf('--session');
export const sessionId = (si >= 0 ? argv[si + 1] : null) || process.env.FABLE_SID || '';

const { call } = await connect();

/**
 * 发送一条探针提示词到 sessionId 会话，等待回复稳定后返回纯文本。
 * @param {string} prompt
 * @returns {Promise<string>}
 */
export async function send(prompt) {
  if (!sessionId) throw new Error('未指定目标会话：用 --session <sid> 或环境变量 FABLE_SID');

  const code = `async (page) => {
    const result = { steps: [] };
    const log = s => result.steps.push(s);

    // 切到目标会话（已在目标页时跳过导航，避免多余刷新）
    await page.bringToFront();
    await page.waitForTimeout(1200);
    const curUrl = await page.evaluate(() => location.href);
    if (!curUrl.includes(${JSON.stringify(sessionId)})) {
      await page.goto('https://arena.ai/agent/' + ${JSON.stringify(sessionId)}, { waitUntil: 'domcontentloaded', timeout: 60000 });
      await page.waitForTimeout(4000);
      log('navigated');
    } else {
      log('already-on-session');
    }

    // 点掉可能出现的确认条
    await page.evaluate(() => {
      const labels = ['是', '否', '继续工作', 'Yes', 'No', 'Continue'];
      for (const b of [...document.querySelectorAll('button')]) {
        if (labels.includes((b.innerText || '').trim())) b.click();
      }
    });

    // 等编辑器就绪
    let ready = false;
    for (let i = 0; i < 30; i++) {
      const s = await page.evaluate(() => {
        const ed = document.querySelector('.ProseMirror[contenteditable="true"]');
        return ed && ed.editor ? 'ready' : 'wait';
      });
      if (s === 'ready') { ready = true; break; }
      await page.waitForTimeout(1000);
    }
    if (!ready) { result.error = 'no-composer'; return JSON.stringify(result); }

    // 写入探针（用键盘输入触发 React 状态）
    await page.evaluate(() => { const ed = document.querySelector('.ProseMirror[contenteditable="true"]'); if (ed) ed.focus(); });
    await page.keyboard.press('Control+A');
    await page.keyboard.press('Backspace');
    await page.keyboard.insertText(${JSON.stringify(prompt)});
    await page.waitForTimeout(800);

    // 等发送按钮可用（等的是上一轮跑完 + 输入就绪）
    let enabled = false;
    for (let i = 0; i < 60; i++) {
      const st = await page.evaluate(() => {
        const b = [...document.querySelectorAll('button')].find(x => (x.getAttribute('aria-label') || '') === 'Send message');
        return b ? (b.disabled ? 'busy' : 'idle') : 'none';
      });
      if (st === 'idle') { enabled = true; break; }
      await page.waitForTimeout(1500);
    }

    // 点发送
    let sent = false;
    for (let i = 0; i < 40; i++) {
      const c = await page.evaluate(() => {
        const b = [...document.querySelectorAll('button')].find(x => (x.getAttribute('aria-label') || '') === 'Send message');
        if (!b || b.disabled) return 'no';
        b.click(); return 'yes';
      });
      if (c === 'yes') { sent = true; break; }
      await page.waitForTimeout(1500);
    }
    if (!sent) { result.error = 'send-failed'; return JSON.stringify(result); }
    log('sent');

    // 记发送前 prose 块数，等新回复出现并稳定
    const before = await page.evaluate(() => document.querySelectorAll('[class*=prose]').length);
    let last = '';
    let stable = 0;
    let sawReply = false;
    for (let i = 0; i < 150; i++) {
      await page.waitForTimeout(5000);
      // URL 漂移自愈：回复过程中页面可能跳回列表页，发现后导航回来
      const u = await page.evaluate(() => location.href);
      if (!u.includes(${JSON.stringify(sessionId)})) {
        log('url-drift, re-navigating');
        await page.goto('https://arena.ai/agent/' + ${JSON.stringify(sessionId)}, { waitUntil: 'domcontentloaded', timeout: 60000 });
        await page.waitForTimeout(3000);
        continue;
      }
      const n = await page.evaluate(() => document.querySelectorAll('[class*=prose]').length);
      if (n > before) {
        const html = await page.evaluate(() => {
          const els = [...document.querySelectorAll('[class*=prose]')];
          const e = els[els.length - 1];
          return e ? e.innerHTML : '';
        });
        if (html.length === last.length) stable++; else { stable = 0; last = html; }
        if (last.length > 40) sawReply = true;
        if (stable >= 3 && last.length > 40) break;
      }
    }
    if (!last && !sawReply) { result.error = 'no-reply'; return JSON.stringify(result); }
    if (!last) { result.error = 'reply-unstable'; return JSON.stringify(result); }

    // 浏览器端只返回原始 HTML，剥除交回 Node 端做
    // （避免 code 里出现 < > 序列，破坏 browser_run_code_unsafe 的传输）
    result.html = last;
    result.ok = true;
    return JSON.stringify(result);
  }`;

  let raw;
  try {
    raw = unquote(await call('browser_run_code_unsafe', { code }, 300000));
  } catch (e) {
    throw new Error('发送探针失败: ' + (e.message || e));
  }

  // 解析返回。优先认标准 ### Result；其次认 ### Error 透出真实错误。
  let res;
  try { res = JSON.parse(raw); }
  catch {
    const errM = /### Error\r?\n([\s\S]*?)(?:\r?\n###|$)/.exec(raw);
    if (errM) throw new Error('浏览器执行探针报错: ' + errM[1].trim().slice(0, 300));
    const m = /### Result\s*\n([\s\S]*?)(\n###|$)/.exec(raw);
    try { res = JSON.parse(m ? m[1].trim() : raw); }
    catch { throw new Error('解析探针回复失败: ' + String(raw).slice(0, 300)); }
  }

  if (res.error) throw new Error('探针发送错误: ' + res.error + ' | steps=' + JSON.stringify(res.steps || []));
  if (!res.ok || (!res.html && !res.text)) throw new Error('未拿到探针回复: ' + JSON.stringify(res.steps || []));

  // Node 端剥 HTML（浏览器端不碰 <> 序列）
  const html = String(res.html || res.text || '');
  const md = html
    .replace(/<h[1-6][^>]*>/gi, ' ').replace(/<li[^>]*>/gi, ' ')
    .replace(/<br\s*\/?>/gi, ' ')
    .replace(/<\/?(?:p|div|ul|ol|blockquote|pre)[^>]*>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/\s+/g, ' ').trim();
  return md;
}

export default { send, sessionId };