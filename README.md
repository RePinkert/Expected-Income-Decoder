# 黄金内外盘价差分析工具

```python
# 🧧 新春bonus 🧧

for street in streets:
    for mouth in (person.mouth for person in street.people):
        first_sentence = mouth.pop()
        assert first_sentence == "恭喜恭喜"

while True:
    try:
        wealth.accumulate()
        bugs.banish()
        happiness.maximize()
    except KeyboardInterrupt:
        break
    finally:
        print("新年快乐，代码无 Bug！")
```

## 项目简介

基于国内AU9999金条和伦敦金的当前价格，分析两者之间的价差关系，帮助快速判断黄金市场的套利机会和价格偏离程度。

## 核心公式

### 公式1：伦敦金换算AU9999（元/克）

```
换算AU9999（元/克）≈ 伦敦金（美元/盎司）× 当日美元/人民币汇率 ÷ 31.1035
```

**说明：**
- 31.1035 为金盎司的克数重量单位
- 该公式将国际金价换算为国内计价方式，便于直接对比

### 公式2：内外盘价差

```
内外盘价差 = 换算AU9999 - 实际中国AU9999
```

**说明：**
- 正值表示伦敦金换算价格高于国内价格（国内便宜）
- 负值表示伦敦金换算价格低于国内价格（国内贵）

### 公式3：内外盘价差比

```
内外盘价差比 = 内外盘价差 / 实际中国AU9999 × 100%
```

**说明：**
- 以百分比形式展示价差相对大小
- 便于直观判断价差幅度

## 应用场景

非常适合快速分析黄金：
- 判断内外盘套利机会
- 监控国内外金价偏离程度
- 辅助黄金投资决策

## 使用方法

运行 `gold_price_converter.py` 脚本，输入相关价格数据即可获取分析结果。
