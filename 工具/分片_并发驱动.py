# -*- coding: utf-8 -*-
"""分片工作区并发驱动（多 Slot 隔离 + 进程互斥锁）。

支持多子代理并发推进：
  python -X utf8 工具/分片_并发驱动.py 分配组 <slot_name>
  python -X utf8 工具/分片_并发驱动.py 入库组 <slot_name> <回复文件>
  python -X utf8 工具/分片_并发驱动.py 状态
"""
import csv
import importlib.util
import json
import msvcrt
import os
import pathlib
import re
import shutil
import subprocess
import sys
import time

BASE = pathlib.Path(r'C:\Users\赵豪\dsh')
OUT = BASE / '交易知识体系汇编'
SHARD_NAME = 'Shard3_b220_243'
ROOT = OUT / '分片工作区' / SHARD_NAME
SLOTS_DIR = ROOT / 'slots'
LOCK_FILE = ROOT / '.concurrent.lock'
BUDGET = {'K': 8, 'S': 5, 'C': 5, 'E': 20}
SKIP = {'已抽取', '工具脚本·无可用内容', '无可用交易内容'}


class FileLock:
    def __init__(self, lock_p):
        self.lock_p = lock_p
        self.fh = None

    def __enter__(self):
        self.lock_p.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(self.lock_p, 'w', encoding='utf-8')
        while True:
            try:
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_NBLCK, 1)
                break
            except OSError:
                time.sleep(0.05)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.fh:
            try:
                self.fh.seek(0)
                msvcrt.locking(self.fh.fileno(), msvcrt.LK_UNLCK, 1)
            except Exception:
                pass
            self.fh.close()
            self.fh = None


def ledger_done():
    ledger = ROOT / 'out/01_资料与索引/来源去向.tsv'
    if not ledger.is_file():
        return set()
    lines = ledger.read_text(encoding='utf-8').splitlines()
    if not lines:
        return set()
    h = lines[0].split('\t')
    si, sti = h.index('source_id'), h.index('处理状态')
    return {l.split('\t')[si] for l in lines[1:]
            if len(l.split('\t')) > sti and l.split('\t')[sti] in SKIP}


def active_slot_picks():
    active = set()
    if SLOTS_DIR.is_dir():
        for gp in SLOTS_DIR.glob('*/pending_group.json'):
            try:
                data = json.loads(gp.read_text(encoding='utf-8'))
                for p in data.get('picks', []):
                    active.add(p)
            except Exception:
                pass
    return active


def batch_rows(n):
    p = OUT / ('工作分片/批%03d_清单.tsv' % n)
    if not p.is_file():
        return []
    return list(csv.DictReader(open(p, encoding='utf-8'), delimiter='\t'))


def resolve_src(r):
    complete = (r.get('完整稿(阅读对象)') or '').strip()
    trimmed = (r.get('精简稿(导航用)') or '').strip()
    rel = complete or trimmed
    if not rel:
        return None, '完整稿和精简稿都为空'
    src = BASE / rel
    if not src.is_file():
        return None, '找不到文件 %s' % rel
    return src, ('' if complete else '仅精简稿')


def own_cards_note(limit=6000):
    items = []
    for d in ('02_知识点', '03_方法与策略', '04_案例'):
        for p in sorted((ROOT / 'out' / d).glob('*.md')):
            try:
                h = p.read_text(encoding='utf-8').splitlines()[0].strip()
            except Exception:
                continue
            items.append('- ' + h)
            if sum(len(x) + 1 for x in items) > limit:
                items.append('（本分片更早的卡未列出，拿不准就新建，不要复用主仓库之外的编号）')
                return '\n'.join(items)
    return '\n'.join(items) if items else '（本分片暂无自建卡）'


def cmd_fetch(slot_name):
    slot_dir = SLOTS_DIR / slot_name
    pending_p = slot_dir / 'pending_group.json'
    if pending_p.is_file():
        print('Slot [%s] 已有 pending 任务，不可重复分配。' % slot_name)
        data = json.loads(pending_p.read_text(encoding='utf-8'))
        print('当前 Picks: %s, 号段: K%d-S%d-C%d-E%d' % (
            data['picks'], data['kmin'], data['smin'], data['cmin'], data['emin']))
        return

    with FileLock(LOCK_FILE):
        meta = json.loads((ROOT / '号段.json').read_text(encoding='utf-8'))
        nxt_p = ROOT / 'next_ids.json'
        if nxt_p.is_file():
            nxt = json.loads(nxt_p.read_text(encoding='utf-8'))
        else:
            nxt = {k: meta[k][0] for k in ('K', 'S', 'C', 'E')}

        done = ledger_done()
        active = active_slot_picks()

        picks, batch_name = [], ''
        for a, b in meta['batches']:
            for n in range(a, b + 1):
                for r in batch_rows(n):
                    sid = r['source_id']
                    if sid not in done and sid not in active:
                        picks.append(r)
                        if not batch_name:
                            batch_name = '批%03d' % n
                        if len(picks) >= 2:
                            break
                if len(picks) >= 2:
                    break
            if picks:
                break

        if not picks:
            print('全部完成：本分片批次范围无未抽取来源！')
            return

        # 检查备料
        staged = []
        for r in picks:
            src, flag = resolve_src(r)
            if src is None:
                print('备料不全: %s %s' % (r['source_id'], flag))
                sys.exit(7)
            staged.append((r, src, flag))

        # 分配号段
        ids = {}
        for k in ('K', 'S', 'C', 'E'):
            lo, hi = meta[k][0], meta[k][1]
            if nxt[k] + BUDGET[k] - 1 > hi:
                print('号段用尽 STOP：%s 已到 %d，上限 %d！' % (k, nxt[k], hi))
                sys.exit(6)
            ids[k] = (nxt[k], nxt[k] + BUDGET[k] - 1)
            nxt[k] += BUDGET[k]

        nxt_p.write_text(json.dumps(nxt, ensure_ascii=False, indent=1), encoding='utf-8')

        # 准备 slot 目录
        slot_dir.mkdir(parents=True, exist_ok=True)
        stage_dir = slot_dir / 'stage'
        if stage_dir.exists():
            shutil.rmtree(stage_dir)
        stage_dir.mkdir(parents=True)

        got = []
        for r, src, flag in staged:
            dst = stage_dir / ('%s_%s' % (r['source_id'], src.name))
            shutil.copy2(src, dst)
            got.append((r, dst))

        # 生成提示
        spec = importlib.util.spec_from_file_location('gen', str(OUT / '工具/Arena任务_生成提示.py'))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)

        note = '本组资料：' + '；'.join('%s（第%s课 %s，课型%s）' % (r['source_id'], r['课号'], r['主题'], r['课型']) for r, _ in got)
        note += '。**若这些资料属于同一系列，注意不要跨系列串联策略；若与已有卡讲同一件事，写「补充 K-xxxx」不要新建。**'
        note += '**请先核对底本层级**：若给的是"(增强版)"笔记而非完整稿，务必在卡片里标「仅增强稿可见」，不要写成完整稿。'
        note += '\n\n本分片已自建卡（判重时与主仓库清单一并考虑，编号只用本次分配）：\n' + own_cards_note()

        t = m.build(picks=[r['source_id'] for r, _ in got],
                    kmin='%04d' % ids['K'][0], kmax='%04d' % ids['K'][1],
                    smin='%04d' % ids['S'][0], smax='%04d' % ids['S'][1],
                    cmin='%04d' % ids['C'][0], cmax='%04d' % ids['C'][1],
                    emin='%04d' % ids['E'][0], emax='%04d' % ids['E'][1],
                    extra_note=note, inline=True, batch=batch_name)

        (slot_dir / 'pending_prompt.md').write_text(t, encoding='utf-8')
        group = {'slot': slot_name, 'batch': batch_name, 'picks': [r['source_id'] for r, _ in got],
                 'kmin': ids['K'][0], 'kmax': ids['K'][1], 'smin': ids['S'][0], 'smax': ids['S'][1],
                 'cmin': ids['C'][0], 'cmax': ids['C'][1], 'emin': ids['E'][0], 'emax': ids['E'][1]}
        pending_p.write_text(json.dumps(group, ensure_ascii=False, indent=1), encoding='utf-8')

    print('Slot [%s] 分配成功: %s %s' % (slot_name, batch_name, group['picks']))
    print('号段: K%04d-%04d S%04d-%04d C%04d-%04d E%04d-%04d' % (
        ids['K'][0], ids['K'][1], ids['S'][0], ids['S'][1],
        ids['C'][0], ids['C'][1], ids['E'][0], ids['E'][1]))
    print('Prompt 路径: %s' % (slot_dir / 'pending_prompt.md'))


def cmd_store(slot_name, reply_path):
    slot_dir = SLOTS_DIR / slot_name
    pending_p = slot_dir / 'pending_group.json'
    if not pending_p.is_file():
        print('Slot [%s] 没有 pending 组！' % slot_name)
        sys.exit(8)

    group = json.loads(pending_p.read_text(encoding='utf-8'))
    rp = pathlib.Path(reply_path)
    if not rp.is_file():
        print('回复文件不存在: %s' % reply_path)
        sys.exit(8)

    with FileLock(LOCK_FILE):
        r = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/Arena入库.py'), str(rp),
                            '%04d' % group['emin'], '%04d' % group['emax'],
                            str(slot_dir / 'stage'), ','.join(group['picks']), str(ROOT / 'out')],
                           capture_output=True, text=True, timeout=600, cwd=str(OUT))
        out = (r.stdout or '') + (r.stderr or '')
        print(out.strip()[-1200:])
        if r.returncode != 0:
            print('Slot [%s] 入库失败（已保留 pending）：exit=%d' % (slot_name, r.returncode))
            sys.exit(r.returncode)

        try:
            raw = rp.read_text(encoding='utf-8')
            heads = len(re.findall(r'(?m)^[ \t]*(?:#{1,6}[ \t]*)?\*{0,2}(?:补充[ \t]*)?[KSC]-\d{4,5}\b', raw))
        except Exception:
            heads = 0
        m = re.search(r'新卡 (\d+)', out or '')
        patched = ('保存补丁' in (out or ''))
        if heads and m and int(m.group(1)) == 0 and not patched:
            print('Slot [%s] 回复里有 %d 个卡片标题但新卡为 0！' % (slot_name, heads))
            sys.exit(9)

        dst = ROOT / 'out/07_审计与交付' / ('分片产出_%s.md' % '_'.join(sorted(group['picks'])))
        shutil.copy2(str(rp), str(dst))
        with open(ROOT / 'groups_done.jsonl', 'a', encoding='utf-8') as fh:
            fh.write(json.dumps({'batch': group['batch'], 'slot': slot_name, 'picks': group['picks'],
                                 'reply': dst.name}, ensure_ascii=False) + '\n')
        pending_p.unlink(missing_ok=True)

    # 运行质检（质检只读，无需锁）
    print('\n--- 运行充实度质检 ---')
    qr = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/质检_卡片充实度.py'), str(dst)],
                        capture_output=True, text=True, cwd=str(OUT))
    qout = (qr.stdout or '') + (qr.stderr or '')
    print(qout.strip())
    if qr.returncode != 0:
        print('!! Slot [%s] 充实度质检不通过，需排查卡片质量！' % slot_name)
    else:
        print('Slot [%s] 入库与质检全部通过 ✓' % slot_name)


def cmd_status():
    done = ledger_done()
    meta = json.loads((ROOT / '号段.json').read_text(encoding='utf-8'))
    total_sources = sum(len(batch_rows(n)) for a, b in meta['batches'] for n in range(a, b + 1))
    shard_sources = []
    for a, b in meta['batches']:
        for n in range(a, b + 1):
            for r in batch_rows(n):
                shard_sources.append(r['source_id'])

    done_in_shard = sum(1 for s in shard_sources if s in done)

    cards_k = len(list((ROOT / 'out/02_知识点').glob('*.md')))
    cards_s = len(list((ROOT / 'out/03_方法与策略').glob('*.md')))
    cards_c = len(list((ROOT / 'out/04_案例').glob('*.md')))

    nxt_p = ROOT / 'next_ids.json'
    nxt = json.loads(nxt_p.read_text(encoding='utf-8')) if nxt_p.is_file() else {}

    print('=== Shard3_b220_243 进度状态 ===')
    print('来源总数: %d | 已完成: %d (%.1f%%) | 剩余: %d' % (
        len(shard_sources), done_in_shard, (done_in_shard / len(shard_sources) * 100) if shard_sources else 0,
        len(shard_sources) - done_in_shard))
    print('累计卡片: K=%d, S=%d, C=%d (总计 %d 张)' % (cards_k, cards_s, cards_c, cards_k + cards_s + cards_c))
    print('当前号段指针: %s' % nxt)

    active = []
    if SLOTS_DIR.is_dir():
        for gp in SLOTS_DIR.glob('*/pending_group.json'):
            try:
                g = json.loads(gp.read_text(encoding='utf-8'))
                active.append('%s (%s %s)' % (g.get('slot'), g.get('batch'), g.get('picks')))
            except Exception:
                pass
    print('当前运行中 Slot: %d 个 (%s)' % (len(active), ', '.join(active) if active else '无'))


def main():
    if len(sys.argv) < 2:
        print('用法: 分片_并发驱动.py <分配组 slot_name | 入库组 slot_name 回复文件 | 状态>')
        sys.exit(1)
    op = sys.argv[1]
    if op == '分配组' and len(sys.argv) >= 3:
        cmd_fetch(sys.argv[2])
    elif op == '入库组' and len(sys.argv) >= 4:
        cmd_store(sys.argv[2], sys.argv[3])
    elif op == '状态':
        cmd_status()
    else:
        print('未知操作: %s' % op)
        sys.exit(1)


if __name__ == '__main__':
    main()
