# -*- coding: utf-8 -*-
"""生成给 Arena 的抽取任务提示（每次自带全部规矩，Arena 无记忆）。"""
import csv
import pathlib
import sys

OUT = pathlib.Path(r'C:\Users\赵豪\dsh\交易知识体系汇编')


CARD_LIST_MAX = 100000   # 卡清单字符上限（提示整体别撑爆输入框；超了就只列最近的）


def card_list():
    groups = []
    total = 0
    for d, tag in (('02_知识点', '知识点'), ('03_方法与策略', '方法'), ('04_案例', '案例')):
        items = []
        for p in sorted((OUT / d).glob('*.md')):
            h = p.read_text(encoding='utf-8').splitlines()[0].lstrip('# ').strip()
            items.append('- ' + h)
        groups.append((tag, items))
        total += sum(len(x) + 1 for x in items)
    # 超限：按「每个分组都保留最新的那部分」截断，并明确告知模型清单不完整
    if total > CARD_LIST_MAX:
        keep = CARD_LIST_MAX // 3
        lines = []
        for tag, items in groups:
            lines.append('**%s**：' % tag)
            if sum(len(x) + 1 for x in items) <= keep:
                lines.extend(items)
            else:
                n = 0
                tail = []
                for x in reversed(items):
                    if n + len(x) + 1 > keep:
                        break
                    tail.append(x)
                    n += len(x) + 1
                lines.append('（更早的 %d 张未列出，判断重复请只按编号区间推测，拿不准就新建）' % (len(items) - len(tail)))
                lines.extend(reversed(tail))
            lines.append('')
        return '\n'.join(lines)
    lines = []
    for tag, items in groups:
        lines.append('**%s**：' % tag)
        lines.extend(items)
        lines.append('')
    return '\n'.join(lines)


def build(picks, kmin, kmax, smin, smax, cmin, cmax, emin, emax, extra_note='', inline=False, batch='批004'):
    import glob
    rows = []
    for f in sorted(glob.glob(str(OUT / '工作分片/批*_清单.tsv'))):
        rows += list(csv.DictReader(open(f, encoding='utf-8'), delimiter='\t'))
    info = [r for r in rows if r['source_id'] in picks]
    if not info:
        raise SystemExit('找不到这些 source_id: %s' % picks)
    if inline:
        parts = ['下面是 %d 份课程笔记的**全文**（因为读不到本地文件，所以直接贴在提示里）。请把它们抽成结构化的知识卡片。' % len(picks), '']
        for r in info:
            fp = pathlib.Path(r'C:\Users\赵豪\dsh') / r['完整稿(阅读对象)']
            parts.append('=' * 20 + ' 资料 %s ｜ %s ' % (r['source_id'], r['主题']) + '=' * 20)
            parts.append('```markdown')
            parts.append(fp.read_text(encoding='utf-8').strip())
            parts.append('```')
            parts.append('')
        head = '\n'.join(parts)
    else:
        head = '我在附件里放了 %d 份课程笔记（文件名以 `SRC-` 开头）。请把它们抽成结构化的知识卡片。' % len(picks)
    # 仅精简稿来源也进入提示，但必须明确其证据上限；完整稿仍是默认阅读对象。
    limited = [r['source_id'] for r in info if not (r.get('完整稿(阅读对象)') or '').strip()]
    if limited:
        head += '\n\n受限来源说明：' + '、'.join(limited) + ' 只有精简稿可核；不得把精简稿未提供的细节写成完整稿事实。\n'
    enh = [r['source_id'] for r in info if '仅增强稿' in (r.get('证据限制') or '')]
    if enh:
        head += ('\n\n本次含 (增强版) 主题汇编：' + '、'.join(enh) +
                 '。它们是**按主题汇编的增强稿，不是逐字完整稿**：'
                 '卡片「底本层级」必须写「仅增强稿可见」，不得把它们当作完整稿逐字引用；'
                 '汇编里若把多课内容并在一起，只能照实记录，不要替原文补跨课结论。\n')
    body = head + """

# 一、项目背景

# 一、项目背景

把某位股票/期货讲师的课程笔记整理成可检索的知识体系。规矩如下，**每条都必须遵守**：

1. **只写原稿有的**。原稿没有的定义、参数、公式、成交记录一律不写，写「原文未明确」。
2. **不许编造，不许用你自己的交易知识补全**。原稿没给数字就不要给数字；原稿没给判据就不要编判据。
3. **不许跨课综合**。不能把 A 课的入场条件 + B 课的止损条件拼成"一套策略"。
4. **只讲多头的课不得自动镜像成空头方法**，反之亦然。
5. **区分立场**。同一份笔记里可能有三种声音：①课程讲述者（老师原话）②书中作者（如《股票作手回忆录》的利弗莫尔）③编辑者写的【老师点评/批判】段与「与已有课程的关系」段。**第三种不是老师原话，不能当规则依据**。每张卡必须写明来源立场。
6. **期货课原稿没写合约月份的**，一律写「原稿未明确」，不做移仓/换月连接。
7. **数字疑点要隔离**。疑为转写错误、或与算术不符的数字，标 `[原稿如此，疑误]`，**不得写进正式规则**。

# 二、要产出三类卡片

## 知识点卡 `K-XXXX`

```
# K-XXXX 名称
> 来源：SRC-xxxxxx（第N课 课名）· 证据 E-xxxx
> 来源立场：课程讲述者采纳／书中作者观点／编辑者评注／被批评的方法／原文态度不明
> 底本层级：完整稿可见／仅增强稿可见／转述待核

一句话定义：……

## 它解决什么问题
## 如何识别
（逐条写成立条件，每条句后标证据ID）
## 适用边界与失效
## 与其他概念的关系
## 案例与证据
```

## 方法卡 `S-XXXX`

```
# S-XXXX 名称
> 来源：… · 证据 E-xxxx
- 性质：观察信号／局部方法／规则完整的策略／待验证组合方案
- 规则版本：
- 完整度分级：已给方向／只给名称缺参数／完全缺失
- 效果证据：

## 目的与适用环境
## 条件与动作
（表格十行：环境过滤／形态或指标形成／确认／入场／初始止损／仓位与资金／持仓与跟踪／加减仓／止盈与退出／失效与放弃；
每行填：条件或动作｜时点与周期｜证据ID｜限制或缺口）
## 规则之间怎样衔接
## 案例和失败方式
## 版本分歧与证据限制
```

## 案例卡 `C-XXXX`

```
# C-XXXX 名称
> 来源：… · 证据 E-xxxx
日期、品种、合约、周期、关联方法ID、来源ID
证据性质：课堂假设／候选预案／作者自述交易／有独立记录

## 当时已知信息
## 原计划与触发
## 后续过程与结果（原稿未报告结果就写「结果未提供」）
## 本例说明的边界
## 数字与证据
```

# 三、证据清单（必须同时产出）

每张卡引用的证据都要在**最后的证据清单**里逐条列出，格式为 **TSV 五列、制表符分隔**：

`证据ID<TAB>source_id<TAB>位置（文件名＋小标题）<TAB>原文摘录（逐字，不许改写，≤300字）<TAB>用途（哪张卡的哪一节）`

**「原文摘录」这一列必须是从附件里逐字复制的一整段原文**（直接复制粘贴即可），
不许概括、缩写、改写、拼接、调整语序。校验程序会把这一列拿回附件逐字比对，
对不上就整组退回重做。**如果某条内容在附件里找不到可以逐字复制的原文，就不要写这条证据**，
也不要为了凑数把它写成摘要——宁可少列证据、少建卡。

证据ID 从 `E-%(emin)s` 开始连续编号。

# 四、先按本次原文建卡

不要为了避免重复而少写。若你明确记得这是已有卡的同一件事，可以写「补充 K-xxxx」；拿不准就新建。重复和对立会在入库后统一核对，不在本次提示里附带旧卡片目录。

# 五、本次任务

## 资料

%(files)s

## ID 号段（严格只用这些，不许越界）

- 知识点卡：`K-%(kmin)s` – `K-%(kmax)s`
- 方法卡：`S-%(smin)s` – `S-%(smax)s`
- 案例卡：`C-%(cmin)s` – `C-%(cmax)s`
- 证据：`E-%(emin)s` – `E-%(emax)s`

## 额外注意

%(extra)s

# 六、输出格式

按这个顺序输出，不要加别的话：

1. `## 卡片` —— 每张卡一个 markdown 代码块（```markdown 包裹），标题就是 `# K-XXXX 名称`
2. `## 证据清单` —— 一个代码块，里面是 TSV 五列
3. `## 底本层级与疑点` —— 逐条列出：哪些内容只有完整稿可见、哪些数字可疑（标 `[原稿如此，疑误]`）、原稿明确没给的东西
4. `## 与已有卡的关系` —— 有没有和已有卡重复或矛盾

**找不到内容就说找不到，不要凑。宁可少建卡，不要编内容。**
""" % dict(files='\n'.join('- `%s`｜%s｜%d 字节' % (r['source_id'], r['主题'], (pathlib.Path(r'C:\Users\赵豪\dsh') / ((r.get('完整稿(阅读对象)') or r.get('精简稿(导航用)') or '')).strip()).stat().st_size) for r in info),
           kmin=kmin, kmax=kmax, smin=smin, smax=smax, cmin=cmin, cmax=cmax, emin=emin, emax=emax, extra=extra_note)
    return body


if __name__ == '__main__':
    import json
    cfg = json.loads(sys.argv[1])
    text = build(**cfg)
    pathlib.Path(cfg['out']).write_text(text, encoding='utf-8')
    print('提示已写:', cfg['out'], len(text), '字符')
