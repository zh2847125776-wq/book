# -*- coding: utf-8 -*-
"""Antigravity 抽取看门狗：循环进程不在就自动拉起；连续两轮零进展则退避。

用法:
    python -X utf8 工具/Antigravity看门狗.py [检查间隔秒, 默认120]
日志:
    C:/tmp/antigravity_watchdog.log
"""
import pathlib
import subprocess
import sys
import time

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')
LOOP_LOG = pathlib.Path('C:/tmp/antigravity_loop.log')
WD_LOG = pathlib.Path('C:/tmp/antigravity_watchdog.log')
INTERVAL = int(sys.argv[1]) if len(sys.argv) > 1 else 120
BACKOFF = 300  # 既定停止后退避 5 分钟
STOP_MARKERS = ('全部批次与来源均已抽取完毕', '无进展，停止循环以待人工检查', '连续两轮无进展')


def log(msg):
    line = '[%s] %s' % (time.strftime('%m-%d %H:%M:%S'), msg)
    print(line, flush=True)
    with open(WD_LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')


def loop_running():
    try:
        r = subprocess.run(
            ['powershell', '-NoProfile', '-Command',
             "@(Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | "
             "Where-Object { $_.CommandLine -match 'Antigravity批量循环|Antigravity驱动_连续抽取' }).Count"],
            capture_output=True, text=True, timeout=60)
        return int((r.stdout or '0').strip() or '0') > 0
    except Exception as e:
        log('查进程失败: %s' % str(e)[:100])
        return True


def stopped_on_purpose():
    if not LOOP_LOG.exists():
        return False
    try:
        lines = LOOP_LOG.read_text(encoding='utf-8', errors='replace').splitlines()
    except Exception:
        return False
    last_start = -1
    for i, l in enumerate(lines):
        if '批量抽取循环启动' in l:
            last_start = i
    seg = '\n'.join(lines[last_start:] if last_start >= 0 else lines[-40:])
    for mk in STOP_MARKERS:
        if mk in seg:
            return mk
    return False


def start_loop():
    cmd = ('cmd.exe /c cd /d "%s" && python -X utf8 "工具\\Antigravity批量循环.py" 2 0 '
           '>> C:\\tmp\\antigravity_loop.out 2>&1' % OUT)
    r = subprocess.run(
        ['powershell', '-NoProfile', '-Command',
         "Invoke-CimMethod -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine='%s'} | "
         "Select-Object -ExpandProperty ReturnValue" % cmd.replace("'", "''")],
        capture_output=True, text=True, timeout=90)
    return (r.stdout or '').strip()


def main():
    log('=== Antigravity 看门狗启动 | 每 %d 秒巡检一次 ===' % INTERVAL)
    while True:
        if not loop_running():
            why = stopped_on_purpose()
            if why == '全部批次与来源均已抽取完毕':
                log('全部批次与来源均已结清完毕！看门狗任务圆满完成，正常退出。')
                break
            elif why:
                log('循环因暂态异常停机（%s）→ 保护性退避 %d 分钟等待网络/节点自愈...' % (why, BACKOFF // 60))
                time.sleep(BACKOFF)
                if not loop_running():
                    log('退避期满，自动重新拉起批量循环...')
                    rv = start_loop()
                    log('拉起返回码: %s' % rv)
            else:
                log('循环进程不在跑 → 自动拉起批量循环')
                rv = start_loop()
                log('拉起返回码: %s' % rv)
        time.sleep(INTERVAL)


if __name__ == '__main__':
    main()
