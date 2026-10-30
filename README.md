# 带货视频导演台

把产品卖点变成**能直接投流的 15 秒素材**：输入产品简报，输出 3 版钩子、6 镜分镜、逐镜提示词、投流切片与封面文案。

面向 TikTok Shop（美区/东南亚）、抖音千川、小红书带货场景。

## 它和故事导演台的区别

| 维度 | 故事导演台 | 带货导演台（本仓库） |
|---|---|---|
| 成功标准 | 叙事完整、情绪弧线 | 3s 留存、CTR、CVR |
| 时长 | 60–180 秒 | 15–45 秒 |
| 结构 | 起承转合 | 钩子→卖点→信任→CTA |
| 镜头 | 服务情绪 | 服务卖点，一镜一卖点 |
| 交付 | 分镜 + 提示词 | **投流素材包**（3 钩子 × 主片 × 切片 × 封面） |

## 目录

```
skill/     ai-commerce-director 技能
├── SKILL.md              身份、五条铁律、七步工作流、输出模板
├── references/
│   ├── 01_四形态模板.md   测评/对比/开箱/教程 的 6 镜骨架
│   ├── 02_钩子库.md       按品类的钩子句式
│   ├── 03_卖点视觉化词典.md 卖点→画面 翻译表
│   ├── 04_合规与披露.md   广告法禁词、FTC、AI 标识
│   ├── 05_平台差异.md     TK 美区/东南亚 vs 抖音 vs 小红书
│   └── 06_案例库.md       服装/家居/美妆 三个完整案例
└── scripts/commerce_check.py  分镜自检

agent/     人设、规则、验收、方法论
plugin/    DSH agent preset
```

## 安装

```powershell
git clone https://github.com/zhang2026bin/commerce-video-director.git
cd commerce-video-director
.\install.ps1
```

脚本会：改写 preset 路径 → 安装技能到 `~/.agents/skills/ai-commerce-director` → 安装插件 → 写进 profile 的 `dsh.profile.bundles`。重启后在 Agent 列表选择 `commerce-video`。

## 怎么用

给一份产品简报即可：

```
产品：高腰阔腿裤，$29.9
人群：25–40 岁女性，通勤
卖点：垂感好、显腿长、腰头不勒
平台：TikTok 美区
形态：结果型 + 前后对比
```

输出六件：3 版钩子、6 镜分镜、逐镜提示词、3 条投流切片、3 版封面文案、合规检查。

## 自检

```powershell
python skill/scripts/commerce_check.py storyboard.md --product "阔腿裤"
```

检查：镜头 ≤6、总时长 ≤15 秒、首镜含产品、末镜有 CTA、禁用词、AI 标识。

## 依据

- TikTok Shop Academy《Content Styles to Help Your Creative Process on TikTok Shop》（2026-05-20）：三段式结构、四形态、3–6 秒钩子、FTC 披露
- 前 3–6 秒留存研究（AppGrowing）
- 资产管线与时长公式：`ai-director/references/12_资产管线与生成实操.md`

## 边界

- 不做医疗功效宣称，不写绝对化用语
- 不虚构使用体验；前后对比必须真实可复现
- AI 生成/数字人内容需标识
- 只出脚本/分镜/提示词，不生成素材、不代投
