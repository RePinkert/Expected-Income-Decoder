#x:\Trans-AM\Expected-Income-Decoder\
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt

# 列出所有可用字体
fonts = [f.name for f in fm.fontManager.ttflist]

# 查找中文字体
chinese_keywords = ['YaHei', 'Hei', 'Song', 'Kai', 'Fang', 'SimHei', 'Microsoft']
chinese_fonts = [f for f in fonts if any(kw in f for kw in chinese_keywords)]

print("=== 可用的中文字体 ===")
for f in chinese_fonts[:30]:
    print(f"  {f}")

print(f"\n总计: {len(chinese_fonts)} 个中文字体")

# 测试绘制中文
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei']
plt.rcParams['axes.unicode_minus'] = False

plt.figure(figsize=(6, 4))
plt.text(0.5, 0.5, '测试中文',
         ha='center', va='center', fontsize=20)
plt.title('黄金定投策略')
plt.show()

print("\n如果弹出窗口显示中文正常，则字体配置成功")