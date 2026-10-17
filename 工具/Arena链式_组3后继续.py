# -*- coding: utf-8 -*-
"""等组3生成完 → 抓取入库 → 再跑驱动的剩余批次。"""
import pathlib, subprocess, sys, time, importlib.util

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
SKILL = pathlib.Path(r'C:\Users\赵豪\.agents\skills\arena-flagship\scripts')
LOG = pathlib.Path('C:/tmp/arena_chain.log')

def log(m):
    line = '[%s] %s' % (time.strftime('%H:%M:%S'), m)
    print(line, flush=True)
    open(LOG, 'a', encoding='utf-8').write(line + '\n')

log('=== 链式任务启动：等组3 → 抓取入库 → 继续驱动 ===')
# 1) 等空闲
for i in range(300):
    r = subprocess.run(['node', str(SKILL / '_idle.mjs')], capture_output=True, text=True, timeout=120, cwd=str(SKILL))
    if 'idle' in (r.stdout or ''):
        log('页面空闲（等了 %d 次）' % i); break
    time.sleep(10)
else:
    log('等空闲超时'); sys.exit(1)

# 2) 抓组3
subprocess.run(['node', str(SKILL / '_wait.mjs'), 'E-0667', 'C:/tmp/g3b_full.md', '3'],
               capture_output=True, text=True, timeout=600, cwd=str(SKILL))
f = pathlib.Path('C:/tmp/g3b_full.md')
log('组3抓取: %d 字符' % (f.stat().st_size if f.exists() else 0))
if f.exists() and f.stat().st_size > 500:
    subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/Arena入库.py'), str(f), '667', '686',
                    'C:/tmp/arena_stage', 'SRC-003597,SRC-004417'], timeout=600)
    log('组3入库完成')
else:
    log('组3抓取为空，跳过（留待重跑）')

# 3) 继续驱动
log('=== 继续驱动批006 ===')
r = subprocess.run(['python', '-X', 'utf8', str(OUT / '工具/Arena驱动_连续抽取.py'), '批006'],
                   capture_output=True, text=True, timeout=14400, cwd=str(OUT))
log('驱动退出码 %d' % r.returncode)
for ln in (r.stdout or '').strip().splitlines()[-25:]:
    log('  ' + ln)
log('=== 链式任务结束 ===')
