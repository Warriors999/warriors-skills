# Warriors Skills

按实际工作需求、通过 AI 辅助编写与持续维护的 8 个定制技能，覆盖视觉研究、PPT 协作、即梦提示词、动效设计与 Photoshop 操作流程。

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
