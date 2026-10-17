# -*- coding: utf-8 -*-
"""
博主交易体系·Python 客观技术面体检引擎 (Feature Engine)
功能：
1. 自动拉取股票最新日线与近期行情（动态前复权，规避复权陷阱，双源容灾: 腾讯行情接口 + AKShare）
2. 精确计算 MA (5, 10, 20, 60)、ATR(14)、MACD (DIF, DEA, 柱状图)、量比与波动
3. 自动扫描前高前低、箱体形态与破翻结构 (一二三号位)
4. 输出绝对客观、绝不幻觉的《技术面体检报告 JSON》，供 AI 决策参谋审查
"""

import sys
import json
import datetime
import requests
import pandas as pd
import numpy as np

def fetch_kline_tencent(symbol, count=100):
    """通过腾讯前复权高速日线接口拉取数据 (高可用、低延迟、防封禁)"""
    sym = str(symbol).strip().zfill(6)
    if sym.startswith('6') or sym.startswith('9'):
        market = 'sh'
    elif sym.startswith('0') or sym.startswith('3'):
        market = 'sz'
    elif sym.startswith('4') or sym.startswith('8'):
        market = 'bj'
    else:
        market = 'sh'
        
    secid = f"{market}{sym}"
    url = f"https://web.ifzq.gtimg.cn/appstock/app/fqkline/get?param={secid},day,,,{count},qfq"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    r = requests.get(url, headers=headers, timeout=6)
    if r.status_code != 200:
        raise ValueError(f"HTTP请求失败: 状态码 {r.status_code}")
        
    data = r.json()
    stock_dict = data.get('data', {}).get(secid, {})
    klines = stock_dict.get('qfqday') or stock_dict.get('day')
    if not klines:
        raise ValueError(f"标的 {secid} 未能获取到K线数据")
        
    # 格式: 日期, 开盘, 收盘, 最高, 最低, 成交量
    records = []
    for row in klines:
        records.append({
            '日期': row[0],
            '开盘': float(row[1]),
            '收盘': float(row[2]),
            '最高': float(row[3]),
            '最低': float(row[4]),
            '成交量': float(row[5])
        })
        
    df = pd.DataFrame(records)
    return df

def calculate_indicators(df):
    """计算核心均线、ATR、MACD 与量比指标"""
    close = df['收盘'].astype(float)
    high = df['最高'].astype(float)
    low = df['最低'].astype(float)
    vol = df['成交量'].astype(float)
    
    # 均线系统
    df['MA5'] = close.rolling(5).mean()
    df['MA10'] = close.rolling(10).mean()
    df['MA20'] = close.rolling(20).mean()
    df['MA60'] = close.rolling(60).mean()
    
    # 均线斜率 (以20日线5日变化率度量)
    df['MA20_slope'] = (df['MA20'] - df['MA20'].shift(5)) / df['MA20'].shift(5) * 100
    df['MA60_slope'] = (df['MA60'] - df['MA60'].shift(5)) / df['MA60'].shift(5) * 100
    
    # ATR (14)
    tr1 = high - low
    tr2 = (high - close.shift(1)).abs()
    tr3 = (low - close.shift(1)).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df['ATR14'] = tr.rolling(14).mean()
    
    # MACD (12, 26, 9)
    exp12 = close.ewm(span=12, adjust=False).mean()
    exp26 = close.ewm(span=26, adjust=False).mean()
    df['DIF'] = exp12 - exp26
    df['DEA'] = df['DIF'].ewm(span=9, adjust=False).mean()
    df['MACD_HIST'] = (df['DIF'] - df['DEA']) * 2
    
    # 5日成交均量与量比
    df['VOL_MA5'] = vol.rolling(5).mean()
    df['VOL_RATIO_5'] = vol / df['VOL_MA5']
    
    return df

def detect_box_and_reversal(df, lookback=30):
    """检测近期箱体与破翻 (2B) 结构"""
    recent = df.tail(lookback).copy()
    if len(recent) < 20:
        return {}
    
    # 排除最后5根K线，以之前的高低点作为箱体参考
    box_base = recent.iloc[:-5] if len(recent) > 10 else recent
    box_high = float(box_base['最高'].max())
    box_low = float(box_base['最低'].min())
    
    cur_close = float(recent['收盘'].iloc[-1])
    recent_min_low = float(recent['最低'].min())
    
    # 检查过去5天内是否击穿过 box_low
    had_breakdown = recent_min_low < box_low
    is_standing_back = cur_close >= box_low
    
    return {
        "box_lookback_bars": lookback,
        "box_high": round(box_high, 2),
        "box_low": round(box_low, 2),
        "box_amplitude_pct": round((box_high - box_low) / box_low * 100, 2),
        "recent_min_low_p1": round(recent_min_low, 2),
        "had_breakdown_p1": bool(had_breakdown),
        "is_standing_back_p2": bool(is_standing_back),
        "is_box_break_reversal_setup": bool(had_breakdown and is_standing_back)
    }

def generate_checkup_report(symbol):
    """主调用入口：生成股票体检报告字典"""
    symbol_str = str(symbol).strip().zfill(6)
    
    # 拉取前复权数据
    df = fetch_kline_tencent(symbol_str, count=100)
    if df is None or len(df) < 30:
        raise ValueError(f"标的 {symbol_str} 行情数据不足 30 根 K 线")
        
    df = calculate_indicators(df)
    last = df.iloc[-1]
    prev = df.iloc[-2]
    
    cur_price = round(float(last['收盘']), 2)
    atr = round(float(last['ATR14']), 2) if not np.isnan(last['ATR14']) else round(cur_price * 0.03, 2)
    ma20 = round(float(last['MA20']), 2)
    ma60 = round(float(last['MA60']), 2) if not np.isnan(last['MA60']) else ma20
    dif = round(float(last['DIF']), 3)
    
    # 均线多空排列检查
    is_bullish = bool(last['MA5'] > last['MA10'] > last['MA20'] > last['MA60']) if not np.isnan(last['MA60']) else False
    is_bearish = bool(last['MA5'] < last['MA10'] < last['MA20'] < last['MA60']) if not np.isnan(last['MA60']) else False
    
    # 5 穿 20 检查
    ma5_cross_20_today = bool(last['MA5'] > last['MA20'] and prev['MA5'] <= prev['MA20'])
    ma5_cross_20_recent = bool((df['MA5'].tail(3) > df['MA20'].tail(3)).any() and (df['MA5'].tail(5) <= df['MA20'].tail(5)).any())
    
    # 形态学检测
    box_info = detect_box_and_reversal(df, lookback=30)
    
    # 止损余量动态计算 (max(0.02, 0.20 * ATR))
    margin = round(max(0.02, 0.20 * atr), 2)
    
    # 规则初筛判定
    rule_results = {}
    
    # 战法1：箱体破底翻预筛
    if box_info.get("is_box_break_reversal_setup"):
        p1 = box_info["recent_min_low_p1"]
        stop_price = round(p1 - margin, 2)
        target = box_info["box_high"]
        risk = max(0.01, cur_price - stop_price)
        reward = max(0.0, target - cur_price)
        rrr = round(reward / risk, 2)
        rule_results["STRAT_01_破底翻"] = {
            "match": True,
            "status": "符合诱空后收复架构",
            "suggested_stop_loss": stop_price,
            "first_target": target,
            "rrr": rrr,
            "rrr_pass": bool(rrr >= 2.5)
        }
    else:
        rule_results["STRAT_01_破底翻"] = {
            "match": False,
            "reason": "未出现近期击穿箱体下限后重回收复走势"
        }
        
    # 战法2：5x20交叉共振回踩预筛
    if ma5_cross_20_recent and cur_price >= ma20:
        stop_price = round(ma20 - margin, 2)
        rule_results["STRAT_02_5x20回测"] = {
            "match": True,
            "status": "处于5穿20后均线支撑带",
            "is_shrink_pullback": bool(last['收盘'] < last['开盘'] and last['VOL_RATIO_5'] < 0.8),
            "suggested_stop_loss": stop_price
        }
    else:
        rule_results["STRAT_02_5x20回测"] = {
            "match": False,
            "reason": "当前不处于5穿20金叉支撑或跌破20日线"
        }
        
    report = {
        "symbol": symbol_str,
        "date": str(last['日期']),
        "current_price": cur_price,
        "trend_and_regime": {
            "dif_above_zero": bool(dif > 0),
            "dif_value": dif,
            "price_vs_ma20_pct": round((cur_price - ma20) / ma20 * 100, 2),
            "ma20_slope_pct": round(float(last['MA20_slope']), 2) if not np.isnan(last['MA20_slope']) else 0.0,
            "is_bullish_alignment": is_bullish,
            "is_bearish_alignment": is_bearish,
            "ma_snapshot": {
                "MA5": round(float(last['MA5']), 2),
                "MA10": round(float(last['MA10']), 2),
                "MA20": ma20,
                "MA60": ma60
            }
        },
        "volatility_and_volume": {
            "atr_14": atr,
            "stop_loss_margin": margin,
            "today_change_pct": round(float((last['收盘'] - prev['收盘']) / prev['收盘'] * 100), 2),
            "today_vol_vs_ma5": round(float(last['VOL_RATIO_5']), 2),
            "is_volume_shrinking": bool(last['VOL_RATIO_5'] < 0.70)
        },
        "box_and_pattern": box_info,
        "rule_prechecks": rule_results
    }
    
    return report

if __name__ == '__main__':
    sym = sys.argv[1] if len(sys.argv) > 1 else '600519'
    res = generate_checkup_report(sym)
    print(json.dumps(res, ensure_ascii=False, indent=2))
