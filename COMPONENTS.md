# Rainbow Fieldnotes / 彩虹手绘工作簿

一套服务于 rainbow鱼 的原创个人主页组件，2026-10-28。以纸感手绘、项目自己的颜色和清楚的文字为主，网站与 GitHub README 共用项目事实和插画。

## 组件

| 组件 | 网站 | GitHub Profile |
| --- | --- | --- |
| 项目书页 | 原生 details / summary，整张卡片可点，+/− 与展开文案反馈 | 前三张直接呈现，另外四张放在总抽屉；每张仍可展开介绍 |
| 项目入口 | 手绘图标在上、文字在下；hover / focus / active 状态 | 同构图片链接，双主题与可读 alt |
| 技能工具架 | 三组各五枚独立水彩图标，名称在下；另六项收于抽屉 | 桌面整排，手机三列的独立构图 |
| 信息抽屉 | 手绘工具箱、日历、档案与彩虹加号，展开旋转反馈 | 原生三角标记加手绘标题，明确点击展开提示 |
| 日常记录 | 2 × 2 统计、连续贡献、彩虹贡献场景 | 相同快照与来源，保留每日工作流 |
| 资源档案 | 历史卡片、原始项目图、原图标文件均保留 | 手绘版工具图标、贡献 snake 与历史入口 |

## 数据与生成

- assets/catalog/projects.json 是七个项目的公开文案与标签来源。
- scripts/profile_components.py 定义七套品牌色、三组技能、SVG 卡片和按钮；项目与技能含独立的手机构图。
- scripts/generate_readme.py 生成两种语言的 README 和双主题组件。运行 python scripts/generate_readme.py。
- index.html 使用语义化 HTML 和双语 data 属性；styles.css 管理整站色彩、排版和交互状态；script.js 只负责增强。
- assets/components/illustrations/ 保存八幅独立插画。原始 logo 与封面仍保留在 assets/projects/ 和 assets/showcase/。
- assets/components/icons/ 保存 36 枚 Qwen 水彩原画切片、4 枚本地派生控制符与两种手绘分隔图。脚本 handpainted_icons.py 共用于 README、网站映射与日更统计渲染。名称用真实文字排版，不依赖生成图里的文字。
- 每组技能在桌面一行五枚；网站手机三列、极窄屏两列，避免把名称缩成不可读小字。GitHub 手机使用三列图版；原始技术图标保留在 assets/widgets/。
- 日更统计仍由原来的 activity generators 和 GitHub Actions 维护，设计生成不请求数据接口、不修改快照时间。

## 主题与动效

默认跟随系统；手动浅色、深色、系统三选一。网站同步 picture 与图像来源；README 使用原生 picture media。手机小于 600px 时使用独立竖版项目、技能与折叠标题。

按钮与工具图标轻微抬起；彩虹加号随展开旋转；插画进入视野一次轻轻归位；项目展开短暂过渡。网站尊重减少动态效果和暂停开关，贡献动画离开视野时切为静态。README 受 GitHub 支持范围约束，不承诺 JavaScript 交互；彩虹贡献景观提供 reduced-motion 静态图。

## 内容边界

公开名 rainbow鱼；身份为浙江大学博士 / PhD researcher at Zhejiang University。插画表达项目概念，不代表实验结果。PhysCast 与 OmniForge 继续标注源码私有。技能标签不附加未经核实的熟练度百分比。
