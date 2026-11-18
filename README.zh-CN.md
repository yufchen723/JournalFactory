# JournalFactory

一座由 Claude 运转的生物学论文工厂，从上到下四步：

1. **调研领域。** 动笔之前，按你的问题检索 PubMed 和 Europe PMC，把论文读成卡片，整理出领域已知什么、在争什么、还缺什么。
2. **读你自己的数据。** 过一遍你的结果和图，评估每个结果有多扎实，对照领域地图找出新意：哪些结论是空白、哪些是延伸、哪些已被别人做了，还缺什么。
3. **用期刊的 skill 组装论文。** 内置的 Cell、Nature 等期刊 skill 包，把故事线、图、文字和统计都按那本期刊的规范来。说出期刊名，或者让证据来选。
4. **在画布上编辑。** 图和正文作为可编辑页面打开：拖动面板、改字、选中任何内容问 Claude、接受或拒绝它的建议、按精确尺寸导出。

![JournalFactory 总览](docs/overview.png)

第 4 步里的编辑器是示意图；第 3 步里的两张小图是同一份代码和模拟数据的真实输出。

在 Claude 里它是 `journal-factory` 这个 skill，命令行是 `jf`。[English](README.md)

## 第 3 步细节：适配任何期刊

| 你说 | 运行 | 结果 |
| --- | --- | --- |
| “投 Nature”“Cancer Cell”“NC” | `jf adapt nature` | 载入内置档案，所有工位按它设定 |
| “投哪本？” | `jf adapt auto --paper projects/<p>/paper.json` | 按你的证据与各期刊门槛的差距排序，选出够得上的最高档期刊；都够不上就说明差在哪，不硬选 |
| 没有内置的期刊 | `jf adapt "Immunity" --new` | 按出版社家族生成档案草稿：结构填好，所有字数限制留空，并列出排版前必须去官网读的页面 |

**内置 13 本：** Cell · Cancer Cell · Cell Reports Medicine · Nature · Nature Genetics · Nature Cancer · Nature Medicine · Nature Biotechnology · Nature Methods · Nature Neuroscience · Nature Communications · Science · Neuro-Oncology。

`jf adapt` 之后跟着变的内容：

| 工位 | 随期刊变化 |
| --- | --- |
| 2 期刊 | 用来对比的证据门槛 |
| 3 故事 | 主图数量；附加图的叫法（Figure S、Extended Data） |
| 4 图 | 宽度、字体、字号、面板字母大小写、线宽范围、分辨率、文件格式 |
| 5 文字 | 字数和字符限制、章节顺序、前置材料（Highlights、eTOC、摘要形式） |
| 6 统计 | 方法部分的名称和限制 |
| 7 投稿 | 必需的附件（reporting summary、key resources table、graphical abstract） |
| 编辑器 | 页面尺寸和 Journal 标签页的实时检查 |

## 四步之下：九个工位

第 1 步对应工位 1；第 2 步对应工位 0 和 2；第 3 步对应工位 3–8；第 4 步是编辑器，从工位 4 起使用。

| # | 工位 | 要回答的问题 | 设备 | 产出 |
| --- | --- | --- | --- | --- |
| 0 | 盘点 | 手里有什么，每个结果有多扎实？ | 8 维度打分、3 种情景 | 证据表 |
| 1 | 领域 | 领域已知什么、争什么、期待什么？ | `jf field`：PubMed + Europe PMC 检索、论文卡片、参考文献核对 | 领域地图 |
| 2 | 期刊 | 现在适合哪本，补了什么之后适合哪本？ | `jf fit`、`jf adapt` | 各情景的匹配表，产线设定完成 |
| 3 | 故事 | 一句话，然后论点，然后图 | 规划报告；每个面板四种标记 | 缺口一目了然的计划 |
| 4 | 图 | 按期刊规范做每张图 | `journal_style`（Python）、`theme_cell`（R）、模板、检查 | 通过检查的图文件 |
| 5 | 文字 | 按期刊的顺序和字数写 | 编辑器、`jf count`、`jf cell text` | 不超限的稿件 |
| 6 | 统计 | 重复单位、检验、审稿人会问什么 | `jf cell legends` | 统计表、清单 |
| 7 | 投稿 | cover letter、前置材料、数据存放、最终文件 | 指南、`jf cell refs` | 投稿文件夹 |
| 8 | 返修 | 从审稿意见到计划和逐条回复 | `jf cell response` | 回复包 |

`jf line projects/<p>/paper.json` 打印你这篇论文的九个工位、每个工位已有什么，以及下一个该做哪个。

## 每个工位给你什么

- **动笔之前的领域调研。** 你把问题写成 PubMed 检索式；它检索 PubMed 和 Europe PMC，把论文读成卡片，逐条核对参考文献，汇成一页：领域已知什么、在争什么，你的每个结论是空白、延伸，还是已被别人做了。
- **按证据选期刊。** 结果在 8 个维度上打 0–3 分，和每本期刊的门槛对比，分三种情景：现在投、只补分析、补新数据。
- **缺口看得见的计划。** 每个面板标四种状态之一：已有、有数据待画、需要分析、需要新数据。还缺实验的结论不会被写成结果。
- **通过检查的图。** 同样十行代码适用于任何期刊：

  ```python
  import journal_style as js
  js.use_journal("nature")            # 或 "cell"、"cancer-cell"、"science" …
  fig, axd = js.mosaic([["A", "A", "B"], ["C", "D", "B"]], width="full", height_mm=120)
  js.templates.bar_points(axd["B"], {"Ctrl": ctrl, "Treated": treated}, ylabel="Signal (a.u.)")
  js.label_panels(axd)                # Nature 是 a b c，Cell 是 A B C
  js.save(fig, "out/Figure 1")        # 先检查，再导出，再检查文件
  ```

  8 个图模板；导出前检查面板对齐和文字重叠，不通过就不导出；导出后检查宽度、字体、字号、线宽、颜色、分辨率、文件大小。

- **按字数限制写稿。** `jf count` 适用于任何期刊；`cell-skills` 是一整套 Cell 专用 skill（画图、写作、统计、自审、返修回复、数据、参考文献）；Nature 系、Cancer Cell 等有随附的参考包。
- **覆盖全稿的编辑器。** 稿件每个部分一页：正文、前置材料、每张主图和附加图、graphical abstract。按毫米拖动和缩放面板，原地改字，Journal 标签页实时检查，选中任何内容问 Claude，接受或拒绝它的修改建议，按精确尺寸导出 PDF。
- **不用图像生成器的示意图。** 本地 BioCartoon 图标检索和手写 SVG 指南。

## 安装

```bash
git clone https://github.com/yufchen723/JournalFactory ~/.claude/skills/journal-factory
~/.claude/skills/journal-factory/bin/jf doctor
bin/jf demo out/ --journal nature     # 不需要任何数据：用模拟数据画一张 6 面板图并检查
```

然后直接对 Claude 说：“按 Nature Genetics 来”“这个课题适合投哪本”“先调研领域”“规划图”“检查 Figure 2”“我们做到哪了”。

需要 Python ≥ 3.9；画图代码需要 matplotlib、numpy、Pillow（R 版需要 ggplot2 和 patchwork）。

## 期刊规范有多可靠

`journals/` 里每个档案都记录了数值是怎么核对的，`jf adapt` 第一行就会显示：

| 级别 | 含义 | 内置档案 |
| --- | --- | --- |
| `official` | 在期刊官网读到，带日期 | Cell、Nature、Nature Genetics、Nature Cancer |
| `secondary` | 其他来源一致 | Cancer Cell |
| `memory` | 尚未核对：可用于规划和起草，排版前必须确认 | 其余 8 本，以及所有用 `--new` 建的档案 |

用 `--new` 建的档案不会编造任何限制：在读过期刊官网之前它们一直留空。期刊会改规范，最终排版前请再看一次官网。

## 隐私

- 你的课题、数据和未发表结果不会被脚本发到任何地方；本仓库的 `projects/` 和 `fields/` 是空的。
- 文献检索只把你写的检索词发给 PubMed、Europe PMC、iCite 和 bioRxiv。
- 编辑器只监听本机 127.0.0.1，带令牌。
- 科研图像不用生成式工具创建或改动。

## 致谢与许可

致谢、来源和许可见 [README.md](README.md#credits)。JournalFactory 自己的文字和代码为 MIT 许可；`vendor/` 下的内容保留各自的许可。
