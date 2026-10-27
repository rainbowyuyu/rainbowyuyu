# Rainbow Fieldnotes / 彩虹手绘工作簿

一套服务于 rainbow鱼 的原创个人主页组件，2026-10-28。以纸感手绘、项目自己的颜色和清楚的文字为主，网站与 GitHub README 共用项目事实和插画。

## 组件

| 组件 | 网站 | GitHub Profile |
| --- | --- | --- |
| 项目书页 | 原生 details / summary，整张卡片可点，+/− 与展开文案反馈 | 前三张直接呈现，另外四张放在总抽屉；每张仍可展开介绍 |
| 项目入口 | 胶囊按钮、圆箭头、hover / focus / active 状态 | 明确目标的图片链接，双主题与可读 alt |
| 技能工具架 | 研究与计算、工程与构建、影像与表达，真实工具标签 | 同样的三组插画与工具标签 |
| 信息抽屉 | 彩虹书签、展开状态与键盘操作 | 原生三角标记加彩虹按钮式标题 |
| 日常记录 | 2 × 2 统计、连续贡献、彩虹贡献场景 | 相同快照与来源，保留每日工作流 |
| 资源档案 | 历史卡片、原始项目图、原来的技术小图标 | 折叠保留原图标、贡献 snake 与历史入口 |

## 数据与生成

- assets/catalog/projects.json 是七个项目的公开文案与标签来源。
- scripts/profile_components.py 定义七套品牌色、三组技能、SVG 卡片和按钮；项目与技能含独立的手机构图。
- scripts/generate_readme.py 生成两种语言的 README 和双主题组件。运行 python scripts/generate_readme.py。
- index.html 使用语义化 HTML 和双语 data 属性；styles.css 管理整站色彩、排版和交互状态；script.js 只负责增强。
- assets/components/illustrations/ 保存八幅独立插画。原始 logo 与封面仍保留在 assets/projects/ 和 assets/showcase/。
- 日更统计仍由原来的 activity generators 和 GitHub Actions 维护，设计生成不请求数据接口、不修改快照时间。

## 主题与动效

默认跟随系统；手动浅色、深色、系统三选一。网站同步 picture 与图像来源；README 使用原生 picture media。手机小于 600px 时使用独立竖版项目、技能与折叠标题。

按钮轻微位移、箭头转向；插画进入视野一次轻轻归位；项目展开短暂过渡。网站尊重减少动态效果和暂停开关，贡献动画离开视野时切为静态。README 受 GitHub 支持范围约束，不承诺 JavaScript 交互；彩虹贡献景观提供 reduced-motion 静态图。

## 内容边界

公开名 rainbow鱼；身份为浙江大学博士 / PhD researcher at Zhejiang University。插画表达项目概念，不代表实验结果。PhysCast 与 OmniForge 继续标注源码私有。技能标签不附加未经核实的熟练度百分比。
