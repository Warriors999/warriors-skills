---
name: photoshop-mcp
description: Use when the user wants Codex to edit a local Photoshop document, PSD layers, exact text, selections, masks, smart objects, or batch exports through the configured photoshop MCP server. Image generation remains with the existing image Plugin.
---

# Photoshop 本机编辑

通过已配置的 `photoshop` MCP 操作本机 Adobe Photoshop。适合精确文字、可编辑图层、蒙版和导出，图片生成沿用现有 OpenAI-Compatible Images 插件。

## 环境依赖

- 需要 Adobe Photoshop 与已配置的 `photoshop` MCP 服务。
- MCP 包：`@alisaitteke/photoshop-mcp`；安装与兼容性以其上游说明为准。
- 启动器和应用路径由使用者在本机配置，本仓库不包含运行包、启动配置或凭据。
- 使用当前 Codex 的模型；不要求新增图片 API Key，也不启动 MCP 包自带的独立聊天 UI。

## 使用流程

1. 遵循 `visual-task-gate`、Warriors 工作守则及本机图片规范。简单编辑给出简短保护项与修改项即可。
2. 使用当前会话实际提供的 Photoshop MCP 工具。先连接/检查应用与文档状态，再使用对应的图层、文字、选区、蒙版、智能对象或导出工具。
3. 如果工具尚未出现，说明需要刷新 MCP 或重启 Codex；不要声称已经操作 Photoshop，也不要改用独立聊天界面。
4. macOS 首次可能要求允许 Codex 控制 Photoshop；遇到系统权限拒绝时指出具体权限，再继续已获授权工作。不要自行更改隐私数据库。
5. 保留源文件与已有未保存文档，编辑另存副本。优先可撤销的工具步骤，不关闭其他工程、不覆盖源文件。
6. 精确中文使用真实文字图层；先检查字体可用性、大小、行距、边界、遮挡和溢出。
7. 新图来自图片插件时按其规则导出到项目，再放入 Photoshop。已有 PSD 不先重生整张图，先读取图层与保护项。
8. 导出后检查实际文件、尺寸、文字、层级及透明通道，展示结果和文件链接。用户仅要求安装时不执行示例编辑或测试工程。

## 执行边界

- 工具名称和参数以当前 MCP 暴露的定义为准，不凭文档中的旧列表猜测。
- 超时可能代表 Photoshop 仍在执行。先查看状态，避免立即重复写入。
- 执行任意 JSX 只在现成工具不足时使用；静态检查不能证明 Photoshop 实际执行成功。
- 图片插件画布和 Photoshop 是两个入口，使用这个 Skill 不自动打开画布。
- 本流程针对 MCP stdio；独立聊天 UI 的可选运行组件需按上游说明另行配置。

## 来源

[上游项目](https://github.com/alisaitteke/photoshop-mcp)。本文件是为本工作流编写的使用说明；第三方 MCP 实现不在本仓库内。
