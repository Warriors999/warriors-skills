# Warriors Skills

按实际工作需求、通过 AI 辅助编写与持续维护的 8 个定制技能，覆盖视觉研究、PPT 协作、即梦提示词、动效设计与 Photoshop 操作流程。

[English](#english) · [安装](#安装) · [技能清单](#技能清单)

这是清理本机信息后的公开版本，主要提供流程与判断规则。运行工具、模型服务、应用程序和凭据需要使用者自行配置。

## 技能清单

| 分类 | 技能 | 用途 |
| --- | --- | --- |
| 工作流程 | [warriors-work-principles](skills/warriors-work-principles/SKILL.md) | 研究、分析、方案、执行、真实产物验收与迭代 |
| 视觉入口 | [visual-task-gate](skills/visual-task-gate/SKILL.md) | 区分输入职责，按任务选择技能并落实视觉验收 |
| PPT | [ppt-design-collaboration](skills/ppt-design-collaboration/SKILL.md) | 参考契约、场景规范、设计制作、可编辑交付与修改 |
| 参考研究 | [pinterest-reference-design](skills/pinterest-reference-design/SKILL.md) | 参考筛选、结构分析、设计转化与素材权利核查 |
| 动效 | [ai-motion-director](skills/ai-motion-director/SKILL.md) | 基于既有关键帧设计动作机制、镜头与片段衔接 |
| 视频文字 | [ai-video-text-safe-workflow](skills/ai-video-text-safe-workflow/SKILL.md) | 中文文字保真、AI 视频与后期合成的分工 |
| 即梦 | [jimeng-prompt-reference-skill](skills/jimeng-prompt-reference-skill/SKILL.md) | 平台/模式分流、参考职责、时间轴和提示词检查 |
| Photoshop | [photoshop-mcp](skills/photoshop-mcp/SKILL.md) | 通过已配置的第三方 MCP 编辑 PSD 文字、图层、蒙版与导出 |

## 使用方式

每个 `skills/<名称>/` 都是独立技能目录，入口为 `SKILL.md`。可让 Codex 的 `skill-installer` 从本仓库选择安装，也可按客户端约定放入其技能目录。若已安装同名版本，先检查现有来源，避免重复安装或覆盖个人配置。

### 安装

使用公开的 Skills CLI，需要 Node.js 22.20 或更高版本：

```bash
# 交互选择要安装的技能和 Agent
npx skills add Warriors999/warriors-skills

# 只安装一个技能，并安装到全局 Agent 技能目录
npx skills add Warriors999/warriors-skills --skill ppt-design-collaboration -g
```

也可以只查看技能提示词而不安装：

```bash
npx skills use Warriors999/warriors-skills@warriors-work-principles
```

不同 Agent 的安装位置和参数可能不同，请先运行 `npx skills add --help`。本仓库不要求安装全部 8 个技能；按任务选择最小组合即可。

已验证：Skills CLI 可从公开仓库识别全部 8 个技能；`ppt-design-collaboration` 已在隔离的临时项目目录完成 Codex 安装验证。更多说明见 [INSTALL.md](INSTALL.md)。

组合使用时，`visual-task-gate` 路由至工作守则及当前任务需要的技能；仅装单个技能时，按入口说明检查其依赖。技能中所述“全局规则”需要在使用环境中启用，不会仅因仓库存在而自动生效。

## 运行依赖与边界

- 图片生成默认衔接 OpenAI-Compatible Images 插件及当前配置的提供商/模型。本仓库不包含插件或模型服务。未配置时说明具体缺口，按用户指定路线处理，不假装调用成功。
- `photoshop-mcp` 需要 Photoshop 和已配置的 [Photoshop MCP](https://github.com/alisaitteke/photoshop-mcp)。本仓库只提供工作流说明，不包含第三方 MCP 实现。
- PPT 制作、图像理解等流程会引用 `pptx`、`presentations`、`vision-tools` 等外部能力；它们不在这 8 个技能之内，是否可用以当前环境为准。
- PPT 审计脚本使用 Python 3.10+；图像审计还需要 Pillow。依赖声明见对应目录的 `requirements.txt`。
- `evals/evals.json` 是行为评测用例定义，不代表已经运行或通过模型行为评测。空白项目模板不包含真实项目记录。
- 平台手册与界面观察保留核查日期和适用范围；历史记录不能保证当前平台能力。

## 来源与发布

编写与参考来源见 [PROVENANCE.md](PROVENANCE.md)。公开版的文件清单及 SHA-256 见 [publication-manifest.json](publication-manifest.json)，发布前检查范围见 [PUBLICATION_CHECKS.md](PUBLICATION_CHECKS.md)。

仓库公开不等于第三方素材可任意使用。本次未指定统一开源许可证；第三方项目及引用资料的权利归各自权利人。

### 通用调用示例

下面的示例只展示调用方式，不包含真实项目、客户资料或效果展示：

```text
使用 $warriors-work-principles，先分析任务约束和验收标准，再给出最小执行方案。

使用 $ppt-design-collaboration，检查这份 PPT 的参考契约、可编辑性和交付验收项。

使用 $jimeng-prompt-reference-skill，区分参考素材职责，按当前视频模式组织提示词，并标出未核验能力。

使用 $ai-video-text-safe-workflow，规划中文文字关键帧、无文字动效底板和后期合成的分工。

使用 $visual-task-gate，识别本次任务的内容来源、版式参考、风格参考与必要执行技能。

使用 $pinterest-reference-design，仅研究参考来源和可迁移的构图规则，先不制作素材。

使用 $ai-motion-director，根据已提供的关键帧规划动作机制与片段衔接，先输出设计说明。

使用 $photoshop-mcp，先检查可用工具与文档状态，再说明本次文字修改的保护项和验收条件。
```

## English

Warriors Skills is a public collection of eight custom skills developed and maintained with AI assistance for visual research, presentation collaboration, Jimeng video prompting, motion direction, and Photoshop MCP workflows.

The repository contains sanitized instructions and reusable decision rules. It does not contain private project files, client material, credentials, local application configuration, generated media, or third-party runtime implementations.

### Quick start

```bash
# Choose skills and agents interactively
npx skills add Warriors999/warriors-skills

# Install one skill globally
npx skills add Warriors999/warriors-skills --skill ppt-design-collaboration -g

# Use a skill without installing it
npx skills use Warriors999/warriors-skills@warriors-work-principles
```

Use only the smallest set of skills needed for the task. Check the current CLI help because agent support and installation paths may change.

### What is included

- `warriors-work-principles`: research, design judgment, execution, verification, and delivery discipline.
- `visual-task-gate`: input classification, skill routing, and visual acceptance checks.
- `ppt-design-collaboration`: presentation research, reference contracts, editable production, and QA.
- `pinterest-reference-design`: reference selection, analysis, rights awareness, and design transfer.
- `ai-motion-director`: motion mechanisms and shot transitions for existing keyframes.
- `ai-video-text-safe-workflow`: text-safe AI video and post-production routing.
- `jimeng-prompt-reference-skill`: mode routing, reference roles, timelines, and prompt linting.
- `photoshop-mcp`: portable workflow instructions for a configured third-party Photoshop MCP.

See [PROVENANCE.md](PROVENANCE.md) for authorship and attribution boundaries.

Discovery and directory status are documented in [DISCOVERY.md](DISCOVERY.md). No leaderboard position or directory approval is claimed.
