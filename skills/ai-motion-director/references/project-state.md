# 项目背景与动作记录

## 何时写文件

项目需要多片段/跨会话衔接且存在项目目录时，将 assets/project-context.md 与 assets/motion-ledger.json 复制到该项目 `motion/`。本 Skill 创建已授权任务的本地工作记录，不写 Codex memories；用户另有目录要求则优先使用。

已有文件先读取，未确定值保留空/null，不补造客户事实、精确文字或模型。明确用户新指令优先；只同步本次变化。一个短提示词任务可沿用对话，不强制落盘。

`project-context.md` 只记录项目共通事实，不记录每段内容。首次仅收到背景时写入已知信息，图片到来后再设计。文本制作方提供的原文是准确文字来源，视觉 OCR 不自动成为权威文案。

## 记录状态

一段可有多个版本，参考版本、设计版本和生成结果分别标识。`status`：

- `proposed`：Codex 建议。
- `adopted`：用户已选或已授权按该方案执行。
- `generated`：有真实输出文件或可核验生成结果。
- `accepted`：用户确认，或在已授权验收条件下实际检查通过。
- `rejected`：放弃该版本，有原因。

`evidence`：`design_only`、`user_reported`、`sampled_frames`、`full_video_review`。状态与证据不能相互替代；用户通过可以 accepted＋user_reported，但不能写成已逐帧核验。

只有 adopted/generated/accepted 记录用于项目重复检查。推荐备选不是已用动作。更新时追加版本，不覆盖旧输入/成片。

## 一条记录包含

`segment_id`、`version`、`reference_files`、`reference_roles`、`purpose`、`status`、`evidence`、`mechanism`、`camera`、`trigger_order`、`climax`、`settle`、`anchors`、`duration_seconds`、`prompt_file`、`output_file`、`platform`、`model`、`mode`、`feedback`。

可选追加 `allowed_transforms`、`motion_quality`（速度/轨迹/响应/收束）与 `generation_tradeoff`，不改变现有 schema_version 或强制补全旧记录。anchors 区分内容与位置；用户许可的主体/文字整体运动单独记入 allowed_transforms。

mechanism 用能跨名称比较的短描述，如“按已有路线传递→局部响应”。颜色和装饰变化不等于机制变化。参考角色只记用户/模式明确的角色；不自动把文件列表当时间顺序。

accepted 记录可作用户实测案例，需保留参数、采用区间和失败点。若要维护全局方法库，先获得用户该次授权；日常项目更新不自动修改 Skill。
