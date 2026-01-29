#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
黄金内外盘价差分析工具
支持数据记忆和CSV格式快捷输入
"""

import json
import os

ORE_TROY_OUNCE = 31.1035  # 金衡盎司 = 31.1035克
DATA_FILE = "gold_data.json"


def load_data():
    """加载保存的数据"""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return None


def save_data(london_price, exchange_rate, actual_au9999):
    """保存数据到文件"""
    data = {
        "london_price": london_price,
        "exchange_rate": exchange_rate,
        "actual_au9999": actual_au9999
    }
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def parse_csv_input(input_str, current_values):
    """
    解析CSV格式输入
    支持格式：5512,7.0,1234.00 或 ,,1277
    """
    parts = input_str.split(',')
    result = list(current_values)

    for i, part in enumerate(parts):
        if i < 3 and part.strip():  # 不为空则更新
            try:
                result[i] = float(part.strip())
            except ValueError:
                print(f"警告：第{i+1}个值 '{part}' 无效，保持原值")

    return result[0], result[1], result[2]


def calculate_and_display(london_price, exchange_rate, actual_au9999):
    """计算并显示分析结果"""
    print()
    print("=" * 55)
    print("                      分析结果")
    print("=" * 55)

    # 核心公式1：伦敦金换算AU9999
    converted_au9999 = london_price * exchange_rate / ORE_TROY_OUNCE

    print(f"\n【公式1】换算AU9999（元/克）")
    print(f"  {london_price:.2f} × {exchange_rate:.4f} ÷ {ORE_TROY_OUNCE}")
    print(f"  = {converted_au9999:.2f} 元/克")

    # 核心公式2：内外盘价差
    price_diff = converted_au9999 - actual_au9999

    print(f"\n【公式2】内外盘价差")
    print(f"  {converted_au9999:.2f} - {actual_au9999:.2f}")
    print(f"  = {price_diff:+.2f} 元/克")

    if price_diff > 0:
        print(f"  → 国内价格偏低（伦敦金换算后更贵）")
    elif price_diff < 0:
        print(f"  → 国内价格偏高（伦敦金换算后更便宜）")

    # 核心公式3：内外盘价差比
    diff_ratio = price_diff / actual_au9999 * 100

    print(f"\n【公式3】内外盘价差比")
    print(f"  {price_diff:+.2f} ÷ {actual_au9999:.2f} × 100%")
    print(f"  = {diff_ratio:+.2f}%")

    print()
    print("=" * 55)


def main():
    print("=" * 55)
    print("           黄金内外盘价差分析工具")
    print("=" * 55)
    print()

    # 加载历史数据
    saved_data = load_data()

    # 主菜单
    if saved_data:
        print("【历史数据】")
        print(f"  1. 伦敦金价格: {saved_data['london_price']:.2f} 美元/盎司")
        print(f"  2. 美元/人民币汇率: {saved_data['exchange_rate']:.4f}")
        print(f"  3. 中国AU9999价格: {saved_data['actual_au9999']:.2f} 元/克")
        print()

        choice = input("使用历史数据？(Y/n): ").strip().lower()

        if choice != 'n':
            calculate_and_display(
                saved_data['london_price'],
                saved_data['exchange_rate'],
                saved_data['actual_au9999']
            )

            # 询问是否修改
            modify = input("\n是否修改数据？(y/N): ").strip().lower()
            if modify != 'y':
                input("\n按回车键退出...")
                return

            # 使用CSV格式修改
            print("\n【CSV格式修改】")
            print("  输入格式：伦敦金,汇率,AU9999")
            print("  示例：")
            print("    5512,7.0,1234.00  → 全部修改")
            print("    ,,1277            → 只改AU9999")
            print("    5550,,            → 只改伦敦金")

            current = (saved_data['london_price'],
                      saved_data['exchange_rate'],
                      saved_data['actual_au9999'])

            csv_input = input(f"\n请输入（当前：{current[0]:.2f},{current[1]:.4f},{current[2]:.2f}）: ").strip()

            if csv_input:
                london_price, exchange_rate, actual_au9999 = parse_csv_input(csv_input, current)
                save_data(london_price, exchange_rate, actual_au9999)
                calculate_and_display(london_price, exchange_rate, actual_au9999)
                input("\n按回车键退出...")
                return

    # 新数据输入
    print("【输入新数据】")
    print("  提示：支持CSV格式输入，如 5512,7.0,1234.00 或 5255,,")
    print("  空值将使用历史数据（如有）或继续单独输入")
    print()

    # CSV 快速输入或逐个输入
    london_price = None
    exchange_rate = None
    actual_au9999 = None

    # 首先尝试 CSV 输入
    csv_input = input("请输入数据（CSV格式或直接回车逐个输入）: ").strip()

    if csv_input and ',' in csv_input:
        # CSV 模式：解析并填充历史值
        current = (
            saved_data.get('london_price', None) if saved_data else None,
            saved_data.get('exchange_rate', None) if saved_data else None,
            saved_data.get('actual_au9999', None) if saved_data else None
        )
        parts = csv_input.split(',')
        if parts[0].strip():
            london_price = float(parts[0].strip())
        if len(parts) > 1 and parts[1].strip():
            exchange_rate = float(parts[1].strip())
        if len(parts) > 2 and parts[2].strip():
            actual_au9999 = float(parts[2].strip())

        # 对于空值，使用历史数据或继续单独输入
        if not london_price and current[0] is not None:
            london_price = current[0]
            print(f"使用历史伦敦金价格: {london_price:.2f}")
        if not exchange_rate and current[1] is not None:
            exchange_rate = current[1]
            print(f"使用历史汇率: {exchange_rate:.4f}")
        if not actual_au9999 and current[2] is not None:
            actual_au9999 = current[2]
            print(f"使用历史AU9999价格: {actual_au9999:.2f}")

    # 单独输入缺失的值
    if london_price is None:
        while True:
            try:
                london_price = float(input("请输入伦敦金价格（美元/盎司）: "))
                break
            except ValueError:
                print("输入无效，请输入数字")

    if exchange_rate is None:
        while True:
            try:
                exchange_rate = float(input("请输入美元/人民币汇率: "))
                break
            except ValueError:
                print("输入无效，请输入数字")

    if actual_au9999 is None:
        while True:
            try:
                actual_au9999 = float(input("请输入实际中国AU9999价格（元/克）: "))
                break
            except ValueError:
                print("输入无效，请输入数字")

    # 保存数据
    save_data(london_price, exchange_rate, actual_au9999)

    # 计算并显示结果
    calculate_and_display(london_price, exchange_rate, actual_au9999)
    input("\n按回车键退出...")


if __name__ == '__main__':
    main()
