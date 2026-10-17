# -*- coding: utf-8 -*-
"""阶段C 看门狗：循环进程不在就自动拉起；额度耗尽／连续零进展则不打扰。

用法: python -X utf8 工具/看门狗.py [检查间隔秒, 默认120]
日志: C:/tmp/arena_watchdog.log

为什么需要它：批量循环是长跑（几百批、以周计），中途可能因为
网页抖动、浏览器被回收、脚本异常等原因退出。人在不在都不该停。
"""
import pathlib
import re
import subprocess
import sys
import time

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
LOOP_LOG = pathlib.Path('C:/tmp/arena_loop.log')
WD_LOG = pathlib.Path('C:/tmp/arena_watchdog.log')
INTERVAL = int(sys.argv[1]) if len(sys.argv) > 1 else 120
BACKOFF = 1800      # 既定停止后的退避：30 分钟再试一次
# 这些情况说明「不是意外退出」，看门狗不要盲目拉起
STOP_MARKERS = ('额度耗尽', '连续两轮零进展', '没有可取的来源了', '需要人工验证')


def log(msg):
    line = '[%s] %s' % (time.strftime('%m-%d %H:%M:%S'), msg)
    print(line, flush=True)
    with open(WD_LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def loop_running():
    """循环或遗留驱动还在时，不允许启动第二个写入进程。"""
    try:
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             "@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
              "Where-Object { $_.CommandLine -match 'Arena批量循环|Arena驱动_连续抽取' }).Count"],
            capture_output=True, text=True, timeout=60)
        return int((r.stdout or '0').strip() or '0') > 0
    except Exception as e:
        log('查进程失败: %s' % str(e)[:100])
        return True          # 查不到就当在跑，避免重复拉起


def stopped_on_purpose():
    """只看**最近一次启动之后**的日志：那次结束是不是「该停的原因」。

    2026-10-01 踩过坑：旧写法在整段日志尾部找标记，翻到了几小时前的一次
    「连续两轮零进展」，于是循环明明死了也不拉起。
    """
    try:
        lines = LOOP_LOG.read_text(encoding='utf-8', errors='replace').splitlines()
    except Exception:
        return False
    last_start = -1
    for i, l in enumerate(lines):
        if '批量循环启动' in l:
            last_start = i
    seg = '\n'.join(lines[last_start:] if last_start >= 0 else lines[-40:])
    for mk in STOP_MARKERS:
        if mk in seg:
            return mk
    return False


def start_loop():
    cmd = ('cmd.exe /c cd /d "%s" && python -X utf8 "工具\\Arena批量循环.py" 2 '
           '>> C:\\tmp\\phaseC_loop.out 2>&1' % OUT)
    r = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine='%s'} | "
         "Select-Object -ExpandProperty ReturnValue" % cmd.replace("'", "''")],
        capture_output=True, text=True, timeout=90)
    return (r.stdout or '').strip()


log('=== 看门狗启动 | 每 %d 秒检查一次 ===' % INTERVAL)
VERIFY_FLAG = pathlib.Path('C:/tmp/arena_verify_stop.flag')
while True:
    time.sleep(INTERVAL)
    if loop_running():
        continue
    # 2026-10-09 YG 红线：页面需要人工验证（Try again / Reset session and reload）时
    # **绝不自动拉起**——自动重试风控页可能封号。人工处理完删掉旗标，看门狗才恢复值守。
    if VERIFY_FLAG.exists():
        log('验证旗标在 → 需要人工处理，看门狗不拉起循环（删 C:/tmp/arena_verify_stop.flag 后恢复）')
        continue
    why = stopped_on_purpose()
    if why:
        # 既定停止（额度／零进展／跑完）也不永久躺平：退避一段时间后再试一次，
        # 这样「额度恢复」「页面抖动已过」都能自愈，又不会疯狂空转。
        log('循环不在跑，上次为既定停止（%s）→ 退避 %d 分钟后再试' % (why, BACKOFF // 60))
        time.sleep(BACKOFF)
    # 退避期间用户可能已恢复循环；启动前必须再查一次。
    if loop_running():
        continue
    log('循环不在跑且非既定停止 → 自动拉起')
    rv = start_loop()
    log('拉起返回码: %s' % rv)
    time.sleep(60)
